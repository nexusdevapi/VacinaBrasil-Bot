from datetime import datetime
# Valida a data de nascimento e retorna a idade
def validate(dia, mes, ano):
    try:
        nascimento = datetime(ano, mes, dia)
        today = datetime.now()
        
        if ano == datetime.now().year:
            age = today.month - mes
            return age
        else:
            age = today.year - nascimento.year
            if (today.month, today.day) < (nascimento.month, nascimento.day):
                age -= 1
            return age
    except ValueError:
        return False