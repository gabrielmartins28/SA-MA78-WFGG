from database import conectar


def inserir_colaborador(nome_colaborador, email_colaborador, telefone_colaborador, cargo_funcionario, status_funcionario, possui_cnh, id_departamento, id_gestor=None):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    INSERT INTO colaborador (nome_colaborador, email_colaborador, telefone_colaborador, cargo_funcionario, status_funcionario, possui_cnh, id_departamento, id_gestor)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    valores = (nome_colaborador, email_colaborador, telefone_colaborador, cargo_funcionario, status_funcionario, possui_cnh, id_departamento, id_gestor)

    cursor.execute(sql, valores)
    conexao.commit()

    print(f"✅ Colaborador {nome_colaborador} inserido com sucesso!")

    cursor.close()
    conexao.close()


def listar_colaborador():
    conexao = conectar()
    cursor = conexao.cursor()

    sql = "SELECT * FROM colaborador"
    cursor.execute(sql)
    resultado = cursor.fetchall()

    for colaborador in resultado:
        print(colaborador)

    cursor.close()
    conexao.close()


def atualizar_colaborador(id_colaborador, nome_colaborador, cargo_funcionario, email_colaborador):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    UPDATE colaborador
    SET nome_colaborador = %s, cargo_funcionario = %s, email_colaborador = %s
    WHERE id_colaborador = %s
    """
    valores = (nome_colaborador, cargo_funcionario, email_colaborador, id_colaborador)

    cursor.execute(sql, valores)
    conexao.commit()

    print(f"✅ Colaborador com ID {id_colaborador} atualizado com sucesso!")

    cursor.close()
    conexao.close()


def deletar_colaborador(id_colaborador):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = "DELETE FROM colaborador WHERE id_colaborador = %s"
    cursor.execute(sql, (id_colaborador,))
    conexao.commit()

    print(f"✅ Colaborador com ID {id_colaborador} deletado com sucesso!")

    cursor.close()
    conexao.close()