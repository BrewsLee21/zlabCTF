import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "a-very-secret-key"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Used in Level 1
    USER_DATA = os.path.join(BASE_DIR, "static/res/level1/user_data.txt") # Used in Level 1 (SQL Injection)
    
    # Used in Level 2
    LEVEL2_FILES_BACKUP_DIR = os.path.join(BASE_DIR, "static/res/level2") # files for level2 that need to be copied to ~/share/files
    FILES_DIR = os.path.expanduser("~/share/files") # Used in Level 2 (Command Injection)
    SECRET_DIR = os.path.expanduser("~/secret") # directory to store level flags for users to find
    CMD_BLACKLIST = ["rm"] # a list of illegal commands to make sure Level 2 is not as dangerous
        
    # Used in Level 3
    FIRST_COMMENT = "<span style='color: red;'>Do cookies se prý ukládají citlivá data.</span><br>Dám flag <strong>komukoliv</strong>, kdo pošle GET request se všemi cookies na url <span class='nosplit'>'/level/3/cookiejar'</span><br>&bull; Zloděj sušenek"
    SECRET_COOKIE_KEY_LEN = 8
    SECRET_COOKIE_VALUE_LEN = 32 # the length of the value of the secret cookies
    EXTRA_COOKIES = 64 # amount of extra cookies generated on Level3

    # displayed levels
    LEVELS = [
        { # Level 1
            "level_number": 1,
            "level_title": "SQL injection",
            "level_description": "Tohle je zranitelný přihlašovací formulář.<br>" \
                                "Jeden z uživatelů v databázi má zváštní uživatelské jméno.<br>Dokážeš ho najít?",
            "level_url": "/level/1",
            "level_flag": "zlabCTF{sql_1nj3ct10n_bllp9khr}"
        },
        { # Level 2
            "level_number": 2,
            "level_title": "Command injection",
            "level_description": "Na serverovém úložišti <span class='code nosplit'>/share/files</span> jsou uloženy soubory uživatelů.<br>" \
                                "Stačí zadat název souboru a vypíše se jeho obsah!<br>" \
                                "Na serveru je ale ještě adresář <span class='code nosplit'>/secret/level2</span>, který obsahuje zajímavá data.",
            "level_url": "/level/2",
            "level_flag": "zlabCTF{c0d3_1nj3ct10n_z829nzh6}"
        },
        { # Level 3
            "level_number": 3,
            "level_title": "Stored XSS",
            "level_description": "Vítej v naší komentářové sekci!<br>" \
                                "Napiš sem něco hezkého.<br>",
            "level_url": "/level/3",
            "level_flag": "zlabCTF{x55_4tt4ck_kjh4sn0p}"
        }
    ]
