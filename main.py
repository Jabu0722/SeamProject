import DataScraper
import URLInput
import OutputToJSON
import logging
import argparse

logging.basicConfig(level=logging.INFO)

def main():
    """
    Main function to scrape Instagram post data and export it to a JSON file.
    """

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Scrape Instagram post data and export to JSON.")
    parser.add_argument("url", type=str, help="The URL of the Instagram post to scrape.")
    parser.add_argument("--headers", help="Path to the headers JSON file (optional).", default=None)
    parser.add_argument("--output", type=str, help="Path to the output JSON file (optional).", default="output.json")
    
    args = parser.parse_args()

    logging.info(f"URL: {args.url}, Headers File Path: {args.headers}, Output File Path: {args.output}")

    if args.url is None or not isinstance(args.url, str):
        logging.error("URL argument is missing or invalid.")
        raise ValueError("A valid URL must be provided.")
    
    try:
        # Scrape the data
        likes, comments = DataScraper.scrapeData(args.url, headersFilePath=args.headers)

        if likes is None or comments is None:
            logging.error("Failed to scrape data from the provided URL.")
            return

        # Export data to JSON
        OutputToJSON.exportToJSON(likes, comments, jsonFilePath=args.output)

        logging.info("Data scraping and export completed successfully.")

    except ValueError as ve:
        logging.error(f"Value Error: {ve}")
    except Exception as e:
        logging.error(f"An unexpected error has occurred (Main): {e}")

if __name__ == "__main__":
    main()