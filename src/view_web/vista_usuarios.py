import sys
sys.path.append("src")
from functools import wraps

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from controller.controladorUsuarios import registrar_usuario, verificar_credenciales, actualizar_contraseña, obtener_usuario_por_id
from controller import controladorDispositivos as cd 

blueprint = Blueprint('vista_usuarios', __name__, template_folder= "Templates")


# para que no lo deje ver el perfil si el usario no esta iniciado 
def login_requerido(f):
    @wraps(f)
    def decorador(*args, **kwargs):
        if 'usuario_id' not in session:
            flash("Debes iniciar sesión para acceder a esta página", "warning")
            return redirect(url_for('vista_usuarios.login'))
        return f(*args, **kwargs)
    return decorador


@blueprint.route('/')
def inicio():
    usuario = session.get('usuario')
    
    if usuario:
        if usuario.get('es_admin'):
            return redirect(url_for('admin.inicio_admin'))
        else:
            return render_template('inicio.html')
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
            session['usuario'] = usuario.to_dict()

            flash("Inicio de sesión exitoso", "success")

            if usuario.es_admin:
                return redirect(url_for('admin.inicio_admin'))
            else:
                return redirect(url_for('vista_usuarios.inicio'))
        
        else:
            flash("Credenciales inválidas", "danger")

    return render_template('login.html')    

# PARA CERRAR SESION
@blueprint.route('/logout')
def logout():
    session.clear()
    flash("Sesión cerrada", "info")
    return redirect(url_for('vista_usuarios.login'))


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

#perfil-------------------------
@blueprint.route('/perfil')
@login_requerido
def perfil():
    usuario_id = session.get('usuario_id')
    usuario = obtener_usuario_por_id(usuario_id) if usuario_id else None

    return render_template('perfil.html', usuario=usuario)

