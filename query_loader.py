from pathlib import Path
from jinja2 import Template


def load_named_query(file_path, query_name):
    """
    Loads a named/labelled query from an SQL file using -- name: <query_name> blocks.
    """
    content = Path(file_path).read_text()
    blocks = content.split("-- name:")
    for block in blocks:
        if block.strip().startswith(query_name):
            return "\n".join(block.strip().splitlines()[1:])
    raise ValueError(f"Query '{query_name}' not found in {file_path}")


def render_query(template_str, **kwargs):
    """
    Renders an SQL query string with Jinja variables for queries that accept inputs.
    """
    return Template(template_str).render(**kwargs)
