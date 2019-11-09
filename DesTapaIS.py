from flask import Flask
from flask import request
import sqlite3
app = Flask(__name__)



def conectar_db():
    conn = sqlite3.connect('datos.db')
    #FALTA COMPROBAR LA EXISTENCIA DE LA TABLA
    c =  conn.cursor()
    #c.execute('''CREATE TABLE USER
    #    (USUARIO              TEXT         NOT NULL,
    #    FECHA_NACIMIENTO     DATE                 ,
    #    CONTRASENA           TEXT         NOT NULL,
    #    EMAIL                TEXT         NOT NULL,
    #    NOMBRE               TEXT                 ,
    #    FOTO                 VARCHAR              ,
    #    NACIONALIDAD         TEXT                 ,
    #    INTRODUCCION         TEXT                 );''')
    c.execute('''INSERT INTO USER (USUARIO,CONTRASENA,EMAIL) VALUES ('A', 123, 'aa@')''')
    return conn
    


def desconectar_db():
    conn.commit()
    conn.close()

#Falta Fecha y foto
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST': 
        usuario = request.form.get('usuario')
        contrasena = request.form.get('contrasena')
        repite_contrasena = request.form.get('repite_contrasena')
        email = request.form.get('email')
        nombre = request.form.get('nombre')
        nacionalidad = request.form.get('nacionalidad')
        introduccion = request.form.get('introduccion')

        if (usuario == "") or (contrasena == "") or (repite_contrasena == "") or (email == ""):
            return "Campo obligatorio no ha sido completado"
        if (contrasena != repite_contrasena):
            return "Contraseñas no coincide"

        conn = conectar_db()
        c = conn.cursor()
        c.execute('''INSERT INTO USER (USUARIO,CONTRASENA,EMAIL) VALUES ('A', 123, 'aa@')''')

        return '''<h1>Registro Completo</h1>'''


    return '''<form method="POST">
                Usuario: <input type="text" name="usuario"><a>(obligatorio)</a><br>
                Contraseña: <input type="text" name="contrasena"><a>(obligatorio)</a><br>
                Repite contraseña: <input type="text" name="repite_contrasena"><a>(obligatorio)</a><br>
                Email: <input type="text" name="email"><a>(obligatorio)</a><br>
                Nombre: <input type="text" name="nombre"><br>
                Nacionalidad: <input type="text" name="nacionalidad"><br>
                Introducción: <input type="text" name="introduccion"><br>
                <input type="submit" value="Submit"><br>
              </form>'''


if __name__ == "__main__":
    app.run(debug=True, post= "127.0.0.0")
