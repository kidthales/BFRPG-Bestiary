#!/usr/bin/python3

"""
sqlize.py
Copyright (c) 2025, Tristan Bonsor

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

import json, sqlite3
import monsterdata

conn = sqlite3.connect('monsterdata.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS monsters (
    armorclass TEXT,
    attackbonus INTEGER,
    damage TEXT,
    description TEXT,
    hitdice TEXT,
    hitdiceroll TEXT,
    morale TEXT,
    movement TEXT,
    name TEXT,
    noappearing TEXT,
    noapproll TEXT,
    noapprolllair TEXT,
    noapprollwild TEXT,
    noattacks TEXT,
    saveas TEXT,
    specialbonus INTEGER,
    treasure TEXT,
    xp TEXT
)''')

cursor.execute('''DELETE FROM monsters''')

sql = '''INSERT INTO monsters(
    armorclass,
    attackbonus,
    damage,
    description,
    hitdice,
    hitdiceroll,
    morale,
    movement,
    name,
    noappearing,
    noapproll,
    noapprolllair,
    noapprollwild,
    noattacks,
    saveas,
    specialbonus,
    treasure,
    xp
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''

values = []

for monster in monsterdata.monsters:
    values.append((
        monster.get('armorclass'),
        monster.get('attackbonus'),
        monster.get('damage'),
        json.dumps(monster.get('description')),
        monster.get('hitdice'),
        json.dumps(monster.get('hitdiceroll')),
        monster.get('morale'),
        monster.get('movement'),
        monster.get('name'),
        monster.get('noappearing'),
        json.dumps(monster.get('noapproll')),
        json.dumps(monster.get('noapprolllair')),
        json.dumps(monster.get('noapprollwild')),
        monster.get('noattacks'),
        monster.get('saveas'),
        monster.get('specialbonus'),
        monster.get('treasure'),
        monster.get('xp')
    ))

cursor.executemany(sql, values)
conn.commit()
conn.close()
