import sys
sys.path.append("src")

from flask import Blueprint, render_template, request, redirect, url_for, flash
from controller.controladorUsuarios import registrar_usuario, obtener_usuarios, verificar_credenciales, actualizar_contraseña

blueprint = Blueprint('vista_usuarios', __name__, "Templates")


# se define por ahora asi, pero el home seria el calculo.
@blueprint.route('/')
def inicio():
    return "<h1>Bienvenido a EcoEnergy 🌱</h1>"


# Ruta para mostrar el formulario de registro
@blueprint.route('/registro', methods=['GET', 'POST'])
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


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        contraseña = request.form['contraseña']

        usuario = verificar_credenciales(correo, contraseña)

        if usuario:
            flash("Inicio de sesión exitoso", "success")
            #return redirect(url_for('vista_usuarios.inicio'))
            return redirect('/')
        else:
            flash("Correo o contraseña incorrectos", "danger")

    return render_template('login.html')


@blueprint.route('/recuperar', methods=['GET', 'POST'])
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


# Ruta para mostrar usuarios (solo como ejemplo, puede servir para el admin)
@blueprint.route('/usuarios')
def lista_usuarios():
    usuarios = obtener_usuarios()
    return render_template('lista_usuarios.html', usuarios=usuarios)
