from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from dotenv import load_dotenv
import os


# Cargar variables de entorno
load_dotenv('connect.env')

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')


#Configuracion de conexión a la base de datos.
def get_db_connection():
    return mysql.connector.connect(
        host = os.getenv('DB_HOST'),
        user = os.getenv('DB_USER'),
        password = os.getenv('DB_PASSWORD'),
        database = os.getenv('DB_NAME')
    )

# Ruta para el inicio de sesión
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        #Consulta para verificar usuario y contraseña:
        query = "SELECT * FROM usuarios WHERE nickname = %s AND contraseña = %s"
        cursor.execute(query, (username,password))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:
            session['user'] = user['nickname']
            session['nombre'] = user['nombre']

            if user['rol'] == 'administrador':
                return redirect(url_for('administrador'))
            else:
                return redirect(url_for('usuario'))
        else:
            flash('Credenciales incorrectas. Intenta otra vez', 'error')

    return render_template('index.html')

# Ruta para el módulo del administrador
@app.route('/administrador')
def administrador():
    if 'nombre' in session:
        return render_template('administrador/home.html', nombre = session['nombre'])
    else:
        return redirect(url_for('index'))

# Ruta para el módulo del usuario
@app.route('/usuario')
def usuario():
    if 'user' in session:
        return render_template('usuario/home.html')
    return redirect(url_for('index'))

#Rutas para los modulos de administrador:
@app.route('/admin/usuarios')
def admin_usuarios():
    return render_template('administrador/usuarios.html', nombre = session['nombre'])

@app.route('/admin/productos')
def admin_productos():
    return render_template('administrador/productos.html', nombre = session['nombre'])

@app.route('/admin/proveedores')
def admin_proveedores():
    return render_template('administrador/proveedores.html', nombre = session['nombre'])

@app.route('/admin/categorias')
def admin_categorias():
    return render_template('administrador/categorias.html', nombre = session['nombre'])

@app.route('/admin/movimientos')
def admin_movimientos():
    return render_template('administrador/movimientos.html', nombre = session['nombre'])

#Ruta para cerrar sesion
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Sesión cerrada exitosamente.')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
