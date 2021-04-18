
class Role:
	def __init__(self, bot):
		self.bot = bot

class Villager(Role):
	def __init__(self, bot):
		Role.__init__(self, bot)

class Elder(Villager):
	def __init__(self, bot):
		Villager.__init__(self, bot)

class Angel(Villager):
	def __init__(self, bot):
		Villager.__init__(self, bot)

class Chaman(Villager):
	def __init__(self, bot):
		Villager.__init__(self, bot)

class Hunter(Villager):
	def __init__(self, bot):
		Villager.__init__(self, bot)

class Cupid(Villager):
	def __init__(self, bot):
		Villager.__init__(self, bot)

class Fox(Villager):
	def __init__(self, bot):
		Villager.__init__(self, bot)

class MoonChild(Villager):
	def __init__(self, bot):
		Villager.__init__(self, bot)

class Salvator(Villager):
	def __init__(self, bot):
		Villager.__init__(self, bot)
 
class Witch(Villager):
	def __init__(self, bot):
		Villager.__init__(self, bot)

class Seer(Villager):
	def __init__(self, bot):
		Villager.__init__(self, bot)

class Thief(Villager):
	def __init__(self, bot):
		Villager.__init__(self, bot)

class Pyromaniac(Villager):
	def __init__(self, bot):
		Villager.__init__(self, bot)

class Death(Villager):
	def __init__(self, bot):
		Villager.__init__(self, bot)

class Dictator(Villager):
	def __init__(self, bot):
		Villager.__init__(self, bot)

class Astrologer(Villager):
	def __init__(self, bot):
		Villager.__init__(self, bot)

class BearShowman(Villager):
	def __init__(self, bot):
		Villager.__init__(self, bot)

class LittleGirl(Villager):
	def __init__(self, bot):
		Villager.__init__(self, bot)

class Werewolf(Role):
	def __init__(self, bot):
		Role.__init__(self, bot)

class InfectFatherOfWolves(Werewolf):
	def __init__(self, bot):
		Werewolf.__init__(self, bot)

class FeltedWolf(Werewolf):
	def __init__(self, bot):
		Werewolf.__init__(self, bot)

class BlackWolf(Werewolf):
	def __init__(self, bot):
		Werewolf.__init__(self, bot)

class WhiteWolf(Werewolf):
	def __init__(self, bot):
		Werewolf.__init__(self, bot)

class Variant(Role):
	def __init__(self, bot, role):
		Role.__init__(self, bot)
		self.role = role

class WildChild(Variant):
	def __init__(self, bot):
		Variant.__init__(self, bot, Villager)

class DogWolf(Variant):
	def __init__(self, bot):
		Variant.__init__(self, bot, None)