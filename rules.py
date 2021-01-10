import utils
from constants import (
ARMY_ORE,
ARMY_SHEEP,
VILLAGE_GRAIN,
VILLAGE_SHEEP,
FORT_ORE,
FORT_GRAIN,
FORT_WOOD,
CITY_ORE,
CITY_WOOD,
CITY_SHEEP)
    
def neighbors(board,coord):
    '''Given (x,y) coord pair returns neighbors on board'''
    x,y,z = utils.to_cube_coords([coord])[0]
    neighbors = [(x+1,y-1,z),(x+1,y,z-1),(x,y+1,z-1),(x-1,y+1,z),(x-1,y,z+1),(x,y-1,z+1)]
    return [coords for coords in utils.to_axial_coords(neighbors) if coords in board.keys()]

#def is_neighbor(board,cell,other_cell):
#    '''Is other cell a neighbor?'''
#    return other_cell.key in neighbors(board,cell.key)

def is_costal(board,cell):
    '''Returns if (x,y) coard pair is on a costal cell on the board'''
    return len(neighbors(board,cell.key)) < 6

#def legal_placement(board,cell,placement_round):
#    if placement_round == 1:
#        return legal_first_placement(board,cell)
#    elif placement_round == 2:
#        return legal_first_placement(board,cell)
#    
#def legal_first_placement(board,cell):
#    return is_costal(board,cell) 
#    
#def legal_second_placement(board,cell):
#    return is_costal(board,cell)

def can_build_army(resources):
    return resources['ore'] >= ARMY_ORE and resources['sheep'] >= ARMY_SHEEP
    
def can_build_village(resources):
    return resources['grain'] >= VILLAGE_GRAIN and resources['sheep'] >= VILLAGE_SHEEP
    
def can_build_fort(resources):
    return resources['ore'] >= FORT_ORE and resources['grain'] >= FORT_GRAIN and resources['wood'] >= FORT_WOOD
    
def can_build_city(resources):
    return resources['ore'] >= CITY_ORE and resources['wood'] >= CITY_WOOD and resources['sheep'] >= CITY_SHEEP

def development_can_support(cell,supported_cell):
    '''Can the development in the cell support the supported cell this turn?'''
    can_support = bool (
        cell.development in ['fort','city'] and
        (not cell.has_supported) 
        and cell.is_neighbor(supported_cell))
    return can_support

def army_can_support(cell,supported_cell):
    '''Can the army in the cell support the supported cell this turn?'''
    return not cell.army_has_supported and cell.is_neighbor(supported_cell)