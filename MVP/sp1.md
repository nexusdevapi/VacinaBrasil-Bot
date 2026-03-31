# API 1º Semestre ADS - Vacina Brasil Bot (NexusDev)

> Status do Projeto: Sprint 1 - Em andamento 🔵

## 🏅 Desafio <a id="desafio"></a>

Desenvolver um assistente virtual para Telegram focado em saúde pública. O objetivo é informar o cidadão sobre calendários vacinais e coberturas por região, utilizando exclusivamente dados de portais públicos oficiais processados localmente (sem APIs externas de bancos de dados ou IA generativa paga).

## 📋 Backlog da Sprint 1 <a id="backlog"></a>

Este backlog reflete o planejamento estratégico e a estimativa de esforço (Story Points) definida para a primeira entrega.

| Rank | Prioridade | User Story | Estimativa (Points) |
| :--: | :--------: | :--- | :---: |
| 1 | Alta | **Organização:** Definir papéis de PO e SM e estabelecer canais de comunicação oficial da equipe. | 2 |
| 2 | Alta | **Mapeamento:** Realizar levantamento de competências técnicas do time para distribuição de tarefas. | 1 |
| 3 | Alta | **Análise:** Estudar os requisitos da API e garantir a conformidade com a restrição de dados locais. | 1 |
| 4 | Alta | **Infraestrutura:** Configurar o repositório GitHub, .gitignore e a estrutura de pastas inicial. | 1 |
| 5 | Alta | **Data Mining:** Coletar e tratar arquivos CSV/JSON de fontes oficiais (DATASUS) sobre vacinação. | 4 |
| 6 | Alta | **Arquitetura:** Desenhar a estrutura lógica das classes Python e fluxo de navegação do bot. | 5 |
| 7 | Alta | **Setup Telegram:** Configurar o BotFather e implementar o comando inicial `/start` no código. | 5 |
| 8 | Alta | **Protótipo:** Desenvolver a lógica de busca que consulta arquivos locais e responde o nome da vacina. | 8 |

---

## ✅ Definition of Ready (DoR)

| Critério | Descrição |
| :--- | :--- |
| **Descrição Clara** | A User Story está bem escrita e compreensível para toda a equipe. |
| **Critérios de Aceitação** | As regras de validação para a tarefa estão descritas. |
| **Estimativa Realizada** | A tarefa possui pontuação de esforço (Story Points) definida. |
| **Responsável Atribuído** | Há um membro da NexusDev designado para a execução no Jira. |
| **Dependências Resolvidas** | Bloqueios externos ou técnicos foram tratados antes do início. |

---

## ✅ Definition of Done (DoD)

| Critério | Descrição |
| :--- | :--- |
| **Funcionalidade Implementada** | Todos os critérios de aceitação da User Story foram atendidos. |
| **Revisão de Código** | O código foi revisado por outro membro ou validado tecnicamente. |
| **Zero APIs Externas** | A entrega utiliza apenas processamento local de dados, conforme o requisito. |
| **Integração no Git** | O código foi mergeado no branch principal sem conflitos. |
| **Validação do PO** | O Product Owner validou que a entrega atende à necessidade do usuário. |

---

## 🎓 Equipe <a id="equipe"></a>

<div align="center">
  <table>
    <tr>
      <th>Membro</th>
      <th>Função</th>
      <th>Github</th>
      <th>Linkedin</th>
    </tr>
    <tr>
      <td>Nicolas Fonseca Meira</td>
      <td>Product Owner</td>
      <td><a href="https://github.com/NicolasFonsecaM"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"></a></td>
      <td><a href="https://www.linkedin.com/in/nicolas-fonseca-60386130b/"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"></a></td>
    </tr>
    <tr>
      <td>Caio Gabriel Ferreira</td>
      <td>Scrum Master</td>
      <td><a href="https://github.com/caiogabrielfp-cpu"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"></a></td>
      <td><a href="https://www.linkedin.com/"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"></a></td>
    </tr>
    <tr>
      <td>Gabriel Yudi Fujimoto</td>
      <td>Scrum Team</td>
      <td><a href="https://github.com/fujimotogabriel"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"></a></td>
      <td><a href="https://www.linkedin.com/"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"></a></td>
    </tr>
    <tr>
      <td>Miguel Silva Gomes</td>
      <td>Scrum Team</td>
      <td><a href="https://github.com/miguelsg97"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"></a></td>
      <td><a href="https://www.linkedin.com/in/miguelsg479/"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"></a></td>
    </tr>
  </table>
</div>
