import sqlite3
from flask import Flask, redirect, url_for, render_template, request, flash, session, escape
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import mimetypes
import os, re
from os import path
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from os.path import join, dirname, realpath
from datetime import date
import datetime
from dateutil.relativedelta import relativedelta

MY_ADDRESS = "proyectois2upm@gmail.com"
script_dir = path.dirname(path.abspath(__file__))
PASSWORD = "softwareupm"
UPLOAD_FOLDER = join(dirname(realpath(__file__)), script_dir+"/static/img")
print(UPLOAD_FOLDER)
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__)
app.secret_key = 'random string'
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
format_email = ["gmail","yahoo"]
format_end = ["com","es"]

@app.route("/home", methods=['GET'])
def home():
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT nombre,email,fecha,foto,nacionalidad,introduccion,genero FROM Users WHERE usuario=?",(session['username'],))
    rows = cursor.fetchone()
    image_file=None
    if rows[3] is not None:
        image_file = url_for('static', filename=rows[3])
    cursor.close()
    conexion.close()
#    conexion2 = conectar_db()
#    cursor2 = conexion2.cursor()
#    cursor2.execute("SELECT Nombre_Amigo, id FROM Solicitudes WHERE Nombre_Usuario = ?", (session["username"],))
#   cols = cursor2.fetchone()
#    cursor2.close()
#    conexion2.close()
    return render_template("index.html",nombre=rows[0],correo=rows[1],fecha=rows[2],foto=image_file,nacionalidad=rows[4],introduccion=rows[5],usuario=session['username'],genero=rows[6])
    #,amigosSolicitud=cols[0],idSolicitud=cols[1])

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
    if request.method == 'POST': 
        usuario = request.form.get('usuario')
        genero = request.form.get('genero')
        contrasena = request.form.get('password')
        repite_contrasena = request.form.get('repite_password')
        email = request.form.get('email')
        nombre = request.form.get('nombre')
        nacionalidad = request.form.get('nacionalidad')
        intro = request.form.get('introduccion')
        fecha = request.form['fecha']
        filename = None

        #EXTRAE FOTO
        if 'file' not in request.files:
            filename = "usuario.png"
        file = request.files['file']
        foto = None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
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
        conexion = conectar_db()
        cursor = conexion.cursor()
        #COMPROBACION DE EDAD VALIDA 
        fecha_aux = fecha.split('-')
        if(calcular_edad(date(int(fecha_aux[0]),int(fecha_aux[1]),int(fecha_aux[2]))) < 18):
            flash("Eres muy pequeño chavalin para estar en un sito como este","error")
            return render_template("register.html")
        #COMPROBACION DE USUARIO UNICO
        cursor.execute("SELECT * FROM Users WHERE usuario = ?",(usuario,))
        rows = cursor.fetchone()
        if rows is not None:
            flash("Usuario existed !","error")
            return render_template("register.html")
        #COMPROBACION DE EMAIL UNICO
        cursor.execute("SELECT * FROM Users WHERE email = ?",(usuario,))
        rows = cursor.fetchone()
        if rows is not None:
            flash("Email existed !!!!","error")
            return render_template("register.html")
        #INSERTAR
        cursor.execute('''INSERT INTO Users ('usuario','genero','password','email','nombre',
        'fecha','foto','nacionalidad','introduccion','verificado') VALUES (?,?,?,?,?,?,?,?,?,0)'''
        ,(usuario,genero,contrasena,email,nombre,fecha,filename,nacionalidad,intro))
        conexion.commit()
        cursor.close()
        conexion.close()
        flash("You are registered. Welcome !!!!","success")
        enviar_correo(email,"http://127.0.0.1:5000/ver/"+usuario,1)
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/ver/<string:username>")
def verified(username, methods=['GET', 'POST']):
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("UPDATE Users SET verificado=1 WHERE usuario=?",(username,))
    conexion.commit()
    cursor.close()
    conexion.close()
    return redirect(url_for("login"))

