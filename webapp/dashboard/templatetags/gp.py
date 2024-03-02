from django import template
import re
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter()
def highlight_search(text, keyword):
    if text is not None:
        text = str(text)
        match = re.search(re.escape(keyword), text, re.IGNORECASE)
        # highlight the content which matches the keyword
        if match:
            matched = match.group(0)
            highlighted = text.replace(matched, '<span class="highlight">{}</span>'.format(matched))
        # if not match display defualt
        else:
            highlighted = text
    else:
        highlighted = ''

    return mark_safe(highlighted)