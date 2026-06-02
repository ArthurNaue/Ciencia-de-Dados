import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config
(
    page_title="Dashboard de Vendas",
    layout="wide"
)

data = pd.read_excel("Vendas_Base_de_Dados.xlsx")
data["Revenue"] = data["Quantidade"] * data["Valor Unitário"]

st.title("Dashboard de Vendas")
st.markdown("---")

st.sidebar.header("Filtros")

store_list = sorted(data["Loja"].unique())
store_list.insert(0, "Todas")

selected_store = st.sidebar.selectbox("Loja", store_list)

if selected_store == "Todas":
    store_data = data
else:
    store_data = data[data["Loja"] == selected_store]

product_list = sorted(store_data["Produto"].unique())
product_list.insert(0, "Todos")

selected_product = st.sidebar.selectbox("Produto", product_list)

if selected_product == "Todos":
    filtered_data = store_data
else:
    filtered_data = store_data[store_data["Produto"] == selected_product]

total_revenue = filtered_data["Revenue"].sum()

col1, col2 = st.columns([1, 2])

with col1:
    st.metric("Faturamento", f"R$ {total_revenue:,.2f}")

with col2:
    if selected_store != "Todas" and selected_product != "Todos":
        st.info
	(
            f"Na loja **{selected_store}**, o produto "
            f"**{selected_product}** faturou "
            f"**R$ {total_revenue:,.2f}**."
        )

st.subheader("Dados")
st.dataframe(filtered_data, use_container_width=True)

st.divider()

chart_data = 
(
    filtered_data.groupby("Loja")["Revenue"]
    .sum()
    .reset_index()
)

bar_chart = px.bar
(
    chart_data,
    x="Loja",
    y="Revenue",
    title="Faturamento por Loja",
    color="Loja",
    text_auto='.2s'
)

if selected_store != "Todas":
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.plotly_chart(bar_chart, use_container_width=True)
        
    with chart_col2:
        pie_data = data[data["Loja"] == selected_store]
        pie_data = 
	(
            pie_data.groupby("Produto")["Revenue"]
            .sum()
            .reset_index()
        )

        pie_chart = px.pie
	(
            pie_data,
            names="Produto",
            values="Revenue",
            title=f"Produtos da loja {selected_store}",
            hole=0.4
        )

        st.plotly_chart(pie_chart, use_container_width=True)
else:
    st.plotly_chart(bar_chart, use_container_width=True)