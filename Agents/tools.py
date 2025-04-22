import base64
import io
import os
from pprint import pprint
from urllib.parse import urlparse

import requests
from agents import function_tool
from google import genai
from google.genai import types
from googleapiclient.discovery import build
from PIL import Image
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (NoTranscriptFound,
                                            TranscriptsDisabled)

client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY"),
)


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


@function_tool
def get_image_description(query: str, num_images: int) -> list[str]:
    """
    Fetch image URLs from Google Custom Search API

    Args:
        query: str: search query
        num_images: int: number of images to fetch

    Returns:
        List[str]: List of image URLs and its description

    """
    api_key = os.environ.get("GEMINI_API_KEY")
    cse_id = os.environ.get("CSE_ID")

    # Build the service object
    service = build("customsearch", "v1", developerKey=api_key)

    # Perform the search
    try:
        res = (
            service.cse()
            .list(q=query, cx=cse_id, searchType="image", num=num_images)
            .execute()
        )
    except Exception:
        return []

    # Extract and return image URL
    image_desc = []
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
                        elif response.status_code == 200:
                            image_base64 = base64.b64encode(response.content).decode(
                                "utf-8"
                            )
                            # Get description using get_contents function
                            description = get_description(image_base64)
                            image_desc.append(
                                {
                                    "url": url,
                                    "description": description,
                                }
                            )

                    except requests.RequestException as e:
                        print(f"Failed to fetch {url}: {e}")
                else:
                    print(f"Unsupported URL scheme {parsed_url.scheme} for URL: {url}")
        return image_desc

    else:
        return []


def get_description(img_content):
    image = types.Part.from_bytes(
        data=base64.b64decode(img_content),
        mime_type="image/png",
    )
    model = "gemini-2.0-flash-001"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(
                    text="Generate a concise description of this image in about 50 words.",
                ),
                image,
            ],
        )
    ]

    response = client.models.generate_content(model=model, contents=contents)
    return response.text


@function_tool
def get_video_and_transcript(query):
    """
    Get video information and transcript from YouTube.

    Args:
        query (str): Search query for YouTube videos.
    Returns:
        dict: A dictionary containing the video URL and transcript.

    """
    api_key = os.environ.get("GEMINI_API_KEY")

    # Initialize YouTube Data API client
    youtube = build("youtube", "v3", developerKey=api_key)

    # Search for videos matching the query
    search_response = (
        youtube.search()
        .list(q=query, part="snippet", type="video", maxResults=3)
        .execute()
    )

    if not search_response["items"]:
        return {"error": "No videos found for the query."}

    # Iterate over the search responses and add them to a list of dict
    video_list = []
    for item in search_response["items"]:
        video_id = item["id"]["videoId"]
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])
            transcript_text = " ".join([entry["text"] for entry in transcript])
        except (TranscriptsDisabled, NoTranscriptFound):
            transcript_text = "Transcript not available for this video."

        video_list.append(
            {
                "video_url": video_url,
                "transcript": transcript_text[:1000],  # Limit to 1000 characters
            }
        )

    # Attempt to fetch the transcript
    return video_list
