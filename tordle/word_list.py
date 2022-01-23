import bisect
import pathlib
import random
from collections import defaultdict
from typing import Iterable, Optional

from . import util

_DEFAULT_WORD_LIST = pathlib.Path(__file__).parent.joinpath("usa_english.txt")


class WordList:

  def __init__(self, words: Optional[Iterable[str]] = None):
    if words is None:
      words = _load_default_word_list()
    self._count = 0
    self._words_by_size = defaultdict(list)
    for word in words:
      self._words_by_size[len(word)].append(util.clean_text(word))
      self._count += 1
    # Sort each list so we can binary search for words later.
    for size in self._words_by_size:
      self._words_by_size[size].sort()

  def __len__(self):
    return self._count

  def get_random_word(self, desired_length: int) -> Optional[str]:
    """Returns a word from the input list of the desired length.

        Returns none if no words of the desired length are available."""
    if desired_length not in self._words_by_size:
      return None
    return random.choice(self._words_by_size[desired_length])

  def __contains__(self, query: str) -> bool:
    query = util.clean_text(query)
    words = self._words_by_size[len(query)]
    if not words:
      return False
    idx = bisect.bisect_left(words, query)
    if idx < 0 or idx >= len(words):
      return False
    return words[idx] == query


def _load_default_word_list():
  assert _DEFAULT_WORD_LIST.is_file()
  with open(_DEFAULT_WORD_LIST) as word_file:
    return [util.clean_text(l) for l in word_file]
