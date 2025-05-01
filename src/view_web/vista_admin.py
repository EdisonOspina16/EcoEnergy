from flask import Blueprint, request, jsonify, render_template, session, redirect, flash, url_for
from functools import wraps
from controller import controladorDispositivos as cd

from SecretConfig import GEMINI_PROMPT

bp_admin = Blueprint('admin', __name__, template_folder= "Templates")

# para que no lo deje ver el perfil si el usario no esta iniciado 
def login_requerido(f):
    @wraps(f)
    def decorador(*args, **kwargs):
        if not session.get('usuario'):               
            flash("Debes iniciar sesión para acceder a esta página", "warning")
            return redirect(url_for('vista_usuarios.login'))
        return f(*args, **kwargs)
    return decorador

@bp_admin.route('/admin')
@login_requerido
def inicio_admin():
    productos = cd.obtener_dispositivos()
    return render_template('admin.html', productos = productos)


@bp_admin.route('/api/dispositivos', methods=['POST'])
def crear_dispositivo_route():

    nombre = request.form.get('nombre_producto')
    categoria = request.form.get('categoria')
    vatios = request.form.get('vatios')

    if not nombre or not categoria or not vatios:
        return jsonify({"error": "Faltan datos requeridos: nombre_producto, categoria o vatios"}), 400

    try:
        vatios= float(vatios)
    except ValueError:
        return jsonify({"error": "El campo 'vatios' debe ser un número"}), 400
    
    resultado, status = cd.crear_dispositivo(nombre, categoria, vatios)
    return jsonify(resultado), status


@bp_admin.route('/api/dispositivos/<int:id>', methods=['PUT'])
def actualizar_dispositivo_route(id):
    if not request.is_json:
        return jsonify({"error": "Se espera un JSON válido"}), 400

    datos = request.get_json()
    nombre = datos.get('nombre_producto')
    categoria = datos.get('categoria')
    vatios = datos.get('vatios')

    resultado, status = cd.actualizar_dispositivo(id, nombre, categoria, vatios)
    return jsonify(resultado), status


@bp_admin.route('/api/dispositivos/<int:id>', methods=['POST','DELETE'])
def eliminar_dispositivo_route(id):
    resultado, status = cd.eliminar_dispositivo(id)
    return jsonify(resultado), status


@bp_admin.route('/api/dispositivos', methods=['GET'])
def obtener_dispositivos_route():
    dispositivos = cd.obtener_dispositivos()
    return jsonify(dispositivos), 200


@bp_admin.route('/api/dispositivos/<int:id>', methods=['GET'])
def obtener_dispositivo_por_id_route(id):
    dispositivo = cd.obtener_dispositivo_por_id(id)
    if dispositivo:
        return jsonify(dispositivo), 200
    return jsonify({"error": "Dispositivo no encontrado"}), 404


@bp_admin.route('/api/dispositivos/consumo', methods=['POST'])
def calcular_consumo_route():
    data = request.get_json()  
    if not data:
        return jsonify({"error": "JSON inválido, se espera clave 'devices'"}), 400

    dispositivos = data['devices']
    resultado, status = cd.calcular_consumo(dispositivos)
    return jsonify(resultado), status

@bp_admin.route('/dispositivos', methods=['GET'])
def mostrar_dispositivos():
    productos_por_categoria = cd.obtener_dispositivos_por_categoria()
    return render_template('inicio.html', products_by_category=productos_por_categoria)

@bp_admin.route('/clasificar_texto', methods=['POST'])
def clasificar_texto_route():
    data = request.get_json()
    if not data:
        return jsonify({"error": "JSON inválido, se espera clave 'text'"}), 400

    texto = data['text'] + ' ' + GEMINI_PROMPT
    try:
        resultado = cd.clasificar_texto(texto)
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500