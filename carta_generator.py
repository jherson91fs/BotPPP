#!/usr/bin/env python3
"""
Generador de Cartas de Presentación para Prácticas Pre Profesionales
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
import os
from services.database_service import consultar_cartas_generadas, existe_carta_para_estudiante_y_empresa
from telegram import Update
from telegram.ext import CallbackContext

def generar_carta_presentacion(estudiante_data, empresa_data, fecha_actual=None):
    """
    Genera una carta de presentación en PDF y la guarda en static/cartas/
    
    Args:
        estudiante_data: Diccionario con datos del estudiante
        empresa_data: Diccionario con datos de la empresa
        fecha_actual: Fecha actual (opcional)
    
    Returns:
        str: Ruta del archivo PDF generado
    """
    
    if fecha_actual is None:
        fecha_actual = datetime.now().strftime("%d de %B de %Y")
    
    # Crear carpeta si no existe
    output_dir = os.path.join('static', 'cartas')
    os.makedirs(output_dir, exist_ok=True)
    
    # Crear nombre del archivo
    filename = f"carta_presentacion_{estudiante_data['codigo']}_{empresa_data['nombre'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    filepath = os.path.join(output_dir, filename)
    
    # Crear el documento
    doc = SimpleDocTemplate(filepath, pagesize=A4)
    story = []
    
    # Obtener estilos
    styles = getSampleStyleSheet()
    
    # Estilos personalizados
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.darkblue
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=12,
        alignment=TA_JUSTIFY,
        leading=18
    )
    
    signature_style = ParagraphStyle(
        'Signature',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=12,
        alignment=TA_LEFT,
        leading=16
    )
    
    # Encabezado de la universidad
    story.append(Paragraph("UNIVERSIDAD PERUANA UNION", title_style))
    story.append(Paragraph("FACULTAD DE INGENIERÍA DE SISTEMAS", title_style))
    story.append(Paragraph("DEPARTAMENTO ACADÉMICO DE INGENIERÍA DE SISTEMAS", title_style))
    story.append(Spacer(1, 20))
    
    # Título del documento
    story.append(Paragraph("CARTA DE PRESENTACIÓN", title_style))
    story.append(Spacer(1, 30))
    
    # Fecha
    story.append(Paragraph(f"Lima, {fecha_actual}", normal_style))
    story.append(Spacer(1, 20))
    
    # Datos de la empresa
    story.append(Paragraph(f"<b>Señores:</b>", normal_style))
    story.append(Paragraph(f"<b>{empresa_data['nombre']}</b>", normal_style))
    story.append(Paragraph(f"<b>RUC: {empresa_data['ruc']}</b>", normal_style))
    story.append(Paragraph(f"<b>Dirección: {empresa_data['direccion']}</b>", normal_style))
    story.append(Spacer(1, 20))
    
    # Gerente general
    if empresa_data.get('gerente_general'):
        story.append(Paragraph(f"<b>Atención: {empresa_data['gerente_general']} (Gerente General)</b>", normal_style))
    
    # Saludo
    story.append(Paragraph("Estimados señores:", normal_style))
    story.append(Spacer(1, 15))
    
    # Cuerpo de la carta
    cuerpo_carta = f"""
    Por medio de la presente, tengo a bien presentar al estudiante <b>{estudiante_data['nombres']} {estudiante_data.get('apellidos','')}</b>, 
    quien cursa el {estudiante_data.get('ciclo','')} ciclo de la carrera de <b>{estudiante_data.get('carrera','')}</b> en nuestra Facultad, 
    con código universitario <b>{estudiante_data['codigo']}</b> y DNI <b>{estudiante_data['dni']}</b>.
    """
    story.append(Paragraph(cuerpo_carta, normal_style))
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("""
    El estudiante mencionado desea realizar sus <b>Prácticas Pre Profesionales</b> en su distinguida empresa, 
    con el objetivo de aplicar los conocimientos adquiridos durante su formación académica y desarrollar 
    competencias profesionales en un entorno laboral real.
    """, normal_style))
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("""
    Durante su formación, el estudiante ha demostrado un excelente rendimiento académico y ha desarrollado 
    habilidades técnicas y competencias profesionales que le permitirán contribuir de manera efectiva 
    a los objetivos de su organización.
    """, normal_style))
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("""
    Por lo tanto, solicitamos a ustedes considerar favorablemente la solicitud del estudiante para realizar 
    sus prácticas pre profesionales en su empresa, brindándole la oportunidad de aplicar sus conocimientos 
    y desarrollar nuevas competencias en un entorno profesional.
    """, normal_style))
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("""
    Agradecemos de antemano su atención y quedamos a la espera de su respuesta favorable.
    """, normal_style))
    story.append(Spacer(1, 30))
    
    # Despedida
    story.append(Paragraph("Atentamente,", normal_style))
    story.append(Spacer(1, 40))
    
    # Firma
    story.append(Paragraph("_________________________", signature_style))
    story.append(Paragraph("<b>Dr. Dani Levano</b>", signature_style))
    story.append(Paragraph("<b>Director del Departamento Académico</b>", signature_style))
    story.append(Paragraph("<b>Ingeniería de Sistemas</b>", signature_style))
    story.append(Paragraph("<b>Universidad Nacional de Ingeniería</b>", signature_style))
    story.append(Spacer(1, 20))
    
    # Información de contacto
    story.append(Paragraph("Información de contacto:", normal_style))
    story.append(Paragraph("Teléfono: (01) 481-1070", signature_style))
    story.append(Paragraph("Email: sistemas@uni.edu.pe", signature_style))
    story.append(Paragraph("Dirección: Av. Túpac Amaru 210, Rímac, Lima", signature_style))
    
    # Construir el PDF
    doc.build(story)
    
    return filepath

def generar_carta_estudiante(estudiante_data, empresa_data, fecha_actual=None):
    """
    Genera una carta de presentación desde la perspectiva del estudiante
    
    Args:
        estudiante_data: Diccionario con datos del estudiante
        empresa_data: Diccionario con datos de la empresa
        fecha_actual: Fecha actual (opcional)
    
    Returns:
        str: Ruta del archivo PDF generado
    """
    
    if fecha_actual is None:
        fecha_actual = datetime.now().strftime("%d de %B de %Y")
    
    # Crear nombre del archivo
    filename = f"carta_estudiante_{estudiante_data['codigo']}_{empresa_data['ruc']}.pdf"
    
    # Crear el documento
    doc = SimpleDocTemplate(filename, pagesize=A4)
    story = []
    
    # Obtener estilos
    styles = getSampleStyleSheet()
    
    # Estilos personalizados
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.darkblue
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=12,
        alignment=TA_JUSTIFY,
        leading=18
    )
    
    header_style = ParagraphStyle(
        'Header',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=12,
        alignment=TA_LEFT,
        leading=16
    )
    
    # Encabezado del estudiante
    story.append(Paragraph(f"<b>{estudiante_data['nombres']} {estudiante_data['apellidos']}</b>", header_style))
    story.append(Paragraph(f"Código: {estudiante_data['codigo']}", header_style))
    story.append(Paragraph(f"DNI: {estudiante_data['dni']}", header_style))
    story.append(Paragraph(f"Carrera: {estudiante_data['carrera']}", header_style))
    story.append(Paragraph(f"Ciclo: {estudiante_data['ciclo']}", header_style))
    story.append(Paragraph("Universidad Nacional de Ingeniería", header_style))
    story.append(Paragraph("Facultad de Ingeniería Industrial y de Sistemas", header_style))
    story.append(Spacer(1, 20))
    
    # Fecha
    story.append(Paragraph(f"Lima, {fecha_actual}", normal_style))
    story.append(Spacer(1, 20))
    
    # Datos de la empresa
    story.append(Paragraph(f"<b>Señores:</b>", normal_style))
    story.append(Paragraph(f"<b>{empresa_data['nombre']}</b>", normal_style))
    story.append(Paragraph(f"<b>RUC: {empresa_data['ruc']}</b>", normal_style))
    story.append(Paragraph(f"<b>Dirección: {empresa_data['direccion']}</b>", normal_style))
    story.append(Spacer(1, 20))
    
    # Gerente general
    if empresa_data.get('gerente_general'):
        story.append(Paragraph(f"<b>Atención: {empresa_data['gerente_general']} (Gerente General)</b>", normal_style))
    
    # Saludo
    story.append(Paragraph("Estimados señores:", normal_style))
    story.append(Spacer(1, 15))
    
    # Cuerpo de la carta
    story.append(Paragraph(f"""
    Me dirijo a ustedes para expresar mi interés en realizar mis <b>Prácticas Pre Profesionales</b> en su distinguida empresa. 
    Soy {estudiante_data['nombres']} {estudiante_data['apellidos']}, estudiante del {estudiante_data['ciclo']} ciclo 
    de la carrera de <b>{estudiante_data['carrera']}</b> en la Universidad Nacional de Ingeniería.
    """, normal_style))
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("""
    Durante mi formación académica, he desarrollado sólidos conocimientos en mi área de estudio y he participado 
    en diversos proyectos que me han permitido aplicar la teoría en situaciones prácticas. Considero que su empresa 
    ofrece un excelente entorno para continuar mi desarrollo profesional.
    """, normal_style))
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("""
    Estoy comprometido con el aprendizaje continuo y tengo la capacidad de adaptarme rápidamente a nuevos entornos 
    y tecnologías. Mi objetivo es contribuir de manera efectiva a los proyectos de su organización mientras 
    adquiero experiencia valiosa en el campo profesional.
    """, normal_style))
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("""
    Agradezco de antemano su consideración y quedo a la espera de una respuesta favorable. 
    Estoy disponible para una entrevista personal en el momento que consideren conveniente.
    """, normal_style))
    story.append(Spacer(1, 30))
    
    # Despedida
    story.append(Paragraph("Atentamente,", normal_style))
    story.append(Spacer(1, 40))
    
    # Firma del estudiante
    story.append(Paragraph("_________________________", header_style))
    story.append(Paragraph(f"<b>{estudiante_data['nombres']} {estudiante_data['apellidos']}</b>", header_style))
    story.append(Paragraph(f"<b>Estudiante de {estudiante_data['carrera']}</b>", header_style))
    story.append(Paragraph("<b>Universidad Nacional de Ingeniería</b>", header_style))
    story.append(Spacer(1, 20))
    
    # Información de contacto del estudiante
    story.append(Paragraph("Información de contacto:", normal_style))
    story.append(Paragraph("Email: [email del estudiante]", header_style))
    story.append(Paragraph("Teléfono: [teléfono del estudiante]", header_style))
    
    # Construir el PDF
    doc.build(story)
    
    return filename

if __name__ == "__main__":
    # Ejemplo de uso
    estudiante_ejemplo = {
        'codigo': '20210001',
        'dni': '12345678',
        'nombres': 'Juan Carlos',
        'apellidos': 'Pérez García',
        'carrera': 'Ingeniería de Sistemas',
        'ciclo': '8vo'
    }
    
    empresa_ejemplo = {
        'nombre': 'Tech Solutions S.A.C.',
        'ruc': '20123456789',
        'direccion': 'Av. Arequipa 123, Lima',
        'gerente_general': 'Dr. Juan Pérez',
        'contacto_email': 'contacto@techsolutions.com'
    }
    
    # Supón que tienes estudiante_id y empresa_id
    if existe_carta_para_estudiante_y_empresa(estudiante_id, empresa_id):
        update.message.reply_text("❌ Ya has generado una carta para esta empresa. No puedes generar otra.")
    # Si no existe, continúa con la generación
    
    # Generar carta
    archivo = generar_carta_presentacion(estudiante_ejemplo, empresa_ejemplo)
    print(f"Carta generada: {archivo}")

def recibir_codigo_estudiante(update: Update, context: CallbackContext):
    # ... código existente ...
    if context.user_data.get('ultima_opcion') == "6. Ver mis cartas generadas":
        estudiante_id = obtener_estudiante_id(codigo_estudiante)
        cartas = consultar_cartas_generadas(estudiante_id)
        if cartas:
            mensaje = "Tus cartas generadas:\n"
            for nombre_empresa, ruta_pdf in cartas:
                mensaje += f"• {nombre_empresa}: {os.path.basename(ruta_pdf) if ruta_pdf else 'Sin PDF'}\n"
            update.message.reply_text(mensaje)
        else:
            update.message.reply_text("No tienes cartas generadas.")
