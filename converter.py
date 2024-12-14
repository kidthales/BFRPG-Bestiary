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

import json, sys, glob, re

xpnum = re.compile("^[0-9,][0-9,]*$")
plusminus = re.compile("([+-])")
dieroll = re.compile("([0-9][0-9]*)d([0-9][0-9]*)")
dieparse = re.compile("([0-9][0-9]*)d([0-9][0-9]*)([+-][0-9][0-9]*)?")


def xpconvert(s):
    if not xpnum.search(s):
        return s
    return "".join(s.split(","))


def safeint(s):
    try:
        return int(s)
    except:
        return 0


def parsedice(s):
    # parse the first word of given string
    # returns parameter list and remainder of string
    lst = s.strip().split(" ", 1)
    first = s
    remain = ""
    if len(lst) > 1:
        remain = lst[1].strip()
        first = lst[0]
    # a literal number is a special case here
    try:
        num = int(first)
        return ([ 0, 0, num ], remain)
    except:
        pass
    # so is it a die roll?
    mo = dieparse.match(first)
    if mo:
        return ([ safeint(mo.group(1)), safeint(mo.group(2)), safeint(mo.group(3)) ], remain)
    return (None, s)


def parsenoapp(data):

    noapp = data.get("noappearing", "0").lower().split()
    if not noapp:
        return

    roll, rem = parsedice(noapp[0])
    if roll:
        data["noapproll"] = roll
        noapp.pop(0) # extract and remove the word

    # parse one word at a time.
    while noapp:
        word = noapp.pop(0)
        if word in ("wild", "lair"):
            roll, rem = parsedice(noapp.pop(0))
            if roll:
                data["noapproll%s" % word] = roll


def parsehitdice(data):

    hd = data.get("hitdice", "0")

    # parse hit dice

    # first, count the special ability bonuses
    lst = hd.split("*")
    data["specialbonus"] = len(lst) - 1
    hd = "".join(lst).strip().lower()

    # the first number in the string is the "base" hit dice

    # die roll is a special case, and we'll need the match object
    drmatch = dieroll.match(hd)
    if drmatch:
        data["hitdiceroll"] = [ int(drmatch.group(1)), int(drmatch.group(2)), 0 ]
        data["attackbonus"] = data["hitdiceroll"][0]
    elif hd.endswith(" hp") or hd.endswith(" hit point") or hd.endswith(" hit points"):
        lst = hd.split()
        data["hitdiceroll"] = [ 0, 0, int(lst[0]) ]
        data["attackbonus"] = 0
    elif hd.startswith("1/2"):
        # 1/2 is a special case
        data["hitdiceroll"] = [ 1, 4, 0 ]
        data["attackbonus"] = 0
    else:
        if hd.endswith(" (variable)"):
            hd = hd[:-11]
        lst = hd.split()
        if len(lst) > 1 and lst[1].startswith("(+"):
            # this is probably an attack bonus
            data["attackbonus"] = int(lst[1][2:-1])
            hd = lst[0]
        lst = plusminus.split(hd)
        bonus = 0
        if len(lst) == 3:
            hd = lst[0]
            bonus = int(lst[2])
            if lst[1] == "-":
                bonus = bonus * -1
        data["hitdiceroll"] = [ int(hd), 8, bonus ]
        if "attackbonus" not in data:
            data["attackbonus"] = int(hd)


def export(data, outs):
    if "name" not in data: # no easy way to be sure we have actual data, so this is a guess
        return
    if "hitdice" in data:
        parsehitdice(data)
    if "noappearing" in data:
        parsenoapp(data)
    for out in outs:
        out.write("%s,\n" % json.dumps(data, sort_keys=True, indent=4))


keymap = {
    "armor class": "armorclass",
    "hit dice": "hitdice",
    "no. appearing": "noappearing",
    "no. of attacks": "noattacks",
    "save as": "saveas",
    "treasure type": "treasure",
}

converters = {
    "xp": xpconvert,
}

files = sorted(glob.glob("Monster-Data*.txt"))

outjs = open("monsterdata.js", "w")
outjson = open("monsterdata.json", "w")
outpy = open("monsterdata.py", "w")

outjs.write("var monsters = [\n")
outjson.write("[\n")
outpy.write("monsters = [\n")

# initialize the state machine
# states: 0 - name
#         1 - data fields
#         2 - description
#         3 - dragon table

state = 0
data = {}

for fn in files:
    inp = open(fn, encoding = "utf-8-sig")
    num = 0

    for line in inp:
    
        num += 1
    
        if line.strip() == "@@" or line.strip() == "@STOP@":
            export(data, (outjs, outjson, outpy))
            data = {}
            state = 0
            if line.strip() == "@STOP@":
                break
    
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
                print("Error in", fn, "on line", num, "expecting data field for", data.get("name", "(name not found)"))
                sys.exit(1)
            key = keymap.get(lst[0].lower(), lst[0].lower())
            dta = lst[1]
            if key in converters:
                dta = converters[key](dta)
            data[key] = dta
    
        elif state == 2:
            if line.strip().startswith("@DRAGON@"):
                state = 3
                data["dragontable"] = [ " ".join(line.strip().split()[1:]) ]
                dragoncol = 0
                continue
            if line.strip():
                data["description"].append(line.strip())

        elif state == 3:
            line = line.strip()
            if not line:
                continue
            if dragoncol == 0:
                data["dragontable"].append([ line ])
                row = data["dragontable"][-1]
                if line == "Breath Weapon":
                    dragoncol = 7
                elif line == "Spells by Level":
                    dragoncol = 0
                else:
                    dragoncol = 1
            else:
                row = data["dragontable"][-1]
                row.append(line)
                dragoncol += 1
                if dragoncol > 7:
                    dragoncol = 0

    inp.close()
    
    # behave as if closing a file ends a monster, since it should
    export(data, (outjs, outjson, outpy))
    data = {}
    state = 0
 
outjs.write("]\n")
outjson.write("]\n")
outpy.write("]\n")

outjs.close()
outjson.close()
outpy.close()
    
    
# end of file.
