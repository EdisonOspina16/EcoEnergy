from datetime import datetime

class Dispositivo:
    def __init__(self, id, id_producto=None, fecha_registro=None, nombre_producto=None, vatios=None):
        self.id = id
        self.id_producto = id_producto
        self.fecha_registro = fecha_registro if fecha_registro else datetime.now()
        self.nombre_producto = nombre_producto
        self.vatios = vatios

    def to_dict(self):
        return {
            "id": self.id,
            "id_producto": self.id_producto,
            "fecha_registro": self.fecha_registro.strftime('%Y-%m-%d %H:%M:%S'),
            "nombre_producto": self.nombre_producto,
            "vatios": self.vatios
        }

    def __repr__(self):
        return f"<Dispositivo ID: {self.id}, Producto: {self.nombre_producto}, Vatios: {self.vatios}>"
