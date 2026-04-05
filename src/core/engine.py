from data_handler.loader import *
def pega_vacina(idade, periodo, resultado, *filtro):
   
    data = carregar_json(f'vacinas_{periodo}.json')
    for x in data:    
        if periodo == 'crianca' or periodo == 'idoso':
            resultado += f"{x[filtro[2]]} - {x[filtro[3]]}\n"

        elif x[filtro[0]] <= idade <= x[filtro[1]]:
            resultado += f"{x[filtro[2]]} - {x[filtro[3]]}\n"

        else:
            pass
    return resultado

def vacinas(idade):
    tabela = ''
    tabela += f"{'Vacina'} - {'Dose'}\n"
    tabela += "-" * 20 + "\n"
    filtros = ['idade_min', 'idade_max', 'vacina', 'dose']

    if type(idade) == str:
        #Handler para vacinas das gestantes
        if idade.startswith('semana_'):
            semana = int(idade.split("_")[1])
            data = carregar_json('vacinas_gestante.json')
            if semana < 20:
                for x in data:
                    if x["idade_min"] == None:
                        tabela += f"{x['vacina']} - {x['dose']}\n"
                    else:
                        pass
            else:
                for x in data:
                    if x["idade_min"] == None:
                        pass
                    elif semana >= x["idade_min"]:
                        tabela += f"{x['vacina']} - {x['dose']}\n"
        
        #Handler do commando /procurar
        else:
            vacina = carregar_todos(idade.split('_')[1])
            tabela = ''
            
            for x in vacina:
                if x['grupo'] == 'crianca':
                    if x['idade'] != 0:
                        tabela += f'A vacina {x['nome']} deve ser tomada com {int(x['idade'])} meses\n'
                    else:
                        tabela += f'A vacina {x['nome']} deve ser tomada ao nascer\n'
                elif x['grupo'] == 'gestante':
                    if x['idade'] == None:
                        tabela += f'A vacina {x['nome']} deve ser tomada no início da gestação\n'
                    else:
                        tabela += f'A vacina {x['nome']} deve ser tomada com {int(x['idade'])} semanas de gestação\n'
                else:
                    tabela += f'A vacina {x['nome']} deve ser tomada a partir dos {int(x['idade'])} anos\n'
        return tabela
    else:
        pass

    #Verifica as vacinas para idosos
    if idade >= 60:
        tabela = pega_vacina(idade, 'idoso', tabela, *filtros)
    #Verifica as vacinas para adultos
    elif idade >= 25:
       tabela = pega_vacina(idade, 'adulto', tabela, *filtros)
    #Verifica as vacinas para adolescentes
    elif idade >= 9:
        tabela = pega_vacina(idade, 'adolescente', tabela, *filtros)
    #Verifica as vacinas para crianças
    elif idade < 9:
        tabela = pega_vacina(idade, 'crianca', tabela, *filtros)      
    return tabela