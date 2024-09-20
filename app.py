from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Necesario para usar `flash`

def conectar_bd():
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            user='root',
            password='admin123',
            database='sistema_biblioteca'
        )
        return conexion
    except mysql.connector.Error as err:
        flash(f"Error conectándose a la base de datos: {err}", "error")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registrar')
def registrar():
    return render_template('registrar.html')

@app.route('/autores', methods=['GET', 'POST'])
def autores():
    if request.method == 'POST':
        nombre = request.form['nombre']
        biografia = request.form['biografia']
        nacionalidad = request.form['nacionalidad']
        if not nombre or not biografia or not nacionalidad:
            flash("Revisa que todos los campos estén llenos", "error")
        else:
            conexion = conectar_bd()
            if conexion:
                try:
                    cursor = conexion.cursor()
                    cursor.execute("""
                        INSERT INTO autor(nombre, biografia, nacionalidad)
                        VALUES (%s, %s, %s)
                    """, (nombre, biografia, nacionalidad))
                    conexion.commit()
                    flash("Autor ingresado correctamente", "success")
                except mysql.connector.Error as err:
                    flash(f"Error al insertar los datos: {err}", "error")
                finally:
                    cursor.close()
                    conexion.close()
    return render_template('autores.html')

@app.route('/libros', methods=['GET', 'POST'])
def libros():
    if request.method == 'POST':
        titulo = request.form['titulo']
        genero = request.form['genero']
        isbn = request.form['isbn']
        fecha_publicacion = request.form['fecha_publicacion']
        numero_copias = request.form['numero_copias']
        if not titulo or not genero or not isbn or not fecha_publicacion or not numero_copias:
            flash("Revisa que todos los campos estén llenos", "error")
        else:
            conexion = conectar_bd()
            if conexion:
                try:
                    cursor = conexion.cursor()
                    cursor.execute("""
                        INSERT INTO libro(titulo, genero, ISBN, fecha_publicacion, numero_copias)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (titulo, genero, isbn, fecha_publicacion, numero_copias))
                    conexion.commit()
                    flash("Libro ingresado correctamente", "success")
                except mysql.connector.Error as err:
                    flash(f"Error al insertar los datos: {err}", "error")
                finally:
                    cursor.close()
                    conexion.close()
    return render_template('libros.html')

@app.route('/miembros', methods=['GET', 'POST'])
def miembros():
    if request.method == 'POST':
        nombre = request.form['nombre']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        correo = request.form['correo']
        fecha_membresia = request.form['fecha_membresia']
        if not nombre or not direccion or not telefono or not correo or not fecha_membresia:
            flash("Revisa que todos los campos estén llenos", "error")
        else:
            conexion = conectar_bd()
            if conexion:
                try:
                    cursor = conexion.cursor()
                    cursor.execute("""
                        INSERT INTO miembro(nombre, direccion, telefono, correo, fecha_membresia)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (nombre, direccion, telefono, correo, fecha_membresia))
                    conexion.commit()
                    flash("Miembro ingresado correctamente", "success")
                except mysql.connector.Error as err:
                    flash(f"Error al insertar los datos: {err}", "error")
                finally:
                    cursor.close()
                    conexion.close()
    return render_template('miembros.html')

