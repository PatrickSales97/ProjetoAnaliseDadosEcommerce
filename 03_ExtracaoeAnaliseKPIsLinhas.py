import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

db_user = 'postgres'
db_pass = 'senhaaaa'
db_host = 'localhost'
db_port = '5432'
db_name = 'ecommerce'

import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns

# Conexão
engine = create_engine(f'postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}')

# Extração
df_vendas = pd.read_sql('SELECT * FROM vendas_completas', engine)

# Transformações
df_vendas['data_venda'] = pd.to_datetime(df_vendas['data_venda'])
df_vendas['mes'] = df_vendas['data_venda'].dt.to_period('M')

# KPI: Receita Total
receita_total = df_vendas['valor_total'].sum()

# KPI: Receita por Canal
receita_por_canal = df_vendas.groupby('canal')['valor_total'].sum()

# KPI: Receita Mensal
receita_mensal = df_vendas.groupby('mes')['valor_total'].sum()

# KPI: Vendas por Estado e Categoria (não temos estado, só categoria)
vendas_por_categoria = df_vendas.groupby('categoria')['valor_total'].sum()

# KPI: Ticket Médio
ticket_medio = receita_total / df_vendas['id'].nunique()

print(f"Receita Total: R${receita_total:,.2f}")
print(f"Ticket Médio: R${ticket_medio:,.2f}")

# Visualização Receita Mensal
plt.figure(figsize=(10,5))
sns.lineplot(x=receita_mensal.index.astype(str), y=receita_mensal.values)
plt.title('Receita Mensal')
plt.xticks(rotation=45)
plt.show()

warnings.filterwarnings('ignore')
