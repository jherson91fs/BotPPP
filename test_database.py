#!/usr/bin/env python3
"""
Script de prueba para verificar la conexión a la base de datos y las funciones principales
"""

from services.database_service import (
    get_connection, 
    obtener_estudiante_id, 
    consultar_horas, 
    consultar_empresas,
    consultar_fechas_criticas,
    consultar_oportunidades_practicas
)

def test_connection():
    """Prueba la conexión a la base de datos"""
    print("🔍 Probando conexión a la base de datos...")
    connection = get_connection()
    if connection:
        print("✅ Conexión exitosa a la base de datos")
        connection.close()
        return True
    else:
        print("❌ Error al conectar a la base de datos")
        return False

def test_estudiante():
    """Prueba la búsqueda de un estudiante"""
    print("\n🔍 Probando búsqueda de estudiante...")
    
    # Probar con un código que probablemente no existe
    codigo_test = "12345"
    estudiante_id = obtener_estudiante_id(codigo_test)
    
    if estudiante_id:
        print(f"✅ Estudiante encontrado con ID: {estudiante_id}")
    else:
        print(f"❌ Estudiante con código {codigo_test} no encontrado")
    
    # Probar con códigos comunes
    codigos_comunes = ["20200001", "20210001", "20220001", "20230001", "20240001"]
    for codigo in codigos_comunes:
        estudiante_id = obtener_estudiante_id(codigo)
        if estudiante_id:
            print(f"✅ Estudiante encontrado: {codigo} -> ID: {estudiante_id}")
            break
    else:
        print("❌ No se encontraron estudiantes con códigos comunes")

def test_consultas():
    """Prueba las consultas principales"""
    print("\n🔍 Probando consultas...")
    
    # Probar consulta de horas
    try:
        horas = consultar_horas("12345")
        print(f"📊 Horas consultadas: {horas}")
    except Exception as e:
        print(f"❌ Error al consultar horas: {e}")
    
    # Probar consulta de empresas
    try:
        empresas = consultar_empresas("12345")
        print(f"🏢 Empresas consultadas: {empresas}")
    except Exception as e:
        print(f"❌ Error al consultar empresas: {e}")
    
    # Probar consulta de fechas críticas
    try:
        fechas = consultar_fechas_criticas()
        print(f"📅 Fechas críticas: {fechas}")
    except Exception as e:
        print(f"❌ Error al consultar fechas críticas: {e}")
    
    # Probar consulta de oportunidades
    try:
        oportunidades = consultar_oportunidades_practicas()
        print(f"💼 Oportunidades: {oportunidades}")
    except Exception as e:
        print(f"❌ Error al consultar oportunidades: {e}")

def main():
    """Función principal de pruebas"""
    print("🚀 Iniciando pruebas de la base de datos...")
    
    # Probar conexión
    if not test_connection():
        print("\n❌ No se puede continuar sin conexión a la base de datos")
        print("Verifica que:")
        print("1. MySQL esté ejecutándose")
        print("2. Las credenciales en config.py sean correctas")
        print("3. La base de datos 'ppp' exista")
        return
    
    # Probar funciones
    test_estudiante()
    test_consultas()
    
    print("\n✅ Pruebas completadas")

if __name__ == "__main__":
    main() 