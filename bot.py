import discord
from discord.ext import commands
import json_handler as json
from re import fullmatch

class Game:
	def __init__(self, bot, name, id):
		self.bot = bot
		self.name = name
		self.id = id
		self.players = set()
	
	async def join(self, player):
		if player in self.players: return
		self.players.add(player)
		await player.send(f"You joined '{self.name}'.")
	
	async def quit(self, player):
		if player not in self.players: return
		self.players.remove(player)
		await player.send(f"You quitted '{self.name}'.")

class GameBot(commands.Bot):
	def __init__(self, command_prefix):
		commands.Bot.__init__(self, command_prefix= command_prefix)

		self.games = set()
		self.from_id = {}
		self.from_name = {}

		@self.command()
		async def ping(ctx):
			await ctx.reply("pong")
		
		@self.command(name= "eval")
		@commands.is_owner()
		async def _eval(ctx):
			async with ctx.channel.typing():
				r = eval(ctx.message.content[len(self.command_prefix + "eval "):])
			hasattr(r, "__str__")
			await ctx.reply(str(r))

		@self.command()
		@commands.guild_only()
		async def create(ctx, name):
			if name in self.from_name.keys():
				await ctx.reply("This game already exists...")
				return
			if not fullmatch(r"[a-zA-Z0-9\-_]{,16}", name):
				await ctx.reply("This name is invalid, please only use 16 of the following characters: letters, digits, dashes and underscores...")
				return
			message = await ctx.reply(f"Game '{name}' has been created!\nReact to this post to join.")
			await message.add_reaction("\N{White Heavy Check Mark}")
			game = Game(bot= self, name= name, id= message.id)
			self.games.add(game)
			self.from_id[message.id] = game
			self.from_name[name] = game
		
		@self.command()
		@commands.guild_only()
		async def deleted(ctx, name):
			if name not in self.from_name.keys():
				await ctx.reply("This game does not exist...")
				return
			await ctx.reply(f"Game '{name}' has been deleted!")
			game = self.from_name[name]
			self.games.remove(game)
			del self.from_id[game.id]
			del self.from_name[name]
		
		@self.command()
		@commands.guild_only()
		async def join(ctx, name):
			if name not in self.from_name.keys():
				await ctx.reply("This game does not exist...")
				return
			game = self.from_name[name]
			if ctx.author in game.players:
				await ctx.reply("You already joined...")
				return
			await game.join(ctx.author)
			await ctx.reply(f"You joined '{name}'.")
		
		@self.command()
		@commands.guild_only()
		async def quit(ctx, name):
			if name not in self.from_name.keys():
				await ctx.reply("This game does not exist...")
				return
			game = self.from_name[name]
			if ctx.author not in game.players:
				await ctx.reply("You are not in this game...")
				return
			await game.quit(ctx.author)
			await ctx.reply(f"You quitted '{name}'.")
	
	async def on_ready(self):
		print("I'm ready!")
	
	async def on_message(self, message):
		await self.process_commands(message)
		if message.author.id == self.user.id:
			await self.self_message(message)
		elif message.type == discord.MessageType.default:
			await self.guild_message(message, message.author, message.guild)
		else:
			await self.dm_message(message, message.author)
	
	async def self_message(self, message):
		pass

	async def guild_message(self, message, author, guild):
		pass

	async def dm_message(self, message, author):
		pass

	async def on_reaction_add(self, reaction, author):
		if author.id == self.user.id:
			return
		for game in self.games:
			if reaction.message.id == game.id:
				await game.join(author)
				return

	async def on_reaction_remove(self, reaction, author):
		if author.id == self.user.id:
			return
		for game in self.games:
			if reaction.message.id == game.id:
				await game.quit(author)
				return

	async def on_command_error(self, ctx, error):
		if isinstance(error, commands.errors.CheckFailure):
			await ctx.send("nop")

def main():
	GameBot(command_prefix= "$mj ").run(json.load("token.json"))

if __name__ == "__main__":
	main()
