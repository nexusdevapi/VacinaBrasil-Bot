from datetime import datetime
# Valida a data de nascimento e retorna a idade
def validate(dia, mes, ano):
    try:
        nascimento = datetime(ano, mes, dia)
        hoje = datetime.now()

        idade = hoje.year - nascimento.year

        if (hoje.month, hoje.day) < (nascimento.month, nascimento.day):
            idade -= 1

        return idade

    except ValueError:
        return False
