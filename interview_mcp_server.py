from mcp.server.fastmcp import FastMCP

mcp = FastMCP("interview-tools")

_ERROR_BUFFER = []

@mcp.tool()
def log_error(error_type: str, original_text: str, suggestion: str) -> dict:
    """Silently records a language error the learner made, for later feedback.

    Args:
        error_type: category, e.g. 'article', 'verb_tense', 'word_choice', 'register'
        original_text: what the learner actually said
        suggestion: the corrected/more natural version
    """
    _ERROR_BUFFER.append(
        {"type": error_type, "original": original_text, "suggestion": suggestion}
    )
    return {"status": "logged", "count": len(_ERROR_BUFFER)}

@mcp.tool()
def get_error_summary() -> dict:
    """Returns all language errors logged so far in this practice session."""
    return {"errors": _ERROR_BUFFER, "count": len(_ERROR_BUFFER)}

if __name__ == "__main__":
    mcp.run(transport="stdio")
