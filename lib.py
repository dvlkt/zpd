# Blah blah insert code here for the AI blah blah

# The score is an evaluation of how far the player is in the game. Usually the score is pretty straight forward and is displayed in-game. For example, in
# the dino game, the score is written right there in the corner and is simply the distance that the dino has ran. Meanwhile in a much more complicated game
# like Minecraft (not saying this AI could handle Minecraft) the score would have to be approximated.
score: float = 0

# This function is called to inform the AI on a changed score. The score is calculated by the mod and handed over to the AI.
def on_score_change(new_score: float):
	score = new_score

	# AI can do some stuff here


# This function is called to inform the AI on what is happening in-game. For example, the dino game could call this every 0.1 seconds to feed the AI a
# representation of what is happening in-game. The data variable is a 2D array consisting of numbers. For example, in the dino game it could be a simplified
# 2D view of the level at that point where 0 is the ground, 1 is the player, 2 is the cacti and 3 is the dragons. But this should not be hardcoded, the AI
# should learn these patterns and numbers on its own. It should be influenced only by the score that it sees.
def on_data(data):
	pass # AI can do some stuff here

# This function is called to inform the AI that the game was lost
def on_lose():
	pass # AI can do some stuff here

ACTION_AMOUNT = 5
# This function is not called by the mod, instead this function should be called by the AI in order to do something. Every action (e.g. jumping, walking,
# running, etc.) is labeled by a number, which the AI feeds into the function. The AI, of course, does not know which number does what. It learns this.
# Since each game has a different number of actions (for example, Minecraft has like 40 while the dino game has only 2), the amount of actions is specified
# in the script using the constant ACTION_AMOUNT.
def on_action(action_num):
	pass # Mod can do some stuff here