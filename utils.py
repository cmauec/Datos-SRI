#!/usr/bin/env python
def _safe_html(s):
  """Escape text to make it safe to display.

  Args:
    s: string, The text to escape.

  Returns:
    The escaped text as a string.
  """
  return cgi.escape(s, quote=1).replace("'", '&#39;')