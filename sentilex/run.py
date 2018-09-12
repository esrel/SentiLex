from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from builtins import str
from typing import Text, List, Dict, Any

from sentilex.utils import add_logging_arguments, configure_colored_logging
from sentilex.scorers.shifter_scorer import ShifterScorer
from sentilex.scorers import nominalize

import string
import copy
import re

import logging
import argparse

logger = logging.getLogger(__name__)


def create_argument_parser():
    parser = argparse.ArgumentParser(description='Lexicon-based Sentiment Analysis')
    parser.add_argument('-d', '--data',     type=str)
    parser.add_argument('-c', '--config',   type=str)
    parser.add_argument('-l', '--language', type=str)
    add_logging_arguments(parser)
    return parser


if __name__ == "__main__":
    parser = create_argument_parser()
    args = parser.parse_args()
    configure_colored_logging(args.loglevel)

    scorer = ShifterScorer(args.config)

    with open(args.data) as fh:
        for row in fh:
            score = scorer.score(row)
            print('Text "{}" is "{}" with score = {}'.format(row.strip(), nominalize(score), score))





