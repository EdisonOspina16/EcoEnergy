from flask import Blueprint, request, jsonify, render_template
from controller import controladorDispositivos as cd

bp_admin = Blueprint('admin', __name__,  url_prefix='/admin')


@bp_admin.route('/admin')
def inicio_admin():

    return render_template('admin.html')


@bp_admin.route('/api/dispositivos', methods=['POST'])
def crear_dispositivo_route():

    nombre = request.form.get('nombre_producto')
    categoria = request.form.get('categoria_producto')
    vatios = request.form.get('consumo_watts')

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
    if request.method == 'POST':
        # Interpretar que POST es una solicitud de eliminación desde formulario
        resultado, status = cd.eliminar_dispositivo(id)
        return jsonify(resultado), status
    elif request.method == 'DELETE':
        # Si de verdad viene DELETE, también lo atiendes
        resultado, status = cd.eliminar_dispositivo(id)
        return jsonify(resultado), status


@bp_admin.route('/api/dispositivos', methods=['GET'])
def obtener_dispositivos_route():
    dispositivos = cd.obtener_todos_dispositivos()
    return jsonify(dispositivos), 200


@bp_admin.route('/api/dispositivos/<int:id>', methods=['GET'])
def obtener_dispositivo_por_id_route(id):
    dispositivo = cd.obtener_dispositivo_por_id(id)
    if dispositivo:
        return jsonify(dispositivo), 200
    return jsonify({"error": "Dispositivo no encontrado"}), 404


@bp_admin.route('/api/dispositivos/consumo', methods=['POST'])
def calcular_consumo_route():
    if not request.is_json:
        return jsonify({"error": "Se espera un JSON válido"}), 400

    datos = request.get_json()
    dispositivos_ids = datos.get('ids', [])

    resultado, status = cd.calcular_consumo(dispositivos_ids)
    return jsonify(resultado), status

@bp_admin.route('/dispositivos', methods=['GET'])
def mostrar_dispositivos():
    productos_por_categoria = cd.obtener_dispositivos_por_categoria()
    return render_template('inicio.html', products_by_category=productos_por_categoria)