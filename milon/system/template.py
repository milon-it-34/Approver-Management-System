
from django import template

register = template.Library()
import re


def regex(pat):
    def inner(fn):
        fn.regex = re.compile(pat)
        return fn

    return inner


@register.filter
@regex(r'[A-Z]*[^A-Z]*')
def wordize(value, arg=None):
    return ' '.join(wordize.regex.findall(str(value))[:-1])



