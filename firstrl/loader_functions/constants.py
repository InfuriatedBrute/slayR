from os.path import curdir

from loader_functions.json_loaders import load_json

constants_dir = curdir + "\\constants\\"
config = load_json(constants_dir + "config.json")
colors = load_json(constants_dir + "colors.json")
items = load_json(constants_dir + "items.json")
enchantments = load_json(constants_dir + "enchantments.json")
item_prefixes = load_json(constants_dir + "item_prefixes.json")