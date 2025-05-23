import pandas as pd
import random
from faker import Faker
from sqlalchemy import create_engine
from datetime import datetime, timedelta

# Configuração do banco
db_user = 'postgres'
db_pass = 'senha'
db_host = 'localhost'
db_port = '5432'
db_name = 'ecommerce'
engine = create_engine(f'postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}')

fake = Faker()

# ---------- CLIENTES ----------
clientes = []
for _ in range(1000):
    clientes.append({
        'nome': fake.name(),
        'email': fake.email(),
        'cidade': fake.city(),
        'estado': fake.state_abbr()
    })
df_clientes = pd.DataFrame(clientes)
df_clientes.to_sql('clientes', engine, if_exists='append', index=False)

# ---------- PRODUTOS ----------
categorias = ['Eletrônicos', 'Roupas', 'Alimentos', 'Livros']
produtos = []
for i in range(50):
    produtos.append({
        'nome': f'Produto {i+1}',
        'categoria': random.choice(categorias),
        'preco': round(random.uniform(10, 500), 2)
    })
df_produtos = pd.DataFrame(produtos)
df_produtos.to_sql('produtos', engine, if_exists='append', index=False)

# ---------- VENDAS ----------
clientes_ids = list(range(1, 1001))
produtos_ids = list(range(1, 51))
canais = ['Online', 'Loja Física', 'Marketplace']

vendas = []
for _ in range(10000):  # 10 mil vendas
    cliente = random.choice(clientes_ids)
    produto = random.choice(produtos_ids)
    quantidade = random.randint(1, 5)
    preco = df_produtos.loc[produto - 1, 'preco']
    data_venda = fake.date_between(start_date='-1y', end_date='today')
    canal = random.choice(canais)
    vendas.append({
        'id_cliente': cliente,
        'id_produto': produto,
        'data_venda': data_venda,
        'quantidade': quantidade,
        'canal': canal,
        'valor_total': round(preco * quantidade, 2)
    })

df_vendas = pd.DataFrame(vendas)
df_vendas.to_sql('vendas', engine, if_exists='append', index=False)

print("Dados inseridos com sucesso!")
