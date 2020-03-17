from typing import Dict, List
from pathlib import Path
import json

from pdf_generation.content import Content, Text, Frame, Value


class Template:
    def __init__(self, path: Path):
        self.path: Path = path
        self.load_template()

    def load_template(self) -> List[Content]:
        with open(self.path.resolve().as_posix()) as json_template:
            return list(
                Content(dict_content) for dict_content in json.load(json_template)
            )


class DescriptorTemplate(Template):
    def load_template(self) -> List[Text]:
        with open(self.path.resolve().as_posix()) as json_template:
            return list(Text(dict_text) for dict_text in json.load(json_template))


class FrameTemplate(Template):
    def load_template(self) -> List[Frame]:
        with open(self.path.resolve().as_posix()) as json_template:
            return list(Frame(dict_frame) for dict_frame in json.load(json_template))


class ValueTemplate(Template):
    def load_template(self):
        with open(self.path.resolve().as_posix()) as json_template:
            return list(Value(dict_value) for dict_value in json.load(json_template))
