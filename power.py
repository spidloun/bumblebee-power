
import bumblebee.engine
import bumblebee.output
import bumblebee.util
import os

SYS_PATH = "/sys/class/power_supply"
BAT_ALIASES = {"BAT0": "Ext", "BAT1": "Int"}
BAT_ICONS = [u"\uf244", u"\uf243", u"\uf242", u"\uf241", u"\uf240"]
PLUG_ICON = u"\uf1e6"

class Module(bumblebee.engine.Module):
	def __init__(self, engine, config):
		super(Module, self).__init__(engine, config, bumblebee.output.Widget(full_text=self.current_power))

	def current_power(self, widget):
		output = ""

		# Read batteries names and paths
		batteries = list(map(lambda x: [x, "%s/%s" % (SYS_PATH, x)], list(filter(lambda x: x.startswith("BAT"), os.listdir(SYS_PATH)))))

		for bat in batteries:
			with open("%s/capacity" % bat[1], "r") as f: capacity = int(f.read())
			with open("%s/status" % bat[1], "r") as f: status = f.read().strip()

			if capacity <= 10: 
				icon = BAT_ICONS[0]
			elif capacity > 10 and capacity <= 40:
				icon = BAT_ICONS[1]
			elif capacity > 40 and capacity <= 65:
				icon = BAT_ICONS[2]
			elif capacity > 65 and capacity < 90:
				icon = BAT_ICONS[3]
			else:
				icon = BAT_ICONS[4]

			bat_name = BAT_ALIASES[bat[0]] if bat[0] in BAT_ALIASES else bat[0]

			output += " %s %d%% (%s)%s |" % (icon, capacity, bat_name, " %s" % PLUG_ICON if status == "Charging" else "")
		return output


