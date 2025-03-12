import re
import shlex
import os
from random import randrange, choice
from time import sleep
from string import ascii_letters

from app import app, db
from app.models import *
from app.config import Config as c

# ================= General =================

def is_from_allowed_dirs(path: str, allowed_dirs: list) -> bool | None:
    """Check if a specified path is in one of the allowed directories. Returns True if it is, False if it isn't and None if the path doesn't exist"""

    if type(allowed_dirs) != list:
        allowed_dirs = [allowed_dirs]
    
    # Get full absolute path
    full_path = os.path.realpath(os.path.expanduser(path))
    # Check if path exists
    if not os.path.exists(full_path):
        return None

    # Check if path is from allowed directories
    # If the path is from one, it returns True, otherwise False is returned after the loop finishes
    for allowed_dir in allowed_dirs:

        allowed_dir = os.path.realpath(os.path.expanduser(allowed_dir))
        
        # if path is from the allowed directory
        if not os.path.relpath(full_path, allowed_dir).startswith(".."):
            return True
    return False

# ===================================================
# ================= Level 1 =================



# ===================================================
# ================= Level 2 =================

allowed_dirs = [os.path.join(c.SECRET_DIR, "level2"), c.FILES_DIR]
error_codes = {
    -1: "Příliš mnoho argumentů!", # Too many arguments
    -2: "Používání přepínačů je zakázáno!", # An option was used, which is prohibited
    -3: "Takový adresář nebo soubor neexistuje!", # No such directory or file found
    -4: "Něco se nepovedlo!", # Something went wrong (Unknown error)
    -5: "Příkaz je buď zakázaný, nebo neexistuje!", # Command is either prohibited or doesn't exist
    -6: "Nebyl specifikován soubor nebo adresář!", # No file specified
    -7: "Tam jít nesmíš!", # You can't go there!
    -8: "Nebyl zadán soubor!" # Given path is a directory, NOT a file
}
    
    
def ls(*args) -> int | list:
    """Implements the ls shell command. Returns a list of directory contents on success and an error code on failure."""

    if len(args) > 2:
        return -1
    if len(args) == 0:
        return ls(str(pwd()))
    if args[0].startswith('-'):
        return -2
    path = os.path.expanduser(args[0])

    path_is_allowed = is_from_allowed_dirs(path, allowed_dirs)

    if path_is_allowed is None:
        return -3
    if path_is_allowed == False:
        return -7
    try:
        ls_output = os.listdir(path)
    except NotADirectoryError:
        return os.path.basename(path)
    except Exception as e:
        print(f"EXCEPTION: {e}")
        return -4

    return ls_output
    
def cat(*args) -> int | str:
    if len(args) > 1:
        return -1
    if len(args) == 0:
        return -6

    path = os.path.expanduser(args[0])
    path_is_allowed = is_from_allowed_dirs(path, allowed_dirs)
    if path_is_allowed is None: # path dosen't exist
        return -3
    if path_is_allowed == False: # path is not allowed
        return -7
    try:
        f = open(path, 'r')
    except FileNotFoundError:
        return -3
    except IsADirectoryError:
        return -8
    except Exception as e:
        print(f"EXCEPTION: {e}")
        f.close()
        return -4

    file_contents = f.read()
    f.close()
    return file_contents

def pwd(*args) -> str:
    return os.getcwd()

def run_cmd(inp: str):
    """Used in Level 2.
        Runs the user's input, tries to act like a shell.
        Returns a list of tuples where each tuple is (command_name, command_result)"""
        
    allowed_cmds = {
        "ls": ls,
        "cat": cat,
        "pwd": pwd
    }
    results = []
    
    commands = re.split(";|&&|\|\|", inp)
    for command in commands:
        parts = shlex.split(command)
        cmd_name = parts[0] if parts else ""
        args = parts[1:] if len(parts) > 1 else ""
        
        print(f"cmd: '{cmd_name}' - args: '{str(args)}'")

        if cmd_name in allowed_cmds:
            results.append((cmd_name, allowed_cmds[cmd_name](*args)))
        elif not cmd_name:
            continue
        else:
            results.append((cmd_name, -5))
    return results

# ===================================================
# ================= Level 3 =================

def clear_comments():
    """Clears the comment section on Level 3 and only puts back the first one"""
    # delete all comments
    Level3Model.query.delete()
    # put back the first comment
    db.session.add(Level3Model(comment_content=c.FIRST_COMMENT))
    db.session.commit()

def get_new_cookie() -> str:
    chars = ascii_letters + "0123456789"
    new_key = ''.join([choice(chars) for _ in range(c.SECRET_COOKIE_KEY_LEN)])
    new_value = ''.join([choice(chars) for _ in range(c.SECRET_COOKIE_VALUE_LEN)])

    return (new_key, new_value)
    
# ===================================================
# ================= Level 4 =================

# ===================================================
# ================= Level 5 =================

def generate_new_pin() -> str:
    """generates a pin number that is pin_length digits long"""
    pin_length = 5
    new_pin = ""
    for _ in range(pin_length):
        new_pin += str(randrange(0, 9))
    return str(new_pin.zfill(pin_length))

def change_pin(level: int):
    """Thread function that changes a pin number in the level5_model table in the databse once every interval"""
    if level == 4:
        with app.app_context():
            Level4Model.query.delete()
            new_pin = Level4Model(pin=generate_new_pin())
            db.session.add(new_pin)
            db.session.commit()
    elif level == 5:
        with app.app_context():
            Level5Model.query.delete()
            new_pin = Level5Model(pin=generate_new_pin())
            db.session.add(new_pin)
            db.session.commit()

# ===================================================
