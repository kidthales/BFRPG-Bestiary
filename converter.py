#!/usr/bin/python3

import json, sys, glob

keymap = {
    "armor class": "armorclass",
    "hit dice": "hitdice",
    "no. appearing": "noappearing",
    "no. of attacks": "noattacks",
    "save as": "saveas",
    "treasure type": "treasure",
}

files = sorted(glob.glob("Monster-Data*.txt"))

outp = open("monsterdata.json", "w")
outpy = open("monsterdata.py", "w")

outp.write("[\n")
outpy.write("monsters = [\n")

# initialize the state machine
# states: 0 - name
#         1 - data fields
#         2 - description

state = 0
data = {}
num = 0

for fn in files:
    inp = open(fn, encoding = "utf-8-sig")

    for line in inp:
    
        num += 1
    
        if line.strip() == "@@" or line.strip() == "@STOP@":
            if "name" in data: # no easy way to be sure we have actual data, so this is a guess
                outp.write("%s,\n" % json.dumps(data, sort_keys=True, indent=4))
                outpy.write("%s,\n" % json.dumps(data, sort_keys=True, indent=4))
            if line.strip() == "@STOP@":
                break
            data = {}
            state = 0
    
        elif state == 0:
            if not line.strip():
                continue
            data["name"] = line.strip()
            state = 1
    
        elif state == 1:
            if not line.strip():
                data["description"] = []
                state = 2
                continue
            lst = tuple(map(lambda s: s.strip(), line.split(":", 1)))
            if len(lst) != 2:
                print("Error on line", num, "expecting data field for", data.get("name", "(name not found)"))
                sys.exit(1)
            key = keymap.get(lst[0].lower(), lst[0].lower())
            data[key] = lst[1]
    
        else:
            if line.strip():
                data["description"].append(line.strip())
    
    inp.close()
    
outp.write("]\n")
outpy.write("]\n")
outp.close()
    
    
# end of file.
