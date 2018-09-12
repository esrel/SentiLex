from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from builtins import str
from typing import Text, List, Dict, Any

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
