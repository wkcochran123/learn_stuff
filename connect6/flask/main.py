import random
import numpy as np
import copy
from tensorflow.keras.models import load_model

from flask import Flask, request
app = Flask(__name__)

def increment_side(side):
    side = (side+1) % 5 
    if side == 0:
        side = side + 1
    return side

def make_new_board():
    board = []
    for _ in range(19):
        row = []
        for _ in range(19):
            row.append(0)
        board.append(row)
    return board

def parse_board(board_string):
    board = make_new_board()
    for i in range(19):
        for j in range(19):
            board[i][j] = int(board_string[19*i+j])
    return board


def board_to_html_table(board,variables):
    ret = "<table border=0 padding=0 margin=0 bgcolor=D2B48C>"
    i = 0
    for x in board:
        j = 0
        ret = ret + "<tr>"
        for y in x:
            local_variables = "i={}&j={}".format(i,j)
            ret = ret + "<td align=center valign=center>"
            if y == 0:
                ret = ret + "<font size=+3><pre><a href=/?"+variables+local_variables+ \
                            " style='text-decoration: none;'>＋</a></pre></font>"
            elif y < 3:
                ret = ret + "<font color=000000 size=+4><pre>●\n</pre></font>"
            else:
                ret = ret + "<font color=FFFFFF size=+4><pre>●\n</pre></font>"
            j = j + 1
            ret = ret + "\n \n</a></pre></td>"
        i = i + 1
        ret = ret + "</tr>"
    ret = ret + "</table>"
    return ret

def encode_board(board):
    bval = ""
    for i in board:
        for j in i:
            bval = "{}{}".format(bval,j)
    return bval

def draw_board(board,side,player):
    
    bval = encode_board(board)

    variables = "side={}&".format(side) +     \
                "board={}&".format(bval) +    \
                "player={}&".format(player)

    return board_to_html_table(board,variables)


def get_header():
    return """
    <!DOCTYPE html>
    <html>
    <head>
    <title>Connect 6</title>
    <style>
       td {
           width: 40px;
           height: 50px;
       }
       a:link, a:visited {
           color: #000000; /* Example color: blue */
           text-decoration: none; /* Optional: removes underline from links */
       }
    </style>
    </head>
    """

def compute_move(board,side):
    model = load_model("../notebooks/random_v_real")

    redo_board = copy.deepcopy(board)
    for x in range(19):
        for y in range(19):
            if board[x][y] > 0:
                if board[x][y] < 3:
                    redo_board[x][y] = 1
                if board[x][y] > 2:
                    redo_board[x][y] = -1
    stone_val = 1 if side < 3 else -1

    selections=[]
    predictions=[]
    for x in range(19):
        for y in range(19):
            if board[x][y] == 0:
                redo_board[x][y] = stone_val
                data_np = np.array([redo_board])
                prediction = model.predict(data_np)
                if (prediction > 0.8):
                    selections.append((x,y))
                    predictions.append(prediction)
                redo_board[x][y] = 0

    print(selections)
    print(predictions)
    (x,y) = random.choice(selections)
    board[x][y] = side
    side = increment_side(side)
    return (board,side)
    


@app.route('/')
def hello_world():
    board = request.args.get("board","")
    i = int(request.args.get("i","9"))
    j = int(request.args.get("j","9"))
    side = int(request.args.get("side","2"))
    t = random.choice(["b","w"])
    print(t)
    player = request.args.get("player",t)
    print(player)

    board_list = []
    if "board" in request.args:
        board_list = parse_board(board)
    else:
        board_list = make_new_board()

    board_list[i][j] = side
    side = increment_side(side)

    if (player == "w" and side == 1) or (player == "b" and side == 3):
        (board_list,side) = compute_move(board_list,side)
        (board_list,side) = compute_move(board_list,side)

    page = get_header() + "<body>"

    if player == "b":
        page = page + "<h2>You are BLACK</h2>"
    else:
        page = page + "<h2>You are WHITE</h2>"

    page = page + draw_board(board_list,side,player) + "</body></html>"
    return 'Hello, World!<br>' + page + "<br><a href=/>Restart</a>"

if __name__ == '__main__':
    app.run(debug=True)

