from data.modelo.reserva import Reserva

class DaoReservas:
    
    def get_all(self, db) -> list[Reserva]:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM reservas")

        reservas_en_db = cursor.fetchall()
        reservas: list[Reserva] = []
        
        for reserva in reservas_en_db:
            nueva_reserva = Reserva(reserva[0], reserva[1], reserva[2], reserva[3], reserva[4], reserva[5], reserva[6])
            reservas.append(nueva_reserva)

        cursor.close()
        return reservas

    def insert(self, db, nombre: str, telefono: str, email: str, fecha: str, hora: str, personas: int):
        cursor = db.cursor()
        sql = ("INSERT INTO reservas (nombre, telefono, email, fecha, hora, personas) VALUES (%s, %s, %s, %s, %s, %s)")
        data = (nombre, telefono, email, fecha, hora, personas)
        cursor.execute(sql, data)
        db.commit()
        cursor.close()

    def delete(self, db, id: int):
        cursor = db.cursor()
        sql = "DELETE FROM reservas WHERE id = %s"
        data = (id,)
        cursor.execute(sql, data)
        db.commit()
        cursor.close()

    def update(self, db, id: int, nombre: str, telefono: str, email: str, fecha: str, hora: str, personas: int):
        cursor = db.cursor()
        sql = """
            UPDATE reservas 
            SET nombre = %s, telefono = %s, email = %s, fecha = %s, hora = %s, personas = %s
            WHERE id = %s
        """
        data = (nombre, telefono, email, fecha, hora, personas, id)
        cursor.execute(sql, data)
        db.commit()
        cursor.close()

    def get_by_id(self, db, id: int) -> Reserva:
        cursor = db.cursor()
        sql = "SELECT * FROM reservas WHERE id = %s"
        cursor.execute(sql, (id,))
        reserva_en_db = cursor.fetchone()

        if reserva_en_db:
            reserva = Reserva(reserva_en_db[0], reserva_en_db[1], reserva_en_db[2], reserva_en_db[3], reserva_en_db[4], reserva_en_db[5], reserva_en_db[6])
        else:
            reserva = None

        cursor.close()
        return reserva
        
    

    
