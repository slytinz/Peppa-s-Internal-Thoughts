# import openai
# import discord
# from discord.ext import commands
# import yaml

# # Read config.yaml and get the openai_key and bot_token
# with open("config.yaml", "r") as file:
#     config_data = yaml.safe_load(file)

# # Set OpenAI API key
# openai.api_key = config_data.get("openai_key")
# bot_token = config_data.get("bot_token")

# # Permissions we need
# intents = discord.Intents.default()
# intents.messages = True
# intents.message_content = True
# intents.members = True

# class DisplayNameMemberConverter(commands.MemberConverter):
#     async def convert(self, ctx, argument):
#         for member in ctx.guild.members:
#             if member.display_name.lower() == argument.lower():
#                 return member
#         raise commands.MemberNotFound(argument)

# # Declaring that our bot is named bot and that its command is !!
# # It also gives the intents we set in the section above
# bot = commands.Bot(command_prefix="!!", intents=intents)

# @bot.event
# async def on_ready():
#     print(f"{bot.user.name} is online.")

# @bot.command(name="test")
# async def test(ctx):
#     await ctx.send("Hello, this is a test command!")

# bot.run(bot_token)
