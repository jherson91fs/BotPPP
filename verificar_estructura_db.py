#!/usr/bin/env python3
"""
Script para verificar la estructura de la base de datos
"""

from services.database_service import get_connection

def verificar_estructura():
    """Verifica la estructura de las tablas en la base de datos"""
    
    try:
        connection = get_connection()
        if connection is None:
            print("❌ Error: No se pudo conectar a la base de datos")
            return False
            
        cursor = connection.cursor()
        
        # Verificar tablas existentes
        cursor.execute("SHOW TABLES")
        tablas = cursor.fetchall()
        
        print("📋 Tablas existentes en la base de datos:")
        for tabla in tablas:
            print(f"  - {tabla[0]}")
        
        print("\n" + "="*50)
        
        # Verificar estructura de cada tabla
        for tabla in tablas:
            nombre_tabla = tabla[0]
            print(f"\n🔍 Estructura de la tabla '{nombre_tabla}':")
            
            cursor.execute(f"DESCRIBE {nombre_tabla}")
            columnas = cursor.fetchall()
            
            for columna in columnas:
                print(f"  - {columna[0]} ({columna[1]}) - {columna[2]}")
        
        cursor.close()
        connection.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Error al verificar estructura: {e}")
        return False

def crear_tablas_si_no_existen():
    """Crea las tablas necesarias si no existen"""
    
    try:
        connection = get_connection()
        if connection is None:
            print("❌ Error: No se pudo conectar a la base de datos")
            return False
            
        cursor = connection.cursor()
        
        # Crear tabla estudiantes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS estudiantes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                codigo VARCHAR(20) UNIQUE NOT NULL,
                dni VARCHAR(20) NOT NULL,
                nombres VARCHAR(100) NOT NULL,
                apellidos VARCHAR(100) NOT NULL,
                carrera VARCHAR(100) NOT NULL,
                ciclo VARCHAR(20) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ Tabla 'estudiantes' creada/verificada")
        
        # Crear tabla empresas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS empresas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                ruc VARCHAR(20) UNIQUE NOT NULL,
                nombre VARCHAR(200) NOT NULL,
                direccion TEXT,
                contacto_email VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ Tabla 'empresas' creada/verificada")
        
        # Crear tabla solicitudes_carta
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS solicitudes_carta (
                id INT AUTO_INCREMENT PRIMARY KEY,
                estudiante_id INT NOT NULL,
                empresa_id INT NOT NULL,
                fecha_solicitud DATE NOT NULL,
                estado ENUM('pendiente', 'aprobada', 'rechazada') DEFAULT 'pendiente',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id),
                FOREIGN KEY (empresa_id) REFERENCES empresas(id)
            )
        """)
        print("✅ Tabla 'solicitudes_carta' creada/verificada")
        
        # Crear tabla fechas_criticas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS fechas_criticas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                descripcion VARCHAR(200) NOT NULL,
                fecha DATE NOT NULL,
                estado ENUM('pendiente', 'completada') DEFAULT 'pendiente',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ Tabla 'fechas_criticas' creada/verificada")
        
        # Crear tabla oportunidades_practicas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS oportunidades_practicas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                empresa_id INT NOT NULL,
                descripcion TEXT NOT NULL,
                fecha_inicio DATE NOT NULL,
                fecha_fin DATE NOT NULL,
                estado ENUM('activo', 'inactivo') DEFAULT 'activo',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (empresa_id) REFERENCES empresas(id)
            )
        """)
        print("✅ Tabla 'oportunidades_practicas' creada/verificada")
        
        connection.commit()
        cursor.close()
        connection.close()
        
        print("\n✅ Todas las tablas han sido creadas/verificadas exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error al crear tablas: {e}")
        return False

def main():
    """Función principal"""
    print("🔍 Verificando estructura de la base de datos...")
    
    # Verificar estructura actual
    verificar_estructura()
    
    print("\n" + "="*50)
    print("🔧 Creando/verificando tablas necesarias...")
    
    # Crear tablas si no existen
    if crear_tablas_si_no_existen():
        print("\n✅ Base de datos configurada correctamente")
        
        # Verificar estructura final
        print("\n" + "="*50)
        print("🔍 Estructura final de la base de datos:")
        verificar_estructura()
    else:
        print("\n❌ Error al configurar la base de datos")

if __name__ == "__main__":
    main() 