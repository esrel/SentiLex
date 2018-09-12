from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from builtins import str
from typing import Text, List, Dict, Any

from sentilex.taggers import Tagger

import string
import copy
import re

import logging
import argparse

logger = logging.getLogger(__name__)


class StringTypeTagger(Tagger):
    """
    Tag list of words with string type
    """
    name = "StringTypeTagger"
    match_dict = {"text": "", "start": None, "end": None, "value": None, "label": None}
    token_pattern = r'\b(?:%s)\b'
    punct_pattern = r'(?:%s)'      # TODO: risky?

    def tag(self, text):
        """
        Tag input text with lexical entries
        :param text:
        :return:
        """
        if type(text) == str:
            text = text.strip().split()
        elif type(text) == list:
            pass
        else:
            logging.debug("Unsupported input format.")

        output = []
        begin = 0
        for w in text:
            str_type = self.get_string_type(w)
            # get indices
            start = ' '.join(text).index(w, begin)
            end = start + len(w)
            begin = end

            token = copy.deepcopy(self.match_dict)
            token['text'] = w
            token['start'] = start
            token['end'] = end
            token['label'] = str_type
            output.append(token)
            logger.debug('String Type of {} is {}'.format(w, str_type))

        return output

    @staticmethod
    def get_string_type(text):
        """
        Get string type for text
        :param text:
        :return:
        """
        str_type = None
        for char in text:
            if char in string.punctuation:
                char_type = 'punct'
            elif char in string.ascii_letters:
                char_type = 'alpha'
            elif char in string.digits:
                char_type = 'digit'
            else:
                char_type = 'other'

            if str_type:
                if str_type != char_type:
                    str_type = 'other'
                    break
            else:
                str_type = char_type
        return str_type


def create_argument_parser():
    parser = argparse.ArgumentParser(description='String Type Tagger')
    parser.add_argument('-d', '--data', type=str)
    return parser


if __name__ == "__main__":
    parser = create_argument_parser()
    args = parser.parse_args()

    tagger = StringTypeTagger()

    with open(args.data) as fh:
        for row in fh:
            print(tagger.tag(row))
