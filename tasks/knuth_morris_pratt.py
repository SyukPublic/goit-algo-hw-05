# -*- coding: utf-8 -*-

"""
Knuth-Morris-Pratt algorithm implementation
"""


def _compute_lps(pattern: str) -> list[int]:
    m = len(pattern)
    table = [0] * m
    length = 0
    k = 1

    while k < m:
        if pattern[k] == pattern[length]:
            length += 1
            table[k] = length
            k += 1
        else:
            if length != 0:
                length = table[length - 1]
            else:
                table[k] = 0
                k += 1

    return table


def kmp_search(text: str, search_pattern: str, find_all: bool = True) -> list[int]:
    """Implementation of the Knuth-Morris-Pratt algorithm

    :param text: The text in which the search is performed (String, mandatory)
    :param search_pattern: The pattern string that needs to be found (String, mandatory)
    :param find_all: Find all occurrences of the pattern in the text; otherwise, only the first one (Boolean, optional)
    :return: Indexes of all positions where the string occurs in the text (List of integer)
    """

    text_length, search_pattern_length = len(text), len(search_pattern)
    if search_pattern_length == 0:
        # Empty pattern = nothing to do
        return []

    lps = _compute_lps(search_pattern)
    matches = []
    i, j = 0, 0
    while i < text_length:
        if search_pattern[j] == text[i]:
            i += 1
            j += 1
            if j == search_pattern_length:
                matches.append(i - j)
                j = lps[j - 1]
                if not find_all:
                    break
        else:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return matches
