# Módulo responsável por funcionalidades referentes a departamentos
from database import conectar

def listar_departamentos():
    conexao = conectar()
    cursor = conexao.cursor()
    
    sql = "SELECT id_departamento, nome_departamento, orcamento_departamento FROM departamentos"
    cursor.execute(sql)
    dados = cursor.fetchall()

    for depto in dados:
        print(depto)

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