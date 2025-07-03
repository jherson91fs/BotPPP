#!/usr/bin/env python3
"""
Utilidades para manejar tipos de datos de la base de datos
"""

from typing import Any, List, Tuple, Optional, Union

def safe_get_tuple_item(tuple_data: Optional[Tuple], index: int, default: Any = None) -> Any:
    """
    Obtiene un elemento de una tupla de forma segura
    
    Args:
        tuple_data: La tupla de la que obtener el elemento
        index: El índice del elemento
        default: Valor por defecto si no se puede obtener el elemento
    
    Returns:
        El elemento en el índice especificado o el valor por defecto
    """
    if tuple_data is None:
        return default
    
    if not isinstance(tuple_data, (list, tuple)):
        return default
    
    if index < 0 or index >= len(tuple_data):
        return default
    
    return tuple_data[index]

def safe_get_list_item(list_data: Optional[List], index: int, default: Any = None) -> Any:
    """
    Obtiene un elemento de una lista de forma segura
    
    Args:
        list_data: La lista de la que obtener el elemento
        index: El índice del elemento
        default: Valor por defecto si no se puede obtener el elemento
    
    Returns:
        El elemento en el índice especificado o el valor por defecto
    """
    if list_data is None:
        return default
    
    if not isinstance(list_data, list):
        return default
    
    if index < 0 or index >= len(list_data):
        return default
    
    return list_data[index]

def format_fecha_critica(fecha_data: Optional[Tuple]) -> str:
    """
    Formatea una fecha crítica para mostrar
    
    Args:
        fecha_data: Tupla con (descripcion, fecha)
    
    Returns:
        String formateado de la fecha crítica
    """
    if fecha_data is None:
        return "Fecha no disponible"
    
    descripcion = safe_get_tuple_item(fecha_data, 0, "Sin descripción")
    fecha = safe_get_tuple_item(fecha_data, 1, "Sin fecha")
    
    return f"📅 {descripcion} - {fecha}"

def format_oportunidad(oportunidad_data: Optional[Tuple]) -> str:
    """
    Formatea una oportunidad de práctica para mostrar
    
    Args:
        oportunidad_data: Tupla con datos de la oportunidad
    
    Returns:
        String formateado de la oportunidad
    """
    if oportunidad_data is None:
        return "Oportunidad no disponible"
    
    if not isinstance(oportunidad_data, (list, tuple)) or len(oportunidad_data) < 4:
        return f"💼 Oportunidad: {oportunidad_data}"
    
    empresa_id = safe_get_tuple_item(oportunidad_data, 0, "Sin empresa")
    descripcion = safe_get_tuple_item(oportunidad_data, 1, "Sin descripción")
    fecha_inicio = safe_get_tuple_item(oportunidad_data, 2, "Sin fecha inicio")
    fecha_fin = safe_get_tuple_item(oportunidad_data, 3, "Sin fecha fin")
    
    return f"💼 Empresa ID: {empresa_id}\n📝 Descripción: {descripcion}\n📅 Fecha: {fecha_inicio} a {fecha_fin}" 