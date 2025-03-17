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
    return "<p>Toto je testovací stránka</p>"

@app.route("/")
@app.route("/index")
@app.route("/level")
def index():
    return render_template("index.html", levels=c.LEVELS)

@app.route("/level/1", methods=["get", "post"])
def level1():
    level_form = Level1Form()
    flag_form = FlagCheckForm()

    if level_form.validate_on_submit():
        username = level_form.data["username"]
        password = level_form.data["password"]
        
        output = "id username password<br>"
        
        conn = db.engine.raw_connection()
        cursor = conn.cursor()
        query = f"SELECT * FROM level1_model WHERE username LIKE 'zlabCTF%'"
        try:
            cursor.execute(query)
        except Exception as e:
            print(e)
            return "Byla nalezena syntaktická chyba v SQL dotazu!"
            
        result = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        
        if not result:
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
        
    if user_input:
        cmd = f"cat {c.FILES_DIR}/{user_input}"
        output = f"Command executed: {cmd}<br><br>"

        output += run_cmd_unsafe(cmd)
        return output

    if entered_flag:
        if entered_flag == c.LEVELS[1]["level_flag"]:
            return "Skvělá práce!"
        else:
            return "Nic moc... Zkus to znovu."
        
    return render_template(f"level_base.html", level_info=c.LEVELS[1], flag_form=FlagCheckForm(), level_form=level_form, levels=c.LEVELS)

@app.route("/level/3", methods=["get", "post"])
def level3():
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

@app.route("/level/<num>")
def level_not_found(num):
    return f"Level '{num}' nebyl nalezen!"
