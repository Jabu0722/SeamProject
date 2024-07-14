import json
import logging

logging.basicConfig(level=logging.INFO)

def exportToJSON(likes: list[str], comments: list[dict], jsonFilePath: str = 'output.json') -> None:

    """
    Export likes and comments to a JSON file.

    Args:
        likes (list of strings): all usernames of people who liked the specified post.
        comments (list of strings): all comments from the specified post formatted as a dictionary with username/comments as the key-value pairs
        json_file_path (str): The file path to save the JSON output. Defaults to 'output.json'.

    Raises:
        IOError: If there is an issue writing to or reading from the file.
    """

    # Ensure likes and comments are lists

    if not isinstance(likes, list):
        raise ValueError("Likes should be a list.")
    if not isinstance(comments, list):
        raise ValueError("Comments should be a list.")

    data = {
        'likes': likes,
        'comments': comments
    }
    try: 
        with open(jsonFilePath, 'w') as file:
            json.dump(data, file, indent=4)
            # Confirm data was written to the file
            logging.info(f"Data exported to {jsonFilePath}")

        # Read the file to confirm the content
        with open(jsonFilePath, 'r') as file:
            content = file.read()
            logging.info("File content:", content)

    except IOError as e:
        logging.error("An error occurred while handling the file: %s", e)

    except Exception as e:
        logging.error("An unexpected error occurred (OutputToJSON): %s", e)
