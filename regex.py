import re


def parse(text: str) -> str:
    rep = {" ": "_", "(": "", ")": ""}  # define desired replacements her

    # use these three lines to do the replacement
    rep = dict((re.escape(k), v) for k, v in rep.items())
    pattern = re.compile("|".join(rep.keys()))
    return pattern.sub(lambda m: rep[re.escape(m.group(0))], text)
