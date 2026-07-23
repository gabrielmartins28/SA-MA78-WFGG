# Módulo responsável por funcionalidades referentes a departamentos
from src.database import conectar


def listar_departamentos():
    conexao = conectar()
    cursor = conexao.cursor()

    sql = "SELECT id_departamento, nome_departamento, orcamento_departamento FROM departamentos"
    cursor.execute(sql)
    dados = cursor.fetchall()

    print(f"\n{'ID':<5} | {'DEPARTAMENTO':<30} | {'ORÇAMENTO':<15}")
    print("-" * 55)
    for departamento in dados:
        id_departamento, nome, orcamento = departamento
        orcamento_str = f"R$ {orcamento:,.2f}"
        print(f"{id_departamento:<5} | {nome:<30} | {orcamento_str:<15}")

    print(f"\nTotal de departamentos: {len(dados)}")

    cursor.close()
    conexao.close()


def cadastrar_departamento(nome, orcamento):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    INSERT INTO departamentos (nome_departamento, orcamento_departamento)
    VALUES (%s, %s)
    """
    valores = (nome, orcamento)
    cursor.execute(sql, valores)
    conexao.commit()
    print("Departamento cadastrado com sucesso!")

    cursor.close()
    conexao.close()


def atualizar_orcamento_departamento(id_departamento, novo_orcamento):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    UPDATE departamentos
    SET orcamento_departamento = %s
    WHERE id_departamento = %s
    """
    valores = (novo_orcamento, id_departamento)
    cursor.execute(sql, valores)
    conexao.commit()
    print("Orçamento atualizado!")

    cursor.close()
    conexao.close()


def deletar_departamento(id_departamento):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = "DELETE FROM departamentos WHERE id_departamento = %s"
    cursor.execute(sql, (id_departamento,))
    conexao.commit()
    print("Departamento deletado!")

    cursor.close()
    conexao.close()