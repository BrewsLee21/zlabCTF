from flask import render_template, request, flash, make_response
from app import app
import os
from passlib.hash import argon2
from random import randint

from app.forms import *
from app.models import *
from app.utils import *
from app.config import Config as c

cookie_received = False # used in level 3

@app.route("/test")
def test():
    return "Tohle je stránka pro testování.<br>Nic tady teď není"

@app.route("/")
@app.route("/index")
@app.route("/level")
def index():
    return render_template("index.html", levels=c.LEVELS)

@app.route("/level/1", methods=["get", "post"])
def level1():
    # ' OR 1=1 AND username LIKE "zlabCTF%" --

    #TODO: Napad, nehashovat hesla, uživatel musí získat heslo konkrétního uživatele a pod ním se přihlásit, aby našel flagu?
    level_form = Level1Form()
    flag_form = FlagCheckForm()

    if level_form.validate_on_submit():
        username = level_form.data["username"]
        password = level_form.data["password"]
        
        output = "id username password<br>"
        
        conn = db.engine.raw_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(f"SELECT * FROM level1_model WHERE username='{username}'")
        except Exception as e:
            print(e)
            return "Byla nalezena syntaktická chyba v SQL dotazu!"
            
        result = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        if len(result) == 1:
            if argon2.verify(password, result[0][2]):
                return render_template("profile.html", levels=c.LEVELS, username=result[0][1], messages=randint(0, 200))
            else:
                flash("Špatné uživatelské jméno nebo heslo.")
                return render_template("level_base.html", level_info=c.LEVELS[0], flag_form=flag_form, level_form=level_form, levels=c.LEVELS)
        elif not result:
            flash("Špatné uživatelské jméno nebo heslo.")
            return render_template("level_base.html", level_info=c.LEVELS[0], flag_form=flag_form, level_form=level_form, levels=c.LEVELS)
        for row in result:
            output += "{0} {1} {2}<br>".format(*row)
        return output
    if flag_form.validate_on_submit():
        if flag_form.data["flag"] == c.LEVELS[0]["level_flag"]:
            return "Skvělá práce!"
        else:
            return "Těsně vedle... Zkus to znovu."
            
    return render_template("level_base.html", level_info=c.LEVELS[0], flag_form=flag_form, level_form=level_form, levels=c.LEVELS)

@app.route("/level/2", methods=["get", "post"])
def level2():
    level_form = Level2Form()
    flag_form = FlagCheckForm()

    if  level_form.validate_on_submit():
        user_input = level_form.data["path"]
    else:
        user_input = None

    if flag_form.validate_on_submit():
        entered_flag = flag_form.data["flag"]
    else:
        entered_flag = None
        
    cmd = f"cat {c.FILES_DIR}/{user_input}"
    if user_input:
        output = f"Command executed: {cmd}<br><br>"
        # each element in the result_list list is a result of an executed command
        result_list = run_cmd(cmd)
        for cmd_name, cmd_result in result_list:
            cmd_result_type = type(cmd_result)
            
            if cmd_result_type == int: # if the result was an error (only errors are represented by integers)
                output += f"{cmd_name}: {error_codes[cmd_result]}<br>"
            elif cmd_result_type == list:
                for item in cmd_result:
                    output += item + " "
                output += "<br>"
            elif cmd_result_type == str:
                output += cmd_result + "<br>"
        return output

    if entered_flag:
        if entered_flag == c.LEVELS[1]["level_flag"]:
            return "Skvělá práce!"
        else:
            return "Nic moc... Zkus to znovu."
        
    return render_template(f"level_base.html", level_info=c.LEVELS[1], flag_form=FlagCheckForm(), level_form=level_form, levels=c.LEVELS)

