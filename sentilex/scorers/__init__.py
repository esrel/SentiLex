class Scorer(object):
    """
    Scorer Class template
    """
    name = None
    language = []
    requires = []
    provides = []
    defaults = {}

    def score(self, text):
        raise NotImplementedError("scorer needs score method.")

    @staticmethod
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
