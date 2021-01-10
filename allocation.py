DEFAULT_VILLAGE_RESOURCES = 1
DEFAULT_CITY_RESOURCES = 2

def default_village_allocation(player,cell):
    '''Default resource allocation for villages'''
    player.resources[cell.resource] += DEFAULT_VILLAGE_RESOURCES
    return cell, DEFAULT_VILLAGE_RESOURCES

def default_city_allocation(player,cell):
    '''Default resource allocation for city'''
    player.resources[cell.resource] += DEFAULT_CITY_RESOURCES
    return cell, DEFAULT_CITY_RESOURCES