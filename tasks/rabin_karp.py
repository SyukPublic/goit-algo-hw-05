# -*- coding: utf-8 -*-

"""
Rabin-Karp algorithm implementation
"""


def rabin_karp_search(text: str, search_pattern: str, find_all: bool = True) -> list[int]:
    """Implementation of the Rabin-Karp algorithm

    :param text: The text in which the search is performed (String, mandatory)
    :param search_pattern: The pattern string that needs to be found (String, mandatory)
    :param find_all: Find all occurrences of the pattern in the text; otherwise, only the first one (Boolean, optional)
    :return: Indexes of all positions where the string occurs in the text (List of integer)
    """

    def calculate_hash(string: str) -> int:
        hash_value = 0
        for char in string:
            hash_value = (hash_value * prime + ord(char)) % modulus
        return hash_value

    def rehash(old_hash: int, old_char: str, new_char: str) -> int:
        new_hash = ((old_hash - ord(old_char) * high_power) * prime + ord(new_char)) % modulus
        if new_hash < 0:
            new_hash += modulus
        return new_hash

    text_length, search_pattern_length = len(text), len(search_pattern)
    if search_pattern_length == 0:
        # Empty pattern = nothing to do
        return []

    prime = 101
    modulus = 10 ** 9 + 7
    high_power = pow(prime, search_pattern_length - 1, modulus)

    pattern_hash = calculate_hash(search_pattern)
    text_hash = calculate_hash(text[:search_pattern_length])

    matches = []
    for i in range(text_length - search_pattern_length + 1):
        if pattern_hash == text_hash:
            if text[i:i + search_pattern_length] == search_pattern:
                matches.append(i)
                if not find_all:
                    break

        if i < text_length - search_pattern_length:
            text_hash = rehash(text_hash, text[i], text[i + search_pattern_length])

    return matches
