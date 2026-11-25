QUERY_INSTRUCTION = (
    "Given a real estate search query in English, retrieve the Portuguese property listings "
    "that best match the buyer's intent."
)


def build_query_prompt(query: str) -> str:
    """Wrap a search query with the retrieval instruction; documents get no prefix.

    Args:
        query: The buyer's search text.
    """
    return f"Instruct: {QUERY_INSTRUCTION}\nQuery: {query}"
