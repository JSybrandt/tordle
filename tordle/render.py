import rich
from rich import layout, live, prompt, table

from . import check, session, util


class SessionRenderer():

  def __init__(self, sess: session.Session):
    self._session = sess
    self._live = None

  def _generate_guess_table(self):
    guess_table = table.Table()
    target_length = len(self._session.target)
    for _ in range(target_length):
      guess_table.add_column(justify="center", width=1)
    total_guesses = self._session.total_guesses
    for idx in range(total_guesses):
      if idx < len(self._session.guess_history):
        guess_table.add_row(*list(self._session.guess_history[idx]))
      else:
        empty_guess = [" "] * target_length
        guess_table.add_row(*empty_guess)
    return guess_table

  def __enter__(self):
    self._live = live.Live(
        self._generate_guess_table(), transient=True, screen=True)
    self._live.__enter__()
    return self

  def __exit__(self, *args, **kwargs):
    self._live.__exit__(*args, **kwargs)
    self._live = None

  def _validate_context(self):
    if self._live is None:
      raise ValueError("SessionRenderer should be invoked with 'with'")

  @property
  def console(self):
    self._validate_context()
    return self._live.console

  def print(self, msg: str):
    self.console.print(msg)

  def prompt_guess(self) -> str:
    self._validate_context()
    while True:
      try:
        guess = prompt.Prompt.ask(">", console=self.console)
        check.validate_guess(guess, len(self._session.target))
        return guess
      except ValueError as e:
        self.print(e)

  def update(self):
    self._live.update(self._generate_guess_table())
    # if self._session.status == session.SessionStatus.ACTIVE:
    # rich.print(self._generate_guess_table())
    # elif self._session.status == session.SessionStatus.DEFEAT:
    # print("DEFEAT")
    # elif self._session.status == session.SessionStatus.VICTORY:
    # print("VICTORY")
    # elif self._session.status == session.SessionStatus.ERROR:
    # print("ERROR")
    # else:
    # raise ValueError("Session is in unsupported state: "
    # f"{self._session.status}")


def _hint_to_char(hint: check.HintCategory):
  if hint == check.HintCategory.MISS:
    return "X"
  if hint == check.HintCategory.CLOSE:
    return "!"
  if hint == check.HintCategory.HIT:
    return "$"
  raise ValueError(f"Unsupported hint: {hint}")
