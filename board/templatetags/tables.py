from django import template

register = template.Library()


@register.inclusion_tag(
    filename="board/includes/get_table_form.html", takes_context=True
)
def get_table(context, board, user):
    from board.models import Board

    board = Board.objects.get(id=board)
    table_string = (
        "<table border='1|0'><tr><td></td><td>A</td><td>B</td><td>C</td></tr>"
    )
    if board.nodes.next_player is not None:
        next_player = True if board.nodes.next_player.pk == user else False
    else:
        next_player = False
    for row in range(1, 4):
        table_string += f"<tr><td>{row}</td>"
        for column in ["A", "B", "C"]:
            if row in board.positions_circle[column]:
                table_string += "<td>O</td>"
            elif row in board.positions_cross[column]:
                table_string += "<td>X</td>"
            else:
                if next_player:
                    table_string += f"<td><input type='radio' name='position' value={column}_{row}>{column}{row}</td>"
                else:
                    table_string += "<td></td>"
        table_string += "</tr>"
    table_string += "</table>"

    return {"table_string": table_string, "next_player": next_player, "board": board}
