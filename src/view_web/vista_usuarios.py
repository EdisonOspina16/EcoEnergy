import sys
sys.path.append("src")
from functools import wraps

<<<<<<< HEAD
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from controller.controladorUsuarios import (
    registrar_usuario, 
    obtener_usuarios, 
    verificar_credenciales, 
    actualizar_contraseña, 
    obtener_usuario_por_id
)
from controller.controladorDispositivos import (
    obtener_productos_y_dispositivos,
    agregar_producto,
    eliminar_producto_y_dispositivos,
    agregar_dispositivo,
    eliminar_dispositivo,
    actualizar_dispositivo
)
=======
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from controller.controladorUsuarios import registrar_usuario, verificar_credenciales, actualizar_contraseña
from controller import controladorDispositivos as cd 
>>>>>>> 67df6a085e60bbe0174c7a69998e32c64f1e486f

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

# se define por ahora asi, pero el home seria el calculo.
@blueprint.route('/')
def inicio():
    usuario = session.get('usuario')
    
    if usuario:
        if usuario.get('es_admin'):
            return redirect(url_for('admin.inicio_admin'))
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

# PARA GUARDAR EL INICIO DE SESION TAMBIEN
        if usuario:
<<<<<<< HEAD
            session['usuario_id'] = usuario['id']
            session['usuario_nombre'] = usuario['nombre']
            session['usuario_correo'] = usuario['correo']
            flash("Inicio de sesión exitoso", "success")
            return redirect('/')
        else:
            flash("Credenciales inválidas", "danger")

    return render_template('login.html')    

# PARA CERRAR SESION
@blueprint.route('/logout')
def logout():
    session.clear()
    flash("Sesión cerrada", "info")
    return redirect(url_for('vista_usuarios.login'))



=======
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
>>>>>>> 67df6a085e60bbe0174c7a69998e32c64f1e486f


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

<<<<<<< HEAD
#perfil-------------------------
@blueprint.route('/perfil')
@login_requerido
def perfil():
    usuario_id = session.get('usuario_id')
    usuario = obtener_usuario_por_id(usuario_id) if usuario_id else None

    return render_template('perfil.html', usuario=usuario)
=======
@blueprint.route('/api/calcular', methods=['POST'])
def calcular_consumo():
    if not request.is_json:
        return jsonify({"error": "Formato inválido, se espera JSON"}), 400
    
    datos = request.get_json()
    dispositivos_ids = datos.get('dispositivos_ids', [])
    
    resultado, status_code = cd.calcular_consumo(dispositivos_ids)
    return jsonify(resultado), status_code
>>>>>>> 67df6a085e60bbe0174c7a69998e32c64f1e486f
