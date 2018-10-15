from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


class Scorer(object):
    """
    Scorer Class template
    """
    name = None
    languages = []
    requires = []
    provides = []
    defaults = {}

    def score(self, text):
        raise NotImplementedError("scorer needs score method.")


def nominalize(score):
    """
    Convert score to nominal value
    :param score:
    :return:
    """
    if score > 0:
        return 'positive'
    elif score < 0:
        return 'negative'
    else:
        return 'neutral'