# BFRPG-Bestiary

Project to provide Basic Fantasy RPG monsters in a machine-consumable format.

Please note that the repository at https://github.com/Solomoriah/BFRPG-Bestiary
is the canonical, official version of this package.  Also note, this package
contains a mix of materials having different licenses.  The converter.py file
is distributed under a BSD 2 Clause license; all textual materials containing
game rules materials are under Creative Commons Attribution-ShareAlike 4.0.

At the moment, the original data is being organized in files named
**Monster-Data-\*.txt**; the format of those files is based roughly on data
copied and pasted from the official Core Rules ODT file.  The **converter.py**
script reads those files and converts the data into JSON format in the file
**monsterdata.json** and into Python format in the file **monsterdata.py**.
Pro tip: some JSON data can be directly processed by Python as it has analogous
data types with compatible literal notations; converter.py simply adds
**monster =** to the beginning of the JSON data to make the Python version.

The converter.py script expects the token @@ on a line by itself as a separator
between monster entries; @STOP@ on a line by itself signifies that the data
following that line should not be interpreted (skip this file and move on).
Each entry begins with the name (on one line) followed by the statblock
information, with a single blank line signifying the end of the statblock (and
thus the beginning of the descriptive text).

## Editing Strategy

Each specific statblock for any monster type should have its own entry;
however, in the Core Rules they are often grouped together.  Separating them
here will sometimes require splitting up or duplicating descriptive text.  As
much as possible, the descriptive text used here should be the same text from
the Core Rules, varying as little as needed for this digital representation.

