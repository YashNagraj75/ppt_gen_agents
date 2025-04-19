import base64
import io
import os
from urllib.parse import urlparse

import requests
from googleapiclient.discovery import build
from PIL import Image


def encode_images():
    base_dir = os.path.dirname(__file__)  # path to utils.py
    # Get all the image paths in the assets directory
    assets_dir = os.path.join(base_dir, "assets")
    image_paths = [
        os.path.join("assets", filename)
        for filename in os.listdir(assets_dir)
        if filename.lower().endswith((".png", ".jpg", ".jpeg"))
    ]

    images_data = {}
    for relative_path in image_paths:
        full_path = os.path.join(base_dir, relative_path)

        with Image.open(full_path) as img:
            max_size = (800, 600)  # Reasonable size that preserves details
            img.thumbnail(max_size, Image.Resampling.LANCZOS)

            buffer = io.BytesIO()
            img.save(buffer, format="PNG", quality=70)  # Lower quality = smaller size
            buffer.seek(0)

            encoded_string = base64.b64encode(buffer.read()).decode("utf-8")

            images_data[relative_path] = {
                "url": f"data:image/png;base64,{encoded_string}",
                "detail": "low",  # Using "low" detail to further reduce payload size
            }
    return images_data


def fetch_image_urls(query: str, api_key: str, cse_id: str) -> list[str]:
    """
    Fetch image URLs from Google Custom Search API

    Args:
        query: str: search query
        api_key: str: Google API key
        cse_id: str: Google Custom Search Engine ID
        num_images: int: number of images to fetch

    Returns:
        List[str]: List of image URLs

    """
    # Build the service object
    service = build("customsearch", "v1", developerKey=api_key)

    # Perform the search
    try:
        res = (
            service.cse().list(q=query, cx=cse_id, searchType="image", num=3).execute()
        )
    except Exception:
        return []

    # Extract and return image URL
    if "items" in res:
        url_list = [item["link"] for item in res["items"]]
        for url in url_list:
            if url:
                parsed_url = urlparse(url)
                if parsed_url.scheme in ["http", "https"]:
                    try:
                        response = requests.get(url)
                        if response.status_code != 200:
                            url_list.remove(url)
                    except requests.RequestException as e:
                        print(f"Failed to fetch {url}: {e}")
                else:
                    print(f"Unsupported URL scheme {parsed_url.scheme} for URL: {url}")
        return url_list

    else:
        return []
