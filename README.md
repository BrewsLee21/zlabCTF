# zlabCTF

## Dlouhodobá maturitní práce

### Ondřej Teplický - 2024/2025

---

> [!WARNING]
> ## POZOR
> Tohle je **zranitelná** webová aplikace, je určená pouze k výukovým účelům!

> [!NOTE]
> Spousta nastavení se dá změnit v app/config.py
 
## Instrukce k použití

Aby to všechno fungovalo, je potřeba udělat následující:

1. Naklonovat tenhle repozitář\
	```git clone https://github.com/BrewsLee21/zlabCTF.git```

	Nebo přes SSH\
	```git clone git@github.com:BrewsLee21/zlabCTF.git```

2. (Volitelné) Vytvořit nový .venv\
	```python -m venv <tvuj_venv>```\
	Většinout se jmenuje .venv\
	```python -m venv .venv```
	
	Potom je potřeba ho aktivovat\
	```source <tvuj_venv>/bin/activate```

	Deaktivovat ho lze takto\
	```deactivate```

3. Nainstalovat potřebné python moduly\
	```pip install -r requirements.txt```

> [!NOTE]
> Pokud používáš venv, tak bude potřeba všechno spouštět v něm, \
> protože obsahuje potřebné python moduly!

4. Inicializovat potřebnou konfiguraci (možná bude potřeba to spustit se sudo)\
	Pokud si vytvořil venv, tak bude potřeba spusit init.py skript takhle\
	```sudo <tvuj_venv>/bin/python init.py```

	Ten vytvoří složky ```~/secret``` a ```~/share/files```, které aplikace bude používat. \
	Tyto složky se dají změnit v ```app/config.py```, kde se jmenují SECRET_DIR a FILES_DIR.
	
	Inicializovat databázy\
	```flask db init```

5. V hlavním adresáři aplikace (zlabctf) spustit aplikaci\
	```flask run```

	Aplikaci můžeš spustit na konkrétní adrese nebo na konkrétním portu\
	```flask run --host=192.168.0.1 --port=8080```

> [!WARNING]
> ```flask run``` Je pouze vývojový server! \
> Na zkoušku je to v pohodě, ale v realitě je lepší použít jiný WSGI server. např.: waitress, gunicorn
	
