class Cell(object):
    
    def __init__(self,key,development=None,army=False):
        self.key = key
        self.resource = None
        self.player = None 
        self.development = development
        self.army = army
        self.supports = 0
        self.has_supported = False
        self.army_has_supported = False
        
    def __repr__(self):
        return f'cell{self.key}[resource={self.resource},player={self.player},development={self.development},army={self.army}]'

    def is_neighbor(self,other_cell):
        '''Is this cell a neighbor of the other cell?'''
        x,y = self.key
        neighbors = [(x+1,y-1),(x+1,y),(x,y+1),(x-1,y+1),(x-1,y),(x,y-1)]
        return other_cell.key in neighbors
        
    @property
    def strength(self):
        strength = 0
        if self.army:
            strength+=1
        if self.development in ['city','fort']:
            strength+1
        strength+=self.supports
        return strength