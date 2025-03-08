from app.config import Config as c
from app import app, db
from app.models import Level1Model, Level3Model, Level4Model, Level5Model

import os
from shutil import copy
from sys import stdout, argv
from passlib.hash import argon2
from random import randint

# ANSI escape codes for terminal colors
RED = "\033[91m"
YELLOW = "\033[33m"
RESET = "\033[0m"

def create_db():
    with app.app_context():
        db.create_all()
    print("Databáze vytvořena")

def create_secret_dir():
    """Creates the SECRET_DIR directory if it doesn't exist"""
    print(f"Vytvářím {c.SECRET_DIR} ...")
    try:
        os.makedirs(c.SECRET_DIR)
    except Exception as e:
        print(f"\t{RED}{e}{RESET}")
    else:
        print(f"\tSložka {c.SECRET_DIR} vytvořena")

def create_secret_flag_file():
    """Creates the level2/flag.txt file inside the SECRET_DIR directory"""
    file_path = os.path.join(c.SECRET_DIR, "level2/flag.txt")
    file_dir = os.path.dirname(file_path)
    print(f"Vytvářím {file_dir} ...")
    try:
        os.makedirs(file_dir)
    except Exception as e:
        print(f"\t{RED}{e}{RESET}")
    else:
        print(f"\tSložka{file_dir} vytvořena")

    print(f"Vytvářím soubor {file_path} ...")
    with open(file_path, 'w') as f:
        f.write(c.LEVELS[1]["level_flag"])
    print(f"\tSoubor {file_path} vytvořen")

def create_files_dir():
    """Creates the FILES_DIR directory if it doesn't exist"""
    print(f"Vytvářím {c.FILES_DIR} ...")
    try:
        os.makedirs(c.FILES_DIR)
    except Exception as e:
        print(f"\t{RED}{e}{RESET}")
    else:
        print(f"\tSložka {c.FILES_DIR} vytvořena")

def copy_files_to_files_dir():
    """Copies the files from app/res/level2 into FILES_DIR"""
    for file in os.listdir("app/res/level2"):
        try:
            copy(f"app/res/level2/{file}", c.FILES_DIR)
        except Exception as e:
            print(f"\t{RED}{e}{RESET}")
        else:
            print(f"\tSoubor {file} zkopírován")
    print(f"Soubory zkopírovány do FILES_DIR")

def populate_level1_table():
    """Removes all data from the level2_model table and populates it again"""
    print(f"Plním tabulku level2_model ze souboru {c.USER_DATA}")
    with open(c.USER_DATA, 'r') as f:
        with app.app_context():
            Level1Model.query.delete()
            for i, line in enumerate(f):
                phase = (i // 5) % 3
                if phase == 0:
                    stdout.write("\r.  ")
                elif phase == 1:
                    stdout.write("\r.. ")
                else:
                    stdout.write("\r...")
                stdout.flush()
                username, password = line.split()
                new_user = Level1Model(username=username, hashed_password=argon2.hash(password))
                db.session.add(new_user)
            db.session.commit()
    print("\nTabulka vyplněna")

def add_first_comment():
    """Removes all data from level3_model table and adds the first comment again"""
    print("Odstraňuji komentáře v Levelu 3")
    with app.app_context():
        Level3Model.query.delete()
        print("\tTabulka levelu 3 vymazána")
        first_comment = Level3Model(comment_content=c.FIRST_COMMENT)
        db.session.add(first_comment)
        db.session.commit()
    print("První komentář byl přidán")

def generate_pins():
    """Removes the pins from the level4 and level5 tables and replaces them with new pins"""
    with app.app_context():
        Level4Model.query.delete()
        Level5Model.query.delete()
        get_pin = lambda: ''.join([str(randint(0, 9)) for _ in range(5)]) 
        db.session.add(Level4Model(pin=get_pin()))
        db.session.add(Level5Model(pin=get_pin()))
        db.session.commit()
    print("Nové piny byly vloženy do tabulek")
    
def init(arg):
    """Initializes the application and gets everything ready"""
    if not arg:
        create_db() # Create the app database
        create_secret_dir() # Create the SECRET_DIR directory
        create_secret_flag_file() # Create the flag.txt file in the SECRET_DIR directory
        create_files_dir() # Create the FILES_DIR directory
        copy_files_to_files_dir() # Copies the files in app/res/level2 into FILES_DIR
        populate_level1_table() # Fill the level1 table with user data from USER_DATA
        add_first_comment() # Adds FIRST_COMMENT into the level3 table
        generate_pins() # Generates random pins and adds them into the level4 and level5 tables
    elif arg == "com":
        add_first_comment()
    elif arg == "pin":
        generate_pins()
    else:
        print(f"{arg}: neznámý argument")

if __name__ == "__main__":
    if len(argv) > 1:
        init(argv[1])
    else:
        init(None)
    print(f"{YELLOW}Některá nastavení se dají změnit v app/config.py{RESET}")
    print("Hotovo")
