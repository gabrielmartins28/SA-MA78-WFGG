"""
main.py - Sistema Corporativo de Gestão de Viagens (WEG)
Menu interativo via terminal (CLI).

Toda a lógica de menu (prints, inputs, loops) fica aqui. Os módulos
importados abaixo contêm apenas as funções de acesso ao banco de dados.
Como essas funções já imprimem seus próprios resultados/confirmações,
o main.py só coleta os dados e delega a chamada.

Os módulos viagem.py, aprovacao.py, colaborador.py, carona.py e despesas.py
foram corrigidos para usar os nomes de coluna reais do banco (ver histórico
do projeto) e agora aceitam mais campos do que antes — o menu abaixo já
reflete essas assinaturas novas.
"""
from modules.departamento import (
    cadastrar_departamento,
    listar_departamentos,
    atualizar_orcamento_departamento,
    deletar_departamento,
)
from modules.colaborador import (
    inserir_colaborador,
    listar_colaborador,
    atualizar_colaborador,
    deletar_colaborador,
)
from modules.aprovacao import (
    inserir_aprovacao,
    listar_aprovacao,
    atualizar_aprovacao,
    deletar_aprovacao,
)
from modules.carona import (
    criar_carona,
    listar_carona,
    atualizar_carona,
    deletar_carona,
)
from modules.viagem import (
    inserir_viagem,
    listar_viagem,
    atualizar_viagem,
    deletar_viagem,
)
from modules.despesas import (
    criar_despesa,
    listar_despesas,
    atualizar_despesa,
    deletar_despesa,
)
from modules.analise_eficacia import (
    cadastrar_analise_eficacia,
    listar_analises_eficacia,
    atualizar_analise_eficacia,
    deletar_analise_eficacia,
)
from modules.objetivo_viagem import (
    cadastrar_objetivo,
    listar_objetivos,
    atualizar_objetivo,
    deletar_objetivo,
)
from modules.frota_veiculo import (
    cadastrar_veiculo,
    listar_veiculos,
    atualizar_status_veiculo,
    deletar_veiculo,
)
from utils.consultas import (
    CATEGORIAS,
    consulta_subordinados_por_gestor,
)


# ==============================================================================
# UTILITÁRIOS DE INTERFACE (prints e leituras de input padronizados)
# ==============================================================================

LARGURA = 60


def exibir_cabecalho(titulo, emoji="🧭"):
    print("\n" + "=" * LARGURA)
    print(f"{emoji}  {titulo.upper()}")
    print("=" * LARGURA)


def pausar():
    input("\nPressione ENTER para continuar...")


def confirmar(mensagem):
    return input(f"{mensagem} (s/n): ").strip().lower() == "s"


def ler_texto(rotulo, obrigatorio=True):
    while True:
        valor = input(f"{rotulo}: ").strip()
        if valor or not obrigatorio:
            return valor or None
        print("⚠️  Este campo é obrigatório.")


def ler_inteiro(rotulo, obrigatorio=True):
    while True:
        valor = input(f"{rotulo}: ").strip()
        if not valor and not obrigatorio:
            return None
        try:
            return int(valor)
        except ValueError:
            print("⚠️  Digite um número inteiro válido.")


def ler_decimal(rotulo):
    while True:
        valor = input(f"{rotulo}: ").strip().replace(",", ".")
        try:
            return float(valor)
        except ValueError:
            print("⚠️  Digite um valor numérico válido (ex: 150.90).")


def ler_booleano(rotulo):
    return input(f"{rotulo} (s/n): ").strip().lower() == "s"


# ==============================================================================
# MÓDULO DE VIAGENS
# ==============================================================================

