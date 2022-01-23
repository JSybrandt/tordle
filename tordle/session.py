import enum
from typing import List

from . import check, util, word_list


class SessionStatus(enum.Enum):
  ACTIVE = 1
  VICTORY = 2
  DEFEAT = 3
  ERROR = 4


class Session():

  def __init__(self, target: str, total_guesses: int,
               words: word_list.WordList):
    try:
      check.validate_word(target, words)
      if total_guesses <= 0:
        raise ValueError("Expected total_guesses to be positive. "
                         f"Got: {total_guesses}")
      self._target = util.clean_text(target)
      self._total_guesses = total_guesses
      self._status = SessionStatus.ACTIVE
      self._guess_history = []
      self._hint_history = []
      self._words = words
    except ValueError as e:
      self._status = SessionStatus.ERROR
      raise e

  @property
  def status(self):
    return self._status

  @property
  def words(self):
    return self._words

  @property
  def target(self):
    return self._target

  @property
  def total_guesses(self):
    return self._total_guesses

  @property
  def guess_count(self):
    return len(self._guess_history)

  @property
  def remaining_guesses(self):
    return self.total_guesses - self.guess_count

  @property
  def guess_history(self):
    return self._guess_history

  @property
  def hint_history(self):
    return self._hint_history

  def guess(self, guess: str) -> List[check.HintCategory]:
    if self.status != SessionStatus.ACTIVE:
      raise ValueError("Cannot make guesses in an inactive session. "
                       f"State: {self.status}")
    if self.remaining_guesses <= 0:
      raise ValueError("No guesses remaining.")
    guess = util.clean_text(guess)
    hint = check.get_hints(guess, self.target, self.words)
    self._guess_history.append(guess)
    self._hint_history.append(hint)
    if check.is_correct(guess, self.target):
      self._status = SessionStatus.VICTORY
    elif self.remaining_guesses == 0:
      self._status = SessionStatus.DEFEAT
    return hint
