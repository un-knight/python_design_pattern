import io
import itertools
import os
import sys
import unicodedata

# Create constant tables
DRAUGHT, PAWN, ROOK, KNIGHT, BISHOP, KING, QUEEN = ("DRAUGHT", "PAWN",
  "ROOK", "KNIGHT", "BISHOP", "KING", "QUEEN")
BLACK, WHITE = ("BLACK", "WHITE")


if sys.platform.startswith("win"):
  def console(char, background):
    return char or " "
  # https://docs.python.org/3.5/library/io.html?highlight=io.stringio#io.StringIO
  sys.stdout = io.StringIO()
else:
  def console(char, background):
    format_str = "\x1B[{}m{}\x1B[0m"
    return format_str.format(43 if background == BLACK else 47, char or " ")


class AbstractBoard:
  def __init__(self, rows, colums):
    self.board = [[None for _ in range(colums) for _ in range(rows)]]
    self.populate_board()

  def populate_board(self):
    raise NotImplementedError()

  def __str__(self):
    squares = []
    for y, row in enumerate(self.board):
      for x, piece in enumerate(row):
        square = console(piece, BLACK if (y + x) % 2 else WHITE)

class CheckersBoard(AbstractBoard):
  def __init__(self):
    self.populate_board()

  def populate_board(self):
    def black():
      return create_piece(DRAUGHT, BLACK)
    def white():
      return create_piece(DRAUGHT, WHITE)
    rows = ((None, black()), (black(), None), (None, black()), 
            (black(), None),
            (None, None), (None, None),
            (None, white()), (white(), None), (None, white()),
            (white(), None))
    self.board = [list(itertools.islice(
      itertools.cycle(squares), 0, len(rows))) for squares in rows]



def main():
  checkers = CheckersBoard()
  print(checkers)

  chess = ChessBoard()
  print(chess)

  if sys.platform.startswith("win"):
    filename = os.path.join("./gameboard.txt")
    with open(filename, "w", encoding="utf-8") as f:
      f.write(sys.stdout.getvalue())
    # Print to screen
    print("wrote {}".format(filename), file=sys.__stdout__)

if __name__ == '__main__':
  main()