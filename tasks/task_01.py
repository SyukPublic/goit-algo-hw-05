# -*- coding: utf-8 -*-

"""
HomeWork Task 1
"""

import timeit
from typing import Optional, Union
from pathlib import Path

from .knuth_morris_pratt import kmp_search
from .boyer_moore import boyer_moore_search
from .rabin_karp import rabin_karp_search


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


def print_tests_result(title: str, datasets: list[tuple[str, str, str]], times: dict[str, dict[str, float]]) -> None:
    """Print results table

    :param title: Title of the result (String, mandatory)
    :param datasets: Datasets for result (List of tuple, mandatory)
    :param times: Results dictionary (Dictionary, optional)
    """

    print(f"\n{title}\n")

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

        datasets_short: list[tuple[str, str, str]] = [
            (
                f"Article 1: Exists in the file",
                article_1,
                ", що не потрібно розуміти",
            ),
            (
                f"Article 1: Not exists in the file",
                article_1,
                ", що ен потрібно розуміти",
            ),
            (
                f"Article 2: Exists in the file",
                article_2,
                "кожен елемент має вказівник",
            ),
            (
                f"Article 2: Not exists in the file",
                article_2,
                "кожен лементе має вказівник",
            ),
        ]

        datasets_long: list[tuple[str, str, str]] = [
            (
                f"Article 1: Exists in the file",
                article_1,
                ", що не потрібно розуміти, як влаштовані алгоритми. Фундаментальні знання допомагають дізнатися, що всередині, як воно працює і чому одне рішення краще",
            ),
            (
                f"Article 1: Not exists in the file",
                article_1,
                ", що ен потрібно розуміти, кя влаштовані алгоритми. Фундаментальні знання допомагають знатисяді, що всередині, як воно і чому одне рішення краще",
            ),
            (
                f"Article 2: Exists in the file",
                article_2,
                "кожен елемент має вказівник на наступний елемент. Основна перевага цієї структури полягає у сталому часі додавання нового елементу.",
            ),
            (
                f"Article 2: Not exists in the file",
                article_2,
                "кожен лементе має вказівник на ступнийна елемент. Основна перевага єїці структури полягає у часі додавання нового елементу.",
            ),
        ]

        search_times: dict[str, dict[str, float]] = {}
        for algorith_name, sort_func, find_all in algorithms:
            times: dict[str, float] = {}
            for name, text, search_pattern in datasets_short:
                times[name] = timeit.timeit(lambda: sort_func(text, search_pattern, find_all=find_all), number=10)
            search_times[algorith_name] = times

        print_tests_result("Short pattern search", datasets_short, search_times)

        search_times = {}
        for algorith_name, sort_func, find_all in algorithms:
            times: dict[str, float] = {}
            for name, text, search_pattern in datasets_long:
                times[name] = timeit.timeit(lambda: sort_func(text, search_pattern, find_all=find_all), number=10)
            search_times[algorith_name] = times

        print_tests_result("Long pattern search", datasets_long, search_times)

    except Exception as e:
        print(e)
