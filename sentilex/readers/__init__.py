from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


class Reader(object):
    """
    Tagger Class template
    """
    # Default parameters
    defaults = {}
    customs = {}

    def read(self, input_file):
        raise NotImplementedError("Reader needs read method.")