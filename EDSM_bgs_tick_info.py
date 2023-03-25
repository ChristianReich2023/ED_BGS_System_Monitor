import json
import requests
import datetime
import pytz

def get_tick_time():
    """
    Function to get the las tick timestamp from the elite BGS API.
    
    Parameters:
        
    Returns:
        Tuple with the following data: fromated timestap , unix timestap 
    """
    formatted_tick = None
    tickTimestamp = None

    try:
        
        # Construct the URL to get the data from
        url = f"https://elitebgs.app/api/ebgs/v5/ticks"
        
        # Send the request and get the response
        response = requests.get(url)
        response.raise_for_status()

        # Check if the response is not empty
        if not response.text:
            raise Exception(f"Error: The API response is empty for Tick information.")

        # Load the response data into a dictionary
        json_data = json.loads(response.text)
        
       # Get the timestamp value from the json_data
        tickTimestamp = json_data[0]['time']

        # Convert the tickTimestamp to a datetime object
        tick_datetime = datetime.datetime.fromisoformat(tickTimestamp.replace("Z", "+00:00"))
        tick_datetime = tick_datetime.replace(tzinfo=pytz.utc)

        # Calculate the time difference between tickTimestamp and current time in UTC
        currentTime = datetime.datetime.now(pytz.utc)  # add .now with UTC timezone

        timeSinceTick = currentTime - tick_datetime 
        
        # Format time delta as proper H:M:S format (drop milliseconds)
        td = str(timeSinceTick).split(".")[0]
        timeSinceTick_str = datetime.datetime.strptime(td, "%H:%M:%S").strftime("%H:%M:%S")

        # format datetime to desired format 
        formatted_tick = datetime.datetime.strptime(tickTimestamp, "%Y-%m-%dT%H:%M:%S.%fZ").strftime('%b %d, %Y - %H:%M:%S')

    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"Error: {e}. No Tick information.")
        return '', ''

    return formatted_tick, timeSinceTick_str

def get_tick_time_unix():
    """
    Function to get the las tick timestamp from the elite BGS API.
    
    Parameters:
        
    Returns:
        Tuple with the following data: unix timestap, unix timedelta
    """
    tickTimestamp = None

    try:
        
        # Construct the URL to get the data from
        url = f"https://elitebgs.app/api/ebgs/v5/ticks"
        
        # Send the request and get the response
        response = requests.get(url)
        response.raise_for_status()

        # Check if the response is not empty
        if not response.text:
            raise Exception(f"Error: The API response is empty for Tick information.")

        # Load the response data into a dictionary
        json_data = json.loads(response.text)
        
       # Get the timestamp value from the json_data
        tickTimestamp = json_data[0]['time']
    
        # Convert the tickTimestamp to a datetime object
        tick_datetime = datetime.datetime.fromisoformat(tickTimestamp.replace("Z", "+00:00"))
        tickTimeUnix = tick_datetime.replace(tzinfo=pytz.utc)

        # Calculate the time difference between tickTimestamp and current time in UTC
        currentTime = datetime.datetime.now(pytz.utc)  # add .now with UTC timezone

        timeSinceTickUnix = currentTime - tickTimeUnix 
       
        # convert tickTimestamp to unix timestamp
        tickTimeUnix = int(tickTimeUnix.timestamp())

    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"Error: {e}. No Tick information.")
        return '', ''

    return tickTimeUnix, timeSinceTickUnix