def menu_viagens():
    while True:
        exibir_cabecalho("Módulo de Viagens", "🧳")
        print("1. ➕ Cadastrar viagem")
        print("2. 📋 Listar viagens")
        print("3. ✏️  Atualizar viagem")
        print("4. 🗑️  Deletar viagem")
        print("0. ↩️  Voltar ao menu principal")
        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            dia_saida = ler_texto("Data de saída (AAAA-MM-DD)")
            dia_retorno = ler_texto("Data de retorno (AAAA-MM-DD)")
            id_colaborador = ler_inteiro("ID do colaborador solicitante")
            justificativa = ler_texto("Justificativa da viagem")
            destino = ler_texto("Destino")
            id_objetivo = ler_inteiro("ID do objetivo da viagem")
            id_veiculo = ler_inteiro("ID do veículo da frota (deixe vazio se não houver)", obrigatorio=False)
            inserir_viagem(
                dia_saida, dia_retorno, id_colaborador, justificativa,
                destino, "Pendente", id_objetivo, id_veiculo,
            )

        elif opcao == "2":
            listar_viagem()

        elif opcao == "3":
            id_viagem = ler_inteiro("ID da viagem a atualizar")
            destino = ler_texto("Novo destino")
            dia_saida = ler_texto("Nova data de saída (AAAA-MM-DD)")
            dia_retorno = ler_texto("Nova data de retorno (AAAA-MM-DD)")
            print("Status disponíveis: Pendente, Aprovada, Rejeitada, Em Andamento, Concluída")
            status = ler_texto("Novo status")
            atualizar_viagem(id_viagem, destino, dia_saida, dia_retorno, status)

        elif opcao == "4":
            id_viagem = ler_inteiro("ID da viagem a deletar")
            if confirmar(f"Confirma a exclusão da viagem {id_viagem}?"):
                deletar_viagem(id_viagem)

        elif opcao == "0":
            break
        else:
            print("\n⚠️  Opção inválida. Tente novamente.")

        pausar()


# ==============================================================================
# MÓDULO DE COLABORADORES
# ==============================================================================

def menu_colaboradores():
    while True:
        exibir_cabecalho("Módulo de Colaboradores", "👤")
        print("1. ➕ Cadastrar colaborador")
        print("2. 📋 Listar colaboradores")
        print("3. ✏️  Atualizar colaborador")
        print("4. 🗑️  Deletar colaborador")
        print("0. ↩️  Voltar ao menu principal")
        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            nome = ler_texto("Nome")
            email = ler_texto("E-mail")
            telefone = ler_texto("Telefone")
            cargo = ler_texto("Cargo")
            status = ler_texto("Status (Ativo/Inativo)")
            possui_cnh = ler_booleano("Possui CNH?")
            id_departamento = ler_inteiro("ID do departamento")
            id_gestor = ler_inteiro("ID do gestor (deixe vazio se não houver)", obrigatorio=False)
            inserir_colaborador(nome, email, telefone, cargo, status, possui_cnh, id_departamento, id_gestor)

        elif opcao == "2":
            listar_colaborador()

        elif opcao == "3":
            id_colaborador = ler_inteiro("ID do colaborador a atualizar")
            nome = ler_texto("Novo nome")
            cargo = ler_texto("Novo cargo")
            email = ler_texto("Novo e-mail")
            atualizar_colaborador(id_colaborador, nome, cargo, email)

        elif opcao == "4":
            id_colaborador = ler_inteiro("ID do colaborador a deletar")
            if confirmar(f"Confirma a exclusão do colaborador {id_colaborador}?"):
                deletar_colaborador(id_colaborador)

        elif opcao == "0":
            break
        else:
            print("\n⚠️  Opção inválida. Tente novamente.")

        pausar()


# ==============================================================================
# MÓDULO DE DEPARTAMENTOS
# ==============================================================================

def menu_departamentos():
    while True:
        exibir_cabecalho("Módulo de Departamentos", "🏢")
        print("1. ➕ Cadastrar departamento")
        print("2. 📋 Listar departamentos")
        print("3. ✏️  Atualizar orçamento")
        print("4. 🗑️  Deletar departamento")
        print("0. ↩️  Voltar ao menu principal")
        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            nome = ler_texto("Nome do departamento")
            orcamento = ler_decimal("Orçamento do departamento")
            cadastrar_departamento(nome, orcamento)

        elif opcao == "2":
            listar_departamentos()

        elif opcao == "3":
            id_departamento = ler_inteiro("ID do departamento")
            novo_orcamento = ler_decimal("Novo orçamento")
            atualizar_orcamento_departamento(id_departamento, novo_orcamento)

        elif opcao == "4":
            id_departamento = ler_inteiro("ID do departamento a deletar")
            if confirmar(f"Confirma a exclusão do departamento {id_departamento}?"):
                deletar_departamento(id_departamento)

        elif opcao == "0":
            break
        else:
            print("\n⚠️  Opção inválida. Tente novamente.")

        pausar()


# ==============================================================================
# MÓDULO DE APROVAÇÕES
# ==============================================================================

