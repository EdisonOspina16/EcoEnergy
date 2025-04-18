class Producto:
    def __init__(self, id, nombre, categoria, vatios):
        self.id = id
        self.nombre = nombre
        self.categoria = categoria
        self.vatios = vatios

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "vatios": self.vatios
        }

    def __repr__(self):
        return f"<Producto {self.nombre} - {self.categoria} - {self.vatios}W>"
