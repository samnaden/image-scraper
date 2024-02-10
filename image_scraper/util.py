import os
import logging
import requests


def download_image(image_url: str, image_name: str, destination_folder: str):
    logging.info(f"downloading {image_url}")
    img_data = requests.get(image_url).content
    image_dest = os.path.join(destination_folder, image_name)
    with open(image_dest, "wb") as handler:
        handler.write(img_data)
