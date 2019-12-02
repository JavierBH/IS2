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
from datetime import date
from dateutil.relativedelta import relativedelta

MY_ADDRESS = "proyectois2upm@gmail.com"
PASSWORD = "softwareupm"
UPLOAD_FOLDER = join(dirname(realpath(__file__)), '/home/xiaojing/Documentos/IS2/img')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__)
app.secret_key = 'random string'
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
format_email = ["gmail","yahoo"]
format_end = ["com","es"]
global conexion

@app.route("/home", methods=['GET'])
def home():
    if request.method == 'GET':
        conn = conectar_db()
        cursor = conn.cursor()
        selector = request.form.get('selector')
        cursor.execute("SELECT Nombre FROM Locales ")
        arr = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        return render_template("index.html",info = arr)
    return render_template("index.html")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convertToBinaryData(filename):
    #Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

#Funcion que calcula la edad de una persona
def calcular_edad(fecha_nacimiento):
    edad = date.today().year - fecha_nacimiento.year
    cumpleanios = fecha_nacimiento + relativedelta(years=edad)
    if cumpleanios > date.today():
        edad = edad - 1
    return edad

@app.route('/register', methods=['GET', 'POST'])
def register():
    global conexion
    if request.method == 'POST': 
        usuario = request.form.get('usuario')
        contrasena = request.form.get('password')
        repite_contrasena = request.form.get('repite_password')
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
        expresion = "[a-z0-9\.\_]+(@)([a-z]+).([a-z]+)"
        tupla = re.match(expresion,email)
        if tupla is None or tupla.group(1)!="@" or tupla.group(2) not in format_email or tupla.group(3) not in format_end:
            flash("Email not valid","error")
            return render_template("register.html")
        #COMPROBACION DE CONTRASEÑA
        if (contrasena != repite_contrasena):
            flash("Password incorrect","error")
            return render_template("register.html")
        cursor = conexion.cursor()
        #COMPROBACION DE EDAD VALIDA 
        fecha_aux = fecha.split('-')
        if(calcular_edad(date(int(fecha_aux[0]),int(fecha_aux[1]),int(fecha_aux[2]))) < 18):
            flash("Eres muy pequeño chavalin para estar en un sito como este","error")
            return render_template("register.html")
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
        cursor.execute('''INSERT INTO Users ('usuario','password','email','nombre',
        'fecha','foto','nacionalidad','introduccion','verificado') VALUES (?,?,?,?,?,?,?,?,0)'''
        ,(usuario,contrasena,email,nombre,fecha,foto,nacionalidad,intro))
        conexion.commit()
        cursor.close()
        flash("You are registered. Welcome !!!!","success")
        enviar_correo(email,"http://127.0.0.1:5000/ver/"+usuario,1)
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/ver/<string:username>")
def verified(username, methods=['GET', 'POST']):
    global conexion
    cursor = conexion.cursor()
    cursor.execute("UPDATE Users SET verificado=1 WHERE usuario=?",(username,))
    conexion.commit()
    cursor.close()
    return redirect(url_for("login"))

@app.route("/", methods = ["GET","POST"])
def login():
    global conexion
    conexion = conectar_db()
    if "username" in session:
        return redirect(url_for("home"))
    if request.method == "POST":
        cursor = conexion.cursor()
        cursor.execute("SELECT verificado FROM Users WHERE usuario = ? AND password=?",(request.form["usuario"],request.form["password"]))
        rows = cursor.fetchone()
        print(rows)
        if rows is not None:
            if rows[0] == 1:
                session["username"] = request.form['usuario']
                flash("You are logged. Welcome !!!!","success")
                return redirect(url_for("home"))
            else:
                flash("You are not verified. Check your e-mail","warning")
        else:
            flash("Error in login. Check credentials","error")
        cursor.close()
    return render_template("login.html")

