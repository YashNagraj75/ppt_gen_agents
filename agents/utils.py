import base64
import os
from PIL import Image
import io


def encode_images():
    base_dir = os.path.dirname(__file__)  # path to utils.py
    image_paths = [
        "assets/barSlide.png",
        "assets/Media.png",
        "assets/mediaLeftTextRight.png",
        "assets/textAndBulletPoints.png",
        "assets/title_slide.png",
        "assets/titleContentSlide.png",
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
                "detail": "low"  # Using "low" detail to further reduce payload size
            }
    return images_data
