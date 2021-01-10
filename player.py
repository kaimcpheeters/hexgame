from constants import *
from game import game
import rules
import movement

class Player(object):
    
    def __init__(self,name,color):
        self.name = name
        self.color = color
        self.resources = {'grain':STARTING_GRAIN,'ore':STARTING_ORE,'sheep':STARTING_SHEEP,'wood':STARTING_WOOD}
        self.has_starting_village = True
        self.has_starting_fort = True
        self.hypo_board = None
        
    @property
    def placement_round(self):
        '''What placement round is the game in? First or second'''
        return sum([self.has_starting_village,self.has_starting_fort])*-1+3
        
    @property
    def resources_sum(self):
        return sum(self.resources.values())
        
    def __repr__(self):
        return f'Player {self.name}(resources={self.resources})'
    
    def place_village(self,cell):
        if game.phase == 'initial placement':
            if self.has_starting_village:
                self.has_starting_village = False
                cell.player = self.name
                cell.development = 'village'
    
    def place_fort(self,cell):
        if game.phase == 'initial placement':
            if self.has_starting_fort:
                self.has_starting_fort = False
                cell.player = self.name
                cell.development = 'fort'
        
    def build_army(self,cell):
        if game.phase == 'building':
            if rules.can_build_army(self.resources):
                self.resources['ore']-=ARMY_ORE
                self.resources['sheep']-=ARMY_SHEEP
                cell.player = self.name
                cell.army = True

    def build_village(self,cell):
        if game.phase == 'building':
            if rules.can_build_village(self.resources):
                self.resources['grain']-=VILLAGE_GRAIN
                self.resources['sheep']-=VILLAGE_SHEEP
                cell.player = self.name
                cell.development = 'village'
        
    def build_fort(self,cell):
        if game.phase == 'building':
            if rules.can_build_fort(self.resources):
                self.resources['ore']-=FORT_ORE
                self.resources['grain']-=FORT_GRAIN
                self.resources['wood']-=FORT_WOOD
                cell.player = self.name
                cell.development = 'fort'
        
    def build_city(self,cell):
        if game.phase == 'building':
            if rules.can_build_city(self.resources):
                self.resources['ore']-=CITY_ORE
                self.resources['wood']-=CITY_WOOD
                self.resources['sheep']-=CITY_SHEEP
                cell.player = self.name
                cell.development = 'city'
    
    def trade(self,resource,count):
        if game.phase == 'trading':
            if self.resources[resource] >= count:
                return (self, resource, count)
            else:
                print(f'Not enough {resource} to trade')
                return (None, None, 0)
                
    def move(self,cell,target_cell):
        if game.phase == 'propose movement':
            if cell.army and cell.is_neighbor(target_cell):
                self.hypo_board = movement.hypo_move(game.board, cell, target_cell)

    def support(self,cell,supported_cell,feature='army'):
        if game.phase == 'propose movement':
            if feature == 'army' and cell.army:
                if rules.army_can_support(cell,supported_cell):
                    supported_cell += SUPPORT_STRENGTH
                    cell.has_supported = True
            elif feature == cell.development:
                if rules.development_can_support(cell, supported_cell):
                    supported_cell += SUPPORT_STRENGTH
                    cell.army_has_supported = True
