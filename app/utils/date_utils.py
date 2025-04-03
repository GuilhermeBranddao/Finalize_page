from datetime import datetime, date
from app.utils.constants import HOLIDAYS

def is_valid_date(selected_date):
    """Verifica se a data é válida."""
    if selected_date.weekday() in (5, 6):  # Sábado e domingo
        return False
    if selected_date > datetime.now().date():  # Futuro
        return False
    if selected_date in HOLIDAYS:  # Feriados
        return False
    return True

def format_date(date_obj):
    """Formata uma data para string no formato desejado."""
    return date_obj.strftime("%Y-%m-%d")
