from flask import Flask, request, jsonify
from services.database_service import consultar_horas, consultar_empresas, registrar_solicitud_carta, consultar_fechas_criticas, consultar_oportunidades_practicas, obtener_estudiante_id, obtener_empresa_id
from carta_generator import generar_carta_presentacion

app = Flask(__name__)

@app.route('/horas/<codigo_estudiante>', methods=['GET'])
def obtener_horas(codigo_estudiante):
    horas = consultar_horas(codigo_estudiante)  # Llama a la función de base de datos
    return jsonify({'codigo_estudiante': codigo_estudiante, 'horas': horas})

@app.route('/empresas/<codigo_estudiante>', methods=['GET'])
def obtener_empresas(codigo_estudiante):
    empresas = consultar_empresas(codigo_estudiante)  # Llama a la función de base de datos
    return jsonify({'codigo_estudiante': codigo_estudiante, 'empresas': empresas})

@app.route('/fechas_criticas', methods=['GET'])
def obtener_fechas_criticas():
    fechas = consultar_fechas_criticas()  # Llama a la función de base de datos
    return jsonify({'fechas_criticas': fechas})

@app.route('/oportunidades', methods=['GET'])
def obtener_oportunidades():
    oportunidades = consultar_oportunidades_practicas()  # Llama a la función de base de datos
    return jsonify({'oportunidades': oportunidades})


@app.route('/solicitar_carta', methods=['POST'])
def solicitar_carta():
    # Aquí tomarías los datos del estudiante y la empresa desde el request
    # y luego los pasarías a la función `registrar_solicitud_carta`
    data = request.get_json()
    estudiante_id = obtener_estudiante_id(data['codigo_estudiante'])
    empresa_id = obtener_empresa_id(data['empresa'])
    fecha_solicitud = data['fecha_solicitud']
    registrar_solicitud_carta(estudiante_id, empresa_id, fecha_solicitud)
    return jsonify({"mensaje": "Solicitud de carta registrada con éxito."})


if __name__ == '__main__':
    app.run(debug=True, port=5001)

