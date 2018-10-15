from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from collections import Counter

import random


def consolidate_spans(tags):
    """
    Resolve any overlapping tags
    :param tags:
    :return:
    """
    # check for overlaps
    # 1. generate spans as lists
    # 2. collect character indices that appear more that once
    # 3. collect tags that overlap
    tags = sorted(tags, key=lambda k: k['start'])
    spans = [list(range(t.get('start'), t.get('end'))) for t in tags]
    overlaps = [k for k, v in dict(Counter([index for span in spans for index in span])).items() if v > 1]

    if overlaps:
        overlap_groups = []
        for char_index in overlaps:
            # group overlapping spans/entities by overlapping chars
            group = [i for i, s in enumerate(spans) if char_index in s]
            overlap_groups.append(group)

        # Flatten overlapping entity lists & create a new entity list
        bad_spans = list(set([i for group in overlap_groups for i in group]))
        good_tags = [e for i, e in enumerate(tags) if i not in bad_spans]

        # make disjoint groups
        overlap_groups = make_disjoint_sets(overlap_groups)
        for indices in overlap_groups:
            # containment consolidation:
            # 1. detect spans contained within other spans & remove them --> greedy
            containment_consolidation(indices, spans)
            # overlap consolidation
            # 2. select the longest of overlapping spans
            overlap_consolidation(indices, spans)

        # append selected entities from each overlap group to the new entity list
        for group in overlap_groups:
            for index in group:
                good_tags.append(tags[index])
        tags = good_tags
    return tags


def overlap_consolidation(indices, spans):
    """
    Choose the longest of overlapping spans
    :param indices:
    :param spans:
    :return:
    """
    for i in indices:
        for j in indices:
            if i != j:
                if len(spans[i]) > len(spans[j]):
                    indices.remove(j)
                elif len(spans[i]) < len(spans[j]):
                    indices.remove(i)
                else:
                    indices.remove(random.choice([i, j]))


def containment_consolidation(indices, spans):
    """
    Detect spans contained within other spans & remove them
    :param indices:
    :param spans
    :return:
    """
    for i in indices:
        for j in indices:
            if i != j:
                if set(spans[j]).issubset(set(spans[i])):
                    indices.remove(j)


def make_disjoint_sets(lists):
    """
    Take list of lists and create disjoint lists by merging the input lists
    :param lists:
    :return:
    """
    sets = [set(l) for l in lists]
    merged = True

    while merged:
        merged = False
        result = []
        while sets:
            common, rest = sets[0], sets[1:]
            sets = []
            for x in rest:
                if x.isdisjoint(common):
                    sets.append(x)
                else:
                    merged = True
                    common |= x
            result.append(common)
        sets = result
    return [list(s) for s in sets]


