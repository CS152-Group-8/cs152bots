import asyncio
import os
from typing import List

import httpx
import tensorflow as tf

model_dict = {
    "minor_detection": tf.keras.models.load_model(
        os.path.join(os.path.dirname(__file__), "models/minor_detection/model.hdf5")
    ),
    "nudity_detection": tf.keras.models.load_model(
        os.path.join(os.path.dirname(__file__), "models/nudity_detection/model.hdf5")
    ),
}


async def fetch_image(client: httpx.AsyncClient, image_url: str) -> bytes:
    """
    Asynchronously fetch an image from a URL.
    """
    response = await client.get(image_url, timeout=10)
    if response.status_code != 200:
        print(f"Failed to fetch image from {image_url}")
        return None
    return response.content


async def fetch_images(image_urls: List[str]) -> List[bytes]:
    """
    Concurrently fetch a list of images from URLs.
    """
    async with httpx.AsyncClient() as client:
        return await asyncio.gather(
            *[fetch_image(client, image_url) for image_url in image_urls]
        )


def process_images(images: List[bytes]) -> tf.Tensor:
    """
    Convert a list of images (as bytes) into a tensor.
    """
    array = []
    for image in images:
        try:
            image = tf.io.decode_image(image, channels=3)
        except tf.errors.InvalidArgumentError:
            print("Failed to decode image")
            continue
        image = tf.image.resize(image, [224, 224])
        image = tf.keras.applications.mobilenet_v2.preprocess_input(image)
        array.append(image)
    return tf.stack(array)


async def images_include_minors(images: List[str]) -> bool:
    """
    Run a list of Discord image URLs through our minor detection model and return
    whether or not any of them are predicted to contain minors.
    """
    image_data = await fetch_images(images)
    batch = process_images(image_data)

    # check if tensor is empty

    model = model_dict["minor_detection"]
    predictions = (model.predict(batch, verbose=0) > 0.5).flatten()
    return any(predictions)


async def images_include_nudity(images: List[str]) -> bool:
    """
    Run a list of Discord image URLs through our nudity detection model and return
    whether or not any of them are predicted to contain nudity.
    """
    image_data = await fetch_images(images)
    batch = process_images(image_data)

    # check if tensor is empty

    model = model_dict["nudity_detection"]
    predictions = (model.predict(batch, verbose=0) <= 0.5).flatten()
    return any(predictions)
