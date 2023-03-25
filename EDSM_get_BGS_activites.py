def get_BGS_activites(influence, population):
    """ 
    Return the appropriate BGS activites based on conditions.

    Parameters:
        influence (float): Influence over population
        population (int): Number of people

    Returns:
        int: The appropriate BGS activites for the given variables
    """
    # influence more than 55 and population more than 1 000 000 000 return 30 actives
    if influence > 55 and population >= 1000000000:
        return int(30)
    # influence more than 55 und popopulationp between 1 000 000 and 1 000 000 000 return 20 actives
    elif influence > 55 and 1000000 <= population < 1000000000:
        return int(20)
    # influence more than 55 und population less than 1 000 000 return 10 actives
    elif influence > 55 and population < 1000000:
        return int(10)
    # influence less than 55 return 0 actives
    elif influence <= 55:
        return int(0)
    