import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import numpy as np
import utils

def vertical_coord(coords):
    return 2.0 * np.sin(np.radians(60)) * (coords[1] - coords[2]) /3.0

def horizontal_coord(coords):
    return [coord[0] for coord in coords]

def filter_coords(board,feature):
    hcoord = [coord[0] for coord in feature_positions(board,feature)]
    vcoord = [vertical_coord(coord) for coord in utils.to_cube_coords(feature_positions(board,feature))]
    return hcoord, vcoord

def army_positions(board):
    return [coords for (coords, cell) in board.items() if cell.army is True]

def development_positions(board,development):
    return [coords for (coords, cell) in board.items() if cell.development == development]

def feature_positions(board,feature):
    if feature == 'army':
        return army_positions(board)
    else:
        return development_positions(board,feature)

def plot_feature(ax,board,feature,colors,markers):
    ax.scatter(*filter_coords(board,feature), c=[c for c in colors], alpha=0.75,
               marker=r'$\{}$'.format(markers), s=800)
    
def plot_army(ax,board,colors):
    ax.scatter(*filter_coords(board,'army'), facecolor='none', edgecolors=colors, s=1800)

def _get_color(board,coord,player_colors):
    return player_colors.get(board.get(coord).player)

def get_colors(board,feature,player_colors):
    return [_get_color(board,coord,player_colors) for coord in feature_positions(board,feature)]

def get_cell_colors(board):
    RESOURCE_COLORS = {'ore':'black','wood':'brown','sheep':'green','grain':'yellow'}
    return [RESOURCE_COLORS.get(cell.resource) for cell in board.values()]

def display_board(board,player_colors):
    cell_colors = get_cell_colors(board)
    army_colors = get_colors(board,'army',player_colors)
    village_colors = get_colors(board,'village',player_colors)
    fort_colors = get_colors(board,'fort',player_colors)
    city_colors = get_colors(board,'city',player_colors)
    
    
    labels = [f'{x},{y}' for x,y in board.keys()]

    # Horizontal cartesian coords
    hcoord = [coord[0] for coord in board.keys()]

    # Vertical cartersian coords
    vcoord = [vertical_coord(coord) for coord in utils.to_cube_coords(board.keys())]

    fig, ax = plt.subplots(1)
    fig.set_size_inches(7.5, 7.5)
    ax.set_aspect('equal')

    for x, y, cell_color, label in zip(hcoord, vcoord, cell_colors, labels):
        hexagon = RegularPolygon((x, y), numVertices=6, radius=2. / 3., 
                             orientation=np.radians(30), 
                             facecolor= cell_color, alpha=0.2, edgecolor='k')
        ax.add_patch(hexagon)
        ax.text(x, y+0.2, label, ha='center', va='center', size=12)

    plot_army(ax,board,army_colors)
    plot_feature(ax,board,'village',village_colors,'boxdot')
    plot_feature(ax,board,'fort',fort_colors,'boxminus')
    plot_feature(ax,board,'city',city_colors,'boxplus')

    plt.show()