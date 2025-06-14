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

columns = [
    ('armorclass', 'TEXT'),
    ('attackbonus', 'INTEGER'),
    ('damage', 'TEXT'),
    ('description', 'JSON'),
    ('hitdice', 'TEXT'),
    ('hitdiceroll', 'JSON'),
    ('morale', 'TEXT'),
    ('movement', 'TEXT'),
    ('name', 'TEXT'),
    ('noappearing', 'TEXT'),
    ('noapproll', 'JSON'),
    ('noapprolllair', 'JSON'),
    ('noapprollwild', 'JSON'),
    ('noattacks', 'TEXT'),
    ('saveas', 'TEXT'),
    ('specialbonus', 'INTEGER'),
    ('treasure', 'TEXT'),
    ('xp', 'TEXT')
]

def generatemonsterstable():
    sqlcreate = 'CREATE TABLE monsters ('
    sqlinsert = 'INSERT INTO monsters ('

    for column in columns:
        sqlcreate += column[0]
        sqlinsert += column[0]

        if column[1] == 'JSON':
            sqlcreate += ' TEXT'
        else:
            sqlcreate += ' ' + column[1]

        if column != columns[-1]:
            sqlcreate += ', '
            sqlinsert += ', '

    sqlcreate += ')'
    sqlinsert += ') VALUES (' + ('?, ' * (len(columns) - 1)) + ' ?)'

    values = []
    for monster in monsterdata.monsters:
        row = ()
        for column in columns:
            if column[1] == 'JSON':
                row += (json.dumps(monster.get(column[0])),)
            else:
                row += (monster.get(column[0]),)
        values.append(row)

    cursor.execute('DROP TABLE IF EXISTS monsters')
    cursor.execute(sqlcreate)
    cursor.executemany(sqlinsert, values)

def generatelicensetable():
    cursor.execute('DROP TABLE IF EXISTS license')
    cursor.execute('CREATE TABLE license (text TEXT)')

    text = ''
    found = False
    with open('LICENSE', 'r') as file:
        for line in file:
            if found and line.strip() != '':
                text += line
            elif line.strip() == 'CC BY-SA License':
                found = True
                text += line
    file.close()

    cursor.execute('INSERT INTO license (text) VALUES (?)', (text,))

conn = sqlite3.connect('monsterdata.sqlite')
cursor = conn.cursor()
generatemonsterstable()
generatelicensetable()
conn.commit()
conn.close()
