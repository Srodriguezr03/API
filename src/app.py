from flask import Flask, render_template, request, jsonify
import pyodbc
from config import config
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configuración de la conexión a SQL Server
conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=172.23.134.163;"
    "DATABASE=Universidad;"
    "UID=Full;"
    "PWD=full123456"
)

# Ruta para obtener datos (GET)
@app.route('/get', methods=['GET'])
def obtener_alumnos():
    try:
        # Establecer la conexión a la base de datos
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Consulta SQL para obtener datos de la tabla Alumnos
        sql = "SELECT AlumnoID, AsignaturaID, Corte, Calificacion FROM Notas"
        cursor.execute(sql)

        # Obtener todos los resultados
        datos = cursor.fetchall()

        # Convertir los resultados a un formato JSON y devolver la respuesta
        respuesta = [{'AlumnoID': row.AlumnoID,
                      'AsignaturaID': row.AsignaturaID,
                      'Corte': row.Corte,
                      'Calificacion': row.Calificacion} for row in datos]

        return jsonify(respuesta)

    except Exception as ex:
        return "Error en la conexión a la base de datos."

# Ruta para mostrar el formulario de registro (GET)
@app.route('/register', methods=['GET'])
def mostrar_formulario():
    return render_template('form.html')

@app.route('/post', methods=['POST'])
def agregar_alumno():
    try:
        # Obtener datos del formulario
        nuevo_alumno = {
            'AlumnoID': request.json['AlumnoID'],
            'AsignaturaID': request.json['AsignaturaID'],
            'Corte': request.json['Corte'],
            'Calificacion': request.json['Calificacion'],
                    }

        # Establecer la conexión a la base de datos
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Insertar nuevo registro en la tabla Alumnos
        sql = "INSERT INTO Notas (AlumnoID, AsignaturaID, Corte, Calificacion) VALUES (?, ?, ?, ?)"
        cursor.execute(sql, nuevo_alumno['AlumnoID'], nuevo_alumno['AsignaturaID'], nuevo_alumno['Corte'],
                       nuevo_alumno['Calificacion'])

        # Confirmar la transacción
        conn.commit()

        # Cerrar el cursor y la conexión
        cursor.close()
        conn.close()

        return "Registro agregado exitosamente."

    except KeyError as e:
        return f"Error en la solicitud. La clave '{e.args[0]}' no está presente."
    except Exception as ex:
        return f"Error al agregar el registro: {str(ex)}"

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run(host='0.0.0.0', port=5000, debug=True)
