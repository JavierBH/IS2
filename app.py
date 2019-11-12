import sqlite3
from flask import Flask, redirect, url_for, render_template, request, flash
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import mimetypes

MY_ADDRESS = "norao97@gmail.com"
PASSWORD = "ratillas"
app = Flask(__name__)
app.secret_key = 'random string'
    
@app.route("/")
def home():
    conectar_db()
    return render_template("home.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST': 
        usuario = request.form.get('usuario')
        contrasena = request.form.get('contrasena')
        repite_contrasena = request.form.get('repite_contrasena')
        email = request.form.get('email')
        nombre = request.form.get('nombre')
        nacionalidad = request.form.get('nacionalidad')
        intro = request.form.get('introduccion')
        fecha = request.form['fecha']
        foto = request.form.get('foto')

        if (usuario == "") or (contrasena == "") or (repite_contrasena == "") or (email == ""):
            return "Campo obligatorio no ha sido completado"
        if (contrasena != repite_contrasena):
            return "Contraseñas no coinciden"
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO Users ('usuario','password','email','name',
        'fecha','foto','nacionalidad','introduccion') VALUES (?,?,?,?,?,?,?,?)'''
        ,(usuario,contrasena,email,nombre,fecha,foto,nacionalidad,intro))
        conn.commit()
        cursor.close()
        conn.close()
        return "<h1>Registro Completo</h1>"
    return render_template("register.html")

@app.route("/login", methods = ["GET","POST"])
def login():
    if request.method == "POST":
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("SELECT password FROM Users WHERE usuario = ? AND password=?",(request.form["username"],request.form["password"]))
        rows = cursor.fetchone()
        if rows is not None:
            flash("You are logged. Welcome !!!!","success")
            return redirect(url_for("home"))
        else:
            flash("Error in login. Check credentials","error")
            #return redirect(url_for("login.html"))
    return render_template("login.html")

@app.route("/recuperar", methods = ["GET","POST"])
def recuperar():
    if request.method == "POST":
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("SELECT usuario FROM Users WHERE email = ?",(request.form["correo"],))
        rows = cursor.fetchone()
        if rows is not None:
            if enviar_correo(request.form["correo"]) == 0:
                flash("E-mail sent. Look at your mail","success")
                return redirect(url_for("new_pass"))
        else:
            flash("Email not valid. Try again","error")
    return render_template("recuperar.html")

@app.route("/recuperar/password", methods = ["GET","POST"])
def new_pass():
    if request.method == "POST":
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("SELECT usuario FROM Users WHERE usuario = ?",(request.form["username"],))
        rows = cursor.fetchone()
        if rows is not None:
            print(request.form["password"])
            print(request.form["username"])
            cursor.execute("UPDATE Users SET password=? WHERE usuario=?",(request.form["password"],request.form["username"]))
            conexion.commit()
            flash("Password change with success","success")
            return redirect(url_for("login"))
        else:
            flash("Username not valid. Try again","error")
    return render_template("new_pass.html")

def enviar_correo(correo):
    try:
        destino = correo
        #message = "Hello, world!"
        message =  "http://127.0.0.1:5000/recuperar/password"
        
        s = smtplib.SMTP("smtp.gmail.com",587)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(MY_ADDRESS,PASSWORD)

        mime_message = MIMEText(message, "plain")
        mime_message["From"] = MY_ADDRESS
        mime_message["To"] = destino
        mime_message["Subject"] = "Correo de prueba"
        #mime_message.attach(MIMEText(message, 'plain'))
        
        s.send_message(mime_message)
        del mime_message
        s.quit()
    except Exception:
        return -1
    return 0

    #return render_template("recuperar.html")


def conectar_db():
    conn = sqlite3.connect('datos.db')
    cursor = conn.cursor()
    sqlite_create_table_query = '''CREATE TABLE IF NOT EXISTS Users (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                usuario TEXT NOT NULL,
                                password TEXT NOT NULL UNIQUE,
                                email TEXT NOT NULL UNIQUE,
                                name TEXT,
                                fecha DATE,
                                foto BLOB,
                                nacionalidad TEXT,
                                introduccion TEXT);'''
    cursor.execute(sqlite_create_table_query)
    conn.commit()
    cursor.close()
    return conn

if __name__== "__main__":
    app.run(debug=True)