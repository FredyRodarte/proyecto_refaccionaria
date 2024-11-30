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

#----------------------------------------------------------------------------------------------------
#aqui estan las funciones de proveedores
#funcion agregada para mostrar los proveedores en la tabla
@app.route('/admin/proveedores')
def admin_proveedores():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT id_proveedor, nombre, contacto, telefono, direccion FROM Proveedores"
    cursor.execute(query)
    proveedores = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('administrador/proveedores.html',proveedores=proveedores)

@app.route('/admin/agregar_proveedor', methods=['GET', 'POST'])
def agregar_proveedor():
    if request.method == 'POST':
        nombre = request.form['nombre']
        contacto = request.form['contacto']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Proveedores (nombre, contacto, telefono, direccion) VALUES (%s, %s, %s, %s)",
                           (nombre, contacto, telefono, direccion))
            conn.commit()
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('admin_proveedores'))
    return render_template('/administrador/agregar_proveedor.html')

@app.route('/admin/modificar_proveedor/<int:id>', methods=['GET', 'POST'])
def modificar_proveedor(id):
    print(f"Modificando proveedor con ID: {id}")
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Proveedores WHERE id_proveedor=%s", (id,))
    proveedor = cursor.fetchone()
    print(f"Proveedor encontrado: {proveedor}")
    if not proveedor:
        return "Proveedor no encontrado", 404
    if request.method == 'POST':
        nombre = request.form['nombre']
        contacto = request.form['contacto']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        cursor.execute("UPDATE Proveedores SET nombre=%s, contacto=%s, telefono=%s, direccion=%s WHERE id_proveedor=%s",
                       (nombre, contacto, telefono, direccion, id))
        conn.commit()
        return redirect(url_for('admin_proveedores'))
    return render_template('/administrador/modificar_proveedor.html', proveedor=proveedor)

@app.route('/admin/eliminar_proveedor/<int:id>',methods=['POST'])
def eliminar_proveedor(id):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Proveedores WHERE id_proveedor=%s", (id,))
        conn.commit()
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('admin_proveedores'))

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