def menu_aprovacoes():
    while True:
        exibir_cabecalho("Módulo de Aprovações", "✅")
        print("1. ➕ Registrar aprovação")
        print("2. 📋 Listar aprovações")
        print("3. ✏️  Atualizar aprovação")
        print("4. 🗑️  Deletar aprovação")
        print("0. ↩️  Voltar ao menu principal")
        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            id_viagem = ler_inteiro("ID da viagem")
            id_colaborador = ler_inteiro("ID do colaborador (aprovador)")
            data_hora = ler_texto("Data/hora da avaliação (AAAA-MM-DD HH:MM)")
            status = ler_texto("Status (Aprovado/Rejeitado)")
            observacoes = ler_texto("Observações/justificativa", obrigatorio=False)
            inserir_aprovacao(id_viagem, id_colaborador, data_hora, status, observacoes)

        elif opcao == "2":
            listar_aprovacao()

        elif opcao == "3":
            id_aprovacao = ler_inteiro("ID da aprovação a atualizar")
            status = ler_texto("Novo status")
            comentario = ler_texto("Novo comentário/observação", obrigatorio=False)
            atualizar_aprovacao(id_aprovacao, status, comentario)

        elif opcao == "4":
            id_aprovacao = ler_inteiro("ID da aprovação a deletar")
            if confirmar(f"Confirma a exclusão da aprovação {id_aprovacao}?"):
                deletar_aprovacao(id_aprovacao)

        elif opcao == "0":
            break
        else:
            print("\n⚠️  Opção inválida. Tente novamente.")

        pausar()


# ==============================================================================
# MÓDULO DE CARONAS
# ==============================================================================

def menu_caronas():
    while True:
        exibir_cabecalho("Módulo de Caronas", "🤝")
        print("1. ➕ Cadastrar carona")
        print("2. 📋 Listar caronas")
        print("3. ✏️  Atualizar carona")
        print("4. 🗑️  Deletar carona")
        print("0. ↩️  Voltar ao menu principal")
        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            id_viagem = ler_inteiro("ID da viagem")
            id_colaborador = ler_inteiro("ID do colaborador (carona)")
            criar_carona(id_viagem, id_colaborador)

        elif opcao == "2":
            listar_carona()

        elif opcao == "3":
            id_carona = ler_inteiro("ID da carona a atualizar")
            id_viagem = ler_inteiro("Novo ID da viagem")
            id_colaborador = ler_inteiro("Novo ID do colaborador")
            atualizar_carona(id_carona, id_viagem, id_colaborador)

        elif opcao == "4":
            id_carona = ler_inteiro("ID da carona a deletar")
            if confirmar(f"Confirma a exclusão da carona {id_carona}?"):
                deletar_carona(id_carona)

        elif opcao == "0":
            break
        else:
            print("\n⚠️  Opção inválida. Tente novamente.")

        pausar()


# ==============================================================================
# MÓDULO DE DESPESAS
# ==============================================================================

def menu_despesas():
    while True:
        exibir_cabecalho("Módulo de Despesas", "💰")
        print("1. ➕ Cadastrar despesa")
        print("2. 📋 Listar despesas")
        print("3. ✏️  Atualizar despesa")
        print("4. 🗑️  Deletar despesa")
        print("0. ↩️  Voltar ao menu principal")
        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            valor = ler_decimal("Valor")
            data_hora = ler_texto("Data/hora da despesa (AAAA-MM-DD HH:MM)")
            categoria = ler_texto("Categoria (ex: Alimentação, Hospedagem, Transporte)")
            forma_pagamento = ler_texto("Forma de pagamento")
            id_viagem = ler_inteiro("ID da viagem relacionada")
            criar_despesa(valor, data_hora, categoria, forma_pagamento, id_viagem)

        elif opcao == "2":
            listar_despesas()

        elif opcao == "3":
            id_despesa = ler_inteiro("ID da despesa a atualizar")
            valor = ler_decimal("Novo valor")
            categoria = ler_texto("Nova categoria")
            forma_pagamento = ler_texto("Nova forma de pagamento")
            atualizar_despesa(id_despesa, valor, categoria, forma_pagamento)

        elif opcao == "4":
            id_despesa = ler_inteiro("ID da despesa a deletar")
            if confirmar(f"Confirma a exclusão da despesa {id_despesa}?"):
                deletar_despesa(id_despesa)

        elif opcao == "0":
            break
        else:
            print("\n⚠️  Opção inválida. Tente novamente.")

        pausar()


