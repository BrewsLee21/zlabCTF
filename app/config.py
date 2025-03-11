import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "a-very-secret-key"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_DIR ="/secret" # directory to store level flags for users to find
    USER_DATA = os.path.join(BASE_DIR, "res/level1/user_data.txt") # Used in Level 1 (SQL Injection)
    FILES_DIR = "/share/files" # Used in Level 2 (Command Injection)
    FIRST_COMMENT = "<span style='color: red;'>Do cookies se prý ukládají citlivá data.</span><br>Dám flag <strong>komukoliv</strong>, kdo pošle GET request se všemi cookies na url <span class='nosplit'>'/level/3/cookiejar'</span><br>&bull; Zloděj sušenek" # Used in Level 3 (Stored XSS)

    LEVELS = [
        { # Level 1
            "level_number": 1,
            "level_title": "SQL injection",
            "level_description": "Tohle je zranitelný přihlašovací formulář.<br>" \
                                "Jeden z uživatelův databázi má zváštní uživatelské jméno.<br>Dokážeš ho najít?",
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
            "level_flag": "zlabCTF{xss_4tt4ck_kjh4sn0p}"
        },
        { # Level 4
            "level_number": 4,
            "level_title": "Brute Force Password Cracking 1",
            "level_description": "Dobrý den, uživateli Admin.<br>" \
                                "Přihlaste se, prosím, pomocí svého hesla, které je maximálně 5 znaků dlouhé a obsahuje pouze malá písmena.",
            "level_url": "/level/4",
            "level_flag": "zlabCTF{brut3_f0rc3_4tt4ck}"
        },
        { # Level 5
            "level_number": 5,
            "level_title": "Brute Force Password Cracking 2",
            "level_description": "Dobrý den, uživateli Admin.<br>" \
                                "Přihlaste se, prosím, pomocí svého hesla, které je maximálně 5 znaků dlouhé a obsahuje pouze čísla.<br>" \
                                "Jelikož byl náš bezpečnostní systém prolomen, rozhodli jsme se limitovat množství povolených pokusů.",
            "level_url": "/level/5",
            "level_flag": "zlabCTF{l0ck0ut_byp455}"
        }
    ]
    
