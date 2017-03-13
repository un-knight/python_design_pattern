#!/usr/bin/env python3
import abc
import os
import re
import sys
import tempfile
from html import escape


html_filename = './login.html'
tk_filename = './login.py'


# Abstract class
class AbstractFormBuilder:

  def add_title(self, title):
    self.title = title

  def form(self):
    pass

  def add_label(self, name, y, x, **kwargs):
    pass

  def add_entry(self, name, y, x):
    pass

  def add_button(self, name, y, x, **kwargs):
    pass

class HtmlFormBuilder(AbstractFormBuilder):

  def __init__(self):
    self.title = 'HtmlFormBuilder'
    self.items = {}

  def add_title(self, title):
    # html.escape() converts the characters `&, <, >` in string title 
    # to HTML-safe sequences.
    super().add_title(escape(title))

  def add_label(self, text, y, x, **kwargs):
    label_form = """<td><label for="{}">{}:</label></td>"""
    self.items[(y, x)] = label_form.format(kwargs['target'], escape(text))

  def add_entry(self, text, y, x, **kwargs):
    html_form = """<td><input name="{}" type="{}" /></td>"""
    self.items[(y, x)] = html_form.format(text, kwargs.get('kind', 'text'))

  def add_button(self, text, y, x, **kwargs):
    html = """<td><input type="submit" value="{}" /></td>""".format(escape(text))
    self.items[(y, x)] = html

  def form(self):
    html = ["<!doctype html>\n<html><head><title>{}</title></head>"
            "<body>".format(self.title), '<form><table border="0">']
    this_row = None
    for key, value in sorted(self.items.items()):
      y, x = key
      if this_row is None:
        html.append("  <tr>")
      elif this_row != y:
        html.append('  </tr>\n  <tr>')
      this_row = y
      html.append("    " + value)
    html.append("  </tr>\n</table></form></body></html>")
    return '\n'.join(html)


class TkFormBuilder(AbstractFormBuilder):

  TEMPLATE = """#!/usr/bin/env python3
import tkinter as tk
import tkinter.ttk as ttk

class {name}Form(tk.Toplevel):

    def __init__(self, master):
        super().__init__(master)
        self.withdraw()     # hide until ready to show
        self.title("{title}")
        {statements}
        self.bind("<Escape>", lambda *args: self.destroy())
        self.deiconify()    # show when widgets are created and laid out
        if self.winfo_viewable():
            self.transient(master)
        self.wait_visibility()
        self.grab_set()
        self.wait_window(self)

if __name__ == "__main__":
    application = tk.Tk()
    window = {name}Form(application)
    application.protocol("WM_DELETE_WINDOW", application.quit)
    application.mainloop()
"""

  def __init__(self):
    self.title = 'TkFormBuilder'
    self.statements = []

  def add_title(self, title):
    super().add_title(title)

  def add_label(self, text, y, x, **kwargs):
    name = self._canonicalize(text)
    create = """self.{}Label = ttk.Label(self, text="{}:")""".format(
             name, text)
    layout = """self.{}Label.grid(row={}, column={}, sticky=tk.W, \
padx="0.75m", pady="0.75m")""".format(name, y, x)
    self.statements.extend((create, layout))

  def add_entry(self, text, y, x, **kwargs):
    name = self._canonicalize(text)
    extra = "" if kwargs.get("kind") != "password" else ', show="*"'
    create = "self.{}Entry = ttk.Entry(self{})".format(name, extra)
    layout = """self.{}Entry.grid(row={}, column={}, sticky=(\
tk.W, tk.E), padx="0.75m", pady="0.75m")""".format(name, y, x)
    self.statements.extend((create, layout))

  def add_button(self, text, y, x, **kwargs):
    name = self._canonicalize(text)
    create = """self.{}Button = ttk.Button(self, text="{}")""".format(name, text)
    layout = """self.{}Button.grid(row={}, column={}, padx="0.75m", \
pady="0.75m")""".format(name, y, x)
    self.statements.extend((create, layout))

  def form(self):
    return TkFormBuilder.TEMPLATE.format(title=self.title,
            name=self._canonicalize(self.title, False),
            statements="\n        ".join(self.statements))

  def _canonicalize(self, text, startLower=True):
    text = re.sub("\W+", "", text)
    if text[0].isdigit():
      return "_" + text
    return text if not startLower else text[0].lower() + text[1:]


# Use `create_login_form` to create both  HTML form and Tkinter form
def create_login_form(builder):
  builder.add_title('Login')
  builder.add_label('Username', 0, 0, target='username')
  builder.add_entry('username', 0, 1)
  builder.add_label('Password', 1, 0, target='password')
  builder.add_entry('password', 1, 1, kind='password')
  builder.add_button('Login', 2, 0)
  builder.add_button('Cancel', 2, 1)
  return builder.form()


def main():
  # Print the form on screen.
  if len(sys.argv) > 1 and sys.argv[1] == '-P':
    print(create_login_form(HtmlFormBuilder()))
    print(create_login_form(TkFormBuilder()))
    return

  # Create html form.
  html_form = create_login_form(HtmlFormBuilder())
  with open(html_filename, 'w', encoding='utf-8') as f:
    f.write(html_form)
  print("wrote", html_filename)

  # Create Tkinter form.
  tk_form = create_login_form(TkFormBuilder())
  with open(tk_filename, 'w', encoding='utf-8') as f:
    f.write(tk_form)
  print('wrote', tk_filename)
  return

if __name__ == '__main__':
  main()