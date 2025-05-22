import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
import warnings

# Conexão
db_user = 'postgres'
db_pass = 'Luma1234'
db_host = 'localhost'
db_port = '5432'
db_name = 'ecommerce'

engine = create_engine(f'postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}')

# Extração
df_vendas = pd.read_sql('SELECT * FROM vendas_completas', engine)

# Transformações
df_vendas['data_venda'] = pd.to_datetime(df_vendas['data_venda'])
df_vendas['mes'] = df_vendas['data_venda'].dt.to_period('M').astype(str)

# KPIs
receita_total = df_vendas['valor_total'].sum()
receita_por_canal = df_vendas.groupby('canal')['valor_total'].sum().reset_index()
receita_mensal = df_vendas.groupby('mes')['valor_total'].sum().reset_index()
vendas_por_categoria = df_vendas.groupby('categoria')['valor_total'].sum().reset_index()
ticket_medio = receita_total / df_vendas['id'].nunique()

print(f"Receita Total: R${receita_total:,.2f}")
print(f"Ticket Médio: R${ticket_medio:,.2f}")

# Gráfico 1: Receita Mensal
fig1 = px.line(receita_mensal, x='mes', y='valor_total', title='Receita Mensal')
fig1.show()

# Gráfico 2: Receita por Canal
fig2 = px.bar(receita_por_canal, x='canal', y='valor_total', title='Receita por Canal', text='valor_total')
fig2.show()

# Gráfico 3: Vendas por Categoria
fig3 = px.bar(vendas_por_categoria, x='categoria', y='valor_total', title='Vendas por Categoria', text='valor_total')
fig3.show()

# Gráfico 4: Receita por Canal (Pizza)
fig4 = px.pie(receita_por_canal, names='canal', values='valor_total', title='Distribuição da Receita por Canal')
fig4.show()