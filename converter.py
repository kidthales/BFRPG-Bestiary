#!/usr/bin/python3

"""
converter.py
Copyright (c) 2024, Chris Gonnerman

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

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
    
    # behave as if closing a file ends a monster, since it should
    if "name" in data: # no easy way to be sure we have actual data, so this is a guess
        outp.write("%s,\n" % json.dumps(data, sort_keys=True, indent=4))
        outpy.write("%s,\n" % json.dumps(data, sort_keys=True, indent=4))
    data = {}
    state = 0
    
outp.write("]\n")
outpy.write("]\n")
outp.close()
    
    
# end of file.
