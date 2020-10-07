from sentilex.utils import add_logging_arguments, configure_colored_logging
from sentilex.scorers.shifter_scorer import ShifterScorer

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
            print('Text "{}" is "{}" with score = {}'.format(row.strip(), scorer.nominalize(score), score))
