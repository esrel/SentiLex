from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from sentilex.scorers import Scorer
from sentilex.taggers.strtype_tagger import StringTypeTagger
from sentilex.utils import get_class_from_path
from sentilex.utils import add_logging_arguments, configure_colored_logging

import json

import logging
import argparse

logger = logging.getLogger(__name__)


class ShifterScorer(Scorer):
    """
    Sentiment scorer based on lexicons of valence shifters, intensifiers, and polarity words
    """
    name = 'shifter_scorer'
    languages = ['en', 'it']
    requires = ['lemmas']
    provides = ['sentiment']

    defaults = {
        'token_separator': ' ',
        'parts_separator': '..',
        'delimiter': "\t"
    }

    taggers = []

    def __init__(self, config_file=None):
        """
        Initialize scorer
        :param config_file:
        """
        self.taggers.append(StringTypeTagger())
        self.load_from_config(config_file)

    def load_from_config(self, config_file=None):
        """
        Parse config json and initialize system
        :param config_file:
        :return:
        """
        conf = json.load(open(config_file))
        language = conf.get('language')
        # initialize lexicon taggers
        if language not in self.languages:
            logger.debug('Language {} is not supporter'.format(language))
        else:
            for name, setting in conf.get('lexicons').items():
                # initialize lexicon reader & read lexicon
                lexicon_file = 'lexicons/' + language + '/' + setting.get('filename')
                reader_class = get_class_from_path(conf.get('reader'))
                reader = reader_class(
                    delimiter=setting.get('delimiter', self.defaults.get('delimiter')),
                    token_separator=setting.get('token_separator', self.defaults.get('token_separator')),
                    parts_separator=setting.get('parts_separator', self.defaults.get('parts_separator'))
                )
                lexicon = reader.read(lexicon_file)

                # initialize tagger
                tagger_class = get_class_from_path(conf.get('tagger'))
                tagger = tagger_class(lexicon, name)

                self.taggers.append(tagger)

            # initialize preprocessor
            preprocessor_class = get_class_from_path(conf.get('preprocessor'))
            self.preprocessor = preprocessor_class(language)

    def score(self, text):
        """
        Score text after tagging
        :param text:
        :return:
        """
        logger.debug("Raw Text: {}".format(text))
        # get lemmas
        text = self.preprocessor.process(text)
        logger.debug("Lemmas: {}".format(text))

        # tag lemmas
        tags = []
        for tagger in self.taggers:
            new_tags = tagger.tag(text)
            tags += new_tags
            logger.debug('Tagged by {}: {}'.format(tagger.name, new_tags))

        score = self.score_tags(tags)
        logger.debug('Sentiment Score: {}'.format(score))

        return score

    def score_tags(self, tags):
        """
        Score tags extracted from text
        :param tags:
        :return:
        """
        scores = []
        shifter = 1
        intensifier = 1

        for t in tags:
            label = t.get('label')
            value = t.get('value')

            if label == 'punct':
                shifter = 1
                intensifier = 1
            elif label == 'shifter':
                shifter = value
            elif label == 'intensifier':
                intensifier = value
            elif label == 'polarity':
                scores.append(shifter * intensifier * value)

        return sum(scores)


def create_argument_parser():
    parser = argparse.ArgumentParser(description='Valence Shifter Sentiment Analysis')
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
            print(score)
