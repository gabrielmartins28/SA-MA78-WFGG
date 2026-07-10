from database import conectar

def cadastrar_analise_eficacia(data_analise, id_viagem, id_colaborador, indicador_sucesso, observacao_colaborador):
    conexao = conectar()
    cursor = conexao.cursor()
    sql = """
    INSERT INTO analise_eficacia_viagem (data_analise, id_viagem, id_colaborador, indicador_sucesso, observacao_colaborador)
    VALUES (%s, %s, %s, %s, %s)
    """
    valores = (data_analise, id_viagem, id_colaborador, indicador_sucesso, observacao_colaborador)
    cursor.execute(sql, valores)
    conexao.commit()
    print("Análise de eficácia cadastrada!")
    cursor.close()
    conexao.close()

def listar_analises_eficacia():
    conexao = conectar()
    cursor = conexao.cursor()
    sql = "SELECT id_analise, data_analise, id_viagem, id_colaborador, indicador_sucesso, observacao_colaborador FROM analise_eficacia_viagem"
    cursor.execute(sql)
    dados = cursor.fetchall()

    print(f"\n{'ID':<5} | {'DATA':<12} | {'ID VIAGEM':<10} | {'ID COLAB':<10} | {'IND. SUCESSO':<13} | {'OBSERVAÇÃO':<40}")
    print("-" * 100)
    for analise in dados:
        id_analise, data, id_viagem, id_colab, indicador, obs = analise
        
        # Formatando a data caso ela retorne como objeto date do MySQL
        data_str = data.strftime('%d/%m/%Y') if data and hasattr(data, 'strftime') else str(data or '')
        obs_resumida = (obs[:37] + '...') if obs and len(obs) > 37 else (obs or '')
        
        print(f"{id_analise:<5} | {data_str:<12} | {id_viagem:<10} | {id_colab:<10} | {indicador:<13} | {obs_resumida:<40}")

    print("\nConsulta de análises de eficácia finalizada.")
    cursor.close()
    conexao.close()

def atualizar_analise_eficacia(id_analise, nova_data, novo_id_viagem, novo_id_colaborador, novo_indicador, nova_observacao):
    conexao = conectar()
    cursor = conexao.cursor()
    sql = """
    UPDATE analise_eficacia_viagem 
    SET data_analise = %s, id_viagem = %s, id_colaborador = %s, indicador_sucesso = %s, observacao_colaborador = %s 
    WHERE id_analise = %s
    """
    valores = (nova_data, novo_id_viagem, novo_id_colaborador, novo_indicador, nova_observacao, id_analise)
    cursor.execute(sql, valores)
    conexao.commit()
    print(f"Análise ID {id_analise} atualizada com sucesso.")
    cursor.close()
    conexao.close()

def deletar_analise_eficacia(id_analise):
    conexao = conectar()
    cursor = conexao.cursor()
    sql = "DELETE FROM analise_eficacia_viagem WHERE id_analise = %s"
    cursor.execute(sql, (id_analise,))
    conexao.commit()
    print(f"Análise ID {id_analise} deletada.")
    cursor.close()
    conexao.close()