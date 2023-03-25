import requests
import json
import pytz
import locale
import math
from datetime import datetime, timedelta
from EDSM_config_reader import get_cleared_systems
from EDSM_get_BGS_activites import get_BGS_activites

def get_influence_history(system, EDSM_ID):
    """
    Function to get the system data from the EDSM API.
    
    Parameters:
        system (string): Name of the system. 
        EDSM_ID (int): ID of the faction in the system.
    
    Returns:
        Tuple with the following data: system name, state, current influence, most recent influence, delta influence, sorted influences, and a list of formatted dates.
    """
    #intialize variables
    sorted_influences = [] # initialize with default value
    formatted_dates = [] # initialize with empty list
    unique_dates = [] # initialize with empty list
    formatted_dates = [] # initialize with empty list
    last_7_influences = {} # initialize with empty dictionary
    
    try:
        # Construct the URL to get the data from
        url = f"https://www.edsm.net/api-v1/system?systemName={system}&showInformation=1"

                # Send the request and get the response
        response = requests.get(url)
        response.raise_for_status()

        # Check if the response is not empty
        if not response.text:
            raise Exception(f"Error: The API response is empty for system {system}.")

        # Load the response data into a dictionary
        EDSMData = json.loads(response.text)
        information = EDSMData['information']
        
        #Get The Data
        population = information['population']

        #add thousand separator
        locale.setlocale(locale.LC_ALL, '')
        formatted_population = locale.format("%d", population, grouping=True)
        
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
        faction = next((f for f in factions if f['id'] == EDSM_ID), None)
    
        # If the faction is not found in this system, return None
        if faction is None:
            raise ValueError(f"No faction found with ID '{EDSM_ID}' in system '{system}'")
            return None
    
        # Get the influence history
        infHistory = faction['influenceHistory'] 

        # Create a list with the last 7 days in unix time
        utc = pytz.UTC
        last_7_dates_unix = [datetime.now().replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=utc) - timedelta(days=i) for i in range(7)]
        last_7_dates_unix = [int((date - datetime(1970, 1, 1, tzinfo=utc)).total_seconds()) for date in last_7_dates_unix]
        last_7_dates_unix.sort(reverse=True)       
        
        #create a list with the last 7 days formatted
        for date in last_7_dates_unix:
            formatted_date = datetime.fromtimestamp(int(date)).strftime("%b %d, %Y")
            formatted_dates.append(formatted_date)  #list with fomrates dates       
        
        # Iterate through the reversed inf_history
        for inf_date in reversed(infHistory):

            # Convert the timestamp to formatted string
            formatted_timestamp = datetime.fromtimestamp(int(inf_date)).strftime("%b %d, %Y")

            # Round off influence value to 2 decimal digits
            infValue = round(infHistory[inf_date] * 100, 2)

            # store influences in a dictionary
            if formatted_timestamp in last_7_influences and last_7_influences[formatted_timestamp]:
                #newest value already in the dictionary
                continue
            else:
                #newest value not in the dictionary
                last_7_influences[formatted_timestamp] = infValue  

            #get last date in last_7_dates_unix
            last_date_unix = last_7_dates_unix[-1]
            if last_date_unix > int(inf_date):
                # last value identified in infHistory
                break
        
        # Fill the missing dates with the last available value
        for date in last_7_influences:
            formatted_date = datetime.strptime(date, "%b %d, %Y").replace(tzinfo=utc)
            unique_dates.append(int(formatted_date.timestamp()))
        unique_dates.sort()
        
        for date in last_7_dates_unix:            
            formatted_date = datetime.fromtimestamp(int(date)).strftime("%b %d, %Y")            
            if date not in unique_dates:
                for inf_date in reversed(infHistory):
                    inf_timestamp = int(inf_date)
                    if inf_timestamp < date:  
                        last_7_influences[formatted_date] = float(round(infHistory[inf_date] * 100, 2))
                        break
               
        # Sort the influence values by date
        sorted_influences = [last_7_influences[date] for date in formatted_dates]

    except Exception as e:
        # Handle the exception and move to the next iteration of the for loop
        print(f"Error: {e}. Skipping system {system}.")

    return system, formatted_population, sorted_influences, formatted_dates

