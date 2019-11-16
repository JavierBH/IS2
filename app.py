import sqlite3
from flask import Flask, redirect, url_for, render_template, request, flash, session, escape
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import mimetypes
import os, re
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from os.path import join, dirname, realpath


MY_ADDRESS = "proyectois2upm@gmail.com"
PASSWORD = "softwareupm"
UPLOAD_FOLDER = join(dirname(realpath(__file__)), '/home/xiaojing/Documentos/IS2/img')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__)
app.secret_key = 'random string'
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
format_email = ["gmail","yahoo"]
format_end = ["com","es"]


@app.route("/home")
def home():
    return render_template("index.html")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convertToBinaryData(filename):
    #Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

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
        foto = None
        
        """#EXTRAE FOTO
        if 'file' not in request.files:
            file = None
            return "file = None"
        file = request.files['file']
        foto = None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #Hay que poner el directorio completo!
            filename = "/home/xiaojing/Documentos/IS2/img/" + filename
            foto = convertToBinaryData(filename)"""
        #COMPROBACION DE CAMPOS OBLIGATORIOS
        if (usuario == "") or (contrasena == "") or (repite_contrasena == "") or (email == ""):
            return "Campo incompleto"
        #COMPROBACION DE LONGITUD DE USUARIO
        if len(usuario) < 6:
            flash("Introduzca un usuario de minimo 6 caracteres","error")
            return render_template("register.html")
        #COMPROBACION DE LONGITUD DE PASSWORD
        if len(contrasena) < 6:
            flash("Introduzca una contraseña de minimo 6 caracteres","error")
            return render_template("register.html")
        #COMPROBACION DE FORMATO CORREO
        expresion = "\w+(@)([a-z]+).([a-z]+)"
        tupla = re.match(expresion,email)
        if tupla.group(1) != "@" or tupla.group(2) not in format_email or tupla.group(3) not in format_end:
            flash("Email not valid","error")
            return render_template("register.html")
        #COMPROBACION DE CONTRASEÑA
        if (contrasena != repite_contrasena):
            flash("Password incorrect","error")
            return render_template("register.html")
        conn = conectar_db()
        cursor = conn.cursor()
        #COMPROBACION DE USUARIO UNICO
        cursor.execute("SELECT * FROM Users WHERE usuario = ?",(usuario, ))
        rows = cursor.fetchone()
        if rows is not None:
            flash("Usuario existed !","error")
            return render_template("register.html")
        #COMPROBACION DE EMAIL UNICO
        cursor.execute("SELECT * FROM Users WHERE email = ?",(usuario, ))
        rows = cursor.fetchone()
        if rows is not None:
            flash("Email existed !!!!","error")
            return render_template("register.html")
        #INSERTAR
        cursor.execute('''INSERT INTO Users ('usuario','password','email','name',
        'fecha','foto','nacionalidad','introduccion') VALUES (?,?,?,?,?,?,?,?)'''
        ,(usuario,contrasena,email,nombre,fecha,foto,nacionalidad,intro))
        conn.commit()
        cursor.close()
        conn.close()
        flash("You are registered. Welcome !!!!","success")
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/", methods = ["GET","POST"])
def login():
    if "username" in session:
        return redirect(url_for("home"))
    if request.method == "POST":
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("SELECT password FROM Users WHERE usuario = ? AND password=?",(request.form["username"],request.form["password"]))
        rows = cursor.fetchone()
        if rows is not None:
            session["username"] = request.form['username']
            flash("You are logged. Welcome !!!!","success")
            return redirect(url_for("home"))
        else:
            flash("Error in login. Check credentials","error")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("username",None)
    return redirect(url_for("login"))

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
            return redirect(url_for("/"))
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

@app.route("/perfil/<string:usuario>")
def mostrar_perfil(usuario):
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT usuario,email, name,fecha,foto,nacionalidad, introduccion FROM Users WHERE usuario = ?", (usuario,))
    for row in cursor:
        return render_template("perfil.html",usuario = row[0],
                                                    email = row[1],
                                                    name = row[2],
                                                    fecha = row[3],
                                                    foto = row[4],
                                                    nacionalidad = row[5],
                                                    introduccion = row[6])
    return "No existe usuario"

def conectar_db():
    conn = sqlite3.connect('datos.db')
    cursor = conn.cursor()
    sqlite_create_table_query = '''CREATE TABLE IF NOT EXISTS Users (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                usuario TEXT NOT NULL UNIQUE,
                                password TEXT NOT NULL,
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