@app.route("/", methods = ["GET","POST"])
def login():
    if "username" in session:
        return redirect(url_for("home"))
    if request.method == "POST":
        conexion = conectar_db()
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
        conexion.close()
    return render_template("login.html")

@app.route("/logout",  methods = ["GET","POST"])
def logout():
    session.pop("username",None)
    return redirect(url_for("login"))

@app.route("/recuperar", methods = ["GET","POST"])
def recuperar():
    if request.method == "POST":
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("SELECT usuario FROM Users WHERE email = ?",(request.form["email"],))
        rows = cursor.fetchone()
        if rows is not None:
            if enviar_correo(request.form["email"],"http://127.0.0.1:5000/recuperar/password",0) == 0:
                flash("E-mail sent. Look at your mail","success")
        else:
            flash("Email not valid. Try again","error")
        cursor.close()
        conexion.close()
    return render_template("recuperar.html")

@app.route("/recuperar/password", methods = ["GET","POST"])
def new_pass():
    if request.method == "POST":
        conexion = conectar_db()
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
        conexion.close()
    return render_template("new_pass.html")

@app.route("/search", methods=['GET'])
def search():
    if request.method == 'GET':
        var_search = request.args.get("var_search")
        var_filter = request.args.get("selector")
        conexion = conectar_db()
        cursor = conexion.cursor()
        if var_filter == "Degustaciones":
            cursor.execute("SELECT Local FROM Degustaciones WHERE Nombre = ?",(var_search,))
            rows = cursor.fetchall()
            if not rows:
                return render_template("add_degustacion.html",name=var_search)
            else:
                locales = list()
                fotos = list()
                for x in rows:
                    print(x[0])
                    locales.append(x[0])
                    cursor.execute("SELECT Foto FROM Locales WHERE Nombre = ?",(x[0],))
                    raws = cursor.fetchone()
                    print(raws)
                    fotos.append(raws[0])
                print(fotos)
                return render_template("ver_locales_degus.html",locales=locales,fotos=fotos)

        elif var_filter == "Locales":
            cursor.execute("SELECT Nombre,Direccion,Reseña FROM Locales WHERE Nombre = ?",(var_search,))
            rows = cursor.fetchone()
            if rows is None:
                flash("El local no existe", "error")
                return render_template("add_local.html",name=var_search)
            else:
                degust = list()
                fotos = list()
                cursor.execute("SELECT Nombre,Foto FROM Degustaciones WHERE Local = ?",(var_search,))
                raws = cursor.fetchall()
                for x in raws:
                    degust.append(x[0])
                    fotos.append(x[1])
                print(degust)
                return render_template("ver_local.html",name=rows[0],dir=rows[1],resena=rows[2],degustaciones=degust,fotos=fotos)
        else:
            cursor.execute("SELECT usuario,genero,email,nombre,fecha,nacionalidad,introduccion,foto FROM Users WHERE usuario=?",(var_search,))
            rows = cursor.fetchone()
            print(rows)
            if rows is None:
                flash("El usuario no existe","error")
                return redirect(url_for("home"))
            else:
                return render_template("ver_perfil.html", user_name=rows[0],genero=rows[1],email=rows[2],nombre=rows[3],fecha=rows[4],nacionalidad=rows[5],introduccion=rows[6],foto=rows[7])
        cursor.close()  
        conexion.close()
    
@app.route("/ver_degus",methods=['GET','POST'])
def ver_degus():
    if request.method == 'GET':
        local = request.args.get("local_button")
        degust = request.args.get("degust_var")
        option_var = request.args.get("option_var")
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("SELECT Nombre,Foto,Descripcion,Tipo,Region,Tamaño,Calificacion_Gusto,Calificacion FROM Degustaciones WHERE Local = ?",(local,))
        rows = cursor.fetchone()
        return render_template("ver_degustacion.html",name=rows[0],foto=rows[1],descr=rows[2],tipo=rows[3],region=rows[4],tamaño=rows[5],calif_gusto=rows[6],calif=rows[7],option=option_var,local_name=local)


