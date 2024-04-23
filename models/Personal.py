class Personal:
    def __init__(self, nombre_completo, puesto, correo_electronico, telefono):
       
       self.nombre_completo = nombre_completo
       self.puesto = puesto
       self.correo_electronico = correo_electronico
       self.telefono = telefono

    def toDBCollection(self):
        return{
            'nombre_completo' :self.nombre_completo,
            'puesto': self.puesto,
            'correo_electronico' : self.correo_electronico,
            'telefono' : self.telefono
        } 