def get_system_data(system, EDSM_ID):
    """
    Function to get the system data from the EDSM API.
    
    Parameters:
        system (string): Name of the system. 
        EDSM_ID (int): ID of the faction in the system.
    
    Returns:
        Tuple with the following data: system name, state, current influence, most recent influence, delta influence, sorted influences, and a list of formatted dates.
    """
    try:
        # Construct the URL to get the data from
        url = f"https://www.edsm.net/api-v1/system?systemName={system}&showInformation=1"

        # Send the request and get the response
        response = requests.get(url)
        response.raise_for_status()

        # Check if the response is not empty
        if not response.text:
            raise Exception(f"Error: The API response is empty for system {system}.")

        # Load the response data into a dictionary
        EDSMData = json.loads(response.text)
        information = EDSMData['information']

        #Get The Data
        population = information['population']
        economy = information['economy']
        
        #add thousand separator
        locale.setlocale(locale.LC_ALL, '')
        formatted_population = locale.format("%d", population, grouping=True)
        
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
        faction = next((f for f in factions if f['id'] == EDSM_ID), None)
    
        # If the faction is not found in this system, return None
        if faction is None:
            return None
    
        # Get the state and current influence of the faction        
        state = faction['activeStates']
        if len(state) > 0:
            state_str = ", ".join([s['state'] for s in state])
        else:
            state_str = "-"

        lastUpdate = faction['lastUpdate']-3600
        formatted_lastUpdate = datetime.fromtimestamp(int(lastUpdate)).strftime("%b %d - %H:%M")
        influence = faction['influence'] * 100
        influence = float(round(influence, 2))
    
        # Get the influence history
        infHistory = faction['influenceHistory'] 
        
        # get the UTC timezone
        utc_timezone = pytz.timezone('UTC')

        # get the current time in UTC timezone
        current_time = datetime.now(utc_timezone)

        # set time to midnight
        today_midnight = current_time.replace(hour=0, minute=0, second=0, microsecond=0)

        # get time since midnight in UTC timezone 
        time_diff = current_time - today_midnight
   
        # get time difference in Unix timestamp format in seconds since midnight
        time_diff_in_seconds = time_diff.total_seconds()

        # convert the current time to Unix timestamp format
        unix_timestamp = int(current_time.timestamp())

        #get the first value from influence history
        most_recent_influence = influence
                
        # Get the influence value from the most recent date
        for inf_date in reversed(infHistory):
            inf_timestamp = int(inf_date)            
            # substract from now the time difference in seconds since midnight to get the influence value from yesterday
            if unix_timestamp - time_diff_in_seconds > inf_timestamp:
                most_recent_influence = float(round(infHistory[inf_date] * 100,2))
                break

        # Calculate the delta influence
        delta_influence = influence - most_recent_influence
        delta_influence = float(round(delta_influence, 2))

        #calulate the posible max Inf gain per system
        MaxInf = ((36-(math.log(population,2))) + (influence)) / ((36 - (math.log(population,2))) + 100)
        MaxInf = round(MaxInf*100,2)
        MaxInfGain = round(MaxInf - influence,2)
        
        #Check if system is cleared for action
        ini_file = "EDSM_config.ini"
        cleared_systems = get_cleared_systems(ini_file)
        
        cleramce = ''
        for cleared_system in cleared_systems:
            if cleared_system == system: 
                cleramce = 'OK' 

        #get the BGS activities information
        operations = get_BGS_activites(influence, population)

    except Exception as e:
        # Handle the exception and move to the next iteration of the for loop
        print(f"Error: {e}. Skipping system {system}.")

    return system, formatted_population, economy, state_str, formatted_lastUpdate, influence, most_recent_influence, delta_influence, cleramce, MaxInf, operations

def get_system_update_time(system, EDSM_ID):
    """
    Function to get the system data from the EDSM API.
    
    Parameters:
        system (string): Name of the system. 
        EDSM_ID (int): ID of the faction in the system.
    
    Returns:
        Tuple with the following data: system name, state, current influence, most recent influence, delta influence, sorted influences, and a list of formatted dates.
    """
    try:
        # Construct the URL to get the data from
        url = f"https://www.edsm.net/api-system-v1/factions?systemName={system}&showHistory=0" 

        # Send the request and get the response
        response = requests.get(url)
        response.raise_for_status()

        # Check if the response is not empty
        if not response.text:
            raise Exception(f"Error: The API response is empty for system {system}.")

        # Load the response data into a dictionary
        EDSMData = json.loads(response.text)
        faction = EDSMData['factions']

        for faction in EDSMData['factions']:
            if faction['id'] == EDSM_ID:
                lastUpdateUnix = faction['lastUpdate']-3600
                    
    except Exception as e:
        # Handle the exception and move to the next iteration of the for loop
        print(f"Error: {e}. Skipping system {system}.")

    return lastUpdateUnix