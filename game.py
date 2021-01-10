from itertools import cycle
from display import display_board
from board import init_board, DEFAULT_BOARD_COORDS
import allocation
import movement

class game(object):
    player_colors = {}
    players = {}
    board = None
    phase = None
    running = False
    phases = ['resource allocation',
              'trading',
              'propose movement',
              'movement execution',
              'building']
    phases_cycle = cycle(phases)
    round_count = 1
    village_allocation = allocation.default_village_allocation
    city_allocation = allocation.default_village_allocation
    
    @classmethod
    def next_phase(cls):
        '''Advance game to next phase'''
        if cls.running:
            cls.phase = next(cls.phases_cycle)
            if cls.phase == cls.phases[-1]:
                cls.increment_round()
        else:
            cls.running = True
            cls.phase = 'initial placement'
        print(cls.phase)

    @classmethod
    def increment_round(cls):
        cls.round_count+=1

    @classmethod
    def resources(cls):
        '''Allocate resources to all players'''
        if cls.phase == 'resource allocation':
            for cell in cls.board.values():
                if cell.development in ['village','city']:
                    player = cls.players[cell.player]
                    if cell.development == 'village':
                        cell, resource_count = cls.village_allocation(player,cell)
                    elif cell.development == 'city':
                        cell, resource_count = cls.city_allocation(player,cell)
                    print (f'Player {player.name} was allocated {resource_count} {cell.resource} from {cell.development} at {cell.key}')

    @classmethod
    def trading(cls,trade1,trade2):
        '''Execute a trade between two players'''
        if cls.phase == 'trading':
            p1, p1_resource, p1_count = trade1
            p2, p2_resource, p2_count = trade2
            if p1 and p2:
                p1.resources[p1_resource] -= p1_count
                p2.resources[p2_resource] -= p2_count
                p1.resources[p2_resource] += p2_count
                p2.resources[p1_resource] += p1_count
                print (f'Player {p1.name} and Player {p2.name} traded')
            else:
                print('Trade failed')

    @classmethod
    def resolve(cls):
        '''Resolve proposed movement'''
        players = [player for player in cls.players.values() if player.hypo_board]
        cls.board = movement.resolve_hypo_moves(cls.board, players)
        cls.reset_supports()

    @classmethod
    def end_game(cls):
        '''End the game and reset state'''
        cls.board = None
        cls.reset_phases()
        cls.reset_players()

    @classmethod
    def reset_phases(cls):
        '''Reset phases of game'''
        cls.running = False
        cls.phase = None
        cls.round_count = 1

    @classmethod
    def reset_players(cls):
        '''Reset registry of players'''
        cls.player_colors = {}
        cls.players = []

    @classmethod
    def reset_supports(cls):
        '''Reset development supports and defenses'''
        for cell in cls.board.values():
            cell.has_supported = False
            cell.army_has_supported = False
            cell.support = 0
            
        for player in cls.players.values():
            player.hypo_board = None

    @classmethod
    def display(cls,board=None):
        '''Display current board state'''
        if not board:
            board = cls.board
        display_board(board,cls.player_colors)

    @classmethod
    def create_board(cls,coords=DEFAULT_BOARD_COORDS,seed=None):
        '''Create a new board'''
        cls.board = init_board(coords,seed)
        return cls.board

    @classmethod
    def create_player(cls,player):
        '''Register a new player so board can represent player's objects'''
        cls.player_colors[player.name]=player.color
        cls.players[player.name] = player
        return player