@app.route("/logout",  methods = ["GET","POST"])
def logout():
    session.pop("username",None)
    return redirect(url_for("login"))

@app.route("/recuperar", methods = ["GET","POST"])
def recuperar():
    global conexion
    if request.method == "POST":
        cursor = conexion.cursor()
        cursor.execute("SELECT usuario FROM Users WHERE email = ?",(request.form["email"],))
        rows = cursor.fetchone()
        if rows is not None:
            if enviar_correo(request.form["email"],"http://127.0.0.1:5000/recuperar/password",0) == 0:
                flash("E-mail sent. Look at your mail","success")
        else:
            flash("Email not valid. Try again","error")
        cursor.close()
    return render_template("recuperar.html")

@app.route("/recuperar/password", methods = ["GET","POST"])
def new_pass():
    global conexion
    if request.method == "POST":
        cursor = conexion.cursor()
        cursor.execute("SELECT usuario FROM Users WHERE usuario = ?",(request.form["usuario"],))
        rows = cursor.fetchone()
        contrasena = request.form.get('password')
        repite_contrasena = request.form.get('repite_password')
        if rows is not None:
            if len(contrasena) < 6:
                flash("Introduzca una contraseña de minimo 6 caracteres","error")
                return render_template("new_pass.html")
            if contrasena == repite_contrasena:
              cursor.execute("UPDATE Users SET password=? WHERE usuario=?",(request.form["password"],request.form["usuario"]))
              conexion.commit()
              flash("Password change with success","success")
              return redirect(url_for("login"))
            else:
                flash("Password Incorrect. Try again","error")
        else:
            flash("Username not valid. Try again","error")
        cursor.close()
    return render_template("new_pass.html")

@app.route("/search")
def search():
    global conexion
    var_search = request.args.get("var_busqueda")
    #var_filter = request.form["var_filter"]
    cursor = conexion.cursor()
    cursor.execute("SELECT usuario FROM Users WHERE usuario = ?",(var_search,))
    rows = cursor.fetchone()
    cursor.close()
    if rows is not None:
        return "hola"
    return render_template("add_degustacion.html")


@app.route("/degustacion", methods=['GET','POST'])
def add_degustacion():
    global conexion
    if request.method == 'POST':
        nombre_deg = request.form.get('nombre_deg')
        tipo = request.form.get('tipo')
        region = request.form.get('region')
        tamaño = request.form.get('tamaño')
        calificacion_gusto = request.form.get('calificacion_gusto')
        calificacion = request.form.get('calificacion')
        local = request.form.get('local')
        descripcion = request.form.get('descripcion')
        foto = request.form.get('foto')
        cursor = conexion.cursor()
        cursor.execute("SELECT Nombre FROM Locales WHERE Nombre = ?",(local,))
        rows = cursor.fetchone()
        if rows is None:
<<<<<<< HEAD
            flash("El local no existe, porfavor añadelo primero","error")
            return render_template("add_local.html")
=======
            return render_template("add_degustacion.html")
>>>>>>> ec8913e6431fd71c3992fcd1f3ea0036bead8a62
        cursor.execute('''INSERT INTO Degustaciones ('Nombre','Foto','Descripcion','Tipo',
        'Region','Tamaño','Calificacion_Gusto','Calificacion','Local') VALUES (?,?,?,?,?,?,?,?,?)'''
        ,(nombre_deg,foto,descripcion,tipo,region,tamaño,calificacion_gusto,calificacion,local))
        conexion.commit()
        cursor.execute("SELECT Degustaciones FROM Locales WHERE Nombre = ?",(local,))
        rows = cursor.fetchone()
        if rows[0] is None:
            cursor.execute("UPDATE Locales SET Degustaciones=? WHERE Nombre=?",(nombre_deg+",",local))
        else:
            cursor.execute("UPDATE Locales SET Degustaciones=(SELECT Degustaciones FROM Locales WHERE Nombre=?) || ? WHERE Nombre=?",(local,nombre_deg+",",local))
        conexion.commit()
        cursor.execute("SELECT Degustaciones FROM Users WHERE usuario = ?",(session.get("username"),))
        rows = cursor.fetchone()
        if rows[0] is None:
            cursor.execute("UPDATE Users SET Degustaciones=? WHERE usuario=?",(nombre_deg+",",session.get("username")))
        else:
            cursor.execute("UPDATE Users SET Degustaciones=(SELECT Degustaciones FROM Users WHERE usuario=?) || ? WHERE usuarii=?",(session.get("username"),nombre_deg+",",session.get("username")))
        conexion.commit()
        cursor.close()
        flash("Degustacion añadida con exito","success")
        return redirect(url_for("home"))
    return render_template("anadir_degustacion.html")


