import string

from tordle import word_list


def test_sample_word_length():
  words = word_list.WordList(["A", "AB", "ABC"])
  assert words.get_random_word(desired_length=1) == "A"
  assert words.get_random_word(desired_length=2) == "AB"
  assert words.get_random_word(desired_length=3) == "ABC"
  assert words.get_random_word(desired_length=4) is None


def test_sample_is_random():
  expected = {"A", "B", "C", "D"}
  words = word_list.WordList(expected)
  actual = {words.get_random_word(1) for _ in range(100)}
  assert actual == expected


def test_default_word_list():
  words = word_list.WordList()
  actual = {words.get_random_word(1) for _ in range(1000)}
  expected = {c for c in string.ascii_uppercase}
  assert actual == expected


def test_word_list_uppercase():
  words = word_list.WordList(["a"])
  assert words.get_random_word(1) == "A"


def test_in():
  expected = {"A", "B", "CC", "DDD"}
  words = word_list.WordList(expected)
  for c in expected:
    assert c in words


def test_not_in():
  expected = {"A", "C", "D"}
  words = word_list.WordList(expected)
  assert "B" not in words
  assert "EE" not in words
