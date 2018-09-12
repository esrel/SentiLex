from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from builtins import str
from typing import Text, List, Dict, Any

from sentilex.taggers import Tagger
from sentilex.readers.lexicon_reader_csv import LexiconReaderCsv
from sentilex.utils.span_utils import consolidate_spans

import copy
import re
import logging
import argparse

logger = logging.getLogger(__name__)


class RegexTagger(Tagger):
    """
    Tag list of words with lexical entries
    """
    name = "RegexTagger"
    defaults = {"token_separator": " ", "parts_separator": ".."}
    token_pattern = r'\b(?:%s)\b'
    parts_pattern = ".*?"  # too permissive

    match_dict = {"text": "", "start": None, "end": None, "value": None, "label": None}

    def __init__(self, lexicon=None, name=None):
        """
        :param lexicon:
        """
        self.name = name if name else self.name
        self.lexicon = self.load(lexicon)

    def load(self, lexicon):
        """
        Convert lexicon to regex
        :param lexicon:
        :param kwargs:
        :return:
        """
        lexicon_dict = {}
        for lexeme in lexicon:
            value = lexeme.get('value')
            if value not in lexicon_dict:
                lexicon_dict[value] = []

            parts = [re.escape(self.defaults.get('token_separator').join(part)) for part in lexeme.tolist()]
            pattern = self.parts_pattern.join(parts)
            lexicon_dict[value].append(pattern)

        patterns = {}
        for key, value_list in lexicon_dict.items():
            patterns[key] = re.compile(self.token_pattern % '|'.join(value_list))

        return patterns

    def tag(self, text):
        """
        Tag input text with lexical entries
        :param text:
        :return:
        """
        if type(text) == str:
            pass
        elif type(text) == list:
            text = ' '.join(text)
        else:
            logging.debug("Unsupported input format.")

        tags = []
        for key, pattern in self.lexicon.items():

            matches = re.finditer(pattern, text)
            if matches:
                for m in matches:
                    span = copy.deepcopy(self.match_dict)
                    span["text"]  = m.group(0)
                    span["start"] = m.start(0)
                    span["end"]   = m.end(0)
                    span["value"] = key
                    span["label"] = self.name

                    tags.append(span)

                    logger.debug("Match: '{}' : '{}'".format(span.get('text'), span.get('value')))

        tags = consolidate_spans(tags)
        return tags


def create_argument_parser():
    parser = argparse.ArgumentParser(description='Regex Lexicon Tagger')
    parser.add_argument('-l', '--lexicon', type=str)
    parser.add_argument('-n', '--name',    type=str)
    parser.add_argument('-d', '--data',    type=str)
    return parser


if __name__ == "__main__":
    parser = create_argument_parser()
    args = parser.parse_args()

    reader = LexiconReaderCsv(delimiter="\t", token_separator='+', parts_separator='..')
    lexicon = reader.read(args.lexicon)

    tagger = RegexTagger(lexicon, args.name)

    with open(args.data) as fh:
        for row in fh:
            tags = tagger.tag(row)
            print(tags)
