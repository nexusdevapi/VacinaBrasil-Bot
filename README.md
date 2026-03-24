# 💉 Assistente de Dados Públicos da Saúde para Vacinação

Projeto Integrador (API) desenvolvido para o **1º semestre de Análise e Desenvolvimento de Sistemas (ADS)** da Fatec, em parceria com o **CADI** (Centro de Apoio à Docência e Institucional).

## 🎯 O Desafio
Desenvolver um assistente virtual voltado para a saúde pública, capaz de informar o cidadão sobre:
* **Calendários de vacinação** para diferentes faixas etárias (crianças, adultos, idosos, etc.).
* **Coberturas vacinais** em diferentes regiões do Brasil.

**Restrições do Projeto (Regras de Negócio):**
* O sistema funciona com base em **Lógica Algorítmica**, sem persistência de dados (não utilizamos bancos de dados tradicionais como SQL/NoSQL).
* A leitura de dados é feita através de arquivos locais de portais oficiais.
* **Proibido o uso de APIs externas** para a inteligência de busca ou integração.

## 🛠️ Tecnologias e Ferramentas
* **Linguagem:** Python 3.x
* **Controle de Versão:** Git e GitHub
* **Gestão de Projeto:** Jira (Metodologia Ágil / Scrum)

## 📂 Estrutura do Repositório

O projeto está organizado da seguinte forma:

```text
/
├── README.md                   # Documentação principal
├── requirements.txt            # Dependências do projeto em Python
├── .gitignore                  # Arquivos e pastas ignorados pelo Git
└── assistente-vacinacao/       # Diretório da aplicação
    ├── data/                   # Arquivos de dados locais (.csv, .json)
    │   ├── raw/                # Dados originais do governo
    │   └── processed/          # Dados limpos/filtrados
    ├── docs/                   # Manuais do projeto
    │   ├── manual_instalacao.md
    │   └── manual_usuario.md
    └── src/                    # Código-fonte principal
        ├── main.py             # Arquivo de execução do assistente (Terminal)
        ├── core/               # Lógica de busca e validação (Cérebro do sistema)
        ├── data_handler/       # Funções para leitura dos dados locais
        └── utils/              # Ferramentas auxiliares e formatação