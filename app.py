import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(
    page_title="Finep Circular - Simulador",
    page_icon="♻️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Título principal
st.title("♻️ Finep Circular")
st.subheader("Simulador de Arranjos e Contrapartida")
st.markdown("**Finep Mais Inovação Brasil – Rodada 2 – Economia Circular e Cidades Sustentáveis**")
st.caption("Apoio à decisão para participação no edital")

# ============================================================
# SIDEBAR – Parâmetros do projeto
# ============================================================
st.sidebar.header("Parâmetros do Projeto")

# Porte da empresa (ou grupo econômico)
porte = st.sidebar.selectbox(
    "Porte da Empresa (ou grupo econômico)",
    ["Microempresa e Pequeno Porte (ROB < R$ 4,8M)",
     "Pequena Empresa (ROB R$ 4,8M a R$ 16M)",
     "Média Empresa I (ROB R$ 16M a R$ 90M)",
     "Média Empresa II (ROB R$ 90M a R$ 300M)",
     "Grande Empresa (ROB > R$ 300M)"],
    help="Considerar a Receita Operacional Bruta do último ano com demonstrativos fechados (Anexo 1, item 6)."
)

# Arranjo
arranjo = st.sidebar.radio(
    "Arranjo desejado",
    ["Simples", "Em Rede"],
    help="Escolha o arranjo de acordo com o número de participantes e regras (Anexo 1, item 3)."
)

# Valor total do projeto (R$)
valor_total = st.sidebar.number_input(
    "Valor Total do Projeto (R$)",
    min_value=5_000_000,
    max_value=30_000_000,
    value=10_000_000,
    step=1_000_000,
    format="%d",
    help="Valor total = solicitação à Finep + contrapartida. Respeite os limites do arranjo (Anexo 1, item 5)."
)

# Se arranjo em rede, perguntar número de coexecutoras (mínimo 2) e se alguma tem ROB >=16M
if arranjo == "Em Rede":
    num_coexec = st.sidebar.number_input(
        "Número de Coexecutoras (mínimo 2)",
        min_value=2,
        max_value=5,
        value=2,
        step=1,
        help="Quantas empresas coexecutoras participarão (Regulamento, item 2.5)."
    )
    tem_rob_16 = st.sidebar.checkbox(
        "Pelo menos uma empresa (proponente ou coexecutora) tem ROB ≥ R$ 16M?",
        help="Exigência para o Arranjo em Rede (Anexo 1, item 3.ii)."
    )
else:
    num_coexec = 0
    tem_rob_16 = True  # não é exigido no Simples

# Seleção de ICT(s)
st.sidebar.subheader("Instituições Científicas, Tecnológicas e de Inovação (ICTs)")

# Opções de ICT disponíveis
opcoes_ict = ["UNAERP", "IFSP", "Outra ICT"]
ict_selecionadas = st.sidebar.multiselect(
    "Selecione a(s) ICT(s) participantes",
    opcoes_ict,
    default=[],
    help="Pelo menos uma ICT é obrigatória (Regulamento, item 2.6). Para o Arranjo em Rede, exige-se ≥5% do orçamento para ICT(s)."
)

# Verificação: se nenhuma ICT selecionada, avisar
if len(ict_selecionadas) == 0:
    st.sidebar.warning("⚠️ Selecione pelo menos uma ICT (obrigatório).")

# Botão de simulação
simular = st.sidebar.button("Simular Cenário", type="primary")

# ============================================================
# EXPLICAÇÕES SOBRE COEXECUTORAS E ICT (fixas no sidebar)
# ============================================================
with st.sidebar.expander("📘 O que é uma Coexecutora?"):
    st.markdown("""
    **Definição (Regulamento, item 2.5, página 2):**
    > "A participação da(s) Coexecutora(s) deverá ser efetiva e relevante na execução do projeto, não podendo se caracterizar como prestação de serviços."
    
    **Requisitos:**
    - A coexecutora deve realizar dispêndios relativos às etapas de desenvolvimento.
    - Pode ser uma empresa brasileira com sede no país e com intuito lucrativo.
    - No Arranjo em Rede, são obrigatórias no mínimo 2 coexecutoras.
    """)

with st.sidebar.expander("📘 O que é uma ICT?"):
    st.markdown("""
    **Definição (Regulamento, item 1.8, páginas 1-2):**
    > "Instituições Científicas, Tecnológicas e de Inovação (ICTs) são órgãos ou entidades da administração pública ou pessoas jurídicas de direito privado sem fins lucrativos, com sede no Brasil, que incluam em sua missão a pesquisa básica ou aplicada ou o desenvolvimento de novos produtos, serviços ou processos."
    
    **Papel no projeto:**
    - Parceria técnico-científica obrigatória (item 2.6).
    - Atuam em desenvolvimento, validação, prototipagem e transferência de tecnologia.
    - Remuneradas via rubrica "Serviços de Consultoria".
    - Pelo menos uma ICT não pode ser instituída ou mantida pela proponente ou coexecutoras (Anexo 1, item 3.i e 3.ii).
    """)

# ============================================================
# DICIONÁRIO DE CONTRAPARTIDA
# ============================================================
contrapartida_table = {
    ("Microempresa e Pequeno Porte (ROB < R$ 4,8M)", "Simples"): 0.05,
    ("Microempresa e Pequeno Porte (ROB < R$ 4,8M)", "Em Rede"): 0.05,
    ("Pequena Empresa (ROB R$ 4,8M a R$ 16M)", "Simples"): 0.10,
    ("Pequena Empresa (ROB R$ 4,8M a R$ 16M)", "Em Rede"): 0.10,
    ("Média Empresa I (ROB R$ 16M a R$ 90M)", "Simples"): 0.30,
    ("Média Empresa I (ROB R$ 16M a R$ 90M)", "Em Rede"): 0.15,
    ("Média Empresa II (ROB R$ 90M a R$ 300M)", "Simples"): 0.40,
    ("Média Empresa II (ROB R$ 90M a R$ 300M)", "Em Rede"): 0.20,
    ("Grande Empresa (ROB > R$ 300M)", "Simples"): 0.50,
    ("Grande Empresa (ROB > R$ 300M)", "Em Rede"): 0.25,
}

# Regras específicas por arranjo
regras = {
    "Simples": [
        "Participantes mínimos: 1 empresa proponente + 1 ICT",
        "Coexecutoras são opcionais (não obrigatórias)",
        "Valor solicitado à Finep: entre R$ 5M e R$ 20M",
        "Pelo menos uma ICT não pode ser instituída ou mantida pela proponente ou coexecutoras"
    ],
    "Em Rede": [
        "Participantes mínimos: 1 proponente + 2 coexecutoras obrigatórias + 1 ICT",
        "Pelo menos 5% do valor total do projeto deve ser destinado a ICT(s)",
        "Ao menos uma empresa deve ter ROB ≥ R$ 16M no último ano fechado",
        "Proponente não pode pertencer ao mesmo grupo econômico de 2 ou mais coexecutoras",
        "Nenhuma coexecutora pode pertencer ao mesmo grupo econômico de outra coexecutora",
        "A ICT responsável por ≥5% do orçamento não pode ser instituída/mantida por qualquer empresa do arranjo"
    ]
}

# ============================================================
# FUNÇÃO PARA VERIFICAR LIMITES DE VALOR
# ============================================================
def verificar_limites(arranjo, valor_total):
    if arranjo == "Simples":
        return 5_000_000 <= valor_total <= 20_000_000
    else:  # Rede
        return 5_000_000 <= valor_total <= 30_000_000

# ============================================================
# EXIBIÇÃO DOS RESULTADOS
# ============================================================
if simular:
    st.header("📊 Resultados da Simulação")

    # ---- VALIDAÇÕES BÁSICAS ----
    # Verificar se há ICT selecionada
    if len(ict_selecionadas) == 0:
        st.error("❌ Você deve selecionar pelo menos uma ICT para participar do projeto.")
        st.stop()

    # Percentual de contrapartida
    perc = contrapartida_table.get((porte, arranjo), None)
    if perc is None:
        st.error("Porte ou arranjo não encontrado na tabela.")
        st.stop()

    # Cálculos
    contrapartida = perc * valor_total
    finep = valor_total - contrapartida

    # Verificar limites
    dentro_limites = verificar_limites(arranjo, valor_total)

    # ---- MÉTRICAS PRINCIPAIS ----
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Percentual de Contrapartida", f"{perc:.1%}")
    with col2:
        st.metric("Valor da Contrapartida (R$)", f"R$ {contrapartida:,.2f}")
    with col3:
        st.metric("Valor Solicitado à Finep (R$)", f"R$ {finep:,.2f}")

    st.divider()

    # ---- VERIFICAÇÃO DE LIMITES ----
    if dentro_limites:
        st.success(f"✅ O valor total do projeto (R$ {valor_total:,.2f}) está dentro dos limites permitidos para o arranjo {arranjo}.")
    else:
        limite_max = "R$ 20M" if arranjo == "Simples" else "R$ 30M"
        st.error(f"❌ O valor total do projeto (R$ {valor_total:,.2f}) NÃO está dentro dos limites para o arranjo {arranjo}. Limite máximo: {limite_max}.")

    # ---- PARTICIPANTES ----
    if arranjo == "Simples":
        participantes = "2 (1 proponente + 1 ICT)"
    else:
        participantes = f"4+ (1 proponente + {num_coexec} coexecutoras + 1 ICT)"
    st.info(f"👥 Participantes mínimos exigidos: **{participantes}**")

    # ---- ICT SELECIONADA(S) ----
    st.subheader("🏛️ ICT(s) selecionada(s)")
    st.write(", ".join(ict_selecionadas) if ict_selecionadas else "Nenhuma ICT selecionada")
    # Verificação de independência (simplificada): como não temos dados, apenas alertamos
    st.caption("⚠️ Verifique se pelo menos uma das ICTs não é mantida pela proponente ou coexecutoras (Anexo 1, item 3).")

    # ---- REGRAS DO ARRANJO ----
    with st.expander("📋 Regras do Arranjo Selecionado", expanded=True):
        for regra in regras[arranjo]:
            st.markdown(f"- {regra}")

    # ---- CONDIÇÕES ESPECÍFICAS PARA REDE ----
    if arranjo == "Em Rede":
        st.subheader("🔍 Verificação de Condições Específicas (Rede)")
        cond1 = num_coexec >= 2
        cond2 = tem_rob_16
        cond3 = (len(ict_selecionadas) > 0)  # existe ICT
        # A regra de 5% para ICT não pode ser verificada aqui, pois não temos o orçamento detalhado
        st.markdown(f"- **Coexecutoras suficientes?** {'✅ Sim' if cond1 else '❌ Não (mínimo 2)'}")
        st.markdown(f"- **Empresa com ROB ≥ R$ 16M?** {'✅ Sim' if cond2 else '❌ Não (exigência obrigatória)'}")
        st.markdown(f"- **ICT participante?** {'✅ Sim' if cond3 else '❌ Não (obrigatória)'}")
        st.markdown(f"- **≥5% do orçamento para ICT?** ⚠️ Deve ser previsto no plano de trabalho (Anexo 1, item 3.ii).")

        if not (cond1 and cond2 and cond3):
            st.warning("⚠️ Algumas condições do Arranjo em Rede não foram atendidas. Considere ajustar ou optar pelo Arranjo Simples.")

    # ---- COMPARAÇÃO COM OUTROS ARRANJOS (MESMO PORTE) ----
    st.subheader("📊 Comparação com outros arranjos (mesmo porte)")
    dados_comp = []
    for arr in ["Simples", "Em Rede"]:
        p = contrapartida_table.get((porte, arr), None)
        if p is not None:
            cp = p * valor_total
            fp = valor_total - cp
            dados_comp.append({
                "Arranjo": arr,
                "Percentual": f"{p:.1%}",
                "Contrapartida (R$)": f"R$ {cp:,.2f}",
                "Finep (R$)": f"R$ {fp:,.2f}",
                "Limite Max. Finep": "R$ 20M" if arr == "Simples" else "R$ 30M"
            })
    df_comp = pd.DataFrame(dados_comp)
    st.table(df_comp)

    # ---- CAPACIDADE FINANCEIRA (SIMPLIFICADA) ----
    st.subheader("💡 Verificação Rápida de Capacidade Financeira")
    st.markdown("""
    Com base no edital (item 7.1.7, páginas 6-7), a empresa deve atender:
    - Patrimônio Líquido **positivo**.
    - Pelo menos um dos seguintes:
        - Se Resultado Operacional (RO) for negativo: Endividamento Oneroso ≤ 30% do Ativo Total **e** Contrapartida ≤ 50% do Ativo Total.
        - Se RO for positivo: Contrapartida ≤ 20% do RO.
        - Se RO positivo e Contrapartida > 20% do RO: Endividamento Oneroso ≤ 30% do Ativo Total **e** Contrapartida ≤ 50% do Ativo Total.
    """)
    st.info(f"📌 Para este cenário, a contrapartida exigida é de **R$ {contrapartida:,.2f}**. Verifique se sua empresa tem capacidade para aportar esse valor, considerando os indicadores acima.")

    # ---- REFERÊNCIAS ----
    st.divider()
    st.caption("Referências: Regulamento (itens 2.5, 2.6, 4.5, 7.1.7) e Anexo 1 (itens 3, 5, 6) do edital.")
    st.caption("Este simulador é apenas uma ferramenta de apoio e não substitui a leitura integral do edital.")

else:
    st.info("👈 Preencha os parâmetros no painel lateral e clique em 'Simular Cenário' para visualizar os resultados.")

# ============================================================
# RODAPÉ
# ============================================================
st.sidebar.markdown("---")
st.sidebar.caption("Desenvolvido com ❤️ para a chamada Finep Circular")
