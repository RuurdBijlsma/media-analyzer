from pathlib import Path
from typing import Any

import numpy as np
import pytest
from numpy.typing import NDArray
from PIL import Image

from media_analyzer.machine_learning.embedding.open_clip_embedder import OpenCLIPEmbedder
from media_analyzer.machine_learning.embedding.zero_clip_embedder import ZeroCLIPEmbedder


@pytest.fixture(name="setup_zero_embedder")
def setup_zero_embedder_fixture(
    assets_folder: Path,
) -> tuple[ZeroCLIPEmbedder, list[Image.Image], NDArray[Any]]:
    """Set up the CLIPEmbedder and images for testing."""
    embedder = ZeroCLIPEmbedder()

    # Load images and create embeddings
    tent_img = Image.open(assets_folder / "tent.jpg")
    cluster_img = Image.open(assets_folder / "cluster.jpg")
    sunset_img = Image.open(assets_folder / "sunset.jpg")
    images: list[Image.Image] = [tent_img, cluster_img, sunset_img]
    images_embedding = embedder.embed_images(images)

    return embedder, images, images_embedding


@pytest.fixture(name="setup_open_embedder")
def setup_open_embedder_fixture(
    assets_folder: Path,
) -> tuple[OpenCLIPEmbedder, list[Image.Image], NDArray[Any]]:
    """Set up the CLIPEmbedder and images for testing."""
    embedder = OpenCLIPEmbedder()

    # Load images and create embeddings
    tent_img = Image.open(assets_folder / "tent.jpg")
    cluster_img = Image.open(assets_folder / "cluster.jpg")
    sunset_img = Image.open(assets_folder / "sunset.jpg")
    images: list[Image.Image] = [tent_img, cluster_img, sunset_img]
    images_embedding = embedder.embed_images(images)

    return embedder, images, images_embedding


@pytest.mark.parametrize(
    ("query", "img_index"),
    [
        ("A sunset over naples.", 2),  # Index 2 corresponds to sunset_img
        ("A tent on a camping.", 0),  # Index 0 corresponds to tent_img
        (
            "A cluster of raspberry pis in front of a laptop.",
            1,
        ),  # Index 1 corresponds to cluster_img
    ],
)
@pytest.mark.cuda
def test_zero_clip_embedder(
    setup_zero_embedder: tuple[
        ZeroCLIPEmbedder,
        list[Image.Image],
        NDArray[Any],
    ],
    query: str,
    img_index: int,
) -> None:
    """Test the CLIPEmbedder."""
    embedder, _, images_embedding = setup_zero_embedder

    text_embedding = embedder.embed_text(query)
    # Calculate cosine similarities between text and each image
    similarities = images_embedding @ np.array(text_embedding)
    # Assert the highest similarity index matches the expected image index
    assert np.argmax(similarities).item() == img_index


@pytest.mark.parametrize(
    ("query", "img_index"),
    [
        ("A sunset over naples.", 2),  # Index 2 corresponds to sunset_img
        ("A tent on a camping.", 0),  # Index 0 corresponds to tent_img
        (
            "A cluster of raspberry pis in front of a laptop.",
            1,
        ),  # Index 1 corresponds to cluster_img
    ],
)
@pytest.mark.cuda
def test_open_clip_embedder(
    setup_open_embedder: tuple[
        OpenCLIPEmbedder,
        list[Image.Image],
        NDArray[Any],
    ],
    query: str,
    img_index: int,
) -> None:
    """Test the CLIPEmbedder."""
    embedder, _, images_embedding = setup_open_embedder

    text_embedding = embedder.embed_text(query)
    # Calculate cosine similarities between text and each image
    similarities = images_embedding @ np.array(text_embedding)
    # Assert the highest similarity index matches the expected image index
    assert np.argmax(similarities).item() == img_index
