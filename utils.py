def to_cube_coords(coords):
    '''Cube coordinates (x,y,z)'''
    return [(x,y,-x-y) for x,y in coords]

def to_axial_coords(coords):
    '''Axial coordinates (x,y)'''
    return [(x,y) for x,y,_ in coords]
