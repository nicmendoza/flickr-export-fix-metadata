# Script to fix metadata for photos exported from Flickr
After exporting images from Flickr, you'll end up with a .zip folder of images and another with metadata files. By default, Flickr has removed the creation date from the EXIF data. This script restores it.

Requires Python 3 and the Pillow library

1. Install Python
2. Unzip and put the images in a folder called photos.
4. Unzip and put the metadata .json files in a folder called metadata.
5. Put this script in the same directory as those folders, and run it in a command line with:
```
pip install pillow
python process_images.py
```
