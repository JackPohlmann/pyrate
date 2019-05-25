import sys
sys.path
sys.path.append('../../')

import pyrate

# Set up the simple example
# This is a 'hardcoded' set of instructions that are used for debugging
testRecipe = pyrate.Recipe(pyrate.simple)

# The Recipe structure can be checked out by using the tree method:
testRecipe.tree()

# If initialized with a set of instructions, running the Recipe is easy:
testRecipe.run()
# Be warned... This will take a LONG time due to the bottlenecks, but it will
# at least show a visual progress update
