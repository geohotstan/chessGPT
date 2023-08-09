import chess
import chess.pgn
import chess.svg
import openai
import lmql
import sys
from state import State
import traceback
from text.local.localtextbots import *


# p = PythonLLaMABot(n)


from flask import Flask, Response, request
app = Flask(__name__)

@app.route("/")
def hello():
  ret = open("index.html").read()
  return ret.replace('start', s.board.fen())


def computer_move(s, v):
  # computer move
  # implement computer move through p
  '''
  move = sorted(explore_leaves(s, v), key=lambda x: x[0], reverse=s.board.turn)
  if len(move) == 0:
    return
  print("top 3:")
  for i,m in enumerate(move[0:3]):
    print("  ",m)
  print(s.board.turn, "moving", move[0][1])
  s.board.push(move[0][1])
  '''

@app.route("/selfplay")
def selfplay():
  s = State()

  ret = '<html><head>'
  # self play
  while not s.board.is_game_over():
    computer_move(s, v)
    ret += '<img width=600 height=600 src="data:image/svg+xml;base64,%s"></img><br/>' % to_svg(s)
  print(s.board.result())

  return ret


# move given in algebraic notation
@app.route("/move")
def move():
  if not s.board.is_game_over():
    move = request.args.get('move',default="")
    if move is not None and move != "":
      print("human moves", move)
      try:
        s.board.push_san(move)
        computer_move(s, v)
      except Exception:
        traceback.print_exc()
      response = app.response_class(
        response=s.board.fen(),
        status=200
      )
      return response
  else:
    print("GAME IS OVER")
    response = app.response_class(
      response="game over",
      status=200
    )
    return response
  print("hello ran")
  return hello()

# moves given as coordinates of piece moved
@app.route("/move_coordinates")
def move_coordinates():
  if not s.board.is_game_over():
    source = int(request.args.get('from', default=''))
    target = int(request.args.get('to', default=''))
    promotion = True if request.args.get('promotion', default='') == 'true' else False

    move = s.board.san(chess.Move(source, target, promotion=chess.QUEEN if promotion else None))

    if move is not None and move != "":
      print("human moves", move)
      try:
        s.board.push_san(move)
        computer_move(s, v)
      except Exception:
        traceback.print_exc()
    response = app.response_class(
      response=s.board.fen(),
      status=200
    )
    return response

  print("GAME IS OVER")
  response = app.response_class(
    response="game over",
    status=200
  )
  return response

@app.route("/newgame")
def newgame():
  s.board.reset()
  response = app.response_class(
    response=s.board.fen(),
    status=200
  )
  return response



# print the list of moves played
game = chess.pgn.Game()
board = chess.Board()
game.setup(board)

board.push_san("e4")
board.push_san("e5")
board.push_san("Nf3")
board.push_san("Nc6")
st = '3. d4 exd4 4. Bxh7+ Kxh7 5. dxe5 Qh4 6. g3 Ng8 7. Nbd2 d5 8. O-O Bh5 9. f4 Bg4 10. Bd2 Re8 11. Bf4 Bc8 12. Be3 Qd5 13. Rfe1 Qa6 14. Qb3 Qe7 15. Qxb7+ Kxb7 16. Nh2 Nh5 17. f5 Ng3 18. h3 Bf8 19. Bh5 g6 20. Ng3 Bg4 21. Rf4 Bd3 22. Re4 O-O-O 23. Qb2 Re8 24. Rad1 Rxh5 25. Nxf5+ Kg7 26. Nh7+ Kh7 27. Bxg6+ Rxg6 28. Ng5+ Kh6 29. Ne3'# 0-1
st = st.split()
st = [i for i in st if i[1] != '.']
for s in st:
  board.push_san(s)
# print(board.move_stack)
game.add_line(board.move_stack)
g = str(game).split('\n\n')[-1]
# print(g)


inp = f"""1. Nf3 Nf6 2. c4 g6 3. Nc3 Bg7 4. d4 O-O 5. Bf4 d5 6. Qb3 dxc4 7. Qxc4 c6 8. e4 Nbd7 9. Rd1 Nb6 10. Qc5 Bg4 11. Bg5 Na4 12. Qa3 Nxc3 13. bxc3 Nxe4 14. Bxe7 Qb6 15. Bc4 Nxc3 16. Bc5 Rfe8+ 17. Kf1 Be6 18. Bxb6 Bxc4+ 19. Kg1 Ne2+ 20. Kf1 Nxd4+ 21. Kg1 Ne2+ 22. Kf1 Nc3+ 23. Kg1 axb6 24. Qb4 Ra4 25. Qxb6 Nxd1 26. h3 Rxa2 27. Kh2 Nxf2 28. Re1 Rxe1 29. Qd8+ Bf8 30. Nxe1 Bd5 31. Nf3 Ne4 32. Qb8 b5 33. h4 h5 34. Ne5 Kg7 35. Kg1 Bc5+ 36. Kf1 Ng3+ 37. Ke1 Bb4+ 38. Kd1 Bb3+ 39. Kc1 Ne2+ 40. Kb1 Nc3+ 41. Kc1 Rc2# 0-1 \n
{g}
"""
# p.process_message(inp)

exit()
print("Moves played:")
print(board.fen())
for n, move in enumerate(board.move_stack, 1):
  print(f'{n}: {move.uci()}')
print(board)
exit()

while not board.is_game_over():
  placement, color, castling, enpassant, half, full = board.fen()
