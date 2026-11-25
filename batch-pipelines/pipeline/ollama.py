import numpy as np
import requests

from pipeline.config import EMBED_MODEL, OLLAMA_HOST, REQUEST_TIMEOUT_SECONDS


def embed(texts: list[str]) -> list[list[float]]:
    """Embed texts with Ollama and L2-normalize each vector.

    Args:
        texts: Texts to embed.
    """
    response = requests.post(
        f"{OLLAMA_HOST}/api/embed",
        json={"model": EMBED_MODEL, "input": texts},
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    vectors = np.array(response.json()["embeddings"], dtype=float)
    return (vectors / np.linalg.norm(vectors, axis=1, keepdims=True)).tolist()
