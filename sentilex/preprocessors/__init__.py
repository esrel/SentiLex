from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from builtins import str
from typing import Text, List, Dict, Any


class Preprocessor(object):

    # pre-processor name
    name = None

    # list of supported languages
    languages = []

    # list of required properties
    provides = []

    # list of provided properties
    requires = []

    # default parameters
    defaults = {}

    def process(self, text):
        raise NotImplementedError("Tagger needs to be able to tag text.")
