# Grupo 9 - 26.2 - Grafos
# Fluxogramas personalizados

## Alunos
|Matrícula | Aluno |
| -- | -- |
| 232003652 | João Paulo Barbosa Pereira Nunes |
| 251023184 | João Pedro da Nóbrega Souza Cordeiro |


## Sobre

Este projeto consiste na criação de fluxogramas personalizados. O usuário pode cadastrar disciplinas e adicionar pré-requisitos, representados por arestas direcionadas. Através do grafo direcionado acíclico gerado, o programa deve gerar um fluxograma através de ordenação topólogica, que pode ser modificado em função de créditos máximos desejados. O projeto possuirá uma interface gráfica.

## Funcionalidades

* Cadastro de matérias (código, nome e créditos)
* Listagem das matérias já cadastradas na sessão atual

## Pré requisitos

* Python 3.9 ou superior instalado
* Git instalado

## Como executar

### 1. Clonar o repositório

```bash
git clone https://github.com/projeto-de-algoritmos-2026/G9_Grafos_PA-26.2.git
cd G9_Grafos_PA-26.2
```

### 2. Criar e ativar o ambiente virtual (venv)

No Linux ou macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

No Windows (PowerShell):

```bash
python -m venv venv
venv\Scripts\Activate.ps1
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Rodar a aplicação

```bash
streamlit run app.py
```

Depois disso, o Streamlit vai abrir automaticamente uma aba no navegador (normalmente em `http://localhost:8501`). Se não abrir sozinho, é só acessar esse endereço manualmente.

## Estrutura do projeto

```
.
├── app.py          # Interface principal (Streamlit)
├── Grafo.py         # Classe GrafoCurso com a lógica de grafo
├── requirements.txt # Dependências do projeto
└── README.md
```

## Como usar

1. No formulário "Cadastrar Matéria", preencha o código (ex: `FGA0313`), o nome (ex: `Requisitos de Software`) e a quantidade de créditos
2. Clique em "Cadastrar"
3. A matéria cadastrada aparece automaticamente na lista ao lado, em "Matérias Cadastradas"
