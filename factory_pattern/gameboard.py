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

# Define AbstractBoard class
class AbstractBoard:
  def __init__(self, rows, columns):
    self.board = [[None for _ in range(columns)] for _ in range(rows)]
    self.populate_board()

  def populate_board(self):
    raise NotImplementedError()

  def __str__(self):
    squares = []
    for y, row in enumerate(self.board):
      for x, piece in enumerate(row):
        square = console(piece, BLACK if (y + x) % 2 else WHITE)
        squares.append(square)
      squares.append("\n")
    return "".join(squares)

# 国际跳棋
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
    # More information about itertools modular
    # https://docs.python.org/3.5/library/itertools.html?highlight=itertools#module-itertools
    self.board = [list(itertools.islice(
      itertools.cycle(squares), 0, len(rows))) for squares in rows]

# 国际象棋
class ChessBoard(AbstractBoard):
  def __init__(self):
    super().__init__(8, 8)

  def populate_board(self):
    for row, color in ((0, BLACK), (7, WHITE)):
      for columns, kind in (((0, 7), ROOK), ((1, 6), KNIGHT),
        ((2, 5), BISHOP), ((3,), QUEEN), ((4,), KING)):
        for column in columns:
          self.board[row][column] = create_piece(kind, color)
    for column in range(8):
      for row, color in ((1, BLACK), (6, WHITE)):
        self.board[row][column] = create_piece(PAWN, color)


def create_piece(kind, color):
  color = "White" if color == WHITE else "Black"
  name = {DRAUGHT: "Draught", PAWN: "ChessPawn", ROOK: "ChessRook",
          KNIGHT: "ChessKnight", BISHOP: "ChessBishop",
          KING: "ChessKing", QUEEN: "ChessQueen"}[kind]
  return globals()[color + name]()


class Piece(str):
  # To save memory space
  # https://docs.python.org/3.5/reference/datamodel.html?highlight=__slots__#object.__slots__
  __slots__ = ()


for code in itertools.chain((0x26C0, 0x26C2), range(0x2654, 0x2660)):
  # Get the character whose unicode code is the integer code
  char = chr(code)
  # Get the name of character assigned to char
  name = unicodedata.name(char).title().replace(" ", "")
  if name.endswith("sMan"):
    name = name[:-4]
  # new is a function
  new = (lambda char: lambda Class: Piece.__new__(Class, char))(char)
  new.__name__ = "__new__"
  # https://docs.python.org/3.5/library/functions.html?highlight=type#type
  Class = type(name, (Piece,), dict(__slots__=(), __new__=new))
  globals()[name] = Class


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