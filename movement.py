import copy

def hypo_move(board,current_cell,target_cell):
    '''Hypothetical move by army from current to target cell'''
    hypo_board = copy.deepcopy(board)
    hypo_target_cell = copy.copy(target_cell)
    hypo_current_cell = copy.copy(current_cell)
    hypo_board[current_cell.key] = hypo_current_cell
    hypo_board[target_cell.key] = hypo_target_cell
    hypo_current_cell.army = False
    hypo_target_cell.army = True
    hypo_target_cell.player = hypo_current_cell.player
    if not hypo_current_cell.development:
        hypo_current_cell.player = None
    return hypo_board


def resolve_hypo_moves(board,players):
    '''Resolve conflicts in moves'''
    for player in players:
        for cell in board.values():
            hypo_cell = player.hypo_board[cell.key]
            if hypo_cell.player != cell.player:
                print (f'Resolving {player.name} move to {cell.key}')
                if hypo_cell.strength > cell.strength: #need to track chains of events (perhaps use count cells that are supporting by key?)
                    board[cell.key] = hypo_cell
    return board