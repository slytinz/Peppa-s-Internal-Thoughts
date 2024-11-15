import discord
import yaml
import torch
from io import BytesIO
from diffusers import StableDiffusionPipeline


# Read config.yaml and get the openai_key and bot_token
with open("config.yaml", "r") as file:
    config_data = yaml.safe_load(file)

# Set OpenAI API key
# openai.api_key = config_data.get("openai_api_key")
discord_token = config_data.get("discord_bot_token")

# Load the Waifu Diffusion model
model = StableDiffusionPipeline.from_pretrained("hakurei/waifu-diffusion", torch_dtype=torch.float32)
# model.to("cuda")  # If you have a GPU, this will speed up generation
# Move the model to CPU (which is the default if you don't have CUDA)
model.to("cpu")

# Create an instance of a client
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!Peppa'):
        prompt = message.content[len('!Peppa '):]

        if not prompt:
            await message.channel.send("MEOW! Please provide a prompt for the image generation.")
            return

        # Generate an image using Waifu Diffusion
        image = model(prompt).images[0]

        # Create a BytesIO object to send the image without saving it
        image_bytes = BytesIO()
        image.save(image_bytes, format="PNG")
        image_bytes.seek(0)  # Reset the pointer to the beginning of the BytesIO object

        # Send the image in Discord as an in-memory file
        await message.channel.send(file=discord.File(image_bytes, filename="generated_image.png"))

# Run the bot
client.run(discord_token)
