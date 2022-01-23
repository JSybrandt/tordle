def clean_text(text: str) -> str:
  return text.strip().upper()


_DEBUG = False


def enable_debug():
  global _DEBUG
  _DEBUG = True


def debugging() -> bool:
  return _DEBUG


def dprint(*args, **kwargs):
  if _DEBUG:
    print("LOG:", *args, **kwargs)
