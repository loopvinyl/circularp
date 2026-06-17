# Finep Circular – Simulador de Arranjos e Contrapartida

Aplicativo interativo para simular cenários de participação no edital **Finep Mais Inovação Brasil – Rodada 2 – Economia Circular e Cidades Sustentáveis**.

## Funcionalidades

- Seleção do porte da empresa (ou grupo econômico)
- Escolha entre **Arranjo Simples** e **Arranjo em Rede**
- Definição do valor total do projeto
- Cálculo automático de:
  - Percentual de contrapartida
  - Valor da contrapartida (aportado pela empresa)
  - Valor solicitado à Finep
  - Verificação de limites mínimos e máximos
- Exibição das regras específicas de cada arranjo
- Verificação de condições obrigatórias (principalmente para Rede)
- Tabela comparativa com outros arranjos para o mesmo porte
- Orientações sobre capacidade financeira (com base no item 7.1.7 do regulamento)

## Como usar

1. Acesse o app online (ou execute localmente).
2. No painel lateral, preencha:
   - Porte da empresa
   - Arranjo desejado
   - Valor total do projeto
   - (se Rede) número de coexecutoras e se alguma tem ROB ≥ R$16M
3. Clique em **Simular Cenário**.
4. Analise os resultados e as recomendações.

## Deploy

### Via Streamlit Cloud (recomendado)

1. Faça o fork ou clone este repositório.
2. Acesse [share.streamlit.io](https://share.streamlit.io) e conecte sua conta GitHub.
3. Selecione o repositório e o branch principal.
4. O Streamlit detectará automaticamente o `app.py` e instalará as dependências a partir do `requirements.txt`.

### Execução local

```bash
pip install -r requirements.txt
streamlit run app.py
