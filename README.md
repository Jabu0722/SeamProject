# SeamProject

## Instagram Data Scraper

This tool scrapes likes and comments from Instagram posts through the command prompt interface. It authenticates users, validates URLs, and outputs the scraped data to a JSON format. 

## Features
- Authenticates Instagram users
- Validates Instagram post URLs
- Scrapes likes and comments from Instagram posts
- Outputs the data to a JSON file

## Dependencies
- BeautifulSoup (bs4)
- Selenium
- Logging
- JSON
- OS

## Setup

### Prerequisites
- Python 3.11.5
- Google Chrome
- ChromeDriver (Ensure the version matches your installed Chrome browser version)

### Install Required Python Packages

```sh
pip install bs4 selenium
```

### Environmental Variables

Set the following environment variables with your Instagram credentials:

#### Windows
```sh
#Using command prompt
set INSTAGRAM_USERNAME="your_username"
set INSTAGRAM_PASSWORD="your_password"

#Using powershell
[System.Environment]::SetEnvironmentVariable('INSTAGRAM_USERNAME', 'your_username', 'User')
[System.Environment]::SetEnvironmentVariable('INSTAGRAM_PASSWORD', 'your_password', 'User')
```

#### MacOS/Linux
```sh
#For temporary sessions
export INSTAGRAM_USERNAME="your_username"
export INSTAGRAM_PASSWORD="your_password"

#For permanent sessions
echo 'export INSTAGRAM_USERNAME="your_username"' >> ~/.bashrc
echo 'export INSTAGRAM_PASSWORD="your_password"' >> ~/.bashrc
```

### Download ChromeDriver

Make sure to download ChromeDriver at https://developer.chrome.com/docs/chromedriver and add it to your system PATH.

## Usage
### Command Line Interface
1. Clone the repository
```sh
#Create a folder for the repository. Copy and paste the folder's path and then use the following commands:
cd YOUR_PATH
git clone https://github.com/Jabu0722/SeamProject.git
```
2. Start up a virtual environment and run the script
```sh
   #Use the following the commands:
   py -m venv venv  (Verify that the Script folder is in the directory after the installation is done)

   #For windows:
   venv\Scripts\activate

   #For MacOS/Linux:
   source venv/bin/activate

   #Now install the required packages:
   pip install beautifulsoup4
   pip install selenium

   #Run the script:
   python main.py "https://www.instagram.com/p/your_post_url/" --headers "path/to/headers.json" --output "path/to/output.json"

   #url: The Instagram post URL to scrape.
   #--headers: (Optional) Path to the headers JSON file.
   #--output: (Optional) Path to the output JSON file. Defaults to output.json if not provided.

   #Deactivate the environment once you're done with the following command:
   deactivate

   #IMPORTANT NOTE: If you have 2FA on, you will need to manually input your credentials and then press enter in the command line when done
 ```  
### JSON Headers File
If you want to provide custom headers for web scraping, create a JSON file (e.g., headers.json) with the headers:

## Modules

### main.py
The main script to run the tool.

### scrapeData.py
Contains the scrapeData function to scrape likes and comments.

### URLInput.py
Contains the validateInstagramURL function to validate Instagram post URLs.

### OutputToJSON.py
Contains the exportToJSON function to export data to a JSON file.

### UserAuthentication.py
Contains functions to authenticate the user and handle web scraping.

## Contact

For any questions or issues, please open an issue on GitHub or contact me at [jabuinquiries@gmail.com].





   











