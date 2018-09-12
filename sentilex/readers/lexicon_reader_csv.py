from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from builtins import str
from typing import Text, List, Dict, Any

import logging

import re
import csv
import os

from sentilex.readers import Reader
from sentilex.lexicons import Lexeme
from sentilex import utils

import argparse

logger = logging.getLogger(__name__)


class LexiconReaderCsv(Reader):
    """
    Class to read lexicon from CSV/TSV
    """

    def __init__(self, delimiter="\t", token_separator=' ', parts_separator='..'):
        """
        :param delimiter:
        :param token_separator:
        :param parts_separator:
        """
        self.delimiter = delimiter
        self.token_separator = token_separator
        self.parts_separator = parts_separator

    def read(self, lexicon_file):
        """
        Read lexicon tsv/csv -- 2 column file as entry & value to tag entry with
        :param lexicon_file:
        :return:
        """
        if not os.path.isfile(lexicon_file):
            logger.debug("Unknown lexicon format. Supported formats are TSV/CSV.")

        lexicon = []
        with open(lexicon_file) as lex_file:
            lex_csv = csv.reader(lex_file, delimiter=self.delimiter)
            for row in lex_csv:
                if len(row) > 1:
                    item, value = [x.strip() for x in row]
                    lexeme = Lexeme(item)
                    lexeme.set('value', float(value))
                    lexeme.set('token_separator', self.token_separator)
                    lexeme.set('parts_separator', self.parts_separator)
                    lexicon.append(lexeme)
                    logger.debug('Adding {} : {}'.format(item, float(value)))
        return lexicon


def create_argument_parser():
    parser = argparse.ArgumentParser(description='CSV/TSV Lexicon Reader')
    parser.add_argument('-l', '--lexicon',   type=str)
    parser.add_argument('-d', '--delimiter', type=str, default="\t")
    # Optional
    parser.add_argument('-t', '--token_separator',  type=str, default=' ')
    parser.add_argument('-p', '--parts_separator',  type=str, default='..')
    utils.add_logging_arguments(parser, default=logging.INFO)
    return parser


if __name__ == "__main__":
    parser = create_argument_parser()
    args = parser.parse_args()
    utils.configure_colored_logging(args.loglevel)

    reader = LexiconReaderCsv(args.delimiter, args.token_separator, args.parts_separator)
    lexicon = reader.read(args.lexicon)
    for lexeme in lexicon:
        print(lexeme.text, lexeme.tolist())
