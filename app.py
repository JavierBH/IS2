import sqlite3
from flask import Flask, redirect, url_for, render_template, request, flash
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from os.path import join, dirname, realpath

UPLOAD_FOLDER = join(dirname(realpath(__file__)), '/home/xiaojing/Documentos/IS2/img')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key = 'random string'
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
    
@app.route("/")
def home():
    conectar_db()
    return render_template("home.html")

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
        
        #EXTRAE FOTO
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
            foto = convertToBinaryData(filename)
        #COMPROBACION DE CAMPOS OBLIGATORIOS
        if (usuario == "") or (contrasena == "") or (repite_contrasena == "") or (email == ""):
            return "Campo incompleto"
        #COMPROBACION DE CONTRASEÑA
        if (contrasena != repite_contrasena):
            return "Contraseñas no coinciden"
        conn = conectar_db()
        cursor = conn.cursor()
        #COMPROBACION DE USUARIO UNICO
        cursor.execute("SELECT * FROM Users WHERE usuario = ?",(usuario, ))
        rows = cursor.fetchone()
        if rows is not None:
            return "Usuario existed !"
        #COMPROBACION DE EMAIL UNICO
        cursor.execute("SELECT * FROM Users WHERE email = ?",(usuario, ))
        rows = cursor.fetchone()
        if rows is not None:
            return "Email existed !!!!"
        #INSERTAR
        cursor.execute('''INSERT INTO Users ('usuario','password','email','name',
        'fecha','foto','nacionalidad','introduccion') VALUES (?,?,?,?,?,?,?,?)'''
        ,(usuario,contrasena,email,nombre,fecha,foto,nacionalidad,intro))
        conn.commit()
        cursor.close()
        conn.close()
        flash("You are registered. Welcome !!!!")
        return redirect(url_for("home"))
    return render_template("register.html")



@app.route("/login", methods = ["GET","POST"])
def login():
    if request.method == "POST":
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("SELECT password FROM Users WHERE name = ? AND password=?",(request.form["username"],request.form["password"]))
        rows = cursor.fetchone()
        if rows is not None:
            flash("You are logged. Welcome !!!!")
            return redirect(url_for("home"))
    return render_template("login.html")

"""@app.route("/recuperar", methods = ["GET","POST"])
def recuperar():"""


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