import mistune

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from pygments.util import ClassNotFound

class MySiteRenderer(mistune.Renderer):
    def block_code(self, code, lang):
        """
        Override mistune.Renderer.block_code to enable
        syntax highlighting with Pygments.
        https://github.com/lepture/mistune
        """
        if lang:
            try:
                lexer = get_lexer_by_name(lang, stripall=True)
            except ClassNotFound:
                code = lang + '\n' + code
                lang = None

        if not lang:
            return '\n<pre><code>%s</code></pre>\n' % \
                mistune.escape(code)

        formatter = HtmlFormatter()
        return highlight(code, lexer, formatter)

def markdown_to_html(md):
    """
    Returns `md` converted from markdown to html.
    """
    renderer = MySiteRenderer()
    markdown = mistune.Markdown(renderer=renderer)
    return markdown.render(md)