def enviar_correo(correo,mensaje,tipo):
    try:
        destino = correo
        s = smtplib.SMTP("smtp.gmail.com",587)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(MY_ADDRESS,PASSWORD)

        mime_message = MIMEText(mensaje, "plain")
        mime_message["From"] = MY_ADDRESS
        mime_message["To"] = destino
        if tipo == 0:
            mime_message["Subject"] = "Recuperación de contraseña"
        else:
            mime_message["Subject"] = "Verificación de cuenta"
        s.send_message(mime_message)
        del mime_message
        s.quit()
    except Exception:
        return -1
    return 0

    #return render_template("recuperar.html")

<<<<<<< HEAD
@app.route("/perfil/<string:usuario>")
def mostrar_perfil(usuario):
    global conexion
=======
@app.route("/perfil")
def mostrar_perfil():
    ''' conexion = conectar_db()
>>>>>>> ec8913e6431fd71c3992fcd1f3ea0036bead8a62
    cursor = conexion.cursor()
   # cursor.execute("SELECT usuario,email, nombre,fecha,foto,nacionalidad, introduccion FROM Users WHERE usuario = ?", (usuario,))
    for row in cursor:
        usuario = row[0]
        email = row[1]
        nombre = row[2]
        fecha = row[3]
        foto = row[4]
        nacionalidad = row[5]
        introduccion = row[6]
    conexion.commit()
    cursor.close()
<<<<<<< HEAD
    return "No existe usuario"
=======
    conexion.close()'''
    return render_template("perfil.html")
>>>>>>> ec8913e6431fd71c3992fcd1f3ea0036bead8a62

@app.route("/local", methods=['GET', 'POST'])
def local():
    global conexion
    if request.method == 'POST': 
        local = request.form['local']
        direccion = request.form['direccion']
        reseña = request.form['reseña']
        degustaciones = None
        cursor = conexion.cursor()
        cursor.execute('''INSERT INTO Locales ('Nombre','Direccion','Reseña','Degustaciones') VALUES (?,?,?,?)'''
        ,(local, direccion, reseña, degustaciones))
        Id = cursor.lastrowid
        cursor.execute("SELECT Locales FROM Users WHERE usuario = ?", (session["username"],))
        for row in cursor:
            local_User = row[0]
        if local_User is None:
            cursor.execute("UPDATE Users SET locales=? WHERE usuario=?",(Id,session["username"]))
        else:
            addLocal = addLista(Id,local_User)
            cursor.execute("UPDATE Users SET locales=? WHERE usuario=?",(addLocal,session["username"]))
        conexion.commit()
        cursor.close()
        flash("Local añadido con exito","success")
        return redirect(url_for("add_degustacion"))
    return render_template("local.html")