@app.route("/level/3", methods=["get", "post"])
def level3():
    # <script>fetch("/level/3/cookiejar?susenka=" + document.cookie)</script>
    # https://stackoverflow.com/questions/252665/i-need-to-get-all-the-cookies-from-the-browser
    # https://www.geeksforgeeks.org/javascript-fetch-method/
    
    level_form = Level3Form()
    flag_form = FlagCheckForm()
    
    try:
        comments = Level3Model.query.all()
    except Exception as e:
        return str(e)

    resp = make_response(render_template("level_base.html", level_info=c.LEVELS[2], flag_form=flag_form, level_form=level_form, levels=c.LEVELS, comments=comments))
    # Remove all current cookies by setting their expire time to 0
    for cookie in request.cookies:
        if cookie == "session":
            continue
        resp.set_cookie(cookie, "", expires=0)
    print("Setting secret cookie!")
    try:
        db_cookie_key, db_cookie_value = CookieModel.query.with_entities(CookieModel.cookie_key, CookieModel.cookie_value).first()
    except Exception as e:
        return str(e)
    resp.set_cookie(db_cookie_key, db_cookie_value)
    for i in range(c.EXTRA_COOKIES):
        extra_cookie_key, extra_cookie_value = get_new_cookie()
        resp.set_cookie(extra_cookie_key, extra_cookie_value)
    
    if level_form.validate_on_submit():
        comment_content = Level3Model(level_form.data["comment_section"])
        db.session.add(comment_content)
        db.session.commit()
        try:
            comments = Level3Model.query.all()
        except Exception as e:
            return str(e)
        return render_template("level_base.html", level_info=c.LEVELS[2], flag_form=flag_form, level_form=level_form, levels=c.LEVELS, comments=comments)

    if flag_form.validate_on_submit():
        clear_comments()
        if flag_form.data["flag"] == c.LEVELS[2]["level_flag"]:
            return "Skvělá práce!"
        else:
            return "Oplatky se nepečou... Zkus to znovu."

    return resp

@app.route("/level/3/cookiejar", methods=["get"])
def cookiejar():
    global cookie_received
    correct_cookie_key, correct_cookie_value = CookieModel.query.with_entities(CookieModel.cookie_key, CookieModel.cookie_value).first()
    

    if cookie_received:
        print("Setting to False ")
        cookie_received = False
        return f"To si pochutnám!\nTady máš flag: {c.LEVELS[2]['level_flag']}"

    for cookies in request.args.items():
        if type(cookies) != list:
            cookies = [cookies]
        for cookie_key, cookie_value in cookies:
            if cookie_key == correct_cookie_key and cookie_value == correct_secret_cookie_value:
                print("Setting to True")
                cookie_received = True
                return "OK"
            # if the cookie_value is a dictionary
            if '=' in cookie_value:
                print("Checking dictionary")
                # if there are several key/value pairs in the dict
                if ';' in cookie_value:
                    dict_values = list(map(lambda x: x.strip(), cookie_value.split(';')))
                    for key_val in dict_values:
                        key, val = key_val.split('=')
                        if key == correct_cookie_key and val == correct_cookie_value:
                            print("Setting to True")
                            cookie_received = True
                            return "OK"
                # else if there is just one key/value pair in the dict
                else:
                    key, val = cookie_value.split('=')
                    if key == correct_cookie_key and val == correct_cookie_value:
                        print("Setting to True")
                        cookie_received = True
                        return "OK"
                        
    return "Co tu chceš? Tady není nic k vidění!"

@app.route("/level/4", methods=["get", "post"])
def level4():
    level_form = Level4Form()
    flag_form = FlagCheckForm()

    if level_form.validate_on_submit():
        correct_pin = Level4Model.query.with_entities(Level4Model.pin).first()[0]
        print(f"Level 4 correct pin: {correct_pin}")
        entered_pin = level_form.data["pin"]
        if entered_pin == correct_pin:
            return f"Vítej, uživateli Admin!\nTady je Váš flag: {c.LEVELS[3]['level_flag']}", 200
        else:
            return "Špatný pin!", 403
    return render_template("level_base.html", level_info=c.LEVELS[3], flag_form=flag_form, level_form=level_form, levels=c.LEVELS)
    
@app.route("/level/5", methods=["get", "post"])
def level5():
    level_form = Level5Form()
    flag_form = FlagCheckForm()

    current_attempts = int(request.cookies.get("login_attempts", 0))
    resp = make_response(render_template("level_base.html", level_info=c.LEVELS[4], flag_form=flag_form, level_form=level_form, levels=c.LEVELS))

    if "login_attempts" not in request.cookies:
        resp.set_cookie("login_attempts", str(current_attempts), max_age=300)

    if level_form.validate_on_submit():
        correct_pin = Level5Model.query.with_entities(Level5Model.pin).first()[0]
        entered_pin = level_form.data["pin"]
        if entered_pin == correct_pin:
            resp.set_cookie("login_attempts", 0, expires=0)
            return f"Vítej, uživateli Admin!\nTady je Váš flag: {c.LEVLES[4]['level_flag']}", 200
        else:
            resp.set_cookie("login_attempts", str(current_attempts + 1), max_age=300)
            return "Špatný pin!", 403
            
    return resp

@app.route("/level/<num>")
def level_not_found(num):
    return f"Level '{num}' nebyl nalezen!"
