SELECT ROUND(SUM(receita), 2)  AS receita_total,
       ROUND(AVG(receita), 2)  AS ticket_medio,
       COUNT(*)                AS pedidos
FROM vendas;

SELECT categoria, ROUND(SUM(receita), 2) AS receita
FROM vendas
GROUP BY categoria
ORDER BY receita DESC
LIMIT 3;

SELECT regiao,
       ROUND(SUM(receita), 2) AS receita,
       ROUND(100.0 * SUM(receita) / (SELECT SUM(receita) FROM vendas), 1) AS pct
FROM vendas
GROUP BY regiao
ORDER BY receita DESC;

SELECT strftime('%Y-%m', data) AS mes,
       ROUND(SUM(receita), 2)  AS receita
FROM vendas
GROUP BY mes
ORDER BY mes;

SELECT canal, ROUND(AVG(receita), 2) AS ticket_medio
FROM vendas
GROUP BY canal
ORDER BY ticket_medio DESC;
