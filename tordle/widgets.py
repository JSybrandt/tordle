from typing import List, Optional

from rich import align, box, layout, panel, table, text
from textual import app, reactive, widget

from . import check, session, util, word_list


def _create_simple_box_table():
  return table.Table(
      show_header=False, show_footer=False, show_lines=True, box=box.SQUARE)


def get_guess_text(letter: str,
                   hint: Optional[check.HintCategory]) -> text.Text:
  guess_text = text.Text(letter)
  if hint is None:
    guess_text.stylize("bold")
  elif hint == check.HintCategory.HIT:
    guess_text.stylize("bold green")
  elif hint == check.HintCategory.MISS:
    guess_text.stylize("bright_black")
  elif hint == check.HintCategory.CLOSE:
    guess_text.stylize("bold yellow")
  else:
    raise NotImplementedError(f"Cannot stylize {hint}")
  return guess_text


class GuessTable(widget.Widget):

  def __init__(self, sess: session.Session):
    super().__init__()
    self._session = sess

  @property
  def total_guesses(self) -> int:
    return self._session.total_guesses

  @property
  def target_length(self) -> int:
    return len(self._session.target)

  @property
  def guess_history(self) -> List[str]:
    return self._session.guess_history

  @property
  def hint_history(self) -> List[check.HintCategory]:
    return self._session.hint_history

  def render(self):
    guess_table = _create_simple_box_table()
    for _ in range(self.target_length):
      guess_table.add_column(justify="center", width=1)
    for idx in range(self.total_guesses):
      if idx < len(self.guess_history):
        guess = self.guess_history[idx]
        hint = self.hint_history[idx]
        texts = [get_guess_text(g, h) for g, h in zip(guess, hint)]
        guess_table.add_row(*texts)
      else:
        empty_guess = [" "] * self.target_length
        guess_table.add_row(*empty_guess)
    return align.Align(guess_table, align="center")


class PendingGuessPanel(widget.Widget):
  pending_guess = reactive.Reactive("")

  def __init__(self, target_length: int):
    super().__init__()
    assert target_length > 0
    self._target_length = target_length

  def render(self):
    pending_table = _create_simple_box_table()
    for _ in range(self._target_length):
      pending_table.add_column()
    guess_w_padding = self.pending_guess + " " * (
        self._target_length - len(self.pending_guess))
    texts = [get_guess_text(g, None) for g in guess_w_padding]
    pending_table.add_row(*texts)
    grid = table.Table.grid()
    grid.add_row(text.Text("Guess:"))
    grid.add_row(pending_table)
    return align.Align(grid, align="center")

  def add_letter(self, letter: str):
    if len(self.pending_guess) < self._target_length:
      letter = util.clean_text(letter)
      check.validate_char(letter)
      self.pending_guess += letter

  def remove_letter(self):
    if len(self.pending_guess) > 0:
      self.pending_guess = self.pending_guess[:-1]

  def clear_guess(self):
    self.pending_guess = ""


class TitlePanel(widget.Widget):
  message = reactive.Reactive("Tordle!")
  style = "bold"

  def render(self):
    return text.Text(self.message, style=self.style)

  def set_victory(self):
    self.style = "green bold"
    self.message = "Victory!"

  def set_defeat(self, target: str):
    self.style = "red bold"
    self.message = f"It was '{target}'"


class ErrorPanel(widget.Widget):
  message = reactive.Reactive("")

  def render(self):
    return text.Text(self.message)


class HintAlphabet(widget.Widget):
  _GRID_WIDTH = 13

  def __init__(self, sess: session.Session):
    super().__init__()
    self._session = sess

  def render(self):
    hint_alphabet = sorted(list(self._session.get_hint_alphabet().items()))
    alphabet_table = _create_simple_box_table()
    for _ in range(self._GRID_WIDTH):
      alphabet_table.add_column()
    for start_idx in range(0, len(hint_alphabet), self._GRID_WIDTH):
      end_idx = start_idx + self._GRID_WIDTH
      batch = hint_alphabet[start_idx:end_idx]
      texts = [get_guess_text(g, h) for g, h in batch]
      alphabet_table.add_row(*texts)
    outer_grid = table.Table.grid()
    outer_grid.add_column()
    outer_grid.add_row(text.Text("Alphabet:"))
    outer_grid.add_row(alphabet_table)
    return align.Align(outer_grid, align="center")


class RootGrid(widget.Widget):

  def __init__(self, sess: session.Session, show_alphabet: bool):
    super().__init__()
    self._session = sess
    self.guess_table = GuessTable(sess)
    self.pending_guess = PendingGuessPanel(len(sess.target))
    self.error_panel = ErrorPanel()
    self.title_panel = TitlePanel()
    self.alphabet = HintAlphabet(sess)
    self._components = [
        self.title_panel,
        self.error_panel,
        self.guess_table,
        self.pending_guess,
    ]
    if show_alphabet:
      self._components.append(self.alphabet)

  def render(self):
    grid = table.Table.grid(expand=True)
    grid.add_column(justify="center")
    for c in self._components:
      grid.add_row(c)
    return grid
