import discord
import datetime
import pytz
import EDSM_generate_reports
import EDSM_bgs_tick_info
from EDSM_config_reader import get_discord_ini_values

# Load the INI file
config = "EDSM_config.ini"

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

#get data from the config.ini file
bot_name, discord_bot_token, discord_channels = get_discord_ini_values(config)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):

    # Get the ID of the current channel
    channel_id = message.channel.id
    
    # Check if the current channel is allowed
    if str(channel_id) not in discord_channels:
        return

    #Igrnore messages send by the bot itself
    if message.author == client.user:
        return
    
    #Only respond to messages the directly mentioned the bot
    if message.content.startswith(client.user.mention):
        wordsInMessage = message.content.split()
        command = wordsInMessage[1] # first word mentioned = command word
        
        if command == '$hello':
            await message.channel.send(f'Hello. I am the {bot_name} and I can post the current BGS reports for the systems.')

        if command == '$help':
            help_text = '\n'.join([
                    f'**{bot_name} bot commands**',
                    f'$hello - Greets the {bot_name}',
                    f'$version - shows the current version of the {bot_name}',
                    '$report - shows the latest BGS report for the systems',
                    '$tick - shows the latest BGS tick info form elite BGS',
                    '$status - shows the latest info about the time between tick and last update for the systems',
                ])
            await message.channel.send(help_text)

        if command == '$version':
            str_message = f'2305 - last updated on Mar 25, 2023 by CMD Dave Biggler'
            await message.channel.send(f'Version: {str_message}')

        if command == '$stop':
            #stop the bot
            await client.close()

        if command == '$tick':
        
            #send last tick info
            formatted_tick, formatted_timeSinceTick = EDSM_bgs_tick_info.get_tick_time()
            str_tick_info = f'Last detected tick UTC: {formatted_tick} - time since last tick: {formatted_timeSinceTick}'
            await message.channel.send(str_tick_info)        

        if command == '$status':
            
            #Header for the report
            str_message = f'**BGS system update info**'
            
            #send report header
            await message.channel.send(str_message)
            
            #send last tick info
            formatted_tick, formatted_timeSinceTick = EDSM_bgs_tick_info.get_tick_time()
            str_tick_info = f'Last detected tick UTC: {formatted_tick} - time since last tick: {formatted_timeSinceTick}'
            await message.channel.send(str_tick_info)
            
            #update the reports & post the reports
            EDSM_generate_reports.EDSM_get_system_update_status (config)
            await message.channel.send(file=discord.File('report_4.png'))

        if command == '$report':
            
            #get the current date
            utc = pytz.utc
            now = datetime.datetime.now(tz=utc).strftime("%b %d, %Y - %H:%M")
            str_message = f'**BGS Report from tick on {now} UTC**'
            
            #send report header
            await message.channel.send(str_message)
            
            #send last tick info
            formatted_tick, formatted_timeSinceTick = EDSM_bgs_tick_info.get_tick_time()
            str_tick_info = f'Last detected tick UTC: {formatted_tick} - time since last tick: {formatted_timeSinceTick}'
            await message.channel.send(str_tick_info)        
            
            #update the reports & post the reports
            EDSM_generate_reports.EDSM_get_report_system_overview (config)
            await message.channel.send(file=discord.File('report_1.png'))
            EDSM_generate_reports.EDSM_get_report_faction_overview (config)
            await message.channel.send(file=discord.File('report_2.png')) 
            EDSM_generate_reports.EDSM_get_report_inf_history (config)
            await message.channel.send(file=discord.File('report_3.png'))

client.run(discord_bot_token)