@app.route("/enviar_solicitud", methods=['GET','POST'])
def enviar_solicitud():
    if request.method == 'POST': 
        id_amigo = request.form['idAmigo']
        conn = conectar_db()
        cursor = conn.cursor()
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO Solicitudes ('Nombre_Usuario','Id_Amigo','Validacion') VALUES (?,?,?)'''
            ,(session["username"], id_amigo, 0))
        conn.commit()
        cursor.close()
        conn.close()
        return render_template("enviar_solicitud.html")
    return render_template("enviar_solicitud.html")

@app.route("/morstrar_solicitud", methods=['GET','POST'])
def mostrar_solicitud():
    conexion = conectar_db()
    cursor = conexion.cursor()
    result = ""
    cursor.execute("SELECT Id_Amigo FROM Solicitudes WHERE Nombre_Usuario = ?", (session["username"],))
    for row in cursor:
        if result == "":
            result = row[0]
        else:
            addLista(row[0], result)
    conn.commit()
    cursor.close()
    conexion.close()
    return render_template("mostrar_solicitud.html",result)


@app.route("/aceptar_solicitud", methods=['GET','POST'])
def aceptar_solicitud():
    if request.method == 'POST': 
        conn = conectar_db()
        cursor = conn.cursor()
        cursor = conn.cursor()
        #PENDIENTE
        conn.commit()
        cursor.close()
        conn.close()
        return render_template("enviar_solicitud.html")
    return render_template("enviar_solicitud.html")


#Devuelve elementos en array de una lista de bbdd
def getLista(bbddText):
    nComas = bbddText.count(',')
    l = bbddText.split(',', nComas+1)
    return l

#Devuelve una string de lista con el elemento dado
def addLista(id, lista):
    strId = str(id)
    strLista = str(lista)
    return strLista + "," + strId

def conectar_db():
    conn = sqlite3.connect('datos.db')
    cursor = conn.cursor()
    #CREA TABLA USERS   
    sqlite_create_users_table_query = '''CREATE TABLE IF NOT EXISTS Users (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                usuario TEXT NOT NULL UNIQUE,
                                password TEXT NOT NULL,
                                email TEXT NOT NULL UNIQUE,
                                nombre TEXT,
                                fecha DATE,
                                foto BLOB,
                                nacionalidad TEXT,
                                introduccion TEXT,
                                verificado INTEGER NOT NULL,
                                Amigos TEXT,
                                Degustaciones TEXT,
                                Locales TEXT);'''
    cursor.execute(sqlite_create_users_table_query)
    #CREA TABLA DEGUSTACIONES
    sqlite_create_degustaciones_table_query = '''CREATE TABLE IF NOT EXISTS Degustaciones (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                Nombre TEXT NOT NULL,
                                Foto BLOB,
                                Descripcion TEXT,
                                Tipo TEXT,
                                Region TEXT,
                                Tamaño TEXT,
                                Calificacion_Gusto TEXT,
                                Calificacion INTEGER,
                                Local TEXT);'''
    cursor.execute(sqlite_create_degustaciones_table_query)
    #CREA TABLA LOCALES
    sqlite_create_locales_table_query = '''CREATE TABLE IF NOT EXISTS Locales (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                Nombre TEXT NOT NULL,
                                Direccion TEXT,
                                Reseña TEXT,
                                Degustaciones TEXT);'''
    cursor.execute(sqlite_create_locales_table_query)
    #CREA TABLA GALARDONES
    sqlite_create_galardones_table_query = '''CREATE TABLE IF NOT EXISTS Galardones (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                Nombre TEXT NOT NULL,
                                Descripcion TEXT,
                                Degustaciones TEXT);'''
    cursor.execute(sqlite_create_galardones_table_query)
    #CREA TABLA SOLICITUDES DE AMIGOS
    sqlite_create_solicitudes_table_query = '''CREATE TABLE IF NOT EXISTS Solicitudes (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                Nombre_Usuario TEXT NOT NULL,
                                Id_Amigo TEXT NOT NULL,
                                Validacion INT);'''
    cursor.execute(sqlite_create_solicitudes_table_query)
    conn.commit()
    cursor.close()
    return conn


if __name__== "__main__":
    app.run(debug=True)
