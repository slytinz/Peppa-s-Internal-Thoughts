import discord
import openai
import yaml

# Read config.yaml and get the openai_key and bot_token
with open("config.yaml", "r") as file:
    config_data = yaml.safe_load(file)

# Set OpenAI API key
openai.api_key = config_data.get("openai_api_key")
discord_token = config_data.get("discord_bot_token")

# Create an instance of a client
intents = discord.Intents.default()
intents.message_content = True
intents.members = True 
client = discord.Client(intents=intents)


# Create a command to generate an image using DALL·E
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!Peppa'):
        prompt = message.content[len('!Peppa '):]  # Extract the prompt from the message (added space after !Peppa)
        
        if not prompt:
            await message.channel.send("MEOW! Please provide a prompt for the image generation.")
            return
        
        try:
            # Use the OpenAI client to generate an image using DALL-E 3
            response = openai.images.generate(
                model="dall-e-2",  # Specify the DALL-E 3 model
                prompt=prompt,
                size="1024x1024",
                quality="standard",  # You can adjust the quality (e.g., 'standard', 'high', etc.)
                n=1  # Number of images to generate
            )
            image_url = response.data[0].url  # Get the URL of the generated image
            await message.channel.send(image_url)  # Send the image URL to the Discord channel
        except Exception as e:
            await message.channel.send(f"Error generating image: {e}")

# Run the bot
client.run(discord_token)