import os
import json
from PIL import Image, ExifTags
from datetime import datetime
import re


def extract_identifier_from_url(url):
    # Extract the identifier from the URL using a regular expression
    match = re.search('/([^_\/]*)_(.*)_o\.jpg$', url)
    if match:
        return match.group(1)
    else:
        print()
        return None


def update_creation_date(image_path, date_taken):
    # Convert date_taken to datetime object
    date_taken = datetime.strptime(date_taken, "%Y-%m-%d %H:%M:%S")

    # Update the creation date of the image file
    os.utime(image_path, (date_taken.timestamp(), date_taken.timestamp()))


def process_images(json_folder, jpg_folder):
    # Iterate through each JSON file in the given folder
    for json_filename in os.listdir(json_folder):
        if json_filename.endswith(".json"):
            json_path = os.path.join(json_folder, json_filename)

            # Load JSON data from the file
            with open(json_path, "r") as json_file:
                data = json.load(json_file)

            try:
                if data.get("original"):

                    # Extract the identifier from the "original" property
                    identifier = extract_identifier_from_url(data.get("original"))

                    if identifier:

                        # Find the matching file in the JPG folder
                        matching_files = [file for file in os.listdir(jpg_folder) if identifier in file]

                    if matching_files:
                        # Take the first matching file (you may need additional logic if there are multiple matches)
                        image_filename = matching_files[0]

                        # Construct the full path to the corresponding JPG file
                        image_path = os.path.join(jpg_folder, image_filename)

                        # Update the creation date of the JPG file
                        update_creation_date(image_path, data["date_taken"])
                        update_exif_creation_date(image_path, data["date_taken"])
                        # print(f"Updated creation date for {image_filename}")
                    else:
                        print(f"JPG file not found for {json_filename}")
                else:
                    print(f"Unable to extract identifier from {json_filename}")
            except:
                print(f"Unable to process {json_filename}")


def update_exif_creation_date(image_path, new_creation_date_string):
    try:
        # Open the image using Pillow
        image = Image.open(image_path)

        # Get the existing EXIF data
        exif_data = image._getexif()

        # Check if the image has EXIF data
        if exif_data is not None:
            # Find the tag for the original creation date
            for tag, value in exif_data.items():
                if ExifTags.TAGS.get(tag) == "DateTimeOriginal":
                    # Update the creation date in the EXIF data
                    new_creation_date = datetime.strptime(new_creation_date_string, "%Y-%m-%d %H:%M:%S")
                    exif_data[tag] = new_creation_date.strftime("%Y:%m:%d %H:%M:%S")

                    # Save the modified EXIF data back to the image
                    image.save(image_path, exif=image.info["exif"])

                    return

        # If the original creation date tag is not found
        print("Image missing EXIF data:", image_path)
        
    except Exception as e:
        print(f"Error updating EXIF data: {e}")


if __name__ == "__main__":
    # Specify the paths to your JSON and JPG folders
    json_folder = "./metadata"
    jpg_folder = "./photos"

    # Process the images and update creation dates
    process_images(json_folder, jpg_folder)
