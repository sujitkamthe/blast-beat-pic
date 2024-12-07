import io
import math
from io import BytesIO

from PIL import Image

BIT_DEPTH = 16

def compress_image(path: str) -> BytesIO:
    with Image.open(path) as image:
        if image.mode == 'RGBA':
            image = image.convert('RGB')
        aspect_ratio = image.width / image.height

        # 2048 = height * aspect_ratio * height * Bit Depth / 8
        new_height = math.sqrt(int((2048 * 8) / (aspect_ratio * BIT_DEPTH)))
        new_width = int(new_height * aspect_ratio)
        new_image = image.resize((new_width, new_height))
        output = io.BytesIO()
        new_image.save(output, format='JPEG')
        return output

