from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from builtins import str
from typing import Text, List, Dict, Any


class Tagger(object):
    """
    Tagger Class template
    """
    # Tagger Name
    name = None

    # Default parameters
    defaults = {}

    def tag(self, text):
        raise NotImplementedError("Tagger needs to be able to tag text.")




