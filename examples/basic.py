"""IMPORTANT: make sure to run the build_defaults.sh script in the top-level
directory and installing the specified Python packages before using PyRATE."""

import sys
sys.path
sys.path.append('../../')
import pprint

import pyrate


# Set up a nicely formatted print function for printing dicts:
pp = pprint.PrettyPrinter(indent=4)
mprint = pp.pprint

# Check out the instructions to see how they are set up:
mprint(pyrate.template)  # The template is a dictionary setup for instructions

# Compare this to the default instructions:
mprint(pyrate.default)

# Now, initialize a Recipe:
myRecipe = pyrate.Recipe()

# Initializing an empty Recipe automatically sets the default instructions.
# Test this by initializing a new recipe and specifying the instructions:
testRecipe = pyrate.Recipe(pyrate.default)
print(myRecipe==testRecipe)

# The asDict method allows the Recipe to be viewed as a dictionary.
# This is especially useful for looking at the hierarchy:
mprint(myRecipe.asDict())

# Notice how the recipe has extra keys 'coreInst' and 'Data'.
# These keys store values that set, load, and run the core module and hold the 
# generated output.

# Also note that setting values to this dictionary do not persist...
myRecipe.asDict()['Plugins']['atmosphere'] = 'foo'
print(myRecipe.asDict()['Plugins']['atmosphere'])

# ...but doing so with the Recipe itself does!
myRecipe['Plugins']['atmosphere'] = 'foo'
print(myRecipe.asDict()['Plugins']['atmosphere'])

# Now set the value back using the named convention of the PyRATE Recipes:
myRecipe.Plugins.atmosphere = 'rttov'
print(myRecipe.asDict()['Plugins']['atmosphere'])

# Or list the possible settings using the keys method:
print(myRecipe.Plugins.keys())

# Finally, running a recipe is very simple:
myRecipe.run()

# Once it is finished, check out what data was generated:
myRecipe.Data.keys()

# Combined with the inputs specified in Recipe.Inputs, the data at every stage
# is preseverd.

# As a final note, all data objects aside from wavenums are SAIGs, or Solid-
# Angle Interpolation Grid. Accessing the per-channel output is accomplished by
# using the get(zenith, azimuth) method, in degrees.
print(myRecipe.Data.pixel.get(0,0))
