from flask import Flask, request
app = Flask(__name__)


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
                ret = ret + "<font size=+2><pre> <a href=/?"+variables+local_variables+ \
                            " style='text-decoration: none;'>＋</a> </pre></font>"
            elif y < 3:
                ret = ret + "<font color=000000 size=+3><pre> ● \n</pre></font>"
            else:
                ret = ret + "<font color=FFFFFF size=+3><pre> ● \n</pre></font>"
            j = j + 1
            ret = ret + "\n \n</a></pre></td>"
        i = i + 1
        ret = ret + "</tr>"
    ret = ret + "</table>"
    return ret

def draw_board(board_string,i,j,side):
    
    board = []
    if board_string == "":
        board = make_new_board()
    else:
        board = parse_board(board_string)

    board[i][j] = side


    bval = ""
    for i in board:
        for j in i:
            bval = "{}{}".format(bval,j)

    side = (side+1) % 5 
    if side == 0:
        side = side + 1

    variables = "side={}&".format(side) +     \
                "board={}&".format(bval)

    return board_to_html_table(board,variables)

@app.route('/')
def hello_world():
    board = request.args.get("board","")
    i = int(request.args.get("i","9"))
    j = int(request.args.get("j","9"))
    side = int(request.args.get("side","2"))
    page = ""
    page = page + draw_board(board,i,j,side)
    return 'Hello, World!<br>' + page + "<br><a href=/>Restart</a>"

if __name__ == '__main__':
    app.run(debug=True)

