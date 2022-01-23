import click
from rich import table
from textual import app

from . import render, session, util, widgets, word_list


class TordleApp(app.App):

  def __init__(self, *args, target_length: int, total_guesses: int, **kwargs):
    super().__init__(*args, **kwargs)
    assert target_length >= 0
    assert total_guesses >= 0
    self._total_guesses = total_guesses
    self._target_length = target_length
    self._words = word_list.WordList()
    self._session = session.Session(
        target=self._words.get_random_word(self._target_length),
        total_guesses=self._total_guesses,
        words=self._words)
    self._root_grid = widgets.RootGrid(self._session)

  async def on_mount(self):
    await self.view.dock(self._root_grid)

  def on_key(self, event):
    if self._session.status != session.SessionStatus.ACTIVE:
      return
    try:
      if event.key == "enter":
        self._session.guess(self._root_grid.pending_guess.pending_guess)
        self._root_grid.pending_guess.clear_guess()
      if event.key in {"ctrl+h", "delete"}:
        self._root_grid.pending_guess.remove_letter()
      elif len(event.key) == 1:
        self._root_grid.pending_guess.add_letter(event.key)
      if self._session.status == session.SessionStatus.VICTORY:
        self._root_grid.title_panel.set_victory()
      elif self._session.status == session.SessionStatus.DEFEAT:
        self._root_grid.title_panel.set_defeat(self._session.target)
      self._root_grid.error_panel.message = ""
    except ValueError as e:
      self._root_grid.error_panel.message = str(e)
    finally:
      self._root_grid.refresh()


@click.command()
@click.option(
    "-l",
    "--target-length",
    default=5,
    help="The number of letters in the target word.")
@click.option(
    "-g",
    "--total-guesses",
    default=6,
    help="The number of guesses you have to get the right word.")
@click.option(
    "--debug/--no-debug",
    default=False,
    help="If enabled, we print everying, incluing the answer.")
def main(debug, **kwargs):
  if debug:
    util.enable_debug()
  TordleApp.run(**kwargs)


if __name__ == "__main__":
  main()
