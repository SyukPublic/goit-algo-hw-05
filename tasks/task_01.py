# -*- coding: utf-8 -*-

"""
HomeWork Task 1
"""

import timeit
from typing import Optional, Union
from pathlib import Path


def get_absolute_path(path: Union[Path, str], current_dir: Optional[Union[Path, str]] = None) -> Path:
    """Return the absolute path for the given path and the current directory

    :param path: specified path (str, Path, mandatory)
    :param current_dir: current directory (str, Path, optional)
    :return: absolute path (Path)
    """
    if not path:
        # The path can not be None or an empty string
        raise ValueError("The path can not be empty")

    if Path(path).is_absolute():
        # If the specified path is an absolute - return it
        return Path(path)

    if current_dir is not None and isinstance(current_dir, str):
        # If the current directory is not specified, use the current working directory
        current_dir = Path(current_dir)

    # Construct an absolute path and return
    return (current_dir if current_dir is not None else Path.cwd()) / path


def load_text_file_data(file_path: Path, encoding: str = "utf-8") -> str:
    """Return the content of the given text file

    :param file_path: specified text file path (Path, mandatory)
    :param encoding: encoding used to decode the file data (string, optional)
    :return: file content (string)
    """

    # Verify that the specified file exists
    if not file_path.exists():
        raise ValueError(f"The file \"{file_path}\" not found")

    # Verify that the specified path is the file
    if not file_path.is_file():
        raise ValueError(f"The specified path \"{file_path}\" is not a file")

    # Open the specified file as a text file
    try:
        with open(file_path, "tr", encoding=encoding) as fh:
            # Read the file data
            file_content = file_path.read_text(encoding=encoding)
            # Return the file data
            return file_content
    except UnicodeDecodeError:
        # The file data is corrupted
        # Raise exception to the upper level
        raise ValueError(f"The file \"{file_path}\" data is corrupted")
    except Exception as e:
        # An unexpected error occurred
        # Raise exception to the upper level
        raise Exception("An unexpected error occurred: {error}.".format(error=repr(e)))


def print_tests_result(datasets: list[tuple[str, str, str]], times: dict[str, dict[str, float]]) -> None:
    """Print results table

    :param datasets: Datasets for result (List of tuple, mandatory)
    :param times: Results dictionary (Dictionary, optional)
    """

    data_max_len = max([len(n) for n, *_ in datasets])
    algo_max_len = max([len(n) for n in times.keys()])
    print("|", " | ".join([f"{'Algorithm':<{algo_max_len}}"] + [f"{n:<{data_max_len}}" for n, *_ in datasets]), "|")
    print("|", " | ".join(["-" * algo_max_len] + ["-" * data_max_len for _ in datasets]), "|")
    for func, times in times.items():
        print(
            "|",
            " | ".join(
                [f"{func:<{algo_max_len}}"] + [f"{times.get(n, 0):<{data_max_len}.08f}" for n, *_ in datasets]
            ),
            "|"
        )


def kmp_search(text: str, search_pattern: str, find_all: bool = True) -> list[int]:
    """Implementation of the Knuth-Morris-Pratt algorithm

    :param text: The text in which the search is performed (String, mandatory)
    :param search_pattern: The pattern string that needs to be found (String, mandatory)
    :param find_all: Find all occurrences of the pattern in the text; otherwise, only the first one (Boolean, optional)
    :return: Indexes of all positions where the string occurs in the text (List of integer)
    """

    def compute_lps(pattern: str) -> list[int]:
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

    text_length, search_pattern_length = len(text), len(search_pattern)
    if search_pattern_length == 0:
        return []

    lps = compute_lps(search_pattern)
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


def boyer_moore_search(text: str, search_pattern: str, find_all: bool = True) -> list[int]:
    """Implementation of the Boyer-Moore algorithm

    :param text: The text in which the search is performed (String, mandatory)
    :param search_pattern: The pattern string that needs to be found (String, mandatory)
    :param find_all: Find all occurrences of the pattern in the text; otherwise, only the first one (Boolean, optional)
    :return: Indexes of all positions where the string occurs in the text (List of integer)
    """

    def build_bad_match_table(pattern: str) -> dict[str, int]:
        table = {}
        for k in range(len(pattern) - 1):
            table[pattern[k]] = len(pattern) - 1 - k
        return table

    def compute_gst(pattern: str) -> list[int]:
        table = [0] * len(pattern)
        l = 0
        for k in range(1, len(pattern)):
            while l > 0 and pattern[l] != pattern[k]:
                l = table[l - 1]
            if pattern[l] == pattern[k]:
                l += 1
            table[k] = l
        return table

    text_length, search_pattern_length = len(text), len(search_pattern)
    if search_pattern_length == 0:
        return []

    bad_match_table = build_bad_match_table(search_pattern)
    gst = compute_gst(search_pattern)
    matches = []
    i = search_pattern_length - 1
    while i < text_length:
        j = search_pattern_length - 1
        while j >= 0 and text[i] == search_pattern[j]:
            i -= 1
            j -= 1
        if j == -1:
            matches.append(i + 1)
            i += search_pattern_length - gst[0] + 1
            if not find_all:
                break
        else:
            i += max(bad_match_table.get(text[i], search_pattern_length), search_pattern_length - j)
    return matches


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


def search_algorithms_compare() -> None:
    try:
        article_1: str = load_text_file_data(get_absolute_path(Path(__file__).parent / "./__data__/стаття 1.txt"))
        article_2: str = load_text_file_data(get_absolute_path(Path(__file__).parent / "./__data__/стаття 2.txt"))

        algorithms: tuple = (
            ("Knuth-Morris-Pratt algorithm (all occurrences)", kmp_search, True),
            ("Knuth-Morris-Pratt algorithm (first occurrence only)", kmp_search, False),
            ("Boyer-Moore algorithm (all occurrences)", boyer_moore_search, True),
            ("Boyer-Moore algorithm (first occurrence only)", boyer_moore_search, False),
            ("Rabin-Karp algorithm (all occurrences)", rabin_karp_search, True),
            ("Rabin-Karp algorithm (first occurrence only)", rabin_karp_search, False),
        )

        datasets: list[tuple[str, str, str]] = [
            (
                f"Article 1: The string that exists in the file",
                article_1,
                ", що не потрібно розуміти, як влаштовані алгоритми",
            ),
            (
                f"Article 1: The string that not exists in the file",
                article_1,
                ", що ен потрібно розуміти, кя влаштовані алгоритми",
            ),
            (
                f"Article 2: The string that exists in the file",
                article_2,
                "кожен елемент має вказівник на наступний елемент",
            ),
            (
                f"Article 2: The string that not exists in the file",
                article_2,
                "кожен лементе має вказівник на ступнийна елемент",
            ),
        ]

        search_times: dict[str, dict[str, float]] = {}
        for algorith_name, sort_func, find_all in algorithms:
            times: dict[str, float] = {}
            for name, text, search_pattern in datasets:
                times[name] = timeit.timeit(lambda: sort_func(text, search_pattern, find_all=find_all), number=10)
            search_times[algorith_name] = times

        print_tests_result(datasets, search_times)

    except Exception as e:
        print(e)
