import enum
import string
from typing import List

from . import util, word_list


class HintCategory(enum.Enum):
  MISS = 1
  CLOSE = 2
  HIT = 3


def get_hints(guess: str, target: str,
              words: word_list.WordList) -> List[HintCategory]:
  """Returns hint results for a guess."""
  guess = util.clean_text(guess)
  target = util.clean_text(target)
  validate_guess(guess, len(target), words)
  hints = [None for _ in guess]
  # Do hits first.
  for i, (guess_c, target_c) in enumerate(zip(guess, target)):
    if guess_c == target_c:
      hints[i] = HintCategory.HIT
  # This should be a list because we may have duplicates.
  remaining_target_chars = [target[i] for i, h in enumerate(hints) if h is None]
  for i, guess_c in enumerate(guess):
    if hints[i] is not None:
      continue
    if guess_c in remaining_target_chars:
      hints[i] = HintCategory.CLOSE
      remaining_target_chars.remove(guess_c)
  # Now, nones are misses.
  for i, h in enumerate(hints):
    if h is None:
      hints[i] = HintCategory.MISS
  return hints


def is_correct(guess: str, target: str) -> bool:
  return util.clean_text(guess) == util.clean_text(target)


_VALID_CHARS = {c for c in string.ascii_uppercase}


def validate_guess(guess: str, target_len: int, words: word_list.WordList):
  """Returns true if the guess is only `target_len` alpha chars."""
  guess = util.clean_text(guess)
  if len(guess) != target_len:
    raise ValueError(f"The guess '{guess}' should be {target_len} "
                     "characters long.")
  validate_word(guess, words)


def validate_word(word: str, words: word_list.WordList):
  assert word is not None
  word = util.clean_text(word)
  if not word:
    raise ValueError("The empty string is not a valid word.")
  if word not in words:
    raise ValueError(f"'{word}' does not appear in the dictionary.")
  if any(c not in _VALID_CHARS for c in word):
    raise ValueError(f"The word'{word}' should only contain letters.")


def validate_char(char: str):
  char = util.clean_text(char)
  if len(char) != 1:
    raise ValueError(f"'{char}' is not a single char.")
  if char not in _VALID_CHARS:
    raise ValueError(f"'{char}' is not a valid letter.")
