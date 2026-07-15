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

    sql = """
    SELECT id_colaborador, nome_colaborador, cargo_funcionario, email_colaborador, status_funcionario, possui_cnh, id_departamento
    FROM colaborador
    """
    cursor.execute(sql)
    dados = cursor.fetchall()

    print(f"\n{'ID':<5} | {'NOME':<25} | {'CARGO':<20} | {'E-MAIL':<28} | {'STATUS':<10} | {'CNH':<4} | {'DEPTO':<6}")
    print("-" * 105)
    for colaborador in dados:
        id_colaborador, nome, cargo, email, status, possui_cnh, id_departamento = colaborador
        nome_resumido = (nome[:22] + '...') if nome and len(nome) > 22 else (nome or '')
        cargo_resumido = (cargo[:17] + '...') if cargo and len(cargo) > 17 else (cargo or '')
        cnh_str = 'Sim' if possui_cnh else 'Não'
        print(f"{id_colaborador:<5} | {nome_resumido:<25} | {cargo_resumido:<20} | {email:<28} | {status:<10} | {cnh_str:<4} | {id_departamento:<6}")

    print(f"\nTotal de colaboradores: {len(dados)}")

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