import pytest

from tordle import check, session, word_list


def test_one_guess_correct():
  words = word_list.WordList(["ABCDE"])
  sess = session.Session(target="ABCDE", total_guesses=1, words=words)
  assert sess.status == session.SessionStatus.ACTIVE
  hints = sess.guess("ABCDE")
  assert hints == [check.HintCategory.HIT] * 5
  assert sess.status == session.SessionStatus.VICTORY
  assert sess.guess_history == ["ABCDE"]


def test_one_guess_all_wrong():
  words = word_list.WordList(["ABCDE", "GHIJK"])
  sess = session.Session(target="ABCDE", total_guesses=1, words=words)
  assert sess.status == session.SessionStatus.ACTIVE
  hints = sess.guess("GHIJK")
  assert hints == [check.HintCategory.MISS] * 5
  assert sess.status == session.SessionStatus.DEFEAT
  assert sess.guess_history == ["GHIJK"]


def test_three_guesses():
  words = word_list.WordList(["ABC", "AAA", "BBB", "CCC", "DDD"])
  sess = session.Session(target="ABC", total_guesses=3, words=words)
  assert sess.status == session.SessionStatus.ACTIVE
  assert sess.remaining_guesses == 3

  hints = sess.guess("AAA")
  assert hints == [
      check.HintCategory.HIT, check.HintCategory.MISS, check.HintCategory.MISS
  ]
  assert sess.status == session.SessionStatus.ACTIVE
  assert sess.remaining_guesses == 2
  assert sess.guess_history == ["AAA"]

  hints = sess.guess("BBB")
  assert hints == [
      check.HintCategory.MISS, check.HintCategory.HIT, check.HintCategory.MISS
  ]
  assert sess.status == session.SessionStatus.ACTIVE
  assert sess.remaining_guesses == 1
  assert sess.guess_history == ["AAA", "BBB"]

  hints = sess.guess("CCC")
  assert hints == [
      check.HintCategory.MISS, check.HintCategory.MISS, check.HintCategory.HIT
  ]
  assert sess.status == session.SessionStatus.DEFEAT
  assert sess.remaining_guesses == 0
  assert sess.guess_history == ["AAA", "BBB", "CCC"]

  # An extra guess is an error.
  with pytest.raises(ValueError):
    sess.guess("DDD")
  assert sess.status == session.SessionStatus.DEFEAT
  assert sess.remaining_guesses == 0
  assert sess.guess_history == ["AAA", "BBB", "CCC"]
