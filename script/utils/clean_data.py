import re


COMMENT = re.compile(r"""
    <!-- (.*?) -->
""", re.VERBOSE | re.DOTALL)

HEAD = re.compile(r"""
    <head (.*?) > .*? </head>
""", re.VERBOSE | re.DOTALL)

SCRIPT = re.compile(r"""
    <script (.*?) > .*? </script>
""", re.VERBOSE | re.DOTALL)

STYLE = re.compile(r"""
    <style (.*?) > (.*?) </style>
""", re.VERBOSE | re.DOTALL)

LINK = re.compile(r"""
    <link .*? />
""", re.VERBOSE | re.DOTALL)

CONDITIONAL = re.compile(r"""
    \[if .*? \] .*? \[endif\]
""", re.VERBOSE | re.DOTALL)

HEAD = re.compile(r"""
    <head> .*? </head>
""", re.VERBOSE | re.DOTALL)


def clean(data):
    for regex in (COMMENT, HEAD, CONDITIONAL, SCRIPT, STYLE, LINK):
        data = regex.sub("", data)
    return data


def visible_text(soup):
    for elem in soup.findAll(['head', 'script', 'style']):
        elem.extract()
    texts = soup.findAll(text=True)
    def visible(element):
        if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
            return False
        elif COMMENT.match(element):
            return False
        return True

    visible_texts = filter(visible, texts)
    return "".join(visible_texts)

