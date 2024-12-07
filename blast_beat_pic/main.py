import io
import json
from pprint import pprint

from PIL import Image

from blast_beat_pic.blas_beat import convert_to_blast_beat, create_drum_machine_project, decode_image


def encode():
    with Image.open("atom.png") as image:
        output = io.BytesIO()
        image.save(output, format='PNG')
        payload = convert_to_blast_beat(output)
        print(json.dumps(payload))
        code = create_drum_machine_project(payload)
        print(code)


def decode():
    image_bytes = decode_image("rbOc15290")
    image = Image.open(image_bytes)
    image.save("decoded.png")


if __name__ == '__main__':
    decode()