import discord
from discord.ext import commands
from re import fullmatch
from os import mkdir
from os.path import exists

import json_handler as json
from game import Game
from roles import Role
from lang import langs

ROOT_FOLDER = "."
DATA_FOLDER = ROOT_FOLDER + "/data"

class GameBot(commands.Bot):
	def make_files(self):
		if not exists(DATA_FOLDER):
			mkdir(DATA_FOLDER)
		pass

	def load_files(self):
		pass

	def dump_files(self):
		pass

	def __init__(self, command_prefix):
		commands.Bot.__init__(self, command_prefix= command_prefix)

		self.games = set()
		self.from_id = {}
		self.from_name = {}

		self.make_files()
		self.load_files()

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
		async def create(ctx, name, lang= None):
			if name in self.from_name.keys():
				await ctx.reply("This game already exists...")
				return
			if not fullmatch(r"[a-zA-Z0-9\-_]{,16}", name):
				await ctx.reply("This name is invalid, please only use 16 of the following characters: letters, digits, dashes and underscores...")
				return
			message = await ctx.reply(f"Game '{name}' has been created!\nReact to this post to join.")
			await message.add_reaction("\N{White Heavy Check Mark}")
			self.create_game(name, message.id, lang)
		
		@self.command()
		@commands.guild_only()
		async def delete(ctx, name):
			if name not in self.from_name.keys():
				await ctx.reply("This game does not exist...")
				return
			await ctx.reply(f"Game '{name}' has been deleted!")
			self.delete_game(name)
		
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
	
	def command(self, name= None, cls= None, **attrs):
		if "aliases" not in attrs:
			attrs["aliases"] = []
		def decorator(func):
			nonlocal name, cls, attrs
			if name is None:
				name = func.__name__
			attrs["aliases"] += [ lang["commands"][name] for lang in langs.values() if "commands" in lang and name in lang["commands"] and lang["commands"][name] not in attrs["aliases"] and lang["commands"][name] != name]
			return commands.Bot.command(self, name= name, cls= cls, **attrs)(func)
		return decorator

	def run(self, token):
		try:
			commands.Bot.run(self, token)
		except:
			self.dump_files()
	
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
	
	async def on_guild_join(self, guild):
		pass
	
	async def on_guild_remove(self, guild):
		pass
	
	def create_game(self, name, id, lang):
			game = Game(self, name, id, lang)
			self.games.add(game)
			self.from_id[id] = game
			self.from_name[name] = game
	
	def delete_game(self, name):
			game = self.from_name[name]
			self.games.remove(game)
			del self.from_id[game.id]
			del self.from_name[name]

def main():
	GameBot(command_prefix= "$mj ").run(json.load("token.json"))

if __name__ == "__main__":
	main()