@app.route("/degustacion", methods=['GET','POST'])
def add_degustacion():
    if request.method == 'POST':
        nombre_deg = request.form.get('degustacion')
        tipo = request.form.get('tipo')
        region = request.form.get('nacionalidad')
        tamaño = request.form.get('tamaño')
        calificacion_gusto = request.form.get('gusto')
        calificacion = request.form.get('calificacion')
        local = request.form.get('local')
        descripcion = request.form.get('descripcion')
        filename = None

        #PARTE DE FOTO
        if 'file' not in request.files:
            file = None
            return "file = None"
        file = request.files['file']
        foto = None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("SELECT Nombre FROM Locales WHERE Nombre = ?",(local,))
        rows = cursor.fetchone()
        if rows is None:
            flash("El local no existe, por favor añadelo primero","error")
            return render_template("add_local.html")
        cursor.execute('''INSERT INTO Degustaciones ('Nombre','Foto','Descripcion','Tipo',
        'Region','Tamaño','Calificacion_Gusto','Calificacion','Local') VALUES (?,?,?,?,?,?,?,?,?)'''
        ,(nombre_deg,filename,descripcion,tipo,region,tamaño,calificacion_gusto,calificacion,local))
        id = cursor.lastrowid
        conexion.commit()
        cursor.execute("SELECT Degustaciones FROM Locales WHERE Nombre = ?",(local,))
        rows = cursor.fetchone()
        if rows[0] is None:
            cursor.execute("UPDATE Locales SET Degustaciones=? WHERE Nombre=?",(str(id)+",",local))
        else:
            cursor.execute("UPDATE Locales SET Degustaciones=(SELECT Degustaciones FROM Locales WHERE Nombre=?) || ? WHERE Nombre=?",(local,str(id)+",",local))
        conexion.commit()
        cursor.execute("SELECT Degustaciones FROM Users WHERE usuario = ?",(session.get("username"),))
        rows = cursor.fetchone()
        if rows[0] is None:
            cursor.execute("UPDATE Users SET Degustaciones=? WHERE usuario=?",(str(id)+" -> "+str(datetime.datetime.now())+", ",session.get("username")))
        else:
            cursor.execute("UPDATE Users SET Degustaciones=(SELECT Degustaciones FROM Users WHERE usuario=?) || ? WHERE usuario=?",(session.get("username"),str(id)+" -> "+str(datetime.datetime.now())+", ",session.get("username")))
        conexion.commit()
        cursor.close()
        conexion.close()
        flash("Degustacion añadida con exito","success")
        return redirect(url_for("home"))
    return render_template("add_degustacion.html")


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

