import re

# obtendo números da faixa etária
def extrair_idade(idade_texto):
    if not idade_texto:
        return None, None

    idade_texto = str(idade_texto).lower()

    if 'ao nascer' in idade_texto:
        return 0, 0

    numeros = re.findall(r'\d+', idade_texto)

    if len(numeros) >= 2:
        return int(numeros[0]), int(numeros[1])
    elif len(numeros) == 1:
        return int(numeros[0]), None
    else:
        return None, None
