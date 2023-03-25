import os
import configparser

def get_report_ini_values(ini_file):
    """
    Function to get the input parameters from the INI file and verify them.
    
    Parameters:
        ini_file (string): Name of the INI file. 
    
    Returns:
        A dictionary containing the input parameters if successful, None otherwise.
    """    
    try:
        #Check if the ini file exists
        if not os.path.exists(ini_file):
            raise Exception(f"{ini_file} does not exist.")

        config = configparser.ConfigParser()
        config.read(ini_file)

        # Check if the 'Report_Data' section exists in the INI file
        if not config.has_section('Report_Data'):
            raise Exception("Error: The 'Data' section does not exist in the INI file.")

        # Get the values of the variables from the INI file
        SYSTEMS = config.get('Report_Data', 'SYSTEMS')
        if not SYSTEMS:
            raise Exception("Error: The 'SYSTEMS' variable in the INI file is not filled.")
        SYSTEMS = SYSTEMS.split(', ')

        FACTION_NAME = config.get('Report_Data', 'FACTION_NAME')
        if not FACTION_NAME:
            raise Exception("Error: The 'FACTION_NAME' variable in the INI file is not filled.")

        try:
            EDSM_ID = config.getint('Report_Data', 'EDSM_ID')
        except ValueError:
            raise Exception("Error: The 'EDSM_ID' variable in the INI file is not a valid integer.")

        return SYSTEMS, FACTION_NAME, EDSM_ID
    
    except Exception as e:
        # Handle the exception and return None
        print(f"Error: {e}")
        return None

def get_cleared_systems(ini_file):
    """
    Function to get the input parameters from the INI file and verify them.
    
    Parameters:
        ini_file (string): Name of the INI file. 
    
    Returns:
        A dictionary containing the input parameters if successful, None otherwise.
    """    
    try:
        # Check if the ini file exists
        if not os.path.exists(ini_file):
            raise Exception(f"{ini_file} does not exist.")
                
        # Initialize a ConfigParser to read the INI file
        config = configparser.ConfigParser()            
        config.read(ini_file)
    
        # Get the values of the variables from the INI file
        CLEARED_SYSTEMS = config.get('Report_Data', 'CLEARED_SYSTEMS')
        if not CLEARED_SYSTEMS:
            raise Exception("Error: The 'CLEARED_SYSTEMS' variable in the INI file is not filled.")
        CLEARED_SYSTEMS = CLEARED_SYSTEMS.split(', ')
        
        return CLEARED_SYSTEMS
    
    except Exception as e:
        # Handle the exception and return None
        print(f"Error: {e}")
        return None


def get_discord_ini_values(ini_file):
    """
    Function to get the input parameters from the INI file and verify them.
    
    Parameters:
        ini_file (string): Name of the INI file. 
    
    Returns:
        A dictionary containing the input parameters if successful, None otherwise.
    """
    try:        
        # Check if the ini file exists
        if not os.path.exists(ini_file):
            raise Exception(f"{ini_file} does not exist.")
            
        # Initialize a ConfigParser to read the INI file
        config = configparser.ConfigParser()            
        config.read(ini_file)
        
        # Get the values of the variables from the INI file
        bot_name = config.get('Discord_Data', 'BOT_NAME')
        if not bot_name:
            raise Exception("Error: The 'BOT_NAME' variable in the INI file is not filled.")
        
        discord_channels = config.get('Discord_Data', 'DISCORD_CHANNEL')
        if not discord_channels:
            raise Exception("Error: The 'DISCORD_CHANNEL' variable in the INI file is not filled.")
        
        discord_bot_token = config.get('Discord_Data', 'DISCORD_TOKEN')
        if not discord_bot_token:
            raise Exception("Error: The 'DISCORD_TOKEN' variable in the INI file is not filled.")
            
        return bot_name, discord_bot_token, discord_channels

    except Exception as e:
        # Handle the exception and return None
        print(f"Error: {e}")
        return None

def get_non_native_factions(ini_file):
    """
    Function to get the input parameters from the INI file and verify them.
    
    Parameters:
        ini_file (string): Name of the INI file. 
    
    Returns:
        A dictionary containing the input parameters if successful, None otherwise.
    """
    try: 
        # Check if the ini file exists
        if not os.path.exists(ini_file):
            raise Exception(f"{ini_file} does not exist.")
        
        #load the parameter from th INI file
        config = configparser.ConfigParser()
        config.optionxform = lambda option: option  # returns options unaltered
        config.read(ini_file)

        non_native_factions = {}
        for system, factions in config.items('Non_Native_Factions'):
            non_native_factions[system] = set(factions.split(', '))
        
        if not non_native_factions:
            raise Exception("Error: The 'Non_Native_Factions' variable in the INI file is not filled.")
        
        return non_native_factions
    
    except Exception as e:
        # Handle the exception and return None
        print(f"Error: {e}")
        return None

def get_report_name(ini_file, report_no):
    """
    Function to get the report name from the INI file and verify them.
    
    Parameters:
        ini_file (string): Name of the INI file. 
    
    Returns:
        A string with the name of the report, None otherwise.
    """
    try: 
        # Check if the ini file exists
        if not os.path.exists(ini_file):
            raise Exception(f"{ini_file} does not exist.")
        
        #load the parameter from th INI file
        config = configparser.ConfigParser()
        config.optionxform = lambda option: option  # returns options unaltered
        config.read(ini_file)
        
        # Check if the 'Report_Data' section exists in the INI file
        if not config.has_section('Report_Data'):
            raise Exception("Error: The 'Data' section does not exist in the INI file.")
        
        report_name = config.get('Report_Data', f"TITLE_REPORT_{report_no}")
        if not report_name:
            raise Exception(f"Error: The 'REPORT_{report_no}' variable in the INI file is not filled.")
        
        return report_name
    
    except Exception as e:
        # Handle the exception and return None
        print(f"Error: {e}")
        return None