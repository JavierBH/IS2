import sqlite3
from flask import Flask, redirect, url_for, render_template, request, flash

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