# -*- coding: utf-8 -*-

"""
Boyer-Moore algorithm implementation
"""


def _build_bad_character_table(pattern: str) -> dict[str, int]:
    """ Creates the "bad character" table for the Boyer-Moore algorithm.
    It describes how many characters can be skipped if a character does not match.

    :param pattern: The pattern string that needs to be found (String, mandatory)
    :return: Dictionary with shift values for all characters in pattern (Dictionary)
    """

    table = {}
    for k in range(len(pattern) - 1):
        table[pattern[k]] = len(pattern) - 1 - k
    return table


def _is_prefix_of_pattern(pattern: str, position: int) -> bool:
    """ Checks whether a part of the pattern is a prefix of the pattern starting at a certain position.
    Used in the "good suffix" to optimize jumps.

    :param pattern: The pattern string that needs to be found (String, mandatory)
    :param position: The index of a specific position (Integer, mandatory)
    :return: Indicator of whether it is a prefix or not (Boolean)
    """

    for i in range(position, len(pattern)):
        # Comparison with the prefix
        j = i - position
        # If it doesn't fit -> no prefix
        if pattern[i] != pattern[j]:
            return False
    return True


def _suffix_length_matching_prefix(pattern: str, position: int) -> int:
    """ Calculates the length of the suffix of a pattern that matches a prefix.
    This function is part of the "good suffix" to optimize jumps.

    :param pattern: The pattern string that needs to be found (String, mandatory)
    :param position: The index of a specific position (Integer, mandatory)
    :return: The length of the suffix of a pattern (Integer)
    """

    # How many characters fit together from the back?
    size = 0
    # Start at the back of the pattern
    i, j = position, len(pattern) - 1
    while i >= 0 and pattern[i] == pattern[j]:
        # Walk backwards
        i -= 1
        j -= 1
        size += 1
    return size


def _build_good_suffix_table(pattern: str) -> list[int]:
    """ Creates the "good suffix" table for the Boyer-Moore algorithm.
    It helps determine how much further the pattern can be shifted if part of the pattern matches.

    :param pattern: The pattern string that needs to be found (String, mandatory)
    :return: List of shift values
    """
    table = [0] * len(pattern)
    last_prefix_position = len(pattern)

    # Backwards through the pattern
    for i in range(len(pattern), 0, -1):
        # Checks if a prefix was found
        if _is_prefix_of_pattern(pattern, i):
            last_prefix_position = i
        table[len(pattern) - i] = last_prefix_position - i + len(pattern)

    # Search for matching suffixes
    for i in range(len(pattern) - 1):
        size = _suffix_length_matching_prefix(pattern, i)
        # Consider suffix matching parts
        table[size] = len(pattern) - 1 - i + size

    return table


def boyer_moore_search(text: str, search_pattern: str, find_all: bool = True) -> list[int]:
    """Implementation of the Boyer-Moore algorithm

    :param text: The text in which the search is performed (String, mandatory)
    :param search_pattern: The pattern string that needs to be found (String, mandatory)
    :param find_all: Find all occurrences of the pattern in the text; otherwise, only the first one (Boolean, optional)
    :return: Indexes of all positions where the string occurs in the text (List of integer)
    """

    text_length, search_pattern_length = len(text), len(search_pattern)
    if search_pattern_length == 0:
        # Empty pattern = nothing to do
        return []

    bad_char_table = _build_bad_character_table(search_pattern)
    good_suffix_table = _build_good_suffix_table(search_pattern)
    matches = []
    i = search_pattern_length - 1
    while i < text_length:
        # Comparison from back to front
        j = search_pattern_length - 1
        # Check if pattern matches a substring
        while j >= 0 and i < text_length and text[i] == search_pattern[j]:
            # Complete pattern found
            if j == 0:
                matches.append(i)
                break
            i -= 1
            j -= 1

        if not find_all and matches:
            break

        if i < text_length:
            # Calculate how much we can shift if the pattern doesn't match
            i += max(
                good_suffix_table[search_pattern_length - 1 - j],
                bad_char_table.get(text[i], search_pattern_length),
            )

    return matches
