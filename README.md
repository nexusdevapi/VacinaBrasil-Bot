# Aprendizado por Projeto Integrado (API) - Vacina Brasil Bot 💉

<p align="center">
  <img src="assets/img/banner_vacina_brasil.png">
</p>

Assistente virtual para Telegram que informa vacinas recomendadas com base na idade do usuário ou na semana de gestação.

Projeto desenvolvido durante o **1º semestre de 2026** por estudantes do curso de **Análise e Desenvolvimento de Sistemas da FATEC São José dos Campos**.

O projeto segue a metodologia ágil **Scrum**, com foco em desenvolvimento colaborativo e organização de tarefas.

## Índice
* [🎯 Objetivo do Projeto](#-objetivo-do-projeto)
* [👥 Equipe](#equipe)
* [🎓 Orientadores](#-orientadores)
* [📋 Requisitos Não Funcionais](#requisitos-não-funcionais)
* [🧰 Tecnologias Utilizadas](#tecnologias-utilizadas)
* [📌 Product Backlog](#product-backlog)
* [📊 Registro das Sprints](#registro-das-sprints)
* [📖 Manual do Usuário](#-manual-do-usuário)
* [🛠️ Manual de Instalação](#-manual-de-instalação)

## 🎯 Objetivo do Projeto

Desenvolver um assistente virtual para Telegram que utilize dados de portais públicos oficiais de saúde sobre vacinação para informar o cidadão sobre:

* Calendário vacinal para diferentes faixas etárias (crianças, adultos e idosos);
* Consulta de vacinas recomendadas a partir da data de nascimento do usuário;
* Consulta de vacinas recomendadas para gestantes de acordo com a semana de gestação.

Não deve haver persistência dos dados através de bancos de dados.

## 👥 Equipe

| Nome                   | Função        | LinkedIn & GitHub                                                                                              |
| :--------------------- | :-----------: | :-----------------------------------------------------------------------------------------------------------: |
| Nicolas Fonseca Meira   | Scrum Master | [<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/linkedin/linkedin-original.svg" width="24"/>](https://www.linkedin.com/in/nicolas-fonseca-60386130b/) [![GitHub Badge](https://img.shields.io/badge/GitHub-111217?style=flat-square&logo=github&logoColor=white)](https://github.com/NicolasFonsecaM) |
| Caio Gabriel Ferreira de Paula |  Product Owner | [<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/linkedin/linkedin-original.svg" width="24"/>](https://www.linkedin.com/in/) [![GitHub Badge](https://img.shields.io/badge/GitHub-111217?style=flat-square&logo=github&logoColor=white)](https://github.com/caiogabrielfp-cpu) |
| Gabriel Yudi Fujimoto  | Scrum Team    | [<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/linkedin/linkedin-original.svg" width="24"/>](https://www.linkedin.com/in/gabriel-fujimoto-a90239367/) [![GitHub Badge](https://img.shields.io/badge/GitHub-111217?style=flat-square&logo=github&logoColor=white)](https://github.com/fujimotogabriel) |
| Miguel Silva Gomes     | Scrum Team    | [<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/linkedin/linkedin-original.svg" width="24"/>](https://www.linkedin.com/in/miguelsg479/) [![GitHub Badge](https://img.shields.io/badge/GitHub-111217?style=flat-square&logo=github&logoColor=white)](https://github.com/miguelsg97) |

## 🎓 Orientadores

- Prof. Jean Carlos Lourenço Costa
- Prof. Giuliano Araújo Bertoti

## 📋 Requisitos Não Funcionais

* Linguagem de Programação Python;
* Repositório Git;
* Manual do Usuário;
* Gestão de Projetos de Software com Jira;
* Manual de Instalação.

## 🧰 Tecnologias Utilizadas

<h4 align="center">
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  </a>
  <a href="https://pytba.readthedocs.io/">
    <img src="https://img.shields.io/badge/pyTelegramBotAPI-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white"/>
  </a>
  <a href="https://telegram.org/">
    <img src="https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white"/>
  </a>
  <a href="https://www.json.org/">
    <img src="https://img.shields.io/badge/JSON-000000?style=for-the-badge&logo=json&logoColor=white"/>
  </a>
  <a href="https://docs.python.org/3/library/datetime.html">
    <img src="https://img.shields.io/badge/datetime-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  </a>
  <a href="https://docs.python.org/3/library/pathlib.html">
    <img src="https://img.shields.io/badge/pathlib-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  </a>
  <a href="https://git-scm.com/">
    <img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white"/>
  </a>
  <a href="https://github.com/">
    <img src="https://img.shields.io/badge/GitHub-121011?style=for-the-badge&logo=github&logoColor=white"/>
  </a>
  <a href="https://code.visualstudio.com/">
    <img src="https://img.shields.io/badge/Visual%20Studio%20Code-007ACC?style=for-the-badge&logo=visualstudiocode&logoColor=white"/>
  </a>
  <a href="https://colab.research.google.com/">
    <img src="https://img.shields.io/badge/Google%20Colab-F9AB00?style=for-the-badge&logo=googlecolab&logoColor=white"/>
  </a>
  <a href="https://www.atlassian.com/software/jira">
    <img src="https://img.shields.io/badge/Jira%20Software-0052CC?style=for-the-badge&logo=jira&logoColor=white"/>
  </a>
</h4>

## 📌 Product Backlog

| Rank | Prioridade | User Story | Sprint |
| :--- | :---: | :--- | :---: |
| 1 | Alta | Como usuário, quero acessar o bot pelo Telegram para iniciar a consulta de informações sobre vacinação. | 1 |
| 2 | Alta | Como usuário, quero informar minha data de nascimento para receber as vacinas recomendadas para minha idade. | 1 |
| 3 | Alta | Como usuário gestante, quero informar a semana de gestação para receber as vacinas recomendadas para esse período. | 1 |
| 4 | Alta | Como equipe de desenvolvimento, precisamos estruturar o repositório Git e organizar as tarefas no Jira para gerenciar o desenvolvimento do projeto. | 1 |
| 5 | Média | Como usuário, quero utilizar botões no Telegram para consultar facilmente as vacinas recomendadas para minha idade ou período de gestação. | 2 |
| 6 | Baixa | Como usuário, quero gerar um resumo simples das vacinas recomendadas para minha faixa etária. | 3 |
| 7 | Média | Como administrador, preciso disponibilizar os manuais de usuário e instalação para permitir a execução do bot em outros ambientes. | 3 |

## 📊 Registro das Sprints

| Sprint            | Previsão   | Status         | Histórico |
|-------------------|------------|----------------|-----------|
| 01                | 05/04/2026 | Concluída ✅   | [MVP](MVP/sp1.md) |

### Sprint 1

<p align="center">
  <img src="assets/relatorio_spr1.png" width="800">
</p>

## 📖 Manual do Usuário

### 1. Apresentação

O bot de vacinação (`@vacinabrasil_bot`) é um assistente no Telegram que permite consultar rapidamente quais vacinas são recomendadas de acordo com a **idade do usuário** ou **período de gestação**.

A interação ocorre diretamente pelo chat do Telegram, onde o usuário seleciona opções ou informa dados básicos, e o sistema retorna as vacinas recomendadas para aquele perfil. A base de dados utilizada pelo bot é composta por arquivos JSON processados a partir de calendários de vacinação disponibilizados pelo Ministério da Saúde em `https://www.gov.br/saude/pt-br/vacinacao/calendario`.

---

### 2. Público-alvo e Problemas Resolvidos 👤🩺

#### Usuários atendidos

* **Responsáveis por crianças:** Pais ou responsáveis que desejam acompanhar as vacinas recomendadas para seus filhos.
* **Jovens e adultos:** Pessoas que querem verificar quais vacinas ou reforços são indicados para sua faixa etária.
* **Idosos:** Usuários que desejam consultar quais imunizações são recomendadas a partir dos 60 anos.
* **Gestantes:** Mulheres que precisam saber quais vacinas são indicadas durante o período de gestação.

#### Problemas que o bot resolve

* **Dificuldade de interpretação do calendário vacinal:** As tabelas oficiais possuem muitas informações. O bot simplifica e mostra apenas as vacinas relevantes para o usuário.
* **Cálculo manual de faixa etária:** Muitas pessoas não sabem em qual categoria do calendário se encaixam. O bot calcula automaticamente a idade a partir da data de nascimento.
* **Acesso rápido à informação:** Em vez de navegar por páginas e documentos, o usuário pode consultar as vacinas diretamente no Telegram.
* **Informação específica para gestantes:** O bot permite consultar rapidamente as vacinas recomendadas conforme a semana de gestação.

---

### 3. Iniciando o Bot

1. Abra o **Telegram**
2. Procure pelo bot `@vacinabrasil_bot` ou leia o QR Code abaixo:

<p align="center">
  <img src="assets/img/qrcode_vacinabrasil_bot.png" width="250"/>
</p>

3. Abra a conversa e digite:

```
/start
```

Após enviar o comando, o bot iniciará a interação e exibirá as opções disponíveis.

---

### 4. Fluxo principal de uso

#### 4.1 Menu inicial

Após o comando `/start`, o bot responderá com a mensagem:

**Escolha sua opção:**

e exibirá dois botões:

* `Desejo ver as minhas vacinas`
* `Sou gestante`

---

#### 4.2 Consulta por data de nascimento

1. Clique em **Desejo ver as minhas vacinas**
2. O bot solicitará o **dia de nascimento** (botões)
3. Em seguida solicitará o **mês de nascimento** (botões)
4. Depois solicitará o **ano de nascimento** (botões)

Após a seleção completa da data, o sistema calcula automaticamente a idade do usuário e identifica a faixa etária correspondente.

O bot então retorna as vacinas recomendadas para aquela idade.

Exemplo de resposta:

```
Vacina - Dose
--------------------
Hepatite B - 3 doses
dT - 3 doses
Febre amarela - 1 dose
```

---

#### 4.3 Consulta para gestantes

1. Clique em **Sou gestante**
2. O bot solicitará a **semana de gestação** (botões)
3. Após a seleção da semana, o sistema retorna as vacinas recomendadas para aquele período da gestação.

Exemplo de resposta:

```
Vacina - Dose
--------------------
Hepatite B - 3 doses
dT - 3 doses
```

---

### 5. Respostas do sistema

Após a consulta, o bot retorna uma lista com as vacinas recomendadas e suas respectivas doses.

Exemplo:

```
Vacina - Dose
--------------------
Hepatite B - 3 doses
dT - 3 doses
Febre amarela - 1 dose
```

As informações são apresentadas de forma direta, indicando o **nome da vacina** e a **dose ou periodicidade recomendada**.

---

### 6. Observações

* O bot precisa estar **em execução** para responder às mensagens.
* Caso alguma combinação de data não seja válida, o sistema solicitará que o processo seja reiniciado.
* O tempo de resposta pode levar alguns segundos enquanto o sistema processa os dados.

---

### 7. Exemplo de uso

Digite:

```
/start
```

Selecione **Desejo ver as minhas vacinas**

Escolha o **dia**, **mês** e **ano** de nascimento utilizando os botões.

Após a seleção completa da data, o bot exibirá as vacinas recomendadas para a faixa etária correspondente.

Exemplo de saída:

```
Vacina - Dose
--------------------
Hepatite B - 3 doses
dT - 3 doses
Febre amarela - 1 dose
```

## 🛠️ Manual de Instalação

Para instalar e executar o bot de maneira local:

### 1.1 Requisitos

Para executar o bot localmente é necessário:

* Conexão à Internet;
* Python **3.10 ou superior** instalado;
* Token de um bot criado no **BotFather (@BotFather no Telegram)**;
* Biblioteca **pyTelegramBotAPI** instalada.

### 1.2 Instalação

Abra um terminal e clone o repositório:

```bash
git clone https://github.com/nexusdevapi/VacinaBrasil-Bot.git
cd VacinaBrasil-Bot
pip install -r requirements.txt
python src/main.py
