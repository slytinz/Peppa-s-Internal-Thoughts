import discord
from discord.ext import commands
import yaml
import torch
from io import BytesIO
from diffusers import StableDiffusionPipeline


# Read config.yaml and get the openai_key and bot_token
with open("config.yaml", "r") as file:
    config_data = yaml.safe_load(file)

# Set OpenAI API key and Discord keys
# openai.api_key = config_data.get("openai_api_key")
discord_token = config_data.get("discord_bot_token")


# ! Load Models
# model = StableDiffusionPipeline.from_pretrained("Envvi/Inkpunk-Diffusion", torch_dtype=torch.float32)
# model = StableDiffusionPipeline.from_pretrained("gsdf/Counterfeit-V2.5", torch_dtype=torch.float32)
model = StableDiffusionPipeline.from_pretrained("nitrosocke/Arcane-Diffusion", torch_dtype=torch.float32)
# torch_dtype=torch.float32

# Check if Hardware is Ready
print(torch.cuda.is_available())  # Should print True if CUDA is available
print(torch.cuda.current_device())  # Prints the current device ID
print(torch.cuda.get_device_name(0))  # Prints the name of the GPU
model.to("cuda" if torch.cuda.is_available() else "cpu")

# Create an instance of a client
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
# Bot's prefix
bot = commands.Bot(command_prefix="!", intent=intents)
# client = discord.Client(intents=intents)

@bot.event
async def on_ready():
    try:
        print(f'Logged in as {bot.user}')
    except Exception as e:
        print(f"Error during bot initialization: {e}")
        await bot.close() 

@bot.command(name="Peppa")
async def generate_image(ctx, *, prompt: str = None):
    if not prompt:
        await ctx.send("MEOW! Bad Kitty! Please provide a prompt for the image generation.")
        return
    
    # Initial message indicating progress
    progress_message = await ctx.send(f"Generating your image {ctx.author.metion}, please wait...")
    
    try:
        image = model(prompt).images[0]
        
        # Setup image to be sent
        image_bytes = BytesIO()
        image.save(image_bytes, format="PNG")
        image_bytes.seek(0)
        
        # Check Image size
        if len(image_bytes.getvalue()) > 8 * 1024 * 1024:
            print("The generated image exceeds Discord's file size limit.")
            await ctx.send("Something went wrong during image generation.")
            raise discord.HTTPException("Image Size exceeds Discord limitations")
        
        # Send Image to Discord
        await ctx.send(file=discord.File(image_bytes, filename="generated_image.png"))
        await progress_message.delete()
        
        print("Image successfully sent to Discord.")
    
    # Handles Generic Errors
    except Exception as e:
      await progress_message.edit(content="Something went wrong during image generation.")
      print(f"Error has occured: {e}")
    # Handles Discord Errors
    except discord.HTTPException as e:
        print(f"Failed to send image to Discord: {e}")

# Run the bot
bot.run(discord_token)
