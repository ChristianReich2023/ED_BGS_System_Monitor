import pandas as pd
import EDSM_format_report_1
import EDSM_format_report_2
import EDSM_format_report_3
import EDSM_format_report_4
import EDSM_config_reader
import EDSM_get_system_data
import EDSM_get_faction_data
import EDSM_bgs_tick_info
import datetime

#Report - System overview
def EDSM_get_report_system_overview(config):
        
    #load the parameter from th INI file
    SYSTEMS, FACTION_NAME, EDSM_ID = EDSM_config_reader.get_report_ini_values(config)

    # Initialize an empty list to store the data
    data = []

    # Loop through the systems
    for system in SYSTEMS:
        try:

            #get the parameters from the EDSM API
            system, population, economy, state, formatted_lastUpdate, influence, most_recent_influence, delta_influence, cleramce, MaxInf, operations = EDSM_get_system_data.get_system_data(system, EDSM_ID)
            
            # Append the data for this system to the data list
            data.append([system, population, economy, state, operations, influence, most_recent_influence, delta_influence, cleramce, MaxInf, formatted_lastUpdate])

        except Exception as e:
            # Handle the exception and move to the next iteration of the for loop
            print(f"Error: {e}. Skipping system {system}.")
            continue

    # Convert the data list to a matplotlib table
    column_headers = ['system', 'population', 'economy', 'active state', 'operations', 'influence', 'last inf', 'delta inf', 'aproval', 'appx max inf', 'last update UTC']
    df = pd.DataFrame(data, columns=column_headers)
    df = df.sort_values("influence", ascending=False)

    # Format and Convert the DataFrame 
    EDSM_format_report_1.render_report1(df)

    return EDSM_get_report_system_overview

def EDSM_get_report_faction_overview(config):
    # Report - Non native factions

    #load the parameter from th INI file
    FACTION_LIST = EDSM_config_reader.get_non_native_factions(config)

    # Initialize an empty list to store the data
    data = []

    # Loop through the systems
    for system, factions in FACTION_LIST.items():
        for faction in factions:
            try:

                #get the parameters from the EDSM API
                state, pendingStates, influence, formatted_lastUpdate = EDSM_get_faction_data.get_faction_data(system, faction)
                
                #get data about the conflict
                criticalStates = ['Election', 'War']
                if state in criticalStates:
                    daysWon, relevant = EDSM_get_faction_data.get_conflict_data(system, faction, factions)
                else:
                    daysWon = ''
                    relevant = ''

                # Append the data for this system to the data list
                data.append([system, faction, influence, state, daysWon, pendingStates, formatted_lastUpdate, relevant])

            except Exception as e:
                # Handle the exception and move to the next iteration of the for loop
                print(f"Error: {e}. Skipping system {system}.")
                continue

    # Convert the data list to a matplotlib table
    column_headers = ['system', 'faction', 'influence', 'active states', 'days won', 'pending states', 'last update (UTC)', 'relevant']
    df = pd.DataFrame(data, columns=column_headers)
    df = df.sort_values(by=["system", "influence"], ascending=[True, False])

    # Format and Convert the DataFrame 
    EDSM_format_report_2.render_report2(df)
    
    return EDSM_get_report_faction_overview

def EDSM_get_report_inf_history(config):
    # Report - influence history of the last 7 days

    #load the parameter from th INI file
    SYSTEMS, FACTION_NAME, EDSM_ID = EDSM_config_reader.get_report_ini_values(config)

    # Initialize an empty list to store the data
    data = []

    # Loop through the systems
    for system in SYSTEMS:
        try:

            #get the parameters from the EDSM API
            system, population, sorted_influences, formatted_dates = EDSM_get_system_data.get_influence_history(system, EDSM_ID)
            
            # Append the data for this system to the data list
            data.append([system, population] + sorted_influences)

        except Exception as e:
            # Handle the exception and move to the next iteration of the for loop
            print(f"Error: {e}. Skipping system {system}.")
            continue

    # Convert the data list to a matplotlib table
    column_headers = ['system', 'population', formatted_dates[0], formatted_dates[1], formatted_dates[2], formatted_dates[3], formatted_dates[4], formatted_dates[5], formatted_dates[6]]
    df = pd.DataFrame(data, columns=column_headers)
    df = df.sort_values(formatted_dates[0], ascending=False)

    # Format and Convert the DataFrame 
    EDSM_format_report_3.render_report3(df)
    
    return EDSM_get_report_inf_history

def EDSM_get_system_update_status(config):

    #load the parameter from th INI file
    SYSTEMS, FACTION_NAME, EDSM_ID = EDSM_config_reader.get_report_ini_values(config)

    # Initialize an empty list to store the data
    data = []	

    #get the parameters from the EDSM API
    tickTimeUnix, timeSinceTickUnix = EDSM_bgs_tick_info.get_tick_time_unix()

    # Loop through the systems
    for system in SYSTEMS:


            #get the parameters from the EDSM API
            lastUpdateUnix = EDSM_get_system_data.get_system_update_time(system, EDSM_ID)
            
            #define the status of the system
            system_timeSinceTick =  lastUpdateUnix - tickTimeUnix
            if system_timeSinceTick > 0:
                status = 'OK'
            elif system_timeSinceTick < 0:
                status = 'update needed'

            # format the timestamps into a readable format
            formatted_lastUpdate = datetime.datetime.fromtimestamp(int(lastUpdateUnix)).strftime('%b %d, %Y - %H:%M')
            formatted_tickTime = datetime.datetime.fromtimestamp(int(tickTimeUnix)).strftime('%b %d, %Y - %H:%M')

            # convert time difference to datetime.timedelta object
            time_diff = datetime.timedelta(seconds=system_timeSinceTick)

            # extract hours, minutes, and seconds from timedelta object
            hours, remainder = divmod(time_diff.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)

            # format the result as 'hms'
            formatted_system_timeSinceTick = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

            # Append the data for this system to the data list
            data.append([system, status, formatted_lastUpdate, formatted_system_timeSinceTick])
  
    # Convert the data list to a matplotlib table
    column_headers = ['system', 'status', 'last update (UTC)', 'since tick']
    df = pd.DataFrame(data, columns=column_headers)
    
    # Format and Convert the DataFrame 
    EDSM_format_report_4.render_report4(df)

    return EDSM_get_system_update_status


