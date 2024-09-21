from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'clave_secreta_para_sesiones'


USUARIO = 'empleado'
CONTRASEÑA = '$uper4utos#'


autos = []


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contraseña = request.form['contraseña']

        if usuario == USUARIO and contraseña == CONTRASEÑA:
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            flash('Datos incorrectos :(', 'error')
    
    return render_template('login.html')


@app.route('/index', methods=['GET', 'POST'])
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        idTipoAuto = request.form['idTipoAuto']
        marca = request.form['marca']
        modelo = request.form['modelo']
        descripcion = request.form['descripcion']
        precio_unitario = float(request.form['precio_unitario'])
        cantidad = int(request.form['cantidad'])
        imagen = request.form['imagen']

        
        if any(auto['idTipoAuto'] == idTipoAuto for auto in autos):
            flash('Error: El ID del auto ya existe. No se puede registrar el mismo ID.', 'error')
            return redirect(url_for('index'))

        
        auto = {
            'idTipoAuto': idTipoAuto,
            'marca': marca,
            'modelo': modelo,
            'descripcion': descripcion,
            'precio_unitario': precio_unitario,
            'cantidad': cantidad,
            'imagen': imagen
        }

        autos.append(auto)
        flash('Auto registrado con éxito.', 'success')
        return redirect(url_for('ver_autos'))

    return render_template('index.html')


@app.route('/autos')
def ver_autos():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    return render_template('autos.html', autos=autos)


@app.route('/eliminar_auto/<int:index>', methods=['POST'])
def eliminar_auto(index):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if index < len(autos):
        autos.pop(index)
        flash('Auto eliminado con éxito.', 'success')

    return redirect(url_for('ver_autos'))


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
