#!/usr/bin/env python3
"""
Script para agregar estudiantes de prueba a la base de datos
"""

from services.database_service import get_connection

def agregar_estudiantes_prueba():
    """Agrega estudiantes de prueba a la base de datos"""
    
    estudiantes_prueba = [
        {
            'codigo': '20210001',
            'dni': '12345678',
            'nombres': 'Juan Carlos',
            'apellidos': 'Pérez García',
            'carrera': 'Ingeniería de Sistemas',
            'ciclo': '8vo'
        },
        {
            'codigo': '20210002',
            'dni': '23456789',
            'nombres': 'María Elena',
            'apellidos': 'Rodríguez López',
            'carrera': 'Ingeniería de Sistemas',
            'ciclo': '7mo'
        },
        {
            'codigo': '20210003',
            'dni': '34567890',
            'nombres': 'Carlos Alberto',
            'apellidos': 'González Silva',
            'carrera': 'Ingeniería de Sistemas',
            'ciclo': '9no'
        },
        {
            'codigo': '20210004',
            'dni': '45678901',
            'nombres': 'Ana Sofía',
            'apellidos': 'Martínez Torres',
            'carrera': 'Ingeniería de Sistemas',
            'ciclo': '6to'
        },
        {
            'codigo': '20210005',
            'dni': '56789012',
            'nombres': 'Luis Fernando',
            'apellidos': 'Herrera Vargas',
            'carrera': 'Ingeniería de Sistemas',
            'ciclo': '8vo'
        }
    ]
    
    try:
        connection = get_connection()
        if connection is None:
            print("❌ Error: No se pudo conectar a la base de datos")
            return False
            
        cursor = connection.cursor()
        
        # Verificar si la tabla existe
        cursor.execute("SHOW TABLES LIKE 'estudiantes'")
        if not cursor.fetchone():
            print("❌ La tabla 'estudiantes' no existe")
            return False
        
        # Agregar estudiantes
        for estudiante in estudiantes_prueba:
            # Verificar si el estudiante ya existe
            cursor.execute("SELECT id FROM estudiantes WHERE codigo = %s", (estudiante['codigo'],))
            if cursor.fetchone():
                print(f"⚠️  Estudiante {estudiante['codigo']} ya existe, saltando...")
                continue
            
                    # Insertar nuevo estudiante
        query = """
            INSERT INTO estudiantes (codigo, dni, nombre, correo, direccion)
            VALUES (%s, %s, %s, %s, %s)
        """
        values = (
            estudiante['codigo'],
            estudiante['dni'],
            estudiante['nombres'],
            f"{estudiante['nombres'].lower().replace(' ', '.')}@uni.edu.pe",
            "Lima, Perú"
        )
            
            cursor.execute(query, values)
            print(f"✅ Estudiante {estudiante['codigo']} agregado: {estudiante['nombres']} {estudiante['apellidos']}")
        
        connection.commit()
        cursor.close()
        connection.close()
        
        print("\n✅ Estudiantes de prueba agregados exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error al agregar estudiantes: {e}")
        return False

def agregar_empresas_prueba():
    """Agrega empresas de prueba a la base de datos"""
    
    empresas_prueba = [
        {
            'ruc': '20123456789',
            'nombre': 'Tech Solutions S.A.C.',
            'direccion': 'Av. Arequipa 123, Lima',
            'contacto_email': 'contacto@techsolutions.com'
        },
        {
            'ruc': '20234567890',
            'nombre': 'Digital Innovations E.I.R.L.',
            'direccion': 'Jr. de la Unión 456, Lima',
            'contacto_email': 'info@digitalinnovations.com'
        },
        {
            'ruc': '20345678901',
            'nombre': 'Software Development Corp.',
            'direccion': 'Av. Javier Prado 789, San Isidro',
            'contacto_email': 'hr@softwaredev.com'
        }
    ]
    
    try:
        connection = get_connection()
        if connection is None:
            print("❌ Error: No se pudo conectar a la base de datos")
            return False
            
        cursor = connection.cursor()
        
        # Verificar si la tabla existe
        cursor.execute("SHOW TABLES LIKE 'empresas'")
        if not cursor.fetchone():
            print("❌ La tabla 'empresas' no existe")
            return False
        
        # Agregar empresas
        for empresa in empresas_prueba:
            # Verificar si la empresa ya existe
            cursor.execute("SELECT id FROM empresas WHERE ruc = %s", (empresa['ruc'],))
            if cursor.fetchone():
                print(f"⚠️  Empresa {empresa['ruc']} ya existe, saltando...")
                continue
            
                    # Insertar nueva empresa
        query = """
            INSERT INTO empresas (nombre, direccion, contacto_email)
            VALUES (%s, %s, %s)
        """
        values = (
            empresa['nombre'],
            empresa['direccion'],
            empresa['contacto_email']
        )
            
            cursor.execute(query, values)
            print(f"✅ Empresa {empresa['ruc']} agregada: {empresa['nombre']}")
        
        connection.commit()
        cursor.close()
        connection.close()
        
        print("\n✅ Empresas de prueba agregadas exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error al agregar empresas: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 Agregando datos de prueba a la base de datos...")
    
    # Agregar estudiantes
    print("\n📚 Agregando estudiantes de prueba...")
    if agregar_estudiantes_prueba():
        print("✅ Estudiantes agregados correctamente")
    else:
        print("❌ Error al agregar estudiantes")
    
    # Agregar empresas
    print("\n🏢 Agregando empresas de prueba...")
    if agregar_empresas_prueba():
        print("✅ Empresas agregadas correctamente")
    else:
        print("❌ Error al agregar empresas")
    
    print("\n🎉 Proceso completado!")
    print("\n📋 Datos de prueba disponibles:")
    print("Estudiantes:")
    print("- Código: 20210001, DNI: 12345678, Nombres: Juan Carlos")
    print("- Código: 20210002, DNI: 23456789, Nombres: María Elena")
    print("- Código: 20210003, DNI: 34567890, Nombres: Carlos Alberto")
    print("- Código: 20210004, DNI: 45678901, Nombres: Ana Sofía")
    print("- Código: 20210005, DNI: 56789012, Nombres: Luis Fernando")
    print("\nEmpresas:")
    print("- RUC: 20123456789, Nombre: Tech Solutions S.A.C.")
    print("- RUC: 20234567890, Nombre: Digital Innovations E.I.R.L.")
    print("- RUC: 20345678901, Nombre: Software Development Corp.")

if __name__ == "__main__":
    main() 