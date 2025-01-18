from pathlib import Path

import numpy as np
from PIL import Image

from media_analyzer.machine_learning.clustering.hdbscan_clustering import perform_clustering
from media_analyzer.machine_learning.embedding.clip_embedder import CLIPEmbedder


def test_clustering(assets_folder: Path) -> None:
    image_names = [
        "ocr.jpg", "cat.jpg", "sunset.jpg", "cluster.jpg",
        "face1_a.jpg", "face1_b.jpg", "face2_a.jpg", "face2_b.jpg",
    ]
    embedder = CLIPEmbedder()
    images = [Image.open(assets_folder / image_name) for image_name in image_names]
    embeddings = [embedder.embed_image(image) for image in images]
    labels = perform_clustering(
        np.vstack(embeddings),
        min_samples=1,
        min_cluster_size=2,
    )
    assert isinstance(labels, list)
