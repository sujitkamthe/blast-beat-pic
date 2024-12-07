from io import BytesIO
from typing import Any

import requests

sounds = [
    "forzee_kick",
    "forzee_snare",
    "forzee_hihat",
    "forzee_tom_lo",
    "forzee_ride",
    "forzee_crash",
    "forzee_tom_hi",
    "forzee_tom_med"
]

slot_prop_names = [
    "slot_volume",
    "slot_pitch",
    "slot_delay",
    "slot_lowpass",
    "slot_lowpass_q",
    "slot_variant",
    "slot_rest",
    "slot_pan"
]

headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Origin": "https://www.onemotion.com",
        "Referer": "https://www.onemotion.com/drum-machine/",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"

    }

def convert_to_blast_beat(bytes: BytesIO) -> dict[str, Any]:
    image_bytes = bytes.getvalue()
    # convert image_bytes to binary string
    image_bits = ''.join(format(x, '08b') for x in image_bytes)
    print(image_bits)
    tracks = get_tracks(image_bits)
    payload = drum_machine_payload(tracks)
    return payload


def get_tracks(image_bits: str) -> list[list[int]]:
    # push each bit into a separate array. Total 64 arrays.
    # Each array will be a track.
    tracks = [[] for _ in range(64)]
    for i, bit in enumerate(image_bits):
        tracks[i % 64].append(int(bit))
    return tracks


def drum_machine_payload(tracks: list[list[int]]) -> dict:
    # get 8 items from the list at a time
    payload: dict[str, Any] = {
        "application": "OneMotion Drum-Machine",
        "kit": "forzee",
        "tempo": 90,
        "shuffle": 0.67,
        "pitch": 8,
        "reverb": 0.4,
        "lowpass": 1,
        "lowpass_q": 0,
        "beats": 8,
        "beat_div": 8,
        "slot_count": 16,
        "effect_type": "studio",
        "effect_amount": 1,
        "beats_per_bar": 4,
        "bars": 32,
        "config": {
            "trackOrder": "default"
        }
    }
    sound_number = 0
    tracks_payload: list[dict[str, Any]] = list()
    for i in range(0, len(tracks), 8):
        slot_props = tracks[i:i + 8]
        sound_name = sounds[sound_number]
        tracks_payload.append(get_track(slot_props, sound_name))
        sound_number += 1
    tracks_payload.append(null_track())
    payload["tracks"] = tracks_payload
    return payload

def get_track(slot_props: list[list[int]], sound_name: str) -> dict[str, Any]:
    track: dict[str, Any] = {
        "sound": sound_name,
        "volume": 1,
        "pitch": 0,
        "delay": 0,
        "delay_steps": 3,
        "lowpass": 1,
        "lowpass_q": 0,
        "variant": 0,
        "rest": 0,
        "pan": 0,
        "shift": 0,
        "effect": 1,
        "slot_effect": [],
        "repeat": 0,
    }
    for slot_prop_name, slot_prop in zip(slot_prop_names, slot_props):
        track[slot_prop_name] = get_slot_dict(slot_prop)
    return track


def get_slot_dict(slot_prop: list[int]) -> dict[str, int]:
    return {str(i): slot_prop[i] for i in range(len(slot_prop))}


def create_drum_machine_project(payload: dict[str, Any]) -> str:
    # make a post request to https://www.onemotion.com/drum-machine/share_as_link.php with payload
    response = requests.post("https://www.onemotion.com/drum-machine/share_as_link.php", headers=headers, json=payload)
    print(response.status_code)
    print(response.text)
    return response.json()["code"]

def decode_image(code: str) -> BytesIO:
    data = get_saved_drum_machine(code)
    track_data: list[dict[str, Any]] = data["content"]["tracks"]
    tracks = []
    for sound in sounds:
        td = next(td for td in track_data if td["sound"] == sound)
        for slot_prop_name in slot_prop_names:
            slot_props = td[slot_prop_name]
            tracks.append(slot_props)

    # convert tracks to image bits. Take 1 bit from each track and append. there are 64 tracks. each track will  have different length.
    image_bits: list[str] = []
    max_length_track = max(len(track) for track in tracks)
    for i in range(0, max_length_track):
        for track in tracks:
            if i < len(track):
                image_bits.append(str(track[i]))
    image_bits_str = ''.join(image_bits)
    print(image_bits_str)
    image_bytes = int(image_bits_str, 2).to_bytes((len(image_bits_str)) // 8, 'big')
    return BytesIO(image_bytes)





def get_saved_drum_machine(code: str) -> dict[str, Any]:
    response = requests.post(f"https://www.onemotion.com/drum-machine/share_as_link.php?code={code}", headers=headers)
    print(response.status_code)
    print(response.text)
    return response.json()


def null_track() -> dict[str, Any]:
    return {
      "sound": None,
      "volume": 1,
      "pitch": 0,
      "delay": 0,
      "delay_steps": 3,
      "lowpass": 1,
      "lowpass_q": 0,
      "rest": 0,
      "pan": 0,
      "slot_volume": [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0
      ],
      "slot_pitch": [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0
      ],
      "slot_delay": [
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1
      ],
      "slot_lowpass": [
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1
      ],
      "slot_lowpass_q": [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0
      ],
      "slot_variant": [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0
      ],
      "slot_rest": [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0
      ],
      "slot_flam": [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0
      ],
      "slot_pan": [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0
      ],
      "slot_effect": {},
      "shift": 0,
      "repeat": 0,
      "effect": 1
    }