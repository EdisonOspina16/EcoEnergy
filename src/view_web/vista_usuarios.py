from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.controller.controladorUsuarios import registrar_usuario, obtener_usuarios, verificar_credenciales, actualizar_contraseña

vista_usuarios = Blueprint('vista_usuarios', __name__)

# Ruta para mostrar el formulario de registro
@vista_usuarios.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        contraseña = request.form['contraseña']

        exito = registrar_usuario(nombre, correo, contraseña)
        if exito:
            flash("Usuario registrado con éxito", "success")
            return redirect(url_for('vista_usuarios.login'))
        else:
            flash("Error al registrar usuario", "danger")

    return render_template('registro.html')


# Ruta para mostrar el login
@vista_usuarios.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


# Ruta para mostrar usuarios (solo como ejemplo)
@vista_usuarios.route('/usuarios')
def lista_usuarios():
    usuarios = obtener_usuarios()
    return render_template('lista_usuarios.html', usuarios=usuarios)

@vista_usuarios.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        contraseña = request.form['contraseña']

        usuario = verificar_credenciales(correo, contraseña)

        if usuario:
            flash("Inicio de sesión exitoso", "success")
            return redirect(url_for('vista_usuarios.lista_usuarios'))
        else:
            flash("Correo o contraseña incorrectos", "danger")

    return render_template('login.html')

@vista_usuarios.route('/recuperar', methods=['GET', 'POST'])
def recuperar():
    if request.method == 'POST':
        correo = request.form['correo']
        nueva_contraseña = request.form['nueva_contraseña']

        exito = actualizar_contraseña(correo, nueva_contraseña)
        if exito:
            flash("Contraseña actualizada correctamente", "success")
            return redirect(url_for('vista_usuarios.login'))
        else:
            flash("No se encontró el correo", "danger")

    return render_template('recuperar.html')
