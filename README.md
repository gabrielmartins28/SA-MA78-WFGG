# 🧳 Sistema Interno de Viagens

Sistema corporativo via terminal (CLI) para gestão de viagens corporativas, inspirado nos processos internos de solicitação, aprovação e prestação de contas de viagens de uma empresa (baseado nos processos da WEG).

Desenvolvido em **Python puro**, com persistência em **MySQL** (hospedado na Aiven), sem frameworks — só `mysql-connector-python` e boas práticas de organização em módulos.

## 📋 Funcionalidades

O sistema é dividido em 9 módulos, acessados por um menu principal:

| Módulo | O que faz |
|---|---|
| 🧳 **Viagens** | Cadastrar, listar, atualizar e cancelar solicitações de viagem |
| 👤 **Colaboradores** | Cadastro e gestão dos colaboradores da empresa |
| 🏢 **Departamentos** | Cadastro de departamentos e controle de orçamento |
| 🚗 **Frota de Veículos** | Cadastro da frota e controle de status/disponibilidade |
| ✅ **Aprovações** | Registro de decisões (aprovado/rejeitado) sobre as viagens |
| 🤝 **Caronas** | Vincula colaboradores que estão dividindo uma viagem |
| 💰 **Despesas** | Lançamento de despesas associadas a cada viagem |
| 🎯 **Objetivos de Viagem** | Cadastro dos motivos/objetivos possíveis de uma viagem |
| 📊 **Análise de Eficácia** | Avaliação pós-viagem (indicador de sucesso, observações) |

Todas as listagens são exibidas em formato de tabela (colunas alinhadas, datas formatadas, valores em R$), não como dados crus do banco.

## 🛠️ Tecnologias

- **Python 3** — linguagem principal, sem frameworks
- **MySQL** — banco de dados relacional (hospedado na [Aiven](https://aiven.io/))
- **mysql-connector-python** — driver de conexão com o banco
- **python-dotenv** — carregamento de variáveis de ambiente (credenciais)

## 📁 Estrutura do projeto

```
.
├── main.py                  # Menu principal (toda a lógica de interface/CLI)
├── database.py               # Conexão com o banco (lê credenciais do .env)
├── viagem.py                 # CRUD de viagens
├── colaborador.py             # CRUD de colaboradores
├── departamento.py            # CRUD de departamentos
├── aprovacao.py               # CRUD de aprovações
├── carona.py                  # CRUD de caronas
├── despesas.py                # CRUD de despesas
├── objetivo_viagem.py          # CRUD de objetivos de viagem
├── frota_veiculo.py            # CRUD da frota de veículos
├── analise_eficacia.py         # CRUD de análise de eficácia
├── database.sql / tables.sql   # Script de criação das tabelas
├── requirements.txt           # Dependências do projeto
└── .env                       # Credenciais do banco (não versionado)
```

Cada módulo é responsável apenas pelo acesso ao banco (inserir, listar, atualizar, deletar) da sua entidade. Toda a interação com o usuário (menus, prints, `input()`) fica centralizada no `main.py`.

## ✅ Pré-requisitos

- Python 3.10+
- Uma instância MySQL acessível (local ou na nuvem, como Aiven)

## 🚀 Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio
   ```

2. Crie e ative um ambiente virtual (opcional, mas recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Crie um arquivo `.env` na raiz do projeto com suas credenciais de banco:
   ```env
   DB_HOST=seu_host
   DB_USER=seu_usuario
   DB_PASSWORD=sua_senha
   DB_NAME=Sistema_interno_Viagens
   DB_PORT=3306
   ```

5. Rode o script `database.sql` (ou `tables.sql`) no seu MySQL para criar as tabelas.

## ▶️ Como executar

```bash
python main.py
```

Navegue pelo menu principal digitando o número da opção desejada.

## ⚠️ Limitações conhecidas

- Nenhum módulo possui busca por ID individual — apenas listagem completa.
- `frota_veiculo.py` permite atualizar somente o status do veículo (não os demais dados).
- `departamento.py` permite atualizar apenas o orçamento (não o nome).
- Não há autenticação de usuário — o sistema assume uso interno confiável.

## 📌 Próximos passos (roadmap)

- [ ] Adicionar busca por ID em todos os módulos
- [ ] Validações de entrada mais robustas (datas, e-mails, valores)
- [ ] Testes automatizados
- [ ] Exportação de relatórios (CSV/PDF)

## 📄 Licença

Projeto acadêmico/pessoal — sem licença definida.