# ==============================================================================
# MÓDULO DE OBJETIVOS DE VIAGEM
# ==============================================================================

def menu_objetivos():
    while True:
        exibir_cabecalho("Módulo de Objetivos de Viagem", "🎯")
        print("1. ➕ Cadastrar objetivo")
        print("2. 📋 Listar objetivos")
        print("3. ✏️  Atualizar objetivo")
        print("4. 🗑️  Deletar objetivo")
        print("0. ↩️  Voltar ao menu principal")
        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            descricao = ler_texto("Descrição do objetivo")
            cadastrar_objetivo(descricao)

        elif opcao == "2":
            listar_objetivos()

        elif opcao == "3":
            id_objetivo = ler_inteiro("ID do objetivo a atualizar")
            nova_descricao = ler_texto("Nova descrição")
            atualizar_objetivo(id_objetivo, nova_descricao)

        elif opcao == "4":
            id_objetivo = ler_inteiro("ID do objetivo a deletar")
            if confirmar(f"Confirma a exclusão do objetivo {id_objetivo}?"):
                deletar_objetivo(id_objetivo)

        elif opcao == "0":
            break
        else:
            print("\n⚠️  Opção inválida. Tente novamente.")

        pausar()


# ==============================================================================
# MÓDULO DE FROTA DE VEÍCULOS
# ⚠️ frota_veiculo.py não possui atualização genérica — só é possível
# atualizar o status do veículo.
# ==============================================================================

def menu_frota():
    while True:
        exibir_cabecalho("Módulo de Frota de Veículos", "🚗")
        print("1. ➕ Cadastrar veículo")
        print("2. 📋 Listar veículos")
        print("3. ✏️  Atualizar status do veículo")
        print("4. 🗑️  Deletar veículo")
        print("0. ↩️  Voltar ao menu principal")
        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            placa = ler_texto("Placa")
            modelo = ler_texto("Modelo")
            marca = ler_texto("Marca")
            capacidade = ler_inteiro("Capacidade de passageiros")
            km_atual = ler_inteiro("Km atual (deixe vazio para 0)", obrigatorio=False) or 0
            cadastrar_veiculo(placa, modelo, marca, capacidade, km_atual)

        elif opcao == "2":
            listar_veiculos()

        elif opcao == "3":
            id_veiculo = ler_inteiro("ID do veículo")
            print("Status sugeridos: Disponivel, Em Uso, Manutencao, Indisponivel")
            novo_status = ler_texto("Novo status")
            atualizar_status_veiculo(id_veiculo, novo_status)

        elif opcao == "4":
            id_veiculo = ler_inteiro("ID do veículo a deletar")
            if confirmar(f"Confirma a exclusão do veículo {id_veiculo}?"):
                deletar_veiculo(id_veiculo)

        elif opcao == "0":
            break
        else:
            print("\n⚠️  Opção inválida. Tente novamente.")

        pausar()


# ==============================================================================
# MÓDULO DE ANÁLISE DE EFICÁCIA
# ==============================================================================

def menu_analise_eficacia():
    while True:
        exibir_cabecalho("Módulo de Análise de Eficácia", "📊")
        print("1. ➕ Registrar análise de uma viagem concluída")
        print("2. 📋 Listar análises")
        print("3. ✏️  Atualizar análise")
        print("4. 🗑️  Deletar análise")
        print("0. ↩️  Voltar ao menu principal")
        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            data_analise = ler_texto("Data da análise (AAAA-MM-DD)")
            id_viagem = ler_inteiro("ID da viagem concluída")
            id_colaborador = ler_inteiro("ID do colaborador avaliador")
            indicador_sucesso = ler_decimal("Indicador de sucesso (nota, ex: 8.5)")
            observacao = ler_texto("Observação do colaborador", obrigatorio=False)
            cadastrar_analise_eficacia(data_analise, id_viagem, id_colaborador, indicador_sucesso, observacao)

        elif opcao == "2":
            listar_analises_eficacia()

        elif opcao == "3":
            id_analise = ler_inteiro("ID da análise a atualizar")
            nova_data = ler_texto("Nova data da análise (AAAA-MM-DD)")
            novo_id_viagem = ler_inteiro("Novo ID da viagem")
            novo_id_colaborador = ler_inteiro("Novo ID do colaborador")
            novo_indicador = ler_decimal("Novo indicador de sucesso")
            nova_observacao = ler_texto("Nova observação", obrigatorio=False)
            atualizar_analise_eficacia(
                id_analise, nova_data, novo_id_viagem, novo_id_colaborador,
                novo_indicador, nova_observacao,
            )

        elif opcao == "4":
            id_analise = ler_inteiro("ID da análise a deletar")
            if confirmar(f"Confirma a exclusão da análise {id_analise}?"):
                deletar_analise_eficacia(id_analise)

        elif opcao == "0":
            break
        else:
            print("\n⚠️  Opção inválida. Tente novamente.")

        pausar()