@app.route("/perfil", methods=['GET', 'POST'])
def modificar_perfil():
    if request.method == 'POST': 
        conexion = conectar_db()
        cursor = conexion.cursor()
        usuario = request.form.get('usuario')
        genero = request.form.get('genero')
        contrasena_old = request.form.get('password')
        contrasena = request.form.get('new_password')
        repite_contrasena = request.form.get('rp_new_password')
        email = request.form.get('email')
        nombre = request.form.get('nombre')
        nacionalidad = request.form.get('nacionalidad')
        intro = request.form.get('introduccion')
        fecha = request.form['fecha']
        foto = None

    #-------USUARIO-------
        #COMPROBAMOS SI USUARIO ES VALIDO Y UPDATE
        if len(usuario) !=0:
            print("elelele")
            if len(usuario) < 6:
                flash("Introduzca un usuario de minimo 6 caracteres","error")
                cursor.close()
                conexion.close()
                return render_template("perfil.html")
            else:
                cursor.execute("SELECT id FROM Users WHERE usuario = ?",(usuario,))
                rows = cursor.fetchone()
                if rows is not None:
                    flash("Usuario existed !","error")
                    cursor.close()
                    conexion.close()
                    return render_template("perfil.html")
            cursor.execute("UPDATE Users SET usuario=? WHERE usuario=?",(usuario,session["username"]))
            conexion.commit()
            session["username"]=usuario
    #------PASSWORD---------
        if len(contrasena_old ) != 0 or len(contrasena) != 0 or len(repite_contrasena) !=0:
        #COMPROBACION DE ANTIGUA PASSWORD
            cursor.execute("SELECT password FROM Users WHERE usuario=?",(session["username"],))
            rows = cursor.fetchone()
            if rows[0] != contrasena_old:
                flash("Contraseña incorrecta","error")
                cursor.close()
                conexion.close()
                return render_template("perfil.html")
        #COMPROBACION DE LONGITUD DE PASSWORD
            if len(contrasena) < 6:
                flash("Introduzca una contraseña de minimo 6 caracteres","error")
                cursor.close()
                conexion.close()
                return render_template("perfil.html")
        #COMPROBACION DE CONTRASEÑA
            if (contrasena != repite_contrasena):
                flash("Password incorrect","error")
                cursor.close()
                conexion.close()
                return render_template("perfil.html")
            cursor.execute("UPDATE Users SET password=? WHERE usuario=?",(contrasena,session["username"]))
            conexion.commit()
    #-------EMAIL------------
        if len(email) != 0 :
        #COMPROBACION DE FORMATO CORREO
            expresion = "[a-z0-9\.\_]+(@)([a-z]+).([a-z]+)"
            tupla = re.match(expresion,email)
            if tupla is None or tupla.group(1)!="@" or tupla.group(2) not in format_email or tupla.group(3) not in format_end:
                flash("Email not valid","error")
                cursor.close()
                conexion.close()
                return render_template("perfil.html")
        #COMPROBACION DE EMAIL UNICO
            cursor.execute("SELECT id FROM Users WHERE email = ?",(usuario,))
            rows = cursor.fetchone()
            if rows is not None:
                flash("Email existed !!!!","error")
                cursor.close()
                conexion.close()
                return render_template("perfil.html")
            cursor.execute("UPDATE Users SET email=? WHERE usuario=?",(email,session["username"]))
            conexion.commit()
    #------FECHA-------------
        if len(fecha) != 0:
        #COMPROBACION DE EDAD VALIDA 
            fecha_aux = fecha.split('-')
            if(calcular_edad(date(int(fecha_aux[0]),int(fecha_aux[1]),int(fecha_aux[2]))) < 18):
                flash("Eres muy pequeño chavalin para estar en un sito como este","error")
                cursor.close()
                conexion.close()
                return render_template("perfil.html")
            cursor.execute("UPDATE Users SET fecha=? WHERE usuario=?",(fecha,session["username"]))
            conexion.commit()
    #--------NAME----------
        if len(nombre) != 0:
            cursor.execute("UPDATE Users SET nombre=? WHERE usuario=?",(nombre,session["username"]))
            conexion.commit()
    #--------GENERO--------
        if len(genero) != 0:
            cursor.execute("UPDATE Users SET genero=? WHERE usuario=?",(genero,session["username"]))
            conexion.commit()
    #--------INTRODUCCION---
        if len(intro) != 0:
            cursor.execute("UPDATE Users SET introduccion=? WHERE usuario=?",(intro,session["username"]))
            conexion.commit()
    #--------NACIONALIDAD
        if nacionalidad is not None:
            cursor.execute("UPDATE Users SET nacionalidad=? WHERE usuario=?",(nacionalidad,session["username"]))
            conexion.commit()
        flash("Cambios modificados con exito","success")
        cursor.close()
        conexion.close()
        return redirect(url_for("home"))  
    return render_template("perfil.html")

