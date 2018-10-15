from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from sentilex.utils import add_logging_arguments, configure_colored_logging
from sentilex.preprocessors import Preprocessor

import spacy

import logging
import argparse

logger = logging.getLogger(__name__)


class SpacyPreprocessor(Preprocessor):
    """
    Text pre-processing using spaCy
    """
    provides = ['lemma']
    languages = ['en', 'it']

    def __init__(self, language='en'):
        self.nlp = spacy.load(language)

    def process(self, text):
        doc = self.nlp(text.strip())
        return ' '.join([w.lemma_ for w in doc])


def create_argument_parser():
    parser = argparse.ArgumentParser(description='Text Lemmatizer')
    parser.add_argument('-d', '--data',     type=str)
    parser.add_argument('-l', '--language', type=str, default='en')
    add_logging_arguments(parser)
    return parser


if __name__ == "__main__":
    parser = create_argument_parser()
    args = parser.parse_args()
    configure_colored_logging(args.loglevel)

    pp = SpacyPreprocessor(language=args.language)

    with open(args.data) as fh:
        for row in fh:
            out = pp.process(row)
            print(out)