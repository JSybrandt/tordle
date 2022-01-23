import pytest

from tordle import check, word_list


def test_is_correct():
  assert check.is_correct("good", "good")
  assert not check.is_correct("good", "fake")


def test_is_correct_ignores_case():
  assert check.is_correct("good", "GOOD")


def test_validate_guess_not_real_word():
  words = word_list.WordList(["garbage"])
  with pytest.raises(ValueError):
    check.validate_guess("guess", len("guess"), words)


def test_validate_guess_bad_len():
  words = word_list.WordList(["guess"])
  with pytest.raises(ValueError):
    check.validate_guess("guess", 3, words)


def test_validate_guess_no_num():
  words = word_list.WordList(["bad123"])
  with pytest.raises(ValueError):
    check.validate_guess("bad123", 6, words)


def test_validate_guess_no_symb():
  words = word_list.WordList(["!@#$%^"])
  with pytest.raises(ValueError):
    check.validate_guess("!@#$%^", 6, words)


def test_validate_word_empty():
  words = word_list.WordList([""])
  with pytest.raises(ValueError):
    check.validate_word("", words)


def test_get_hints_all_hit():
  words = word_list.WordList(["abc"])
  assert check.get_hints("abc", "abc", words) == [check.HintCategory.HIT] * 3


def test_get_hints_all_miss():
  words = word_list.WordList(["abc", "efg"])
  assert check.get_hints("abc", "efg", words) == [check.HintCategory.MISS] * 3


def test_get_hints_all_close():
  words = word_list.WordList(["abc", "bca"])
  assert check.get_hints("abc", "bca", words) == [check.HintCategory.CLOSE] * 3


def test_get_hints_duplicate_in_target():
  words = word_list.WordList(["AAAC", "BABA"])
  assert check.get_hints("AAAC", "BABA", words) == [
      check.HintCategory.CLOSE,  # A != B, but there's another A
      check.HintCategory.HIT,  # A == A, hit.
      check.HintCategory.MISS,  # A != B, and the other is "claimed."
      check.HintCategory.MISS,  # C != B, and there's no C.
  ]


def test_get_hints_ignore_case():
  words = word_list.WordList(["abc", "ABC"])
  assert check.get_hints("abc", "ABC", words) == [check.HintCategory.HIT] * 3
