Python Silksong (and possibly Hollow Knight) Save Decrypter/Encrypter
---------------------------------------------------------------------

This is a decrypter/encrypter for the game
[Hollow Knight: Silksong](https://store.steampowered.com/app/1030300/Hollow_Knight_Silksong/),
by the lovely [Team Cherry](https://www.teamcherry.com.au/) folks.  The
savegame once decrypted is just a regular ol' [JSON](https://www.json.org/)
file which is pretty easily editable by hand or by more specialized tools.

It looks like this is actually probably identical to the original
[Hollow Knight](https://store.steampowered.com/app/367520/Hollow_Knight/)'s savefile
format, so it can probably be used for that game as well.  Go figure!

There are more fully-complete Silksong save editors out there, and plenty
of examples of decrypters/encrypters which are available right on the
web, without having to install local software.  Here's a few which exist
at time of writing (just grabbing the first few which pop up with a search):

- <https://martinshift.github.io/silksaver/> (<https://github.com/martinshift/silksaver/>)
- <https://www.silksongsaveeditor.org/>
- <https://www.nexusmods.com/hollowknightsilksong/mods/93>

This utility stops short of actual editing, though: it'll just take the savegame
and output JSON, or take JSON and output a savegame.  That is all!

This utility only supports PC savegames.  I have no intention of adding in support
for other platforms' savegames, though if you send in a reasonable PR I probably
wouldn't say no to merging it.

Installation
------------

This is a Python 3 script, and has only been tested on Python 3.13.  There's no
actual installation -- just check it out from git or download the `.py` and give
it a run, assuming you have Python installed.  This document assumes you know
how to run Python scripts, and are comfortable working in the commandline.  If not,
there are probably far easier ways for you to edit your saves (see some of the
links above).

The script does require [pycrypto](https://pypi.org/project/pycrypto/).  You
can install that with something like `pip install pycrypto`, `pip install -r
requirements.txt`, or it may already be installed, if you're on a Linux system
and using the system Python install to run.

Savegame Locations
------------------

As usual, PCGamingWiki is a good source of info for this.  ie:
<https://www.pcgamingwiki.com/wiki/Hollow_Knight:_Silksong#Save_game_data_location>

To copy the data from there, though (as of September 2025):

- **Windows**: `%USERPROFILE%\AppData\LocalLow\Team Cherry\Hollow Knight Silksong\`
- **Microsoft Store**: `%LOCALAPPDATA%\Packages\TeamCherry.HollowKnightSilksong_y4jvztpgccj42\SystemAppData\wgs`
- **macOS (OS X)**: `$HOME/Library/Application Support/unity.Team-Cherry.Silksong/default`
- **Linux**: `$XDG_CONFIG_HOME/unity3d/Team Cherry/Hollow Knight Silksong/`

The actual savegames are likely stored under another directory which will be your
Steam/Epic/whatever userid, and then Slot 1's savegame would be for instance `user1.dat`.

Usage
-----

Running the script with `-h` or `--help` will show you the syntax:

    usage: silksong-save-decrypt.py [-h] [-f] (-e | -d) input output

    Encrypt/Decrypt Silksong (and possibly Hollow Knight) Savegames (PC Only)

    positional arguments:
      input          Input filename
      output         Output filename

    options:
      -h, --help     show this help message and exit
      -f, --force    Force overwrite of output file, if it already exists
      -e, --encrypt  Encrypt savegame
      -d, --decrypt  Decrypt savegame (will write a JSON file)

A thrilling example of decrypting:

    $ ./silksong-save-decrypt.py -d user1.dat user1.json
    Wrote decrypted data to: user1.json

And an equally-thrilling example of re-encrypting:

    $ ./silksong-save-decrypt.py -e user1.json user1.dat

    WARNING: user1.dat already exists!
    Overwrite [y/N]? y
    Wrote encrypted data to: user1.dat

To overwrite without confirmation, specify `-f`/`--force`:

    $ ./silksong-save-decrypt.py -f -e user1.json user1.dat
    Wrote encrypted data to: user1.dat

CREDITS
-------

I gleaned the savefile format via [bloodorca](https://github.com/bloodorca)'s
[online Hollow Knight savefile editor](https://github.com/bloodorca/hollow),
specifically [functions.js](https://github.com/bloodorca/hollow/blob/489b2d313953a6b54e49b9b8633657c9baee7bd0/src/functions.js).
I actually didn't even notice at the time that it was technically a
Hollow Knight-specific tool; thought I had been looking at a Silksong tool.

LICENSE
-------

Python Silksong Save Decrypter/Encrypter code is licensed under the
[New/Modified (3-Clause) BSD License](https://opensource.org/licenses/BSD-3-Clause).
A copy is also found in [COPYING.txt](COPYING.txt).

Changelog
---------

**2025-09-22**:
 * Initial release