@app.route('/prestamos', methods=['GET', 'POST'])
def prestamos():
    if request.method == 'POST':
        id_libro = request.form['id_libro']
        id_miembro = request.form['id_miembro']
        fecha_prestamo = request.form['fecha_prestamo']
        fecha_devolucion = request.form['fecha_devolucion']
        estado = request.form['estado']
        if not id_libro or not id_miembro or not fecha_prestamo or not fecha_devolucion or not estado:
            flash("Revisa que todos los campos estén llenos", "error")
        else:
            conexion = conectar_bd()
            if conexion:
                try:
                    cursor = conexion.cursor()
                    cursor.execute("""
                        INSERT INTO prestamo(id_libro, id_miembro, fecha_prestamo, fecha_devolucion, estado)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (id_libro, id_miembro, fecha_prestamo, fecha_devolucion, estado))
                    conexion.commit()
                    flash("Préstamo ingresado correctamente", "success")
                except mysql.connector.Error as err:
                    flash(f"Error al insertar los datos: {err}", "error")
                finally:
                    cursor.close()
                    conexion.close()
    return render_template('prestamos.html')

@app.route('/libros_autores', methods=['GET', 'POST'])
def libros_autores():
    if request.method == 'POST':
        id_libro = request.form['id_libro']
        id_autor = request.form['id_autor']
        if not id_libro or not id_autor:
            flash("Revisa que todos los campos estén llenos", "error")
        else:
            conexion = conectar_bd()
            if conexion:
                try:
                    cursor = conexion.cursor()
                    cursor.execute("""
                        INSERT INTO libroautor(id_libro, id_autor)
                        VALUES (%s, %s)
                    """, (id_libro, id_autor))
                    conexion.commit()
                    flash("Registro ingresado correctamente", "success")
                except mysql.connector.Error as err:
                    flash(f"Error al insertar los datos: {err}", "error")
                finally:
                    cursor.close()
                    conexion.close()
    return render_template('libros_autores.html')

@app.route('/reportes')
def reportes():
    return render_template('reportes.html')

@app.route('/libros_disponibles')
def libros_disponibles():
    conexion = conectar_bd()
    if conexion is None:
        return "Error al conectar con la base de datos"
    
    cursor = conexion.cursor()
    query = "SELECT titulo, genero, numero_copias FROM Libro WHERE numero_copias > 0;"
    cursor.execute(query)
    libros = cursor.fetchall()
    cursor.close()
    conexion.close()
    
    return render_template('libros_disponibles.html', libros=libros)

@app.route('/autores_libros')
def autores_libros():
    conexion = conectar_bd()
    if conexion is None:
        return "Error al conectar con la base de datos"
    
    cursor = conexion.cursor()
    query = """
    SELECT A.nombre, L.titulo
    FROM Autor A
    JOIN LibroAutor LA ON A.id_autor = LA.id_autor
    JOIN Libro L ON LA.id_libro = L.id_libro;
    """
    cursor.execute(query)
    autores_libros = cursor.fetchall()
    cursor.close()
    conexion.close()
    
    return render_template('autores_libros.html', autores_libros=autores_libros)

@app.route('/prestamos_atrasados')
def prestamos_atrasados():
    conexion = conectar_bd()
    if conexion is None:
        return "Error al conectar con la base de datos"
    
    cursor = conexion.cursor()
    query = """
    SELECT M.nombre, L.titulo,P.fecha_prestamo, P.fecha_devolucion
    FROM Prestamo P
    JOIN Miembro M ON P.id_miembro = M.id_miembro
    JOIN Libro L ON P.id_libro = L.id_libro
    WHERE P.estado = 'atrasado';
    """
    cursor.execute(query)
    prestamos_atrasados = cursor.fetchall()
    cursor.close()
    conexion.close()
    
    return render_template('prestamos_atrasados.html', prestamos_atrasados=prestamos_atrasados)


@app.route('/miembro_especifico', methods=['GET', 'POST'])
def miembro_especifico():
    if request.method == 'POST':
        nombre = request.form['nombre']
        conexion = conectar_bd()
        if conexion is None:
            return "Error al conectar con la base de datos"
        
        cursor = conexion.cursor()
        query = """
        SELECT L.titulo, P.fecha_prestamo, P.fecha_devolucion
        FROM Prestamo P
        JOIN Libro L ON P.id_libro = L.id_libro
        JOIN Miembro M ON P.id_miembro = M.id_miembro
        WHERE M.nombre = %s;
        """
        cursor.execute(query, (nombre,))
        prestamos = cursor.fetchall()
        cursor.close()
        conexion.close()
        
        return render_template('miembro_especifico.html', prestamos=prestamos, nombre=nombre)
    
    return render_template('miembro_especifico.html', prestamos=None)

@app.route('/libros_genero')
def libros_genero():
    # Conectar a la base de datos
    conexion = conectar_bd()
    if conexion is None:
        return "Error al conectar con la base de datos"
    
    # Crear cursor y ejecutar la consulta SQL
    cursor = conexion.cursor()
    query = "SELECT genero, COUNT(*) AS cantidad_libros FROM Libro GROUP BY genero;"
    cursor.execute(query)
    
    # Obtener los resultados
    libros_genero = cursor.fetchall()
    
    # Cerrar el cursor y la conexión
    cursor.close()
    conexion.close()
    
    # Renderizar la plantilla con los resultados
    return render_template('libros_genero.html', libros_genero=libros_genero)

@app.route('/mensual_prestamos')
def mensual_prestamos():
    conexion = conectar_bd()
    if conexion is None:
        return "Error al conectar con la base de datos"
    
    cursor = conexion.cursor()
    query = """
    SELECT 
        DATE_FORMAT(P.fecha_prestamo, '%Y-%m') AS mes,
        COUNT(CASE WHEN P.estado = 'Devuelto' THEN 1 END) AS devoluciones,
        COUNT(CASE WHEN P.estado = 'Pendiente' THEN 1 END) AS prestamos
    FROM Prestamo P
    GROUP BY DATE_FORMAT(P.fecha_prestamo, '%Y-%m');
    """
    cursor.execute(query)
    prestamos_mensuales = cursor.fetchall()
    cursor.close()
    conexion.close()
    
    return render_template('mensual_prestamos.html', prestamos_mensuales=prestamos_mensuales)

@app.route('/libros_mas_prestados')
def libros_mas_prestados():
    conexion = conectar_bd()
    if conexion is None:
        return "Error al conectar con la base de datos"
    
    cursor = conexion.cursor()
    query = """
    SELECT L.titulo, COUNT(P.id_prestamo) AS veces_prestado
    FROM Prestamo P
    JOIN Libro L ON P.id_libro = L.id_libro
    GROUP BY L.titulo
    ORDER BY veces_prestado DESC;
    """
    cursor.execute(query)
    libros_prestados = cursor.fetchall()
    cursor.close()
    conexion.close()
    
    return render_template('libros_mas_prestados.html', libros_prestados=libros_prestados)

@app.route('/genero_popular')
def genero_popular():
    conexion = conectar_bd()
    if conexion is None:
        return "Error al conectar con la base de datos"
    
    cursor = conexion.cursor()
    query = """
    SELECT L.genero, COUNT(P.id_prestamo) AS prestamos_realizados
    FROM Prestamo P
    JOIN Libro L ON P.id_libro = L.id_libro
    GROUP BY L.genero
    ORDER BY prestamos_realizados DESC;
    """
    cursor.execute(query)
    generos_populares = cursor.fetchall()
    cursor.close()
    conexion.close()
    
    return render_template('genero_popular.html', generos_populares=generos_populares)



if __name__ == '__main__':
    app.run(debug=True)
