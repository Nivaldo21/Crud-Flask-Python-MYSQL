from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

# initializations
app = Flask(__name__)

# Mysql Connection
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_DB'] = 'ia'
app.config['MYSQL_PORT'] = 3308
mysql = MySQL(app)

# settings
app.secret_key = "mysecretkey"

# routes
@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM trabajadores')
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', contacts = data)

@app.route('/add_trabajador', methods=['POST'])
def add_trabajador():
    if request.method == 'POST':
        nombre = request.form['nombre']
        salario = request.form['salario']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO trabajadores (nombre, salario) VALUES (%s,%s)", (nombre, salario))
        mysql.connection.commit()
        flash('Trabajador Añadido con exito')
        return redirect(url_for('Index'))

@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM trabajadores WHERE id = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-trabajador.html', contact = data[0])

@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        salario = request.form['salario']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE trabajadores
            SET nombre = %s,
                salario = %s
            WHERE id = %s
        """, (nombre, salario, id))
        flash('Trabajador editado con exito')
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_trabajador(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM trabajadores WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Trabajador eliminado con exito')
    return redirect(url_for('Index'))

# starting the app
if __name__ == "__main__":
    app.run(port=3000, debug=True)