# ==============================================================================
# MÓDULO DE CONSULTAS FREQUENTES (RELATÓRIOS)
# ==============================================================================
# As consultas ficam agrupadas nas mesmas 6 categorias de banco/consultas.sql.
# A lista de categorias e consultas vem de consultas.CATEGORIAS, então basta
# adicionar uma nova função + entrada lá para que ela apareça aqui também.

def menu_consultas_categoria(categoria):
    titulo_categoria, emoji_categoria, consultas = categoria

    while True:
        exibir_cabecalho(titulo_categoria, emoji_categoria)
        for i, (rotulo, _funcao) in enumerate(consultas, start=1):
            print(f"{i}. {rotulo}")
        print("0. ↩️  Voltar para as categorias")
        opcao = input("\nEscolha uma consulta: ").strip()

        if opcao == "0":
            break

        if opcao.isdigit() and 1 <= int(opcao) <= len(consultas):
            _rotulo, funcao = consultas[int(opcao) - 1]

            # A consulta de subordinados por gestor precisa de um ID informado
            # pelo usuário; as demais são executadas sem parâmetros.
            if funcao is consulta_subordinados_por_gestor:
                id_gestor = ler_inteiro("ID do gestor")
                funcao(id_gestor)
            else:
                funcao()
        else:
            print("\n⚠️  Opção inválida. Tente novamente.")
            continue

        pausar()


def menu_consultas_frequentes():
    while True:
        exibir_cabecalho("Consultas Frequentes", "📈")
        for i, (titulo_categoria, emoji_categoria, _consultas) in enumerate(CATEGORIAS, start=1):
            print(f"{i}. {emoji_categoria} {titulo_categoria}")
        print("0. ↩️  Voltar ao menu principal")
        opcao = input("\nEscolha uma categoria: ").strip()

        if opcao == "0":
            break

        if opcao.isdigit() and 1 <= int(opcao) <= len(CATEGORIAS):
            menu_consultas_categoria(CATEGORIAS[int(opcao) - 1])
        else:
            print("\n⚠️  Opção inválida. Tente novamente.")


# ==============================================================================
# MENU PRINCIPAL
# ==============================================================================

while True:

    exibir_cabecalho("Sistema Interno de Viagens — WEG", "🚀")
    print(" 1. 🧳 Módulo de Viagens")
    print(" 2. 👤 Módulo de Colaboradores")
    print(" 3. 🏢 Módulo de Departamentos")
    print(" 4. 🚗 Módulo de Frota de Veículos")
    print(" 5. ✅ Módulo de Aprovações")
    print(" 6. 🤝 Módulo de Caronas")
    print(" 7. 💰 Módulo de Despesas")
    print(" 8. 🎯 Módulo de Objetivos de Viagem")
    print(" 9. 📊 Módulo de Análise de Eficácia")
    print("10  📈 Consultas Frequentes")
    print(" 0. 🚪 Sair do sistema")

    opcao = input("\nEscolha uma opção: ").strip()

    # Viagens
    if opcao == "1":
        menu_viagens()

    # Colaboradores
    elif opcao == "2":
        menu_colaboradores()

    # Departamentos
    elif opcao == "3":
        menu_departamentos()

    # Frota de veículos
    elif opcao == "4":
        menu_frota()

    # Aprovações
    elif opcao == "5":
        menu_aprovacoes()

    # Caronas
    elif opcao == "6":
        menu_caronas()

    # Despesas
    elif opcao == "7":
        menu_despesas()

    # Objetivos de viagem
    elif opcao == "8":
        menu_objetivos()

    # Análise de eficácia
    elif opcao == "9":
        menu_analise_eficacia()

    # Consultas frequentes
    elif opcao == "10":
        menu_consultas_frequentes()

    # Sair
    elif opcao == "0":
        print("\n👋 Encerrando o sistema. Até a próxima!")
        break

    else:
        print("\n⚠️  Opção inválida. Tente novamente.")