@app.route("/local", methods=['GET', 'POST'])
def local():
    if request.method == 'POST': 
        local = request.form['local']
        direccion = request.form['direccion']
        reseña = request.form['reseña']
        degustaciones = None
        filename = None

        #EXTRAE FOTO
        if 'file' not in request.files:
            filename = "usuario.png"
        file = request.files['file']
        foto = None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute('''INSERT INTO Locales ('Nombre','Direccion','Reseña','Degustaciones','Foto') VALUES (?,?,?,?,?)'''
        ,(local, direccion, reseña, degustaciones,filename))
        Id = cursor.lastrowid
        cursor.execute("SELECT Locales FROM Users WHERE usuario = ?", (session["username"],))
        for row in cursor:
            local_User = row[0]
        if local_User is None:
            cursor.execute("UPDATE Users SET locales=? WHERE usuario=?",(str(Id)+" -> "+str(datetime.datetime.now())+", ",session["username"]))
        else:
            addLocal = addLista(str(Id)+" -> "+str(datetime.datetime.now())+", ",local_User)
            cursor.execute("UPDATE Users SET locales=? WHERE usuario=?",(addLocal,session["username"]))
        conexion.commit()
        cursor.close()
        conexion.close()
        flash("Local añadido con exito","success")
        return redirect(url_for("add_degustacion"))
    return render_template("add_local.html")

@app.route("/enviar_solicitud", methods=['GET','POST'])
def enviar_solicitud():
    if request.method == 'POST': 
        nombre_amigo = request.form['nombreAmigo']
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("SELECT Amigos FROM Users WHERE usuario = ?", (session["username"],))
        amigos = None
        for row in cursor:
            am = row[0]
            amigos = str(am)
        cursor.execute("SELECT id FROM Users WHERE usuario = ?", (nombre_amigo,))
        for row in cursor:
            Id = row[0]
        if amigos is not None :
            if  (str(Id) in amigos):
                return "Ya son amigos"
        cursor.execute('''INSERT INTO Solicitudes ('Nombre_Usuario','Nombre_Amigo','Validacion') VALUES (?,?,?)'''
            ,(session["username"], nombre_amigo, 0))
        conn.commit()
        cursor.close()
        conn.close()
        flash("Solicitud enviada", "success")
    return redirect(url_for("home"))

@app.route("/loc_megusta", methods=['GET','POST'])
def loc_megusta():
    if request.method == 'GET':
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("SELECT Loc_Gusta FROM Users WHERE usuario = ?", (session["username"],))
        for row in cursor:
            loc = row[0]
        if loc is None:
            cursor.execute
            cursor.execute("UPDATE Users SET Loc_Gusta=? WHERE usuario=?",(str(loc)+" -> "+str(datetime.datetime.now())+", ",session["username"]))
        else:
            addLoc = addLista(str(loc)+" -> "+str(datetime.datetime.now())+", ",loc)
            cursor.execute("UPDATE Users SET locales=? WHERE usuario=?",(addLoc,session["username"]))
        conexion.commit()
        cursor.close()
        conexion.close()
    return redirect(url_for("home"))

@app.route("/deg_megusta", methods=['GET','POST'])
def deg_megusta():
    if request.method == 'GET':
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("SELECT Deg_Gusta FROM Users WHERE usuario = ?", (session["username"],))
        for row in cursor:
            deg = row[0]
        if deg is None:
            cursor.execute
            cursor.execute("UPDATE Users SET Deg_Gusta=? WHERE usuario=?",(str(deg)+" -> "+str(datetime.datetime.now())+", ",session["username"]))
        else:
            addDeg = addLista(str(deg)+" -> "+str(datetime.datetime.now())+", ",deg)
            cursor.execute("UPDATE Users SET Deg_Gusta=? WHERE usuario=?",(addDeg,session["username"]))
        conexion.commit()
        cursor.close()
        conexion.close()
    return redirect(url_for("home"))


@app.route("/mostrar_solicitud", methods=['GET','POST'])
def mostrar_solicitud():
    if request.method == 'POST': 
        conexion = conectar_db()
        cursor = conexion.cursor()
        result = ""
        cursor.execute("SELECT Nombre_Amigo, id FROM Solicitudes WHERE Nombre_Usuario = ?", (session["username"],))
        for row in cursor:
            if result == "":
                result = str(row[0]) + "," + str(row[1]) + ","
            else:
                result = result + str(row[0]) + "," + str(row[1])
        cursor.close()
        conexion.close()
    return render_template("mostrar_solicitud.html",res = result)


