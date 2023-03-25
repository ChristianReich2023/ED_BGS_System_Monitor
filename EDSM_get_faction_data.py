import requests
import json
from datetime import datetime

def get_faction_data(system, faction):
    """
    Function to get the faction  data in a system from the EDSM API.
    
    Parameters:
        system (string): Name of the system. 
        faction (string): Name of the faction in the system.
    
    Returns:
        Tuple with the following data: current state, current influence, ...
    """
    try:
        
        # Construct the URL to get the data from
        url = f"https://www.edsm.net/api-system-v1/factions?systemName={system}&showHistory=1" 

        # Send the request and get the response
        response = requests.get(url)
        response.raise_for_status()

        # Check if the response is not empty
        if not response.text:
            raise Exception(f"Error: The API response is empty for system {system}.")

        # Load the response data into a dictionary
        EDSMData = json.loads(response.text)

        # Get the list of factions
        factions = EDSMData['factions']

        # Find the faction we're interested in
        faction = next((f for f in factions if f['name'] == faction), None)
    
        # If the faction is not found in this system, return None
        if faction is None:
            return None
    
        # Get the active state and of the faction        
        activeState = faction['activeStates']
        if len(activeState) > 0:
            activState_str = ", ".join([s['state'] for s in activeState])
        else:
            activState_str = "-"

        # Get the pending state of the faction        
        pendingState = faction['pendingStates']
        if len(pendingState) > 0:
            pendingState_str = ", ".join([s['state'] for s in pendingState])
        else:
            pendingState_str = "-"
        
        # Get the last update and current influence of the faction        
        lastUpdate = faction['lastUpdate']-3600
        formatted_lastUpdate = datetime.fromtimestamp(int(lastUpdate)).strftime("%b %d - %H:%M")
        influence = faction['influence'] * 100
        influence = float(round(influence, 2))
    
    except Exception as e:
        # Handle the exception and move to the next iteration of the for loop
        print(f"Error: {e}. Skipping system {system}.")

    return activState_str, pendingState_str, influence, formatted_lastUpdate

def get_conflict_data(system, faction, factions):
    """
    Function to get the faction  data in a system from the elite BGS API.
    
    Parameters:
        system (string): Name of the system. 
        faction (string): Name of the faction in the system.
    
    Returns:
        Tuple with the following data: days won, relevant for BGS,...
    """
    daysWon = None # Initialize to None 
    relevant = None # Initialize to None 
    
    try:
        
        # Construct the URL to get the data from
        url = f"https://elitebgs.app/api/ebgs/v5/factions?name={faction}&system={system}"
        
        # Send the request and get the response
        response = requests.get(url)
        response.raise_for_status()

        # Check if the response is not empty
        if not response.text:
            raise Exception(f"Error: The API response is empty for system {system}.")

        # Load the response data into a dictionary
        json_data = json.loads(response.text)
        faction_data = json_data['docs'][0]
                
        faction_systems = faction_data['faction_presence']
      
        for system_data in faction_systems:
            if system_data['system_name'] == system:
                for conflict in system_data['conflicts']:
                    days_won = conflict.get('days_won')
                    if conflict.get('opponent_name') in factions:
                        return days_won, ''
                return days_won, 'X'
                
        raise ValueError(f"Faction {faction} has no data on {system}")
    
    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"Error: {e}. Skipping system {system}.")
        return '', ''

    return daysWon, relevant