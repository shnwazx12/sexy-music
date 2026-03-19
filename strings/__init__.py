import os
from typing import List

import yaml

languages = {}
languages_present = {}

# Use absolute path so it works regardless of working directory (Render, Docker, etc.)
_LANGS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "langs")


def get_string(lang: str):
    return languages.get(lang, languages.get("en", {}))


for filename in os.listdir(_LANGS_DIR):
    if "en" not in languages:
        languages["en"] = yaml.safe_load(
            open(os.path.join(_LANGS_DIR, "en.yml"), encoding="utf8")
        )
        languages_present["en"] = languages["en"]["name"]
    if filename.endswith(".yml"):
        lang_code = filename[:-4]
        if lang_code not in languages:
            languages[lang_code] = yaml.safe_load(
                open(os.path.join(_LANGS_DIR, filename), encoding="utf8")
            )
            languages_present[lang_code] = languages[lang_code]["name"]
