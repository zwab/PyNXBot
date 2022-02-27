# Go to root of PyNXBot
import sys
import json
sys.path.append('../')

from structure import PK8
from nxbot import BDSPBot
from lookups import Util

config = json.load(open("../config.json"))
b = BDSPBot(config["IP"])

# Dump Party Slot 1
pk8 = PK8(b.readParty(1))
if pk8.isValid() and pk8.ec() != 0: # Check pokemon is real
    print(f"{pk8.species()}_{Util.STRINGS.species[pk8.species()]}_pid-{pk8.pid():X}_ec-{pk8.ec():X}")
else:
    print("Invalid Pokemon")

print()
b.close()
