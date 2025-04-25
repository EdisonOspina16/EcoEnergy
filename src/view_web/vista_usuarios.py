import sys
sys.path.append("src")

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from controller.controladorUsuarios import registrar_usuario, verificar_credenciales, actualizar_contraseña
from controller import controladorDispositivos as cd 

blueprint = Blueprint('vista_usuarios', __name__, "Templates")


@blueprint.route('/')
def inicio():
    usuario = session.get('usuario')
    
    if usuario:
        if usuario.get('es_admin'):
            return redirect(url_for('vista_admin.bp_admin'))
        else:
            return redirect(url_for('vista_usuarios.blueprint'))
    else:
        return render_template('inicio.html')  # Página pública si no está logueado
    

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
            # Guardamos en la sesión los datos necesarios
            session['usuario'] = usuario.to_dict()

            flash("Inicio de sesión exitoso", "success")

            # Redirigimos según si es admin o no
            if usuario.es_admin:
                return redirect(url_for('admin.inicio_admin'))
            else:
                return redirect(url_for('vista_usuarios.inicio'))

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

# -----------------------------------------
# FUNCIONES BLUEPRINTS PARA VISTA USUARIOS.     
# -----------------------------------------

@blueprint.route('/api/dispositivos', methods=['GET'])
def obtener_dispositivos():
    dispositivos = cd.obtener_todos_dispositivos()
    return jsonify(dispositivos)

@blueprint.route('/api/calcular', methods=['POST'])
def calcular_consumo():
    if not request.is_json:
        return jsonify({"error": "Formato inválido, se espera JSON"}), 400
    
    datos = request.get_json()
    dispositivos_ids = datos.get('dispositivos_ids', [])
    
    resultado, status_code = cd.calcular_consumo(dispositivos_ids)
    return jsonify(resultado), status_code