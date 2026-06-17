import streamlit as st
import pandas as pd

# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================
st.set_page_config(
    page_title="Finep Circular - Decisor",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# TÍTULO E INTRODUÇÃO
# ============================================================
st.title("♻️ Finep Circular – Ferramenta de Decisão")
st.markdown("""
**Simulador interativo para escolha do arranjo na chamada:**  
*Finep Mais Inovação Brasil – Rodada 2 – Economia Circular e Cidades Sustentáveis*

**Projeto base:**  
Compostagem descentralizada com transporte de resíduos orgânicos (bombonas de 50L) de restaurantes para o Assentamento Mário Lago (Ribeirão Preto).  
Os produtores rurais do assentamento **retiram os resíduos das bombonas**, colocam-nos em big bags para compostagem, **devolvem as bombonas vazias** aos restaurantes, utilizam o composto nas hortas e podem comercializar o excedente.
""")
st.divider()

# ============================================================
# SIDEBAR – PARÂMETROS DO PROJETO
# ============================================================
st.sidebar.header("⚙️ Parâmetros do Projeto")

# ---------- Porte da empresa ----------
porte = st.sidebar.selectbox(
    "Porte da Empresa (ou grupo econômico)",
    [
        "Microempresa e Pequeno Porte (ROB < R$ 4,8M)",
        "Pequena Empresa (ROB R$ 4,8M a R$ 16M)",
        "Média Empresa I (ROB R$ 16M a R$ 90M)",
        "Média Empresa II (ROB R$ 90M a R$ 300M)",
        "Grande Empresa (ROB > R$ 300M)"
    ],
    help="Receita Operacional Bruta do último ano com demonstrativos fechados (Anexo 1, item 6)."
)

# ---------- Valor total do projeto ----------
valor_total = st.sidebar.number_input(
    "Valor Total do Projeto (R$)",
    min_value=5_000_000,
    max_value=30_000_000,
    value=10_000_000,
    step=1_000_000,
    format="%d",
    help="Valor total = solicitação à Finep + contrapartida. Respeita os limites do arranjo (Anexo 1, item 5)."
)

# ---------- Arranjo (radio) ----------
arranjo = st.sidebar.radio(
    "Arranjo desejado",
    ["Simples", "Em Rede"],
    help="Escolha o arranjo de acordo com os participantes e regras (Anexo 1, item 3)."
)

# ---------- Coexecutoras (agora sempre visível) ----------
if arranjo == "Simples":
    num_coexec = st.sidebar.number_input(
        "Número de Coexecutoras (opcional, mínimo 0)",
        min_value=0,
        max_value=5,
        value=0,
        step=1,
        help="No Arranjo Simples, coexecutoras são opcionais (Regulamento, item 2.5)."
    )
    tem_rob_16 = True  # não é exigido no Simples
else:  # Em Rede
    num_coexec = st.sidebar.number_input(
        "Número de Coexecutoras (mínimo 2)",
        min_value=2,
        max_value=5,
        value=2,
        step=1,
        help="Quantas empresas parceiras (com fins lucrativos) participarão ativamente (Regulamento, item 2.5)."
    )
    tem_rob_16 = st.sidebar.checkbox(
        "Pelo menos uma empresa (proponente ou coexecutora) tem ROB ≥ R$ 16M?",
        help="Exigência obrigatória para Arranjo em Rede (Anexo 1, item 3.ii)."
    )

# ---------- ICTs ----------
st.sidebar.subheader("🏛️ Instituições Científicas (ICTs)")
ict_selecionadas = st.sidebar.multiselect(
    "Selecione a(s) ICT(s) participantes",
    ["UNAERP", "IFSP"],
    default=[],
    help="Pelo menos uma ICT é obrigatória (Regulamento, item 2.6). Pode selecionar ambas."
)

# Verifica se há ICT selecionada
sem_ict = len(ict_selecionadas) == 0

# ---------- Parceiro Social (facultativo) ----------
parceiro_social = st.sidebar.checkbox(
    "Incluir Parceiro Social (Cooperativa de Agricultores do Assentamento Mário Lago)",
    value=True,
    help="Gera 1 ponto extra no mérito. O parceiro NÃO recebe recursos financeiros da Finep, mas recebe as bombonas com resíduos para retirar o conteúdo e devolver as bombonas vazias."
)

# ---------- Botão de simulação ----------
simular = st.sidebar.button("🔄 Simular Cenário", type="primary", use_container_width=True)

# ---------- EXPANSORES COM EXPLICAÇÕES ----------
with st.sidebar.expander("📘 O que é uma Coexecutora?"):
    st.markdown("""
    **Definição (Regulamento, item 2.5, p.2):**  
    *"A participação da(s) Coexecutora(s) deverá ser efetiva e relevante na execução do projeto, não podendo se caracterizar como prestação de serviços."*

    **Requisitos:**
    - Deve ser **empresa com fins lucrativos** (CNPJ).
    - Realiza dispêndios próprios (gastos) no projeto.
    - No Arranjo Simples, são **opcionais**.
    - No Arranjo em Rede, são **obrigatórias no mínimo 2**.

    **Exemplo para seu projeto:**
    - **Transportadora** que faz a coleta e transporte das bombonas de 50L.
    - **Rede de restaurantes** que separa e armazena os resíduos orgânicos.
    - **Empresa de compostagem** que processa o material em big bags.

    ⚠️ **A cooperativa do assentamento NÃO pode ser coexecutora** – é parceira social (sem fins lucrativos).
    """)

with st.sidebar.expander("📘 O que é uma ICT?"):
    st.markdown("""
    **Definição (Regulamento, item 1.8, p.1-2):**  
    *"Instituições Científicas, Tecnológicas e de Inovação (ICTs) são órgãos ou entidades da administração pública ou pessoas jurídicas de direito privado sem fins lucrativos, com sede no Brasil, que incluam em sua missão a pesquisa básica ou aplicada ou o desenvolvimento de novos produtos, serviços ou processos."*

    **Papel no projeto:**
    - Parceria técnico-científica **obrigatória** (item 2.6).
    - Atuam em desenvolvimento, validação, prototipagem e transferência de tecnologia.
    - Remuneradas via rubrica **"Serviços de Consultoria"**.
    - Pode ter mais de uma ICT (ex.: UNAERP **e** IFSP).
    - Pelo menos uma ICT deve ser **independente** (não mantida pela proponente/coexecutoras).
    """)

with st.sidebar.expander("📘 O que é Parceiro Social?"):
    st.markdown("""
    **Definição (item 7.2.8, p.9-10):**  
    *"Participação de cooperativas de catadores, associações, redes organizadas, Organizações de Controle Social (OCS) ou demais formas coletivas de pequenos produtores da biodiversidade."*

    **No seu projeto:** a cooperativa de agricultores do Assentamento Mário Lago.

    **Fluxo real da parceria:**
    1. Os restaurantes geram resíduos orgânicos (restos de vegetais, frutas e comidas).
    2. A logística (proponente ou transportadora) coleta as bombonas de 50L **cheias** e leva até o assentamento.
    3. Os produtores rurais **retiram os resíduos** das bombonas e os colocam em **big bags** para transformar em composto.
    4. Os produtores **devolvem as bombonas vazias** aos restaurantes, que as enchem novamente.
    5. O composto gerado é utilizado nas hortas do assentamento.
    6. O **excedente** de hortaliças e do composto pode ser comercializado futuramente.

    **Regras:**
    - **Facultativo** – dá 1 ponto extra no mérito.
    - **Não pode receber recursos financeiros** da subvenção (não é beneficiária).
    - A participação é documentada pela **Carta de Manifestação de Interesse (Anexo 6)**.

    ⚠️ **O parceiro social recebe os insumos (resíduos) e a infraestrutura para compostagem, mas NÃO recebe dinheiro da Finep.**
    """)

with st.sidebar.expander("📘 O que é ROB (Receita Operacional Bruta)?"):
    st.markdown("""
    **ROB** significa **Receita Operacional Bruta**.

    - É a receita bruta da empresa com suas atividades operacionais principais, conforme consta no **Demonstrativo de Resultados do Exercício (DRE)**.
    - Para fins deste edital, considera-se a **ROB do último ano com demonstrativos financeiros fechados** (Anexo 1, item 6, p.4).

    **Para que serve?**
    - A ROB classifica o porte da empresa (Micro, Pequena, Média I, Média II ou Grande).
    - Essa classificação define o **percentual mínimo de contrapartida** que a empresa precisará aportar no projeto.

    **Atenção (Regulamento, item 4.5.1, p.4):**
    - No caso de propostas com **múltiplas empresas (coexecutoras)**, considera-se a ROB da **empresa de maior porte** para definir o percentual.
    - No caso de **grupo econômico**, considera-se o maior faturamento do grupo.

    **Exemplo prático:** Se a proponente tiver ROB de R$ 50M (Média I) e a coexecutora tiver R$ 200M (Média II), a contrapartida será calculada com base no porte da Média II (maior ROB).
    """)

st.sidebar.markdown("---")
st.sidebar.caption("**Referências:** Regulamento, Anexo 1, FAQ e Apresentação da chamada.")

# ============================================================
# DICIONÁRIOS E FUNÇÕES
# ============================================================

# Tabela de contrapartida (Anexo 1, item 6)
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

# Regras específicas por arranjo (para exibição)
regras = {
    "Simples": [
        "Participantes mínimos: 1 empresa proponente + 1 ICT",
        "Coexecutoras são **opcionais** (não obrigatórias)",
        "Valor solicitado à Finep: entre **R$ 5M e R$ 20M**",
        "Pelo menos uma ICT não pode ser instituída ou mantida pela proponente ou coexecutoras",
        "A cooperativa do assentamento pode ser **Parceira Social** (facultativo, +1 ponto) – ela recebe as bombonas, retira os resíduos para big bags, devolve as bombonas vazias, e utiliza o composto nas hortas. **Não recebe recursos financeiros da Finep.**"
    ],
    "Em Rede": [
        "Participantes mínimos: 1 proponente + **2 coexecutoras obrigatórias** + 1 ICT",
        "Pelo menos **5% do valor total** do projeto deve ser destinado a ICT(s)",
        "Ao menos uma empresa deve ter **ROB ≥ R$ 16M** no último ano fechado",
        "Proponente não pode pertencer ao mesmo grupo econômico de 2 ou mais coexecutoras",
        "Nenhuma coexecutora pode pertencer ao mesmo grupo econômico de outra",
        "A ICT responsável por ≥5% do orçamento não pode ser instituída/mantida por qualquer empresa do arranjo",
        "Todas as coexecutoras devem ser empresas com **fins lucrativos** (CNPJ). A cooperativa do assentamento é Parceira Social, não coexecutora."
    ]
}

def verificar_limites(arranjo, valor_total):
    if arranjo == "Simples":
        return 5_000_000 <= valor_total <= 20_000_000
    else:  # Rede
        return 5_000_000 <= valor_total <= 30_000_000

# ============================================================
# EXIBIÇÃO DOS RESULTADOS
# ============================================================

if simular:
    # ---- VALIDAÇÕES INICIAIS ----
    if sem_ict:
        st.error("❌ Você **deve** selecionar pelo menos uma ICT (UNAERP ou IFSP) para participar.")
        st.stop()

    if arranjo == "Em Rede" and num_coexec < 2:
        st.error("❌ No Arranjo em Rede, é obrigatório ter **no mínimo 2 coexecutoras**.")
        st.stop()

    if arranjo == "Em Rede" and not tem_rob_16:
        st.error("❌ No Arranjo em Rede, **pelo menos uma empresa** (proponente ou coexecutora) deve ter ROB ≥ R$ 16M.")
        st.stop()

    # ---- CÁLCULOS ----
    perc = contrapartida_table.get((porte, arranjo), None)
    if perc is None:
        st.error("Porte ou arranjo não encontrado na tabela de contrapartida.")
        st.stop()

    contrapartida = perc * valor_total
    finep = valor_total - contrapartida
    dentro_limites = verificar_limites(arranjo, valor_total)

    # ---- CABEÇALHO DOS RESULTADOS ----
    st.header("📊 Resultados da Simulação")
    st.markdown(f"**Arranjo selecionado:** `{arranjo}`  |  **Porte da empresa:** `{porte}`")

    # ---- MÉTRICAS PRINCIPAIS ----
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Percentual de Contrapartida", f"{perc:.1%}")
    with col2:
        st.metric("Valor da Contrapartida (R$)", f"R$ {contrapartida:,.2f}")
    with col3:
        st.metric("Valor Solicitado à Finep (R$)", f"R$ {finep:,.2f}")

    # ---- VERIFICAÇÃO DE LIMITES ----
    if dentro_limites:
        st.success(f"✅ O valor total (R$ {valor_total:,.2f}) está dentro dos limites para o arranjo {arranjo}.")
    else:
        limite = "R$ 20M" if arranjo == "Simples" else "R$ 30M"
        st.error(f"❌ O valor total (R$ {valor_total:,.2f}) **excede** o limite máximo para o arranjo {arranjo} ({limite}). Ajuste o valor ou mude o arranjo.")

    # ---- PARTICIPANTES ----
    st.subheader("👥 Participantes no Projeto")
    if arranjo == "Simples":
        st.markdown(f"- **Proponente:** 1 empresa (com fins lucrativos) – líder e responsável")
        st.markdown(f"- **Coexecutoras:** {num_coexec} (opcionais, você escolheu {num_coexec})")
        st.markdown(f"- **ICT(s):** {', '.join(ict_selecionadas) if ict_selecionadas else 'Nenhuma selecionada'} (obrigatória)")
    else:  # Rede
        st.markdown(f"- **Proponente:** 1 empresa (com fins lucrativos) – líder e responsável")
        st.markdown(f"- **Coexecutoras:** {num_coexec} empresas (com fins lucrativos) – obrigatórias, participação efetiva")
        st.markdown(f"- **ICT(s):** {', '.join(ict_selecionadas) if ict_selecionadas else 'Nenhuma selecionada'} (obrigatória, ≥5% do orçamento)")

    if parceiro_social:
        st.markdown("""
        - **Parceiro Social:** Cooperativa de Agricultores do Assentamento Mário Lago (facultativo, +1 ponto)  
          ↳ **Fluxo:** recebe as bombonas de 50L **cheias** → retira os resíduos para big bags → **devolve as bombonas vazias** aos restaurantes → compostagem → uso nas hortas → comercialização do excedente.  
          ⚠️ **Não recebe recursos financeiros da Finep** – apenas os insumos e suporte técnico.
        """)

    # ---- REGRAS DO ARRANJO ----
    with st.expander("📋 Regras do Arranjo Selecionado (clique para expandir)", expanded=True):
        for regra in regras[arranjo]:
            st.markdown(f"- {regra}")

    # ---- CHECKLIST DE ELEGIBILIDADE ----
    st.subheader("✅ Checklist de Elegibilidade para este Arranjo")

    check_items = []

    # Itens comuns
    check_items.append(("Há pelo menos uma ICT selecionada?", len(ict_selecionadas) >= 1, "Regulamento 2.6"))
    check_items.append(("Pelo menos uma ICT é independente (não mantida pela proponente)?", True, "Anexo 1, item 3 (verificar com as ICTs)"))
    check_items.append(("Valor total dentro do limite do arranjo?", dentro_limites, "Anexo 1, item 5"))
    if parceiro_social:
        check_items.append(("Parceiro Social tem Carta de Manifestação de Interesse (Anexo 6) assinada?", True, "Anexo 6 (obrigatório para pontuação)"))

    # Itens específicos
    if arranjo == "Simples":
        check_items.append(("Proponente é empresa com fins lucrativos?", True, "Regulamento 2.1"))
        # Para Simples, não exigimos ROB >=16M, mas podemos verificar se as coexecutoras são lucrativas se houver
        if num_coexec > 0:
            check_items.append(("Coexecutoras são empresas com fins lucrativos?", True, "Regulamento 2.1 (a verificar)"))
    else:  # Rede
        check_items.append(("Número de coexecutoras ≥ 2?", num_coexec >= 2, "Anexo 1, item 3.ii"))
        check_items.append(("Cada coexecutora é empresa com fins lucrativos?", True, "Regulamento 2.1 (a verificar)"))
        check_items.append(("Pelo menos uma empresa tem ROB ≥ R$ 16M?", tem_rob_16, "Anexo 1, item 3.ii"))
        check_items.append(("Proponente e coexecutoras não têm conflitos de grupo econômico?", True, "Anexo 1, item 3.ii (a verificar)"))

    # Exibe checklist
    for desc, ok, ref in check_items:
        icon = "✅" if ok else "❌"
        st.markdown(f"{icon} **{desc}** – *{ref}*" + ("" if ok else " ⚠️ **ATENÇÃO!**"))

    # ---- COMPARAÇÃO ENTRE OS DOIS ARRANJOS (MESMO PORTE) ----
    st.subheader("📊 Comparação Lado a Lado: Simples vs Rede (mesmo porte)")

    dados_comp = []
    for arr in ["Simples", "Em Rede"]:
        p = contrapartida_table.get((porte, arr), None)
        if p is not None:
            cp = p * valor_total
            fp = valor_total - cp
            dados_comp.append({
                "Arranjo": arr,
                "% Contrapartida": f"{p:.1%}",
                "Contrapartida (R$)": f"R$ {cp:,.2f}",
                "Finep (R$)": f"R$ {fp:,.2f}",
                "Limite Máximo Finep": "R$ 20M" if arr == "Simples" else "R$ 30M",
                "Coexecutoras obrigatórias": "Não" if arr == "Simples" else "Sim (≥2)"
            })
    df_comp = pd.DataFrame(dados_comp)
    st.table(df_comp)

    # Destaque da economia
    if arranjo == "Em Rede":
        perc_simples = contrapartida_table.get((porte, "Simples"), None)
        if perc_simples is not None:
            cp_simples = perc_simples * valor_total
            economia = cp_simples - contrapartida
            if economia > 0:
                st.success(f"💰 Comparado ao Arranjo Simples, você **economiza R$ {economia:,.2f}** em contrapartida com o Arranjo em Rede.")
            else:
                st.info("Para este porte, os percentuais de contrapartida são iguais nos dois arranjos.")
    else:
        perc_rede = contrapartida_table.get((porte, "Em Rede"), None)
        if perc_rede is not None:
            cp_rede = perc_rede * valor_total
            diferenca = contrapartida - cp_rede
            if diferenca > 0:
                st.info(f"Se optar pelo Arranjo em Rede, você poderia reduzir a contrapartida em R$ {diferenca:,.2f}, mas precisaria de 2 coexecutoras.")

    # ---- CAPACIDADE FINANCEIRA (item 7.1.7) ----
    st.subheader("💡 Verificação de Capacidade Financeira (Regulamento, item 7.1.7)")

    st.markdown("""
    A empresa deve atender **cumulativamente**:
    - **Patrimônio Líquido** positivo.
    - Pelo menos **um** dos seguintes parâmetros:
        1. Se Resultado Operacional (RO) for negativo:  
           Endividamento Oneroso ≤ 30% do Ativo Total **e** Contrapartida ≤ 50% do Ativo Total.
        2. Se RO for positivo e Contrapartida ≤ 20% do RO: OK.
        3. Se RO for positivo e Contrapartida > 20% do RO:  
           Endividamento Oneroso ≤ 30% do Ativo Total **e** Contrapartida ≤ 50% do Ativo Total.
    """)

    st.info(f"📌 **Para este cenário, a contrapartida exigida é de R$ {contrapartida:,.2f}.**  \nVerifique se sua empresa tem capacidade para aportar esse valor, consultando os demonstrativos financeiros.")

    # ---- EXEMPLO PRÁTICO PARA O PROJETO ----
    with st.expander("🌱 Exemplo prático para seu projeto (compostagem e hortas)", expanded=True):
        st.markdown("""
        **Cenário Simples (recomendado se você não tem 2 parceiras empresariais):**
        - **Proponente:** Sua empresa (logística reversa) – recebe R$ 7M da Finep e aporta R$ 3M.
        - **ICT:** UNAERP (validação e pesquisa).
        - **Parceiro Social:** Cooperativa do Assentamento – recebe as bombonas **cheias**, retira os resíduos para big bags, **devolve as bombonas vazias**, faz a compostagem, usa o composto nas hortas e pode vender o excedente.  
          ⚠️ **Não recebe dinheiro da Finep**, apenas os insumos e suporte técnico.
        - **Atividades:** Coleta, transporte, compostagem descentralizada, cultivo de hortaliças, monitoramento.
        - **Contrapartida:** 30% (exemplo para Média I) = R$ 3M.
        
        **Cenário Rede (se você tiver 2 parceiras):**
        - **Proponente:** Sua empresa – coordena, recebe R$ 8,5M, aporta R$ 1,5M.
        - **Coexecutora 1:** Transportadora local (faz o frete das bombonas de 50L).
        - **Coexecutora 2:** Rede de restaurantes (separa e armazena resíduos orgânicos).
        - **ICT:** IFSP ou UNAERP (validação).
        - **Parceiro Social:** Assentamento – recebe as bombonas, retira os resíduos, devolve as bombonas vazias, processa em big bags, usa composto nas hortas e comercializa excedente.
        - **Contrapartida:** 15% = R$ 1,5M (economia de R$ 1,5M em relação ao Simples).
        """)

    # ---- REFERÊNCIAS FINAIS ----
    st.divider()
    st.caption("**Referências:** Regulamento (itens 2.5, 2.6, 4.5, 7.1.7), Anexo 1 (itens 3, 5, 6), FAQ (p.4-9).")
    st.caption("Este simulador é uma ferramenta de apoio e não substitui a leitura integral do edital. Consulte um especialista para validação final.")

else:
    # ---- TELA INICIAL (antes da simulação) ----
    st.info("👈 **Preencha os parâmetros no painel lateral e clique em 'Simular Cenário'** para visualizar os resultados e comparar os arranjos.")

    st.markdown("""
    ### O que você vai encontrar aqui:
    - **Comparação lado a lado** dos dois arranjos (Simples vs Rede).
    - **Cálculo automático** da contrapartida e do valor da Finep.
    - **Checklist de elegibilidade** para cada arranjo.
    - **Explicações práticas** com exemplos do seu projeto.
    - **Alertas** sobre regras como: cooperativa não pode ser coexecutora, necessidade de 2 coexecutoras no Rede, ROB ≥ R$16M, etc.
    - **Fluxo real da parceria:** restaurantes → bombonas 50L (cheias) → assentamento → retirada dos resíduos → devolução das bombonas vazias → big bags → compostagem → hortas → venda do excedente.
    """)

# ============================================================
# RODAPÉ FIXO
# ============================================================
st.sidebar.markdown("---")
st.sidebar.caption("Desenvolvido para apoiar a tomada de decisão na chamada Finep Circular.")
