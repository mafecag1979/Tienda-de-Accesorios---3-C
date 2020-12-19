from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

#Inicialización
app = Flask(__name__)

#MYSQL Connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'flaskcontacts'
mysql = MySQL(app)

#Settings
app.secret_key = 'mysecretkey'

####
#Para usuarios
####
@app.route('/usuarios') #Decorador
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM usuarios')
    data = cur.fetchall()    
    return render_template('index.html', usuarios = data)

@app.route('/add_usuario', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        nombre = request.form['Nombre']
        apellido = request.form['Apellido']
        correo = request.form['Correo']
        usuario = request.form['Usuario']
        tipo = request.form['Tipo']

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO usuarios (nombre, apellido, correo, usuario, tipo) VALUES (%s, %s, %s, %s, %s)', 
                    (nombre, apellido, correo, usuario, tipo))
        mysql.connection.commit()

        flash('Usuario agregado satisfactoriamente')

        print(nombre, apellido, correo, usuario)
        return redirect(url_for('Index')) #redireccionar a página principal

@app.route('/edit/<id>')
def get_usuario(id):
    cur = mysql.connection.cursor() 
    cur.execute('SELECT * FROM usuarios WHERE id = %s', (id,)) 
    #coma después de ID para leer como tupla
    data = cur.fetchall()
    return render_template('edit-usuario.html', usuario = data[0])

@app.route('/update/<id>', methods = ['POST'])
def update_usuario(id):
    if request.method == 'POST':
        nombre = request.form['Nombre']
        apellido = request.form['Apellido']
        correo = request.form['Correo']
        usuario = request.form['Usuario']
        tipo = request.form['Tipo']
        cur = mysql.connection.cursor()
        cur.execute(""" 
            UPDATE usuarios
            SET Nombre = %s,
                Apellido = %s,
                Correo = %s,
                Usuario = %s,
                Tipo = %s
            WHERE id = %s
        """, (nombre, apellido, correo, usuario, tipo, id))
        mysql.connection.commit()
        flash('Usuario actualizado satisfactoriamente')
        return redirect(url_for('Index'))    

@app.route('/delete/<string:id>')
def delete_usuario(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM usuarios WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Usuario eliminado satisfactoriamente')
    return redirect(url_for('Index'))


####
#Para productos
####

@app.route('/productos') #Decorador
def lista_productos():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM productos')
    data = cur.fetchall()    
    return render_template('productos.html', productos = data)

@app.route('/add_producto', methods=['POST'])
def add_producto():
    if request.method == 'POST':
        nombre = request.form['Nombre']
        descripcion = request.form['Descripcion']
        valor = request.form['Valor']
        categoria = request.form['Categoria']        

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO productos (nombre, descripcion, valor, categoria) VALUES (%s, %s, %s, %s)', 
                    (nombre, descripcion, valor, categoria))
        mysql.connection.commit()

        flash('Producto agregado satisfactoriamente')

        print(nombre, descripcion, valor, categoria)
        return redirect(url_for('lista_productos')) #redireccionar a página principal

@app.route('/edit_producto/<id>')
def get_producto(id):
    cur = mysql.connection.cursor() 
    cur.execute('SELECT * FROM productos WHERE id = %s', (id,)) 
    #coma después de ID para leer como tupla
    data = cur.fetchall()
    return render_template('edit-producto.html', producto = data[0])

@app.route('/update_producto/<id>', methods = ['POST'])
def update_productoo(id):
    if request.method == 'POST':
        nombre = request.form['Nombre']
        descripcion = request.form['Descripcion']
        valor = request.form['Valor']
        categoria = request.form['Categoria']      
        cur = mysql.connection.cursor()
        cur.execute(""" 
            UPDATE productos
            SET Nombre = %s,
                Descripcion = %s,
                Valor = %s,
                Categoria = %s
            WHERE id = %s
        """, (nombre, descripcion, valor, categoria, id))
        mysql.connection.commit()
        flash('Producto actualizado satisfactoriamente')
        return redirect(url_for('lista_productos')) 

@app.route('/delete_producto/<string:id>')
def delete_producto(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM productos WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Producto eliminado satisfactoriamente')
    return redirect(url_for('lista_productos'))

if __name__ == '__main__':
    app.run(port = 3000, debug = True)



