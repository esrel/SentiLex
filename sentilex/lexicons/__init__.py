from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from builtins import str
from typing import Text, List, Dict, Any


class Lexeme(object):
    """
    Lexeme Class
    """

    def __init__(self, text, data=None):
        self.text = text
        self.data = data if data else {}

    def set(self, prop, info):
        self.data[prop] = info

    def get(self, prop, default=None):
        return self.data.get(prop, default)

    def tolist(self):
        token_separator=self.data.get('token_separator', ' ')
        parts_separator=self.data.get('parts_separator', '..')
        tokens = [part.split(token_separator) for part in self.text.split(parts_separator)]
        return tokens
