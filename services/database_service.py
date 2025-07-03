import mysql.connector
from mysql.connector import Error

# Función para obtener la conexión a la base de datos
def get_connection():
    try:
        connection = mysql.connector.connect(
            host="184.72.67.169",  # Cambiar según el servidor
            user="admin",  # Cambiar con tu usuario
            password="Admin123!",  # Cambiar con tu contraseña
            database="TurismoWeb"  # Nombre de tu base de datos
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

# 1. Función para obtener el ID del estudiante por su código
def obtener_estudiante_id(codigo_estudiante):
    try:
        connection = get_connection()
        if connection is None:
            print("Error: No se pudo conectar a la base de datos")
            return None
            
        cursor = connection.cursor()
        query = "SELECT id FROM estudiantes WHERE codigo = %s"
        cursor.execute(query, (codigo_estudiante,))
        estudiante_id = cursor.fetchone()
        cursor.close()
        connection.close()
        
        if estudiante_id:
            return estudiante_id[0]  # Regresa el ID del estudiante
        else:
            print(f"Estudiante con código {codigo_estudiante} no encontrado")
            return None  # Si no encuentra el estudiante, regresa None
    except Exception as e:
        print(f"Error al obtener estudiante ID: {e}")
        return None

# 1.1. Función para validar estudiante completo (código, DNI, nombres)
def validar_estudiante_completo(codigo_estudiante, dni, nombres):
    try:
        connection = get_connection()
        if connection is None:
            print("Error: No se pudo conectar a la base de datos")
            return None
            
        cursor = connection.cursor()
        query = """
            SELECT id, codigo, dni, nombre 
            FROM estudiantes 
            WHERE codigo = %s AND dni = %s AND nombre = %s
        """
        cursor.execute(query, (codigo_estudiante, dni, nombres))
        estudiante = cursor.fetchone()
        cursor.close()
        connection.close()
        
        if estudiante:
            return {
                'id': estudiante[0],
                'codigo': estudiante[1],
                'dni': estudiante[2],
                'nombres': estudiante[3],
                'apellidos': '',  # No existe en la tabla actual
                'carrera': 'Ingeniería de Sistemas',  # Valor por defecto
                'ciclo': '8vo'  # Valor por defecto
            }
        else:
            print(f"Estudiante no encontrado o datos incorrectos")
            return None
    except Exception as e:
        print(f"Error al validar estudiante: {e}")
        return None

# 2. Función para obtener el ID de la empresa por su nombre
def obtener_empresa_id(empresa_nombre):
    try:
        connection = get_connection()
        if connection is None:
            print("Error: No se pudo conectar a la base de datos")
            return None
            
        cursor = connection.cursor()
        query = "SELECT id FROM empresas WHERE nombre = %s"
        cursor.execute(query, (empresa_nombre,))
        resultado = cursor.fetchone()
        cursor.close()
        connection.close()
        
        if resultado:
            return resultado[0]  # Regresa el ID de la empresa
        else:
            print(f"Empresa '{empresa_nombre}' no encontrada")
            return None
    except Exception as e:
        print(f"Error al obtener empresa ID: {e}")
        return None

# 2.1. Función para obtener empresa por RUC
def obtener_empresa_por_ruc(ruc):
    try:
        connection = get_connection()
        if connection is None:
            print("Error: No se pudo conectar a la base de datos")
            return None
            
        cursor = connection.cursor()
        # Como no hay columna RUC, usamos el nombre como identificador
        query = "SELECT id, nombre, direccion, contacto_email FROM empresas WHERE nombre = %s"
        cursor.execute(query, (ruc,))
        resultado = cursor.fetchone()
        cursor.close()
        connection.close()
        
        if resultado:
            return {
                'id': resultado[0],
                'nombre': resultado[1],
                'direccion': resultado[2],
                'contacto_email': resultado[3],
                'ruc': ruc  # Usar el RUC como nombre temporal
            }
        else:
            print(f"Empresa con nombre {ruc} no encontrada")
            return None
    except Exception as e:
        print(f"Error al obtener empresa por RUC: {e}")
        return None

# 2.2. Función para crear nueva empresa
def crear_empresa(ruc, nombre, direccion, contacto_email):
    try:
        connection = get_connection()
        if connection is None:
            print("Error: No se pudo conectar a la base de datos")
            return None
            
        cursor = connection.cursor()
        query = """
            INSERT INTO empresas (nombre, direccion, contacto_email) 
            VALUES (%s, %s, %s)
        """
        cursor.execute(query, (nombre, direccion, contacto_email))
        connection.commit()
        empresa_id = cursor.lastrowid
        cursor.close()
        connection.close()
        
        print(f"Empresa creada con ID: {empresa_id}")
        return empresa_id
    except Exception as e:
        print(f"Error al crear empresa: {e}")
        return None

# 3. Función para registrar una solicitud de carta
def registrar_solicitud_carta(estudiante_id, empresa_id, fecha_solicitud, ruta_pdf=None):
    try:
        connection = get_connection()
        if connection is None:
            print("Error: No se pudo conectar a la base de datos")
            return False
        cursor = connection.cursor()
        if ruta_pdf:
            query = """
                INSERT INTO solicitudes_carta (estudiante_id, empresa_id, fecha_solicitud, ruta_pdf)
                VALUES (%s, %s, %s, %s)
            """
            values = (estudiante_id, empresa_id, fecha_solicitud, ruta_pdf)
        else:
            query = """
                INSERT INTO solicitudes_carta (estudiante_id, empresa_id, fecha_solicitud)
                VALUES (%s, %s, %s)
            """
            values = (estudiante_id, empresa_id, fecha_solicitud)
        cursor.execute(query, values)
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Exception as e:
        print(f"Error al registrar solicitud de carta: {e}")
        return False

# 4. Función para consultar las horas acumuladas por el estudiante
def consultar_horas(codigo_estudiante):
    try:
        connection = get_connection()
        if connection is None:
            print("Error: No se pudo conectar a la base de datos")
            return 0
            
        cursor = connection.cursor()
        query = """
            SELECT SUM(horas) 
            FROM practicas
            JOIN estudiantes_empresas ON practicas.estudiante_empresa_id = estudiantes_empresas.id
            JOIN estudiantes ON estudiantes.id = estudiantes_empresas.estudiante_id
            WHERE estudiantes.codigo = %s
        """
        cursor.execute(query, (codigo_estudiante,))
        resultado = cursor.fetchone()
        cursor.close()
        connection.close()
        
        if resultado and resultado[0] is not None:
            return resultado[0]
        else:
            return 0
    except Exception as e:
        print(f"Error al consultar horas: {e}")
        return 0

# 5. Función para consultar las empresas en las que el estudiante realizó prácticas
def consultar_empresas(codigo_estudiante):
    try:
        connection = get_connection()
        if connection is None:
            print("Error: No se pudo conectar a la base de datos")
            return []
            
        cursor = connection.cursor()
        query = """
            SELECT empresas.nombre 
            FROM empresas
            JOIN estudiantes_empresas ON empresas.id = estudiantes_empresas.empresa_id
            JOIN estudiantes ON estudiantes.id = estudiantes_empresas.estudiante_id
            WHERE estudiantes.codigo = %s
        """
        cursor.execute(query, (codigo_estudiante,))
        empresas = cursor.fetchall()
        cursor.close()
        connection.close()
        return [empresa[0] for empresa in empresas] if empresas else []
    except Exception as e:
        print(f"Error al consultar empresas: {e}")
        return []

# 6. Función para obtener todas las fechas críticas (que están pendientes)
def consultar_fechas_criticas():
    try:
        connection = get_connection()
        if connection is None:
            print("Error: No se pudo conectar a la base de datos")
            return []
            
        cursor = connection.cursor()
        query = "SELECT descripcion, fecha FROM fechas_criticas WHERE estado = 'pendiente'"
        cursor.execute(query)
        fechas_criticas = cursor.fetchall()
        cursor.close()
        connection.close()
        return fechas_criticas
    except Exception as e:
        print(f"Error al consultar fechas críticas: {e}")
        return []

# 7. Función para obtener todas las oportunidades de prácticas activas
def consultar_oportunidades_practicas():
    try:
        connection = get_connection()
        if connection is None:
            print("Error: No se pudo conectar a la base de datos")
            return []
            
        cursor = connection.cursor()
        query = "SELECT empresa_id, descripcion, fecha_inicio, fecha_fin FROM oportunidades_practicas WHERE estado = 'activo'"
        cursor.execute(query)
        oportunidades = cursor.fetchall()
        cursor.close()
        connection.close()
        return oportunidades
    except Exception as e:
        print(f"Error al consultar oportunidades: {e}")
        return []

# 8. Función para consultar todas las cartas generadas por un estudiante
def consultar_cartas_generadas(estudiante_id):
    try:
        connection = get_connection()
        if connection is None:
            print("Error: No se pudo conectar a la base de datos")
            return []
        cursor = connection.cursor()
        query = """
            SELECT empresas.nombre, solicitudes_carta.ruta_pdf
            FROM solicitudes_carta
            JOIN empresas ON solicitudes_carta.empresa_id = empresas.id
            WHERE solicitudes_carta.estudiante_id = %s
        """
        cursor.execute(query, (estudiante_id,))
        cartas = cursor.fetchall()
        cursor.close()
        connection.close()
        return cartas
    except Exception as e:
        print(f"Error al consultar cartas generadas: {e}")
        return []

# 9. Función para verificar si ya existe una carta para un estudiante y empresa
def existe_carta_para_estudiante_y_empresa(estudiante_id, empresa_id):
    try:
        connection = get_connection()
        if connection is None:
            print("Error: No se pudo conectar a la base de datos")
            return False
        cursor = connection.cursor()
        query = """
            SELECT id FROM solicitudes_carta
            WHERE estudiante_id = %s AND empresa_id = %s
        """
        cursor.execute(query, (estudiante_id, empresa_id))
        existe = cursor.fetchone() is not None
        cursor.close()
        connection.close()
        return existe
    except Exception as e:
        print(f"Error al verificar carta existente: {e}")
        return False
