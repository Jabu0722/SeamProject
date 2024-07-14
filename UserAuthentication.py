from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
import time
import json
from selenium.common.exceptions import TimeoutException, ElementNotVisibleException, ElementNotInteractableException, WebDriverException, JavascriptException
import logging
import os

logging.basicConfig(level=logging.INFO)

def loadHeaders(headersFilePath: str) -> dict:
    """
    Load headers from a JSON file.

    Args:
        headersFilePath (str): The path to the headers JSON file.

    Returns:
        dict: A dictionary of headers.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        ValueError: If the content of the file is not a valid JSON dictionary.
        IOError: If an I/O error occurs while reading the file.
        json.JSONDecodeError: If the JSON is not properly formatted.
    """

    if not os.path.isfile(headersFilePath):
        logging.error(f"File not found: {headersFilePath}")
        raise FileNotFoundError(f"File not found: {headersFilePath}")

    try:
        with open(headersFilePath, 'r') as f:
            config = json.load(f)
            if not isinstance(config, dict):
                logging.error(f"The content of {headersFilePath} is not a dictionary.")
                raise ValueError("Invalid JSON content: Expected a dictionary.")
            
        return config
    
    except FileNotFoundError:
        logging.error(f"File not found {headersFilePath}")
        raise
    except IOError as e:
        logging.error(f"Error reading file {headersFilePath}: {e}")
        raise
    except json.JSONDecodeError as e:
        logging.error(f"Invalid JSON format in file {headersFilePath}: {e}")
        raise

def check_captcha(driver) -> None:
    """
    Check for the presence of a CAPTCHA and prompt the user to solve it.

    Args:
        driver (webdriver): The Selenium WebDriver instance.

    Raises:
        Exception: If an unexpected error occurs while checking for CAPTCHA.
    """

    try:
        # Adjust the selector as needed for the captcha element
        captcha_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[name^='a-'][src^='https://www.google.com/recaptcha/api2/anchor?']"))
        )
        print("Captcha detected. Please solve it manually.")
        input("Press Enter after solving the captcha...")

    except TimeoutException:
        logging.info("No captcha detected.")
    except Exception as e:
        logging.error(f"Unexpected error while checking captcha (UserAuthentication): {e}")

def scroll_comment_section(driver) -> None:
    """
    Scroll through the comment section of the post to load all comments.

    Args:
        driver (webdriver): The Selenium WebDriver instance.

    Raises:
        Exception: If an error occurs while scrolling the comment section.
    """

    # Locate the comment section using XPath (make sure to update this with the correct XPath)
    try:
        commentSection = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.x5yr21d.xw2csxc.x1odjw0f.x1n2onr6')))

        # Scroll through the comment section
        lastHeight = driver.execute_script("return arguments[0].scrollHeight", commentSection)
        while True:
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", commentSection)
            time.sleep(3.5)  # Adjust sleep time as needed
            newHeight = driver.execute_script("return arguments[0].scrollHeight", commentSection)
            if newHeight == lastHeight:
                break
            lastHeight = newHeight

    #error handling
    except TimeoutException:
        logging.error("Timed out waiting for the comment section to load.")
        raise
    except ElementNotInteractableException:
        logging.error("Comment section is not interactable.")
        raise
    except WebDriverException as e:
        logging.error(f"WebDriver exception occurred: {e}")
        raise
    except JavascriptException as e:
        logging.error(f"JavaScript execution error while scrolling: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error has occurred (UserAuthentication): {e}")
        raise
          
def checkFor2FA(driver) -> None:
    """
    Checks for signs of 2FA and asks for manual intervention if necessary

    Args:
        driver (webdriver): The Selenium WebDriver instance.

    Raises:
        Exception: If an error occurs while scrolling the comment section.
    """
    try:
        two_factor_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//span[@class="_aa4a" and text()="Security Code"]')))

        input("Press Enter after you've entered the verification code...")

        time.sleep(5)  # Wait for verification to complete

    except TimeoutException:
        logging.info("No 2FA required.")
    
    except Exception as e:
        logging.info(f"Unexpected error has occurred (UserAuthentication): {e}")

def userAuthenticator(url: str, username: str, password: str, headerFilePath = None) -> tuple:
    """
    Authenticate the user with Instagram and scrape likes and comments from a post.

    Args:
        url (str): The URL of the Instagram post.
        username (str): The Instagram username.
        password (str): The Instagram password.
        headerFilePath (str, optional): Path to a JSON file with headers.

    Returns:
        tuple: HTML content of the post and HTML content of the 'liked by' section.

    Raises:
        Exception: If an error occurs during the authentication and scraping process.
    """
    
    options = Options()

    if headerFilePath is not None:

        headers = loadHeaders(headerFilePath)

        for header, value in headers.items():
            options.add_argument(f"--header={header}: {value}")
            
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
            
        time.sleep(2)

        check_captcha(driver=driver)
        
        logInLink = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Log In')]")))
        logInLink.click()

        usernameButton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
        time.sleep(1)
        passwordButton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))
            
        time.sleep(2)

        usernameButton.clear()
        passwordButton.clear()

        usernameButton.send_keys(f"{username}")
        passwordButton.send_keys(f"{password}")
        loginButton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))

        time.sleep(5)

        loginButton.click()

        time.sleep(5)

        checkFor2FA(driver=driver)

        notNowButton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and contains(text(), 'Not now')]")))
        notNowButton.click()

        try:
            notNowButton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and contains(text(), 'Not Now')]")))
            notNowButton.click()
        except (TimeoutException, ElementNotInteractableException):
            pass
        
        time.sleep(3)

        driver.refresh()     

        scroll_comment_section(driver=driver)      

        html = driver.page_source

        url = url = url[0:40] + "liked_by/"
        
        driver.get(url)

        time.sleep(20)

        likesHTML = driver.page_source

    except Exception as e:
        logging.error(f"Error during authentication: {e}")
        return None, None
    
    finally:
        driver.quit()

    return html, likesHTML



