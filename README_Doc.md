# News Translator & Summarizer

A Streamlit-based web application that translates and summarizes news articles using the Groq API. This application allows users to input news article URLs and get translations and summaries in their preferred language.

## Features

- Article content extraction from URLs
- Article translation to multiple languages
- Article summarization
- Clean and intuitive user interface
- Secure API key management

## Project Structure

```
translation/
├── .env                    # Environment variables file (contains API keys)
├── .gitignore             # Git ignore file for excluding sensitive data
├── .streamlit/            # Streamlit configuration directory
├── streamlit_app.py       # Main application file
├── requirements.txt       # Project dependencies
└── url/                   # Directory containing URL-related data
```

## Files Description

- `streamlit_app.py`: The main application file containing the Streamlit web interface and core functionality for article processing, translation, and summarization.
- `.env`: Contains sensitive environment variables like API keys (not tracked in git)
- `.gitignore`: Specifies which files Git should ignore (includes .env and other sensitive files)
- `requirements.txt`: Lists all Python dependencies required to run the project

## Setup and Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory and add your API key:
   ```
   API_KEY=your_groq_api_key_here
   ```
4. Run the application:
   ```bash
   streamlit run streamlit_app.py
   ```

## Dependencies

- streamlit (>=1.30.0): Web application framework
- requests (>=2.31.0): HTTP library for making API requests
- python-dotenv (>=1.0.0): Environment variable management
- beautifulsoup4 (>=4.12.0): Web scraping and HTML parsing

## Security

- API keys are stored in the `.env` file
- The `.gitignore` file prevents sensitive data from being committed to the repository
- Environment variables are loaded securely using python-dotenv

## Usage

1. Start the application using `streamlit run streamlit_app.py`
2. Enter a news article URL in the input field
3. Select your desired target language
4. Click the process button to get the translated and summarized content

## Note

Make sure to keep your API keys confidential and never commit them to version control. Always use the `.env` file for storing sensitive information.
