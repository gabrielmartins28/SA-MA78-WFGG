# 📖 Histórias de Usuário (User Stories) - Sistema Corporativo de Viagens WEG

Este documento traduz os Requisitos Funcionais e Regras de Negócio em Histórias de Usuário no formato ágil.

---

## 👤 Epico 01: Gestão de Pessoas e Infraestrutura
* **US01 - Cadastro de Gestores e Colaboradores:** 
  > **Como** Administrador do Sistema,  
  > **Quero** cadastrar colaboradores informando cargo, CNH e gestor direto,  
  > **Para que** a hierarquia e as permissões de direção sejam respeitadas no fluxo de viagens.

* **US02 - Gestão de Frota e Bloqueios:**  
  > **Como** Gestor de Frota,  
  > **Quero** gerenciar os veículos da empresa e suas disponibilidades,  
  > **Para que** não haja choque de datas nem alocação de motoristas sem CNH válida.

---

## 🚗 Epico 02: Solicitação e Otimização de Viagens
* **US03 - Solicitação de Viagem com Propósito:**  
  > **Como** Colaborador Solicitante (ex: Carlos Mendes),  
  > **Quero** solicitar uma viagem escolhendo destino, veículo e o objetivo pré-cadastrado,  
  > **Para que** meu pedido tenha justificativa clara e passe pela validação do meu gestor.

* **US04 - Inclusão de Caronas:**  
  > **Como** Colaborador Solicitante,  
  > **Quero** vincular outros colaboradores como carona na minha solicitação,  
  > **Para que** a frota da empresa seja otimizada e o custo por pessoa seja reduzido.

---

## 💰 Epico 03: Aprovação, Custos e Avaliação (ROI)
* **US05 - Aprovação com Trava Orçamentária:**  
  > **Como** Gestor Aprovador (ex: Ana Ferreira),  
  > **Quero** aprovar ou rejeitar solicitações com base no saldo orçamentário do meu departamento,  
  > **Para que** os custos de viagem não excedam o limite mensal definido.

* **US06 - Lançamento e Prestação de Contas:**  
  > **Como** Colaborador Viajante,  
  > **Quero** lançar os comprovantes e despesas (hotel, alimentação, combustível),  
  > **Para que** o custo seja atrelado ao Centro de Custo correto.

* **US07 - Avaliação de Eficácia pós-viagem:**  
  > **Como** Gestor Aprovador,  
  > **Quero** atribuir uma nota de 1 a 5 e um parecer técnico após a conclusão da viagem,  
  > **Para que** a empresa mensure o Retorno sobre o Investimento (ROI).