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
#------------------------------------------
#Funciones de usuario
@app.route('/admin/usuarios')
def admin_usuarios():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM usuarios"
    cursor.execute(query)
    usuarios = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('administrador/usuarios.html', nombre = session['nombre'], usuarios = usuarios)

@app.route('/admin/guardar_usuario', methods=['GET','POST'])
def guardar_usuario():

    return render_template('/administrador/guardar_usuarios.html', usuario=usuario)

@app.route('/admin/eliminar_usuario/<int:user_id>', methods=['POST'])
def eliminar_usuario(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (user_id,))
        conn.commit()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return '', 204  # Respuesta vacía para AJAX (sin recargar página)
        else:
            flash('Usuario eliminado exitosamente', 'success')
            return redirect(url_for('usuarios'))
        
    except mysql.connector.Error as err:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return str(err), 500
        else:
            flash(f"Error al eliminar el usuario: {err}", 'danger')
            return redirect(url_for('usuarios'))
    finally:
        cursor.close()
        conn.close()


#--------------------------------------------------------------------------------------------------------
#(Eduardo picazo)
# Aqui estan las funciones para Productos
@app.route('/admin/productos')
def admin_productos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT id_producto, nombre, descripcion,cantidad, categoria_id, proveedor_id, ubicacion FROM Productos"
    cursor.execute(query)
    productos = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('administrador/productos.html', productos = productos)

@app.route('/admin/agregar_producto', methods=['GET', 'POST'])
def agregar_productos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        cantidad = request.form['cantidad']
        categoria_id = request.form['categoria_id']
        proveedor_id = request.form['proveedor_id']
        ubicacion = request.form['ubicacion']

        conn = get_db_connection()
        try:
            cursor = conn.cursor()

            # Validar existencia de categoria_id
            cursor.execute("SELECT COUNT(*) FROM Categorias WHERE id_categoria = %s", (categoria_id,))
            categoria_existe = cursor.fetchone()[0] > 0

            # Validar existencia de proveedor_id
            cursor.execute("SELECT COUNT(*) FROM Proveedores WHERE id_proveedor = %s", (proveedor_id,))
            proveedor_existe = cursor.fetchone()[0] > 0

            if not categoria_existe or not proveedor_existe:
                flash("La categoría o el proveedor no existen. Por favor, verifica los datos.", "error")
                return redirect(url_for('agregar_productos'))

            # Insertar producto si todo está bien
            cursor.execute("""
                INSERT INTO Productos (nombre, descripcion, cantidad, categoria_id, proveedor_id, ubicacion)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (nombre, descripcion, cantidad, categoria_id, proveedor_id, ubicacion))
            conn.commit()
            flash("Producto agregado exitosamente.", "success")
            return redirect(url_for('admin_productos'))
        finally:
            cursor.close()
            conn.close()
    

    else:
        # Consultar categorías y proveedores para el formulario
        try:
            cursor.execute("SELECT id_categoria, nombre FROM Categorias")
            categorias = cursor.fetchall()

            cursor.execute("SELECT id_proveedor, nombre, contacto FROM Proveedores")
            proveedores = cursor.fetchall()
        finally:
            cursor.close()
            conn.close()
        

        return render_template('/administrador/agregar_productos.html',
                               categorias = categorias,
                               proveedores = proveedores)
    



@app.route('/admin/modificar_producto/<int:id>', methods=['GET', 'POST'])
def modificar_producto(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Obtener el producto actual
    cursor.execute("SELECT * FROM Productos WHERE id_producto=%s", (id,))
    producto = cursor.fetchone()
    if not producto:
        return "Producto no encontrado", 404

    # Obtener categorías y proveedores para los menús desplegables
    cursor.execute("SELECT id_categoria, nombre FROM Categorias")
    categorias = cursor.fetchall()

    cursor.execute("SELECT id_proveedor, nombre, contacto FROM Proveedores")
    proveedores = cursor.fetchall()

    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        cantidad = request.form['cantidad']
        categoria_id = request.form['categoria_id']
        proveedor_id = request.form['proveedor_id']
        ubicacion = request.form['ubicacion']
        
        # Validar existencia de categoría y proveedor
        cursor.execute("SELECT COUNT(*) FROM Categorias WHERE id_categoria = %s", (categoria_id,))
        categoria_existe = cursor.fetchone()['COUNT(*)'] > 0

        cursor.execute("SELECT COUNT(*) FROM Proveedores WHERE id_proveedor = %s", (proveedor_id,))
        proveedor_existe = cursor.fetchone()['COUNT(*)'] > 0

        if not categoria_existe or not proveedor_existe:
            # Mostrar mensaje de error si alguno no existe
            flash("La categoría o el proveedor especificados no existen.", "error")
            return render_template(
                '/administrador/modificar_productos.html',
                producto=producto,
                categorias=categorias,
                proveedores=proveedores
            )

        # Actualizar el producto si todo es válido
        cursor.execute("""
            UPDATE Productos 
            SET nombre=%s, descripcion=%s, cantidad=%s, categoria_id=%s, proveedor_id=%s, ubicacion=%s 
            WHERE id_producto=%s
        """, (nombre, descripcion, cantidad, categoria_id, proveedor_id, ubicacion, id))
        conn.commit()
        flash("Producto actualizado con éxito.", "success")
        return redirect(url_for('admin_productos'))

    # Renderizar el formulario con los datos actuales
    return render_template(
        '/administrador/modificar_productos.html',
        producto=producto,
        categorias=categorias,
        proveedores=proveedores
    )


@app.route('/admin/eliminar_producto/<int:id>',methods=['POST'])
def eliminar_producto(id):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Productos WHERE id_producto=%s", (id,))
        conn.commit()
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('admin_productos'))



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