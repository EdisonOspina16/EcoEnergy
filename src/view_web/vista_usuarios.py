import sys
sys.path.append("src")
from functools import wraps

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
    return render_template('inicio.html')
    

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
# FUNCIONES PARA EL agregar-ADMIN.
# -----------------------------------------

@blueprint.route('/')
def index():
    productos, dispositivos = obtener_productos_y_dispositivos()

    productos_por_categoria = {}
    for producto in productos:
        categoria = producto['categoria']
        productos_por_categoria.setdefault(categoria, []).append(producto)

    total_vatios = sum(d['vatios'] for d in dispositivos if d['vatios'])
    consumo_diario_kwh = round(total_vatios * 24 / 1000, 2) if total_vatios else None
    consumo_mensual_kwh = round(total_vatios * 24 * 30 / 1000, 2) if total_vatios else None

    return render_template(
        'index.html',
        productos=productos,
        productos_por_categoria=productos_por_categoria,
        dispositivos=dispositivos,
        total_vatios=total_vatios,
        consumo_diario_kwh=consumo_diario_kwh,
        consumo_mensual_kwh=consumo_mensual_kwh
    )


@blueprint.route('/agregar_producto', methods=['POST'])
def ruta_agregar_producto():
    nombre = request.form.get('product_name')
    categoria = request.form.get('product_category')
    vatios = request.form.get('product_watts')

    if not nombre or not categoria or not vatios:
        flash('Por favor complete todos los campos', 'error')
        return redirect(url_for('vista_usuarios.index'))

    try:
        vatios = int(vatios)
    except ValueError:
        flash('El valor de vatios debe ser un número entero', 'error')
        return redirect(url_for('vista_usuarios.index'))

    agregar_producto(nombre, categoria, vatios)
    flash(f'Producto "{nombre}" añadido correctamente', 'success')
    return redirect(url_for('vista_usuarios.index'))


@blueprint.route('/eliminar_producto/<int:producto_id>', methods=['POST'])
def ruta_eliminar_producto(producto_id):
    eliminar_producto_y_dispositivos(producto_id)
    flash('Producto eliminado correctamente', 'success')
    return redirect(url_for('vista_usuarios.index'))


@blueprint.route('/agregar_dispositivo', methods=['POST'])
def ruta_agregar_dispositivo():
    agregar_dispositivo()
    return redirect(url_for('vista_usuarios.index'))


@blueprint.route('/eliminar_dispositivo/<int:dispositivo_id>', methods=['POST'])
def ruta_eliminar_dispositivo(dispositivo_id):
    eliminar_dispositivo(dispositivo_id)
    return redirect(url_for('vista_usuarios.index'))


@blueprint.route('/actualizar_dispositivo/<int:dispositivo_id>', methods=['POST'])
def ruta_actualizar_dispositivo(dispositivo_id):
    id_producto = request.form.get(f'dispositivo-{dispositivo_id}')
    if not id_producto:
        flash('Debe seleccionar un producto para el dispositivo', 'error')
        return redirect(url_for('vista_usuarios.index'))

    actualizar_dispositivo(dispositivo_id, id_producto)
    return redirect(url_for('vista_usuarios.index'))

#perfil-------------------------
@blueprint.route('/perfil')
@login_requerido
def perfil():
    usuario_id = session.get('usuario_id')
    usuario = obtener_usuario_por_id(usuario_id) if usuario_id else None

    return render_template('perfil.html', usuario=usuario)