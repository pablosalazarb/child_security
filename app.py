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

#Vista de registro de usuarios nuevos
@app.route('/new-register')
def register():    
    data = {
        'titulo' : 'Child Security - Registrate'
    }
    #Mensaje a mostrar por cualquier error
    msg = ''
    #Almacenamos la fecha de este instante
    today = datetime.now()
    f_reg = today.date
    foto = ''
    conn = mysql.connect()

    #Guardamos la peticion (request)
    req = request.form
    #Corroboramos el user y password
    if request.method == 'POST' and 'nombre' in request.form and 'apellido' in request.form and 'usename' in request.form and 'email' in request.form and 'password' in request.form:
        #Guardamos las variables para tener mejor acceso
        params = {
            'nombre' : req.get("nombre"),
            'apellido' : req.get("apellido"),
            'username' : req.get("username"),
            'email' : req.get("email"),
            'password' : req.get("password"),
            'f_reg' : f_reg,
            'foto_perfil' : foto
        }
        #Revisamos si los datos de la cuenta existen en la base de datos
        cursor = conn.cursor()
        query = 'INSERT into usuarios (nombre, apellido, user, correo, password, fecha_reg, foto_perfil) values(%(nombre)s, %(apellido)s, %(username)s, %(email)s, %(password)s, %(f_reg)s, %(foto_perfil)s)'
        #Ejecutamos la sentencia
        cursor.execute(query, params)
        #Ejecutamos un commit (para que se ejecute la query)
        conn.commit()
        #Redirigimod al dashboard principal con el usuario loggeado
        return redirect('/dashboard')
    else:
        #Si el usuario/contrasenia son incorrectos
        msg = 'Uno de los datos ingresados no es correcto...'
    #Renderizamos el form de registrar con la variable mensaje (si hubiese)
    return render_template('register.html', data=data, msg=msg)

#Validamos en la vista principal de la app para protegerla de usuarios no autenticados
@app.route('/dashboard')
def index():
    data = {
        'titulo' : 'Child Security'
    }
    #Si la variable de session loggedin existe en session
    if 'loggedin' in session:
        #El usuario tiene session activa, renderizamos el dashboard
        return render_template('dashboard.html', data=data, username=session['username'], profilepic=session['profile_pic'], nombre=session['name'], apellido=session['surname'])
    return redirect(url_for('/'))