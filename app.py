import streamlit as st
import requests
import os
from typing import Dict, Any
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure page settings
st.set_page_config(
    page_title="News Translator & Summarizer",
    page_icon="📰",
    layout="wide"
)

# Constants
GROQ_API_KEY = os.getenv("API_KEY")  # Get API key from environment variable
GROQ_API_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.1-70b-versatile"

# Available languages for translation
LANGUAGES = [
    "Telugu", "Hindi", "Tamil", "Bengali", "Marathi", "French", 
    "Spanish", "German", "Chinese", "Japanese", "Korean"
]

def fetch_article_content(url: str) -> str:
    """Fetch article content from URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove unwanted elements
        for tag in soup(['script', 'style', 'nav', 'header', 'footer', 'ads']):
            tag.decompose()
            
        # Get main content (adjust selectors based on target websites)
        article_text = ""
        main_content = soup.find('article') or soup.find(class_=['article', 'content', 'post'])
        
        if main_content:
            paragraphs = main_content.find_all('p')
            article_text = ' '.join([p.get_text().strip() for p in paragraphs])
        else:
            # Fallback to all paragraphs if no article container found
            paragraphs = soup.find_all('p')
            article_text = ' '.join([p.get_text().strip() for p in paragraphs])
            
        return article_text.strip()
    except Exception as e:
        raise Exception(f"Failed to fetch article content: {str(e)}")

def process_article(text: str, url: str, target_language: str) -> Dict[Any, Any]:
    """Process the article using Groq API for summary and translation."""
    
    # Fetch content if URL is provided
    if url and not text:
        try:
            text = fetch_article_content(url)
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    messages = [
        {
            "role": "system",
            "content": "You are a professional translator and summarizer. Provide concise summaries and accurate translations."
        },
        {
            "role": "user",
            "content": f"""Please analyze this article and provide:
1. A concise summary in English (100-150 words)
2. An accurate translation of the summary in {target_language}

Article: {text}

Format your response exactly as:
SUMMARY: <english_summary>
TRANSLATION: <translated_summary>"""
        }
    ]
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.3,  # Lower temperature for more focused outputs
        "max_tokens": 1024,
        "top_p": 1
    }
    
    try:
        response = requests.post(GROQ_API_ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        return {
            "success": True,
            "content": result["choices"][0]["message"]["content"]
        }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": f"API request failed: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Processing error: {str(e)}"
        }

def main():
    st.title("📰 News Translator & Summarizer")
    st.write("Get summaries and translations of news articles using Groq's LLM")
    
    # Input method selection
    input_method = st.radio(
        "Choose input method:",
        ["URL", "Text"],
        horizontal=True
    )
    
    url = ""
    text = ""
    
    if input_method == "URL":
        url = st.text_input(
            "Enter article URL:",
            placeholder="https://example.com/news-article"
        )
    else:
        text = st.text_area(
            "Enter article text:",
            height=200
        )
    
    # Language selection
    target_language = st.selectbox(
        "Select target language for translation:",
        LANGUAGES
    )
    
    if st.button("Process Article", type="primary"):
        if (input_method == "URL" and url) or (input_method == "Text" and text):
            with st.spinner("Processing article..."):
                result = process_article(text, url, target_language)
                
                if result["success"]:
                    # Parse the response
                    content = result["content"]
                    summary = ""
                    translation = ""
                    
                    # Split content into summary and translation
                    parts = content.split("TRANSLATION:")
                    if len(parts) >= 2:
                        summary = parts[0].replace("SUMMARY:", "").strip()
                        translation = parts[1].strip()
                    
                    # Display results in columns
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("English Summary")
                        st.write(summary)
                    
                    with col2:
                        st.subheader(f"{target_language} Translation")
                        st.write(translation)
                else:
                    st.error(f"Error processing article: {result['error']}")
        else:
            st.warning("Please provide either a URL or text content.")

if __name__ == "__main__":
    main() 