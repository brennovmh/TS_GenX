import pandas as pd
import streamlit as st
import plotly.express as px

# Carregar os dados ### ALTERE AQUI O ARQUIVO QUANDO NECESSÁRIO
df = pd.read_csv("tpm_filtrado_TS.csv", decimal=',')

# Adicionar a logo no topo
logo_path = "HCB.png"
st.image(logo_path, use_column_width=False)

# Título da aplicação
st.title("Análise de Expressão Diferencial")

# Campo para exploração de dados
st.sidebar.subheader("Selecione um gene")

# Corrigir o nome da variável para 'selected_gene'
selected_gene = st.sidebar.selectbox("Selecione um gene:", df['gene_symbol'].unique())

# Filtrar o DataFrame com base no gene selecionado
selected_gene_df = df[df['gene_symbol'] == selected_gene]

# Criar caixas de seleção para escolher amostras
selected_samples = st.multiselect("Escolha as amostras:", selected_gene_df.columns[1:])

if selected_samples:
    # Filtrar o DataFrame com base nas amostras selecionadas
    filtered_df = selected_gene_df[['gene_symbol'] + selected_samples].melt(id_vars='gene_symbol', var_name='Amostras', value_name='Log2-TPM')

    # Tratar valores não numéricos ou vazios antes da conversão
    filtered_df['Log2-TPM'] = pd.to_numeric(filtered_df['Log2-TPM'].str.replace(',', '.'), errors='coerce')

    # Remover linhas com valores nulos após a conversão
    filtered_df = filtered_df.dropna()

    # Plotar o gráfico de barras
    fig = px.bar(
        filtered_df,
        x='Amostras',
        y='Log2-TPM',
        color='Amostras',
        labels={"Log2-TPM": "Log2-TPM", "Amostras": "Amostras"},
        title=f"Expressão Gênica para {selected_gene}",
    )
    fig.update_layout(
        width=900,
        height=550,
        font=dict(
            family="Arial",
            size=18,
            color="RebeccaPurple"
        )
    )

    # Exibir o gráfico
    st.plotly_chart(fig)
else:
    st.warning("Selecione ao menos uma amostra para visualizar os dados.")

