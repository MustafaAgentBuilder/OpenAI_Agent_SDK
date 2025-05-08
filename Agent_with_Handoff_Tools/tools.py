"""
Agent Tools Module
------------------
Provides search and news-fetching tools for agent workflows using external APIs.
All API keys are loaded from environment variables for security.
"""

import os
import requests
import json
from typing import List, Dict, Any, Union
from agents import function_tool as tool
from dotenv import load_dotenv

load_dotenv()

SERPER_API_KEY = os.getenv("SERPER_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

@tool
def search_everything(query: str) -> Union[List[Dict[str, str]], Dict[str, str]]:
    """
    Search Google using the Serper API and return structured results.

    Args:
        query (str): The search query (e.g., 'latest AI news').

    Returns:
        list: A list of search result dicts (Title, Link, Snippet).
        dict: Error message in case of failure.
    """
    url = 'https://google.serper.dev/search'
    headers = {
        'X-API-KEY': SERPER_API_KEY,
        'Content-Type': 'application/json'
    }
    payload = {'q': query}

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        data = response.json()
        results = data.get('organic', [])
        output = [
            {
                'Title': result.get('title', ''),
                'Link': result.get('link', ''),
                'Snippet': result.get('snippet', '')
            }
            for result in results
        ]
        return output
    except requests.exceptions.RequestException as e:
        return {"error": f"An error occurred: {e}"}

@tool
def fetch_latest_news(category: str = 'general', country: str = 'us') -> Union[str, Dict[str, str]]:
    """
    Fetches the latest news headlines from the NewsAPI.

    Args:
        category (str): The news category (default: 'general').
        country (str): The country code (default: 'us').

    Returns:
        str: The latest news headlines.
        dict: Error message in case of failure.
    """
    url = f"https://newsapi.org/v2/top-headlines?category={category}&country={country}&apiKey={NEWS_API_KEY}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            articles = data.get('articles', [])
            if articles:
                news = [
                    f"{i+1}. {article['title']} (Source: {article['source']['name']})"
                    for i, article in enumerate(articles[:5])
                ]
                return "\n".join(news)
            else:
                return "No news articles found."
        else:
            return f"Error: Unable to fetch news (Status Code: {response.status_code})"
    except Exception as e:
        return {"error": str(e)}
