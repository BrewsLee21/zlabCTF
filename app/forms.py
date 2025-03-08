from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class Level1Form(FlaskForm):
    username = StringField("", validators=[DataRequired()], render_kw={"placeholder": "Uživatelské jméno"})
    password = PasswordField("", validators=[DataRequired()], render_kw={"placeholder": "Heslo"})
    submit = SubmitField("Přihlásit se", render_kw={"class": "submit-btn"})

class Level2Form(FlaskForm):
    path = StringField("", validators=[DataRequired()], render_kw={"placeholder": "Soubor"})
    submit = SubmitField("Odeslat", render_kw={"class": "submit-btn"})

class Level3Form(FlaskForm):
    comment_section = TextAreaField("", validators=[DataRequired()], render_kw={"placeholder": "Zde napiš komentář...", "class": "comment-section-text-field"})
    submit = SubmitField("Zveřejnit", validators=[DataRequired()], render_kw={"class": "submit-btn"})

class Level4Form(FlaskForm):
    pin = PasswordField("", validators=[DataRequired()], render_kw={"placeholder": "pin"})
    submit = SubmitField("Přihlásit se", validators=[DataRequired()], render_kw={"class": "submit-btn"})

class Level5Form(FlaskForm):
    pin = PasswordField("", validators=[DataRequired()], render_kw={"placeholder": "pin"})
    submit = SubmitField("Přihlásit se", validators=[DataRequired()], render_kw={"class": "submit-btn"})
    
class FlagCheckForm(FlaskForm):
    flag = StringField("", validators=[DataRequired()], render_kw={"placeholder": "zlabCTF{...}"})
    submit = SubmitField("Vyzkoušet", render_kw={"class": "submit-btn"})
