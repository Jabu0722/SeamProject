import re

def validateInstagramURL(url: str) -> bool:

    """
    Validate whether the given URL is a valid Instagram post URL.

    Args:
        url (str): The URL to be validated.

    Returns:
        bool: True if the URL is a valid Instagram post URL, False otherwise.
    """

    if not isinstance(url, str):
        raise ValueError("URL must be a string.")
    
    sitePattern = f"https?://(www\.)?instagram\.com"
    postPattern = f"/p"

    return bool(re.search(sitePattern, url)) and bool(re.search(postPattern, url)) 


