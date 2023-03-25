EDSM_Systems_Monitor
This project is a data scrapper that pulls data from EDSM API and converts the data into a  table as png-file. The data represents the state and influence of a faction in a specific system. The data is read from an INI file and is used to retrieve the information from the EDSM API. The resulting data is then processed and sorted to highlight the systems with the highest current influence. The resulting data is then converted into a pandas table and written to a file. The matplotlib table is styled using Bootstrap CSS, and color-coding is applied to highlight the systems with the highest influence. This project can be used by players of the video game Elite Dangerous to track the influence of factions in various systems.

1. Main files
EDSM_discord_bot-py
    Runs a Discord bot that responds to specific commands in a Discord channel. 
    Here is a brief overview of what the script does:

    Imports necessary modules, including the discord module, datetime module, pytz module, and various custom modules such as EDSM_generate_reports and EDSM_bgs_tick_info.
    Loads values from an INI file using a custom function get_discord_ini_values.
    Initializes a Discord client with specified intents.
    Defines functions for when the bot is ready and when a message is sent in a channel.
    The on_message function checks if the channel is allowed, ignores messages sent by the bot, and only responds to messages that directly mention the bot with specific commands (e.g. $hello, $version, $report).
    When a message is sent with a specific command, the bot sends a response in the channel with information or an attached image. For example, if the command is $hello, the bot responds with a greeting. If the command is $report, the bot generates an image with a BGS report and sends it to the channel.

EDSM_maual_report.py
    For testing the reports or generation the reports without the bot. The reports are saved as PNG images and are printed to the console after each report is generated.

EDSM_config.ini
    The file is organized into three sections, indicated by the section: 
    [Report_Data], [Non_Native_Factions], and [Discord_Data].

    The [Report_Data] section contains several key-value pairs that provide general information about the report, including the names of various star systems, the name of the faction being monitored, and the IDs associated with the report on external databases (EDSM_ID). The section also includes a list of systems cleared for BGS activies (CLEARED_SYSTEMS), as well as the title strings (TITLE_REPORT_1-4) that describe the different reports.

    The [Non_Native_Factions] section contains information about factions that are not native to the monitored star systems. Each key-value pair in this section represents a star system and the non-native faction(s) operating within it. 

    Finally, the [Discord_Data] section contains configuration information for a Discord bot that appears to be associated with the report. This includes the name of the bot (BOT_NAME), a list of channel IDs where the bot will post updates (DISCORD_CHANNEL), and a Discord token (DISCORD_TOKEN) that allows the bot to connect to the Discord API.

2. Libraries
EDSM_generate_reports.py
    generates reports based on data from the EDSM (Elite Dangerous Star Map) API. It contains four functions EDSM_get_report_system_overview, EDSM_get_report_faction_overview, EDSM_get_report_inf_history, and EDSM_get_system_update_status.

    EDSM_get_report_system_overview generates a report that provides an overview of the given systems including their population, economy, state, operations, influence, last influence, delta influence, approval, approximate maximum influence, and last update UTC. The function makes use of other modules to obtain the necessary data from the EDSM API and to format the report.

    EDSM_get_report_faction_overview generates a report that provides an overview of the non-native factions in a given system including their influence, active states, days won, pending states, and last update (UTC). The function makes use of other modules to obtain the necessary data from the EDSM API and to format the report.

    EDSM_get_report_inf_history generates a report that provides the influence history of the last 7 days for a given system. The function makes use of other modules to obtain the necessary data from the EDSM API and to format the report.

    EDSM_get_system_update_status generates a report that provides the last update status of the given systems. The function makes use of other modules to obtain the necessary data from the EDSM API and to format the report.

EDSM_format_report_n.py (for all 4 reports)
    renders a table as a matplotlib plot. The table data is passed as an argument, along with various formatting parameters such as column widths, font size, and cell colors. The function creates a plot figure and axis if one is not provided, and then generates the table using the table function of the matplotlib.pyplot module.

    The function first sets up the font and font size to be used in the table using the plt.rc function. It then creates the table using the table function, passing in the table data, column labels, and various formatting arguments and generates the report'n'.pgn (for all 4 reports) files.

    If needed the column size can be modified in this library by chaning the float values in the paramter col_width in the render_report function.


EDSM_get_system_data.py
    using the EDSM API to get the influence history of a faction in a particular system. It uses the requests library to send HTTP requests to the EDSM API and the json library to parse JSON responses. It also uses other Python libraries such as pytz and locale to format dates and numbers.

    The get_influence_history function takes two parameters, the name of the system and the ID of the faction in that system. It returns a tuple with the following data: system name, state, current influence, most recent influence, delta influence, sorted influences, and a list of formatted dates.

    The function first sends a GET request to the EDSM API to get system data, including the population of the system. It then sends another GET request to the EDSM API to get faction data for the specified system. It finds the faction with the specified ID and gets the influence history of that faction.

    The function creates a list of the last 7 days in Unix time and formats them as a list of strings. It then iterates through the influence history of the faction and stores the influence values in a dictionary. It fills in missing dates with the last available value and sorts the influence values by date. Finally, it returns the requested data as a tuple.

EDSM_get_faction_data.py
    The first function get_faction_data(system, faction) extracts data from the EDSM API for a specified faction in a specified system. It returns a tuple with the current state, current influence, and last update time for the faction.

    The second function get_conflict_data(system, faction, factions) extracts data from the Elite BGS API for a specified faction in a specified system. It returns a tuple with the number of days won in a conflict and a flag indicating if the faction is relevant in the conflict.

    Both functions catch exceptions related to making a request to the API or parsing the response and print an error message indicating what went wrong. If an exception is caught, the function returns empty strings or None values.

EDSM_get_BGS_activites.py
    function that takes in two parameters, influence and population, and returns an integer value indicating the appropriate BGS operation based on certain conditions.

    If the influence is greater than 55 and the population is greater than or equal to 1 billion, the function returns the integer value 30. If the influence is greater than 55 and the population is between 1 million and 1 billion, the function returns the integer value 20. If the influence is greater than 55 and the population is less than 1 million, the function returns the integer value 10. If the influence is less than or equal to 55, the function returns the integer value 0.

EDSM_bgs_tick_info.py
    defines two functions that obtain the timestamp of the last tick from an API endpoint. The first function, get_tick_time(), returns the formatted timestamp and the time difference between the current time and the tick time. The second function, get_tick_time_unix(), returns the tick timestamp and the time difference between the current time and the tick time in Unix time format.

EDSM_config_reader.py
    defines four functions that read and parse different configuration values from an INI file. The get_report_ini_values function returns the values of SYSTEMS, FACTION_NAME and EDSM_ID from the [Report_Data] section of the INI file. The get_cleared_systems function returns the values of CLEARED_SYSTEMS from the same section. The get_discord_ini_values function returns the values of BOT_NAME, DISCORD_CHANNEL, and DISCORD_TOKEN from the [Discord_Data] section of the INI file. Finally, the get_non_native_factions function returns a dictionary of sets containing the non-native factions for each system defined in the [Non_Native_Factions] section of the INI file.

