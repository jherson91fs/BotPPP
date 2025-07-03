from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, Filters, ConversationHandler, CallbackQueryHandler
from services.database_service import registrar_solicitud_carta, consultar_horas, consultar_empresas, consultar_fechas_criticas, consultar_oportunidades_practicas, obtener_estudiante_id, obtener_empresa_id, existe_carta_para_estudiante_y_empresa, consultar_cartas_generadas
from type_helpers import format_fecha_critica, format_oportunidad
import os
from datetime import datetime
from carta_generator import generar_carta_presentacion

# Estados de la conversación
MENU, NOMBRE, CODIGO, DNI, EMPRESA, RUC_EMPRESA, DIRECCION = range(7)

# Función de inicio
def start(update: Update, context: CallbackContext):
    """Inicia la conversación y muestra el menú principal."""
    keyboard = [
        ['1. Solicitar Carta de Presentación'],
        ['2. Consultar Horas'],
        ['3. Consultar Empresas'],
        ['4. Ver Fechas Críticas'],
        ['5. Ver Oportunidades de Prácticas'],
        ['6. Ver mis cartas generadas']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    
    update.message.reply_text(
        "¡Hola! Soy el chatbot de Prácticas Pre Profesionales.\n"
        "¿Qué deseas hacer?",
        reply_markup=reply_markup
    )
    return MENU

def menu_handler(update: Update, context: CallbackContext):
    """Maneja la selección del menú principal."""
    text = update.message.text
    
    # Asegurar que context.user_data existe
    if context.user_data is None:
        context.user_data = {}
    
    if "1. Solicitar Carta de Presentación" in text:
        # Limpiar datos previos
        context.user_data.clear()
        update.message.reply_text(
            "Perfecto, vamos a solicitar tu carta de presentación.\n"
            "Primero, ingresa tu nombre completo:",
            reply_markup=ReplyKeyboardRemove()
        )
        return NOMBRE
    
    elif "2. Consultar Horas" in text:
        # Limpiar datos previos y guardar la opción seleccionada
        context.user_data.clear()
        context.user_data['ultima_opcion'] = "2. Consultar Horas"
        update.message.reply_text(
            "Para consultar tus horas, ingresa tu código de estudiante:",
            reply_markup=ReplyKeyboardRemove()
        )
        return CODIGO
    
    elif "3. Consultar Empresas" in text:
        # Limpiar datos previos y guardar la opción seleccionada
        context.user_data.clear()
        context.user_data['ultima_opcion'] = "3. Consultar Empresas"
        update.message.reply_text(
            "Para consultar tus empresas, ingresa tu código de estudiante:",
            reply_markup=ReplyKeyboardRemove()
        )
        return CODIGO
    
    elif "4. Ver Fechas Críticas" in text:
        return mostrar_fechas_criticas(update, context)
    
    elif "5. Ver Oportunidades de Prácticas" in text:
        return mostrar_oportunidades(update, context)
    
    elif "🔄 Realizar otra consulta" in text:
        return start(update, context)
    
    elif "🏠 Salir" in text:
        update.message.reply_text(
            "¡Hasta luego! Usa /start cuando quieras volver a usar el bot.",
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END
    
    elif "📄 Descargar carta" in text:
        ruta_pdf = context.user_data.get('ruta_pdf')
        if ruta_pdf and os.path.exists(ruta_pdf):
            with open(ruta_pdf, 'rb') as pdf_file:
                update.message.reply_document(
                    document=pdf_file,
                    filename=os.path.basename(ruta_pdf),
                    caption="📄 Aquí tienes tu carta de presentación."
                )
        else:
            update.message.reply_text("❌ No se encontró la carta para descargar. Por favor, genera una nueva.")
        return mostrar_menu_final(update, context)
    
    elif "6. Ver mis cartas generadas" in text or "📑 6. Ver mis cartas generadas" in text:
        context.user_data.clear()
        context.user_data['ultima_opcion'] = "6. Ver mis cartas generadas"
        update.message.reply_text(
            "Para ver tus cartas generadas, ingresa tu código de estudiante:",
            reply_markup=ReplyKeyboardRemove()
        )
        return CODIGO
    
    else:
        keyboard = [
            ['📝 1. Solicitar Carta de Presentación'],
            ['📊 2. Consultar Horas'],
            ['🏢 3. Consultar Empresas'],
            ['📅 4. Ver Fechas Críticas'],
            ['💼 5. Ver Oportunidades de Prácticas'],
            ['📑 6. Ver mis cartas generadas']
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        update.message.reply_text(
            "Por favor, selecciona una opción válida del menú.",
            reply_markup=reply_markup
        )
        return MENU

def recibir_nombre(update: Update, context: CallbackContext):
    """Recibe el nombre del estudiante."""
    if context.user_data is None:
        context.user_data = {}
    context.user_data['nombre'] = update.message.text
    update.message.reply_text("Ahora ingresa tu código de estudiante:")
    return CODIGO

def recibir_codigo_estudiante(update: Update, context: CallbackContext):
    """Recibe y valida el código de estudiante."""
    codigo_estudiante = update.message.text
    print(f"Recibido código de estudiante: {codigo_estudiante}")  # Debug
    
    try:
        estudiante_id = obtener_estudiante_id(codigo_estudiante)
        print(f"Estudiante ID obtenido: {estudiante_id}")  # Debug
        
        if estudiante_id:
            if context.user_data is None:
                context.user_data = {}
            context.user_data['codigo'] = codigo_estudiante
            context.user_data['estudiante_id'] = estudiante_id

            # Si la última opción fue ver cartas generadas, mostrar cartas
            if context.user_data.get('ultima_opcion') == "6. Ver mis cartas generadas":
                cartas = consultar_cartas_generadas(estudiante_id)
                if cartas:
                    mensaje = "Tus cartas generadas:\n"
                    keyboard = []
                    for nombre_empresa, ruta_pdf in cartas:
                        if ruta_pdf:
                            keyboard.append([InlineKeyboardButton(
                                f"{nombre_empresa}", callback_data=f"descargar_carta|{ruta_pdf}"
                            )])
                        else:
                            mensaje += f"• {nombre_empresa}: Sin PDF\n"
                    if keyboard:
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        update.message.reply_text(mensaje + "Selecciona una empresa para descargar la carta:", reply_markup=reply_markup)
                    else:
                        update.message.reply_text(mensaje)
                else:
                    update.message.reply_text("No tienes cartas generadas.")
                return mostrar_menu_final(update, context)

            # Verificar si estamos en el flujo de carta o consulta
            if context.user_data.get('nombre'):
                # Flujo de carta de presentación
                update.message.reply_text(f"✅ Código de estudiante {codigo_estudiante} encontrado.")
                update.message.reply_text("Ahora ingresa tu DNI:")
                return DNI
            else:
                # Flujo de consulta
                return procesar_consulta(update, context, codigo_estudiante)
        else:
            update.message.reply_text(
                "❌ Código de estudiante no encontrado. Por favor, verifica e ingresa nuevamente:"
            )
            return CODIGO
            
    except Exception as e:
        print(f"Error al consultar estudiante: {e}")
        update.message.reply_text(
            "❌ Error al consultar la base de datos. Por favor, intenta nuevamente:"
        )
        return CODIGO

def procesar_consulta(update: Update, context: CallbackContext, codigo_estudiante):
    """Procesa las consultas de horas y empresas."""
    # Asegurar que context.user_data existe
    if context.user_data is None:
        context.user_data = {}
    
    # Determinar qué consulta hacer basándose en el contexto
    ultima_opcion = context.user_data.get('ultima_opcion', '')
    if "2. Consultar Horas" in ultima_opcion:
        return consultar_horas_estudiante(update, context, codigo_estudiante)
    elif "3. Consultar Empresas" in ultima_opcion:
        return consultar_empresas_estudiante(update, context, codigo_estudiante)
    else:
        update.message.reply_text("Opción no válida.")
        return ConversationHandler.END

def consultar_horas_estudiante(update: Update, context: CallbackContext, codigo_estudiante):
    """Consulta las horas del estudiante."""
    try:
        horas = consultar_horas(codigo_estudiante)
        update.message.reply_text(f"📊 Has acumulado {horas} horas de prácticas.")
        return mostrar_menu_final(update, context)
    except Exception as e:
        print(f"Error al consultar horas: {e}")
        update.message.reply_text("❌ Error al consultar las horas. Por favor, intenta nuevamente.")
        return ConversationHandler.END

def consultar_empresas_estudiante(update: Update, context: CallbackContext, codigo_estudiante):
    """Consulta las empresas del estudiante."""
    try:
        empresas = consultar_empresas(codigo_estudiante)
        if empresas:
            empresas_texto = "\n".join([f"• {empresa}" for empresa in empresas])
            update.message.reply_text(f"🏢 Has realizado prácticas en las siguientes empresas:\n{empresas_texto}")
        else:
            update.message.reply_text("📝 No tienes empresas registradas.")
        return mostrar_menu_final(update, context)
    except Exception as e:
        print(f"Error al consultar empresas: {e}")
        update.message.reply_text("❌ Error al consultar las empresas. Por favor, intenta nuevamente.")
        return ConversationHandler.END

def recibir_dni(update: Update, context: CallbackContext):
    """Recibe el DNI del estudiante."""
    if context.user_data is None:
        context.user_data = {}
    context.user_data['dni'] = update.message.text
    update.message.reply_text("Ingresa la razón social de la empresa donde solicitarás la carta:")
    return EMPRESA

def recibir_empresa(update: Update, context: CallbackContext):
    """Recibe la empresa."""
    if context.user_data is None:
        context.user_data = {}
    context.user_data['empresa'] = update.message.text
    update.message.reply_text("Ingresa el RUC de la empresa:")
    return RUC_EMPRESA

def recibir_ruc_empresa(update: Update, context: CallbackContext):
    """Recibe el RUC de la empresa."""
    if context.user_data is None:
        context.user_data = {}
    context.user_data['ruc'] = update.message.text
    update.message.reply_text("Ingresa la dirección de la empresa:")
    return DIRECCION

def recibir_direccion(update: Update, context: CallbackContext):
    """Recibe la dirección y genera la carta."""
    if context.user_data is None:
        context.user_data = {}
    context.user_data['direccion'] = update.message.text
    
    try:
        # Registrar la solicitud en la base de datos
        estudiante_id = context.user_data['estudiante_id']
        empresa_id = obtener_empresa_id(context.user_data['empresa'])
        
        if empresa_id is None:
            update.message.reply_text("❌ Empresa no encontrada. Por favor, verifica el nombre de la empresa.")
            return EMPRESA
        
        # Validar que no exista ya una carta para este estudiante y empresa
        # if existe_carta_para_estudiante_y_empresa(estudiante_id, empresa_id):
        #     update.message.reply_text("❌ Ya has generado una carta para esta empresa. No puedes generar otra.")
        #     return mostrar_menu_final(update, context)
        
        fecha_solicitud = "2025-01-02"  # Fecha actual (se puede mejorar)
        
        if registrar_solicitud_carta(estudiante_id, empresa_id, fecha_solicitud):
            print("Llamando a generar_carta_presentacion...")
            try:
                # Construir los diccionarios con los datos necesarios
                estudiante_data = {
                    'codigo': context.user_data['codigo'],
                    'nombres': context.user_data['nombre'],
                    'dni': context.user_data['dni'],
                    # Agrega otros campos si los tienes, como 'apellidos', 'carrera', 'ciclo'
                }
                empresa_data = {
                    'nombre': context.user_data['empresa'],
                    'ruc': context.user_data['ruc'],
                    'direccion': context.user_data['direccion'],
                }

                ruta_pdf = generar_carta_presentacion(estudiante_data, empresa_data)
                registrar_solicitud_carta(estudiante_id, empresa_id, fecha_solicitud, ruta_pdf)
                print(f"PDF generado en: {ruta_pdf}")
                context.user_data['ruta_pdf'] = ruta_pdf
                update.message.reply_text(
                    "✅ ¡Tu carta de presentación ha sido generada con éxito!\n"
                    "Recibirás una notificación cuando esté lista."
                )
                return mostrar_menu_final(update, context)
            except Exception as e:
                print(f"Error al generar PDF: {e}")
                update.message.reply_text("❌ Error al generar la carta. Por favor, intenta nuevamente.")
                return ConversationHandler.END
        else:
            update.message.reply_text("❌ Error al registrar la solicitud. Por favor, intenta nuevamente.")
            return ConversationHandler.END
        
    except Exception as e:
        print(f"Error al generar carta: {e}")
        update.message.reply_text("❌ Error al generar la carta. Por favor, intenta nuevamente.")
        return ConversationHandler.END

def mostrar_fechas_criticas(update: Update, context: CallbackContext):
    """Muestra las fechas críticas."""
    try:
        fechas = consultar_fechas_criticas()
        if fechas:
            fechas_texto = "\n".join([format_fecha_critica(fecha) for fecha in fechas])
            update.message.reply_text(f"📋 Fechas críticas pendientes:\n{fechas_texto}")
        else:
            update.message.reply_text("✅ No hay fechas críticas pendientes.")
        return mostrar_menu_final(update, context)
    except Exception as e:
        print(f"Error al consultar fechas críticas: {e}")
        update.message.reply_text("❌ Error al consultar las fechas críticas.")
        return ConversationHandler.END

def mostrar_oportunidades(update: Update, context: CallbackContext):
    """Muestra las oportunidades de prácticas."""
    try:
        oportunidades = consultar_oportunidades_practicas()
        if oportunidades:
            for oportunidad in oportunidades:
                mensaje = format_oportunidad(oportunidad)
                update.message.reply_text(mensaje)
        else:
            update.message.reply_text("📝 No hay oportunidades de prácticas activas.")
        return mostrar_menu_final(update, context)
    except Exception as e:
        print(f"Error al consultar oportunidades: {e}")
        update.message.reply_text("❌ Error al consultar las oportunidades.")
        return ConversationHandler.END

def mostrar_menu_final(update: Update, context: CallbackContext):
    """Muestra el menú final después de completar una operación."""
    keyboard = []
    # Solo mostrar el botón si hay carta generada
    if context.user_data.get('ruta_pdf'):
        keyboard.append(['📄 Descargar carta'])
    keyboard.append(['🔄 Realizar otra consulta'])
    keyboard.append(['🏠 Salir'])
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    
    update.message.reply_text(
        "¿Deseas realizar otra acción?",
        reply_markup=reply_markup
    )
    return MENU

def cancel(update: Update, context: CallbackContext):
    """Cancela la conversación."""
    update.message.reply_text(
        "Operación cancelada. Usa /start para comenzar de nuevo.",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

def descargar_carta_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    data = query.data
    if data.startswith("descargar_carta|"):
        ruta_pdf = data.split("|", 1)[1]
        if ruta_pdf and os.path.exists(ruta_pdf):
            with open(ruta_pdf, 'rb') as pdf_file:
                query.message.reply_document(
                    document=pdf_file,
                    filename=os.path.basename(ruta_pdf),
                    caption="📄 Aquí tienes tu carta de presentación."
                )
        else:
            query.message.reply_text("❌ No se encontró el archivo PDF para esta carta.")
    return mostrar_menu_final(update, context)

def main():
    """Función principal del bot."""
    # Reemplaza por tu token de BotFather
    updater = Updater("7364353585:AAFvGKyxzg6UULJoDmhS2rwVTOPdGfOsPoY", use_context=True)
    dispatcher = updater.dispatcher

    # Crear el ConversationHandler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            MENU: [MessageHandler(Filters.text & ~Filters.command, menu_handler)],
            NOMBRE: [MessageHandler(Filters.text & ~Filters.command, recibir_nombre)],
            CODIGO: [MessageHandler(Filters.text & ~Filters.command, recibir_codigo_estudiante)],
            DNI: [MessageHandler(Filters.text & ~Filters.command, recibir_dni)],
            EMPRESA: [MessageHandler(Filters.text & ~Filters.command, recibir_empresa)],
            RUC_EMPRESA: [MessageHandler(Filters.text & ~Filters.command, recibir_ruc_empresa)],
            DIRECCION: [MessageHandler(Filters.text & ~Filters.command, recibir_direccion)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        allow_reentry=True
    )

    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(CallbackQueryHandler(descargar_carta_callback, pattern=r"^descargar_carta\|"))

    # Inicia el bot
    print("Bot iniciado...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
