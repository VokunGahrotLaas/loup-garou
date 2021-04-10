
class Game:
	def __init__(self, bot, name, id, lang):
		self.bot = bot
		self.name = name
		self.lang = lang
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
