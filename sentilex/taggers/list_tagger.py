from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from builtins import str
from typing import Text, List, Dict, Any

from sentilex.taggers import Tagger
from sentilex.readers.lexicon_reader_csv import LexiconReaderCsv
from sentilex.utils.span_utils import consolidate_spans

import numpy as np
import copy

import logging
import argparse


class ListTagger(Tagger):
    """
    Tag list of words with lexical entries
    """
    name = "ListTagger"
    defaults = {"token_separator": " ", "parts_separator": ".."}
    match_dict = {"text": "", "start": None, "end": None, "value": None, "label": None}

    def __init__(self, lexicon=None, name=None):
        """
        :param lexicon:
        """
        self.name = name if name else self.name
        self.lexicon = self.load(lexicon)

    def load(self, lexicon):
        """
        Load lexicon in usable format
        :param lexicon:
        :return:
        """
        return lexicon

    def tag(self, text):
        """
        Tag input list with lexical entries
        :param text:
        :return:
        """
        if type(text) == str:
            text = text.strip().split()
        elif type(text) == list:
            pass
        else:
            logging.debug("Unsupported input format.")

        tags = []
        for lexeme in self.lexicon:
            parts = lexeme.tolist()
            parts_tags = []
            for part in parts:
                part_tags = self.tag_list(part, text)
                if part_tags:
                    parts_tags.append(part_tags)

            # check if all parts are present & add to matches
            if len(parts_tags) == len(parts):
                tags += [t for p in parts_tags for t in p]

            tags = consolidate_spans(tags)
        return tags

    def tag_list(self, parts, whole):
        """
        Find if a list is a subset of another
        :param parts:
        :param whole:
        :return:
        """
        tags = []
        parts_len = len(parts)
        whole_len = len(whole)
        if parts_len == 0 or whole_len == 0:
            return tags
        elif parts_len > whole_len:
            return tags
        elif len(set(parts) & set(whole)) == 0:
            return tags
        else:
            for i in range(whole_len):
                if (i + parts_len) <= whole_len and whole[i:i + parts_len] == parts:
                    tag = copy.deepcopy(self.match_dict)
                    parts_txt = self.defaults.get('token_separator').join(parts)
                    whole_txt = self.defaults.get('token_separator').join(whole)
                    start = whole_txt.index(parts_txt, i)
                    tag['text'] = parts_txt
                    tag['start'] = start
                    tag['end'] = start + parts_len
                    tag['label'] = self.name
                    tags.append(tag)
        return tags


def create_argument_parser():
    parser = argparse.ArgumentParser(description='List Lexicon Tagger')
    parser.add_argument('-l', '--lexicon', type=str)
    parser.add_argument('-n', '--name',    type=str)
    parser.add_argument('-d', '--data',    type=str)
    return parser


if __name__ == "__main__":
    parser = create_argument_parser()
    args = parser.parse_args()

    reader = LexiconReaderCsv(delimiter="\t", token_separator='+', parts_separator='..')
    lexicon = reader.read(args.lexicon)

    tagger = ListTagger(lexicon, args.name)

    with open(args.data) as fh:
        for row in fh:
            tags = tagger.tag(row)
            print(tags)
