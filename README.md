# BFRPG-Bestiary

Project to provide Basic Fantasy RPG monsters in a machine-consumable format.

Please note that the repository at https://github.com/Solomoriah/BFRPG-Bestiary
is the canonical, official version of this package.

At the moment, the original data is being organized in files named
**Monster-Data-\*.txt**; the format of those files is based roughly on data
copied and pasted from the official Core Rules ODT file.  The **converter.py**
script reads those files and converts the data into JSON format in the file
**monster-data.json**.

The converter.py script expects the token @@ on a line by itself as a separator
between monster entries; @STOP@ on a line by itself signifies that the data
following that line should not be interpreted (skip this file and move on).
Each entry begins with the name (on one line) followed by the statblock
information, with a single blank line signifying the end of the statblock (and
thus the beginning of the descriptive text).
