from bs4 import BeautifulSoup
import UserAuthentication
import URLInput
import os
import OutputToJSON 
import logging

logging.basicConfig(level=logging.INFO)

"""
Instagram Data Scraper

This module provides functionality to scrape likes and comments from Instagram posts.
It authenticates users, validates URLs, and outputs the scraped data to a JSON format.

Dependencies:
- BeautifulSoup (bs4)
- Selenium
- Logging
- JSON
- OS
"""

def loadCredentials() -> None:
    """
    Load Instagram credentials from environment variables.

    Returns:
        tuple: A tuple containing the Instagram username and password.

    Raises:
        ValueError: If the credentials are not set in environment variables.
    """

    username = os.getenv('INSTAGRAM_USERNAME')
    password = os.getenv('INSTAGRAM_PASSWORD')

    if not username or not password:
        logging.error("Credentials not found in environment variables.")
        raise ValueError("Credentials not set.")
    return username, password

def scrapeData(url: str, headersFilePath=None) -> tuple:
    """
    Scrape likes and comments from an Instagram post.

    Args:
        url (str): The URL of the Instagram post to scrape.
        headers_file_path (str, optional): Path to the headers file for web scraping.

    Returns:
        tuple: A tuple containing two lists: likes and comments.
               Each comment is a dictionary with 'username' and 'comment' as keys.

    Raises:
        ValueError: If the provided URL is not valid.
        Exception: For unexpected errors during scraping.
    """
    if not URLInput.validateInstagramURL(url=url):
        logging.error("Invalid Instagram URL provided.")
        raise ValueError("Enter a valid Instagram URL and try again")
    
    try:
        username, password = loadCredentials()

        if headersFilePath:
            logging.info(f"Loading headers from: {headersFilePath}")
        else:
            logging.info("No headers file path provided.")

        commentsHtml, likesHTML = UserAuthentication.userAuthenticator(url, username=username, password=password, headerFilePath=headersFilePath)

        soupForComments = BeautifulSoup(commentsHtml, 'html.parser')

        soupForLikes = BeautifulSoup(likesHTML, 'html.parser')

        likes = []
        likeElements = soupForLikes.find_all('span', class_="_ap3a")

        for element in likeElements:
            likes.append(element.text)

        comments = []
        commentElements = soupForComments.find_all('span', class_="x1lliihq x1plvlek xryxfnj x1n2onr6 x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye xvs91rp xo1l8bm x5n08af x10wh9bi x1wdrske x8viiok x18hxmgj" )
            
        for i in range(len(commentElements)):        
            if (i % 2 != 0 and i != len(commentElements) - 1):
                username = commentElements[i].text
                comment = commentElements[i + 1].text
                comments.append({'username': username, 'comment': comment })

        return likes, comments   
        
    except ValueError as ve:
        logging.error(f"Value Error: {ve}")
        raise
        return None, None
    except Exception as e:
        logging.error(f"An unexpected error has occurred (DataScraper): {e}")
        raise
        return None, None


