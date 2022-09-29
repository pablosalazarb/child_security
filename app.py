"""
Controller para la aplicacion CHILD SECURITY
Plataforma online - hibrida y escalable a otros dispositivos
"""

from flask import Flask, render_template, request, redirect, url_for, session
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
from datetime import datetime
import re

#Iniializamos la app
app = Flask(__name__)

#Configuramos la llave secreta de seguridad
app.secret_key = 'child_sec'

#Conexion a la bd
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'child_sec_db'

#Creamos un cursor para recorrer la bd
mysql = MySQL(app, cursorclass=DictCursor)

#Vista de la pagina de inicio, login o register
@app.route('/', methods=['GET', 'POST'])
def login():
    data = {
        'titulo': 'Child Security - Inicia Sesion'
    }
    #Mensaje que se mostrara si obtenemos algun error
    msg = ''
    #Guardamos el request en una variable para posteriormento consultarlo
    req = request.form
    #Revisamos si el user y pass existen en la consulta post generada
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        #Almacenamos en variables para poder acceder mas facil
        username = req.get("username")
        password = req.get("password")
        #Revisamos si los datos de la cuenta existen en nuestra bd
        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT * FROM usuarios WHERE usuario = %s AND password = %s', (username, password))
        #Fetch para asociar todo en un solo registro y lo guardamos
        account = cursor.fetchone()
        #Si la cuenta existe en la tabla de nuestra bd
        if account:
            #Creamos datos de session
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['usuario']
            session['name'] = account['nombre']
            session['surname'] = account['apellido']
            session['email'] = account['correo']
            session['f_reg'] = account['fecha_reg']
            session['profile_pic'] = account['fotografia']
            #Formateamos el mensaje de error
            msg = ""
            #Redireccionamos a la pagina principal
            return redirect('/dashboard')
        else:
            #Si el usuario/password son incorrectos
            msg = 'Los datos ingresados son incorrectos'
    return render_template('login.html' , data=data, msg=msg)

    