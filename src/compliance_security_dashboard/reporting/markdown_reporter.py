"""Markdown report rendering placeholder."""

from jinja2 import Template


def render_markdown(template_text: str, context: dict[str, object]) -> str:
    """Render a Markdown report from a template string."""
    return Template(template_text).render(**context)
