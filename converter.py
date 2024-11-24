#!/usr/bin/python3

import json, sys

inp = open("Monster-Data.txt", encoding = "utf-8-sig")
outp = open("Core-Monsters.json", "w")

outp.write("[\n")

# initialize the state machine
# states: 0 - name
#         1 - data fields
#         2 - description

state = 0
data = {}
num = 0

for line in inp:

    num += 1

    if line.strip() == "@@" or line.strip() == "@STOP@":
        if "name" in data: # no easy way to be sure we have actual data, so this is a guess
            outp.write("%s,\n" % json.dumps(data, sort_keys=True, indent=4))
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
        data[lst[0].lower()] = lst[1]

    else:
        if line.strip():
            data["description"].append(line.strip())

outp.write("]\n")
outp.close()

inp.close()


# end of file.
