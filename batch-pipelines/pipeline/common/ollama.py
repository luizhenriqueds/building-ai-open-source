import base64

import numpy as np
import requests

from pipeline.common.config import (
    EMBED_MODEL,
    OLLAMA_HOST,
    REQUEST_TIMEOUT_SECONDS,
    VISUAL_MODEL,
    VISUAL_NUM_CTX,
    VISUAL_SEED,
    VISUAL_TEMPERATURE,
    VISUAL_TIMEOUT_SECONDS,
)


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


def describe_image(image: bytes, prompt: str, schema: dict) -> str:
    """Ask the vision model about an image and return its JSON answer.

    Args:
        image: Raw image bytes.
        prompt: Instruction for the model.
        schema: JSON schema the answer must follow.
    """
    message = {"role": "user", "content": prompt, "images": [base64.b64encode(image).decode()]}
    response = requests.post(
        f"{OLLAMA_HOST}/api/chat",
        json={
            "model": VISUAL_MODEL,
            "messages": [message],
            "format": schema,
            "stream": False,
            "think": False,
            "options": {
                "temperature": VISUAL_TEMPERATURE,
                "seed": VISUAL_SEED,
                "num_ctx": VISUAL_NUM_CTX,
            },
        },
        timeout=VISUAL_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    return response.json()["message"]["content"]
