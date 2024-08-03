import discord
import subprocess
import shlex

# Create an instance of a client
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Your bot's token (replace 'YOUR_BOT_TOKEN' with your actual bot token)
TOKEN = 'MTI2OTA4NzYxMjM1NDk1MzI3Ng.GYBC4b.A0vu8GrWr9T68RBuTEyeN-EEYH5RyVnOzlyfJM'

# Event triggered when the bot is ready
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

# Event triggered when a message is received
@client.event
async def on_message(message):
    # Prevent the bot from responding to its own messages
    if message.author == client.user:
        return

    # Command prefix and command parsing
    if message.content.startswith('!exec '):
        # Extract the command from the message
        command = message.content[len('!exec '):]
        
        # Validate and sanitize the command
        if not command or 'rm ' in command or 'sudo ' in command:
            await message.channel.send('Invalid command.')
            return
        
        try:
            # Execute the command
            process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            
            # Send the command output to the Discord channel
            if stdout:
                await message.channel.send(f'Output:\n{stdout.decode()}')
            if stderr:
                await message.channel.send(f'Error:\n{stderr.decode()}')
        except Exception as e:
            await message.channel.send(f'An error occurred: {str(e)}')

# Run the bot
client.run(TOKEN)