@app.route("/aceptar_solicitud", methods=['GET','POST'])
def aceptar_solicitud():
    if request.method == 'POST': 
        id_solicitud = request.form['idAmigo']
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE Solicitudes SET Validacion=? WHERE id=?",(1,id_solicitud))
        conn.commit()
        cursor.execute("SELECT Amigos FROM Users WHERE usuario = ?", (session["username"],))
        for row in cursor:
            solicitud_User = row[0]
        if solicitud_User is None:
            cursor.execute("UPDATE Users SET Amigos=? WHERE usuario=?",(str(id_solicitud),session["username"]))
        else:
            addAmigo = addLista(id_solicitud,solicitud_User)
            cursor.execute("UPDATE Users SET Amigos=? WHERE usuario=?",(addAmigo,session["username"]))
            conn.commit()
        cursor.close()
        conn.close()
        return render_template("aceptar_solicitud.html")
    return render_template("aceptar_solicitud.html")

@app.route("/eliminar_solicitud", methods=['GET','POST'])
def eliminar_solicitud():
    if request.method == 'POST':
        id_solicitud = request.form['idAmigo']
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Solicitudes WHERE id=?",(id_solicitud,))
        conn.commit()
        cursor.close()
        conn.close()
        return "eliminado"
    return "elimanado"

@app.route("/actividad_reciente", methods=['GET','POST'])
def actividad_reciente():
    actividades = None
    conn = conectar_db()
    cursor = conn.cursor()
    print("entra")
    amigos = list()
    cursor.execute("SELECT Amigos FROM Users WHERE usuario = ?", (session["username"],))
    for row in cursor:
        amig = row[0]
    list_amigos = getLista(amig)
    for x in list_amigos:
        print("dentro del for x" + str(x))
        amigos.append(x)
    for y in amigos:
        print("dentro del for y" + str(y))
        cursor.execute("SELECT Locales FROM Users WHERE usuario = ?", (y,))
        print("despues de select locales")
        rows = cursor.fetchone()
        print("fetchone" + str(rows))
        for row2 in cursor:
            print("row2 de locales" + str(row[0]))
            if actividades is None:
                actividades = row2[0]
            else:
                actividades = "," + row2[0]
        cursor.execute("SELECT Degustaciones FROM Users WHERE usuario = ?", (y,))
        for row3 in cursor:
            actividades = "," + row3[0]
        cursor.execute("SELECT Deg_Gusta FROM Users WHERE usuario = ?", (y,))
        for row4 in cursor:
            actividades = "," + row4[0]
        cursor.execute("SELECT Loc_Gusta FROM Users WHERE usuario = ?", (y,))
        for row5 in cursor:
            actividades = "," + row5[0]
    print("actividades" + str(actividades))
    #return "actividad reciente"
    return "actividades recientes"

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
                                genero TEXT,
                                password TEXT NOT NULL,
                                email TEXT NOT NULL UNIQUE,
                                nombre TEXT,
                                fecha DATE,
                                foto TEXT,
                                nacionalidad TEXT,
                                introduccion TEXT,
                                verificado INTEGER NOT NULL,
                                Amigos TEXT,
                                Degustaciones TEXT,
                                Locales TEXT,
                                Deg_Gusta TEXT,
                                Loc_Gusta TEXT);'''
    cursor.execute(sqlite_create_users_table_query)
    #CREA TABLA DEGUSTACIONES
    sqlite_create_degustaciones_table_query = '''CREATE TABLE IF NOT EXISTS Degustaciones (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                Nombre TEXT NOT NULL,
                                Foto TEXT,
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
                                Foto TEXT,
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
                                Nombre_Amigo TEXT NOT NULL,
                                Validacion INT);'''
    cursor.execute(sqlite_create_solicitudes_table_query)
    conn.commit()
    cursor.close()
    return conn


if __name__== "__main__":
    app.run(debug=True)
