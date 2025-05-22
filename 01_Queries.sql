CREATE TABLE clientes (
    id_cliente SERIAL PRIMARY KEY,
    nome VARCHAR(100),
    email VARCHAR(100),
    sexo VARCHAR(10),
    data_nascimento DATE,
    data_cadastro DATE
);

CREATE TABLE produtos (
    id_produto SERIAL PRIMARY KEY,
    nome_produto VARCHAR(100),
    categoria VARCHAR(50),
    preco NUMERIC(10,2)
);

CREATE TABLE vendas (
    id_venda SERIAL PRIMARY KEY,
    id_cliente INTEGER REFERENCES clientes(id_cliente),
    id_produto INTEGER REFERENCES produtos(id_produto),
    data_venda DATE,
    quantidade INTEGER,
    canal_venda VARCHAR(20)
);

--Criação das Views no PostgreSQL (cria uma view e na parte code insere os códigos abaixo, para cada view)
SELECT
    c.estado,
    p.categoria,
    v.canal,
    COUNT(*) AS total_vendas,
    SUM(v.valor_total) AS receita_total
FROM vendas v
JOIN clientes c ON v.id_cliente = c.id
JOIN produtos p ON v.id_produto = p.id
GROUP BY c.estado, p.categoria, v.canal;

SELECT
    DATE_TRUNC('month', data_venda) AS mes,
    SUM(valor_total) AS receita
FROM vendas
GROUP BY mes
ORDER BY mes;
