import psycopg2

-- 1. Muestre todos los restaurantes que ofrezcan un plato especı́fico 
-- ingresado y que esté disponible.

conn = psycopg2.connect(
    dbname="grupo37",
    user="grupo37",
    password="areupwned",
    host="pavlov.ing.puc.cl",
    port="22"
)

nombre_del_plato = 'Pizza Margarita'-- TODO: HACERLO VARIABLE!

query_one = """
SELECT restaurante.nombre
FROM restaurante
JOIN plato ON restaurante.nombre = plato.nombre_restaurante
WHERE plato.nombre = (%s) AND plato.disponibilidad = TRUE;
"""

cur = conn.cursor()

cur.execute(query_one, (nombre_del_plato,))

response = cur.fetchall()

for row in response:
    print("row",row)

cur.close()
conn.close()

-- 2. Muestre todos los pedidos de un usuario especı́fico ingresado y 
-- su gasto mensual (solo los pedidos concretados)

conn = psycopg2.connect(
    dbname="grupo37",
    user="grupo37",
    password="areupwned",
    host="pavlov.ing.puc.cl",
    port="22"
)

nombre_cliente = '//TODO: nombre clienteeeee'

query_two = """
SELECT Cliente.email, 
       EXTRACT(MONTH FROM Pedido.fecha) AS Mes,
	   COUNT(Pedido.id) AS Total_Pedidos,
       SUM(Pedido.costo) AS Gasto_Mensual
FROM Cliente
JOIN Pedido ON Cliente.email = Pedido.email_cliente
WHERE (Cliente.email = (%s) AND Pedido.estado = 'entregado a cliente')
GROUP BY Cliente.email, EXTRACT(MONTH FROM Pedido.fecha);
"""

cur = conn.cursor()

cur.execute(query_two, (email_cliente,MONTHHHFORMATO))

response = cur.fetchall()

for row in response:
    print("Restaurante:", row[0])


cur.close()
conn.close()

-- 3. Muestre todos pedidos concretados y cancelados y el valor 
-- total de ellos

cur = conn.cursor()

query_three = """
SELECT 
    'Concretado' AS estado,
    SUM(pedido.costo) AS valor_total
FROM pedido
WHERE estado = 'entregado a cliente'
UNION ALL
SELECT 
    'Cancelado' AS estado,
    SUM(pedido.costo) AS valor_total
FROM pedido
WHERE estado IN ('Cliente cancela', 'restaurant cancela', 'delivery cancela');
"""

cur.execute(query_three)
result = cur.fetchall()

for row in result:
    print(row)

cur.close()
conn.close()

-- 4. Dado un estilo de plato ingresado por el usuario, muestre todas los platos con ese tipo,
-- los restaurantes que las ofrecen y las opciones de delivery.

cur = conn.cursor()

estilo_plato = 'Internacional' --TODO: ESTILO DE PLATO DINAMICO

query_four = """
SELECT plato.nombre AS plato,
plato.estilo AS estilo,
restaurante.nombre AS restaurante,
sucursal.sucursal AS sucursal,
delivery.nombre  AS delivery
FROM plato

JOIN restaurante ON plato.nombre_restaurante = restaurante.nombre

JOIN sucursal ON restaurante.nombre = sucursal.nombre_restaurante

JOIN delivery_de_sucursal ON sucursal.id = delivery_de_sucursal.id_sucursal

JOIN delivery ON delivery_de_sucursal.id_delivery = delivery.id

	
WHERE plato.estilo = (%s);
"""

cur.execute(query_four, (estilo_plato,))
result = cur.fetchall()

for row in result:
    print(row)

cur.close()
conn.close()

-- 5. Dado un estilo de plato seleccionado por el usuario, muestre 
--todas las platos que pertenezcan a ese estilo y sus restricciones.

cur = conn.cursor()

estilo_plato = 'TODO: ESTILO DE PLATO AQUI'

query_five = """
SELECT plato.restriccion AS restriccion,
       string_agg(plato.nombre, ', ') AS platos
FROM plato
WHERE plato.estilo = (%S) 
GROUP BY plato.restriccion;
""" --TODO: SE VEN LAS RESTRICCIONES COMO INT, HAY QUE PASARLAS A STRING

cur.execute(query_five, (estilo_plato,))
result = cur.fetchall()

for row in result:
    print(row)

cur.close()
conn.close()

-- 6. Dado un cliente ingresado por el usuario, muestre todas las restaurantes 
-- a las que tiene acceso con sus suscripciones.

cur = conn.cursor()

nombre_cliente = 'Agustin Reyes' TODO: cambiar variable

-- TODO: OPTIMISZAR LOS JOINS AQUI Y EN LA ANTERIOR CONSULTA
-- EN ESPECIAL LOS LEFT JOIN REVISAR BIEN!!!!!!!!!!!!!
-- query_six = """
-- SELECT cliente.nombre AS cliente,
-- 	string_agg(restaurante.nombre,', ') AS restaurante
-- FROM cliente

-- JOIN suscripcion 
--     ON cliente.id = suscripcion.id_cliente
-- JOIN delivery AS delivery_suscripcion
-- 	ON delivery_suscripcion.id = suscripcion.id_delivery

-- JOIN delivery_de_sucursal 
-- 	ON delivery_de_sucursal.id_delivery = delivery_suscripcion.id
	
-- JOIN delivery AS delivery
-- 	ON delivery.id = delivery_de_sucursal.id_sucursal


-- JOIN sucursal
-- 	ON sucursal.id = delivery_de_sucursal.id_sucursal

-- JOIN restaurante ON
-- 	sucursal.nombre_restaurante = restaurante.nombre

-- WHERE suscripcion.estado = 'Vigente' AND cliente.nombre = (%s)
-- GROUP BY cliente.nombre;

-- """
        query_six = """
        SELECT cliente.email AS cliente,
            string_agg(restaurante.nombre,', ') AS restaurante
        FROM cliente

        JOIN suscripcion 
            ON cliente.id = suscripcion.id_cliente
        JOIN delivery AS delivery_suscripcion
            ON delivery_suscripcion.id = suscripcion.id_delivery
        JOIN delivery_de_sucursal 
            ON delivery_de_sucursal.id_delivery = delivery_suscripcion.id
            
        JOIN delivery AS delivery
            ON delivery.id = delivery_de_sucursal.id_sucursal
        JOIN sucursal
            ON sucursal.id = delivery_de_sucursal.id_sucursal
        JOIN restaurante ON
            sucursal.nombre_restaurante = restaurante.nombre

        WHERE suscripcion.estado = 'Vigente' AND cliente.email = (%s)
        GROUP BY cliente.email;
            """


cur.execute(query_six, (nombre_cliente,))
result = cur.fetchall()

for row in result:
    print(row)

cur.close()
conn.close()

-- 7. Muestre la suma de dinero gastada por cada cliente en pedidos 
-- no incluidas en planes de suscripción.

cur = conn.cursor()


-- query_seven = """
-- SELECT cliente.nombre AS cliente,
-- 	COALESCE(SUM(pedido.costo), 0) AS suma_gastada
-- FROM cliente

-- LEFT JOIN pedido
-- 	ON pedido.email_cliente = cliente.email
-- JOIN suscripcion
-- 	ON suscripcion.id_cliente = cliente.id AND (suscripcion.estado = 'Cancelada' OR suscripcion IS NULL)
-- GROUP BY cliente.nombre;
-- """

        query_seven = """
        SELECT cliente.email AS cliente,
            COALESCE(SUM(pedido.costo), 0) AS suma_gastada
        FROM cliente

        LEFT JOIN pedido
            ON pedido.email_cliente = cliente.email
        JOIN suscripcion
            ON suscripcion.id_cliente = cliente.id AND (suscripcion.estado = 'Cancelada' OR suscripcion IS NULL)
        GROUP BY cliente.email;
            """

cur.execute(query_seven)
result = cur.fetchall()

for row in result:
    print(row)

cur.close()
conn.close()

-- 8. Muestre todos los platos y los restaurantes que los ofrecen.

cur = conn.cursor()


query_eight = """
SELECT plato.nombre AS plato,
       string_agg(restaurante.nombre,', ') AS restaurante
FROM plato

JOIN Restaurante 
    ON plato.nombre_restaurante = restaurante.nombre
GROUP BY plato.nombre;
"""

cur.execute(query_eight)

-- 9. Dado un número ingresado por el usuario, muestre todos las evaluaciones de Clientes,
-- Delivery, Despachador y Restaurant/sucursal superiores a él.


numero_ingresado = 'TODO: NUMERO INGRESADO AQUI'

query_nine = """
-- SELECT cliente.email AS cliente,
-- 	delivery.nombre AS delivery,
-- 	despachador.nombre AS despachador,
-- 	sucursal.sucursal AS sucursal,
-- 	restaurante.nombre AS restaurante 
	
-- FROM cliente
-- 	WHERE cliente.puntaje > (%s),


SELECT 
    'cliente' AS entidad,
    email AS nombre,
    CAST(puntaje AS TEXT) AS puntaje_cliente,
    NULL AS puntaje_delivery,
    NULL AS puntaje_despachador,
    NULL AS puntaje_sucursal,
    NULL AS puntaje_restaurante
FROM 
    cliente
WHERE 
    puntaje > 1 AND puntaje <= 5

UNION ALL

SELECT 
    'delivery' AS entidad,
    nombre AS nombre,
    NULL AS puntaje_cliente,
    CAST(puntaje AS TEXT) AS puntaje_delivery,
    NULL AS puntaje_despachador,
    NULL AS puntaje_sucursal,
    NULL AS puntaje_restaurante
FROM 
    delivery
WHERE 
    puntaje > 1 AND puntaje <= 5

UNION ALL

SELECT 
    'despachador' AS entidad,
    nombre AS nombre,
    NULL AS puntaje_cliente,
    NULL AS puntaje_delivery,
    CAST(puntaje AS TEXT) AS puntaje_despachador,
    NULL AS puntaje_sucursal,
    NULL AS puntaje_restaurante
FROM 
    despachador
WHERE 
    puntaje > 1 AND puntaje <= 5

UNION ALL

SELECT 
    'sucursal' AS entidad,
    sucursal AS nombre,
    NULL AS puntaje_cliente,
    NULL AS puntaje_delivery,
    NULL AS puntaje_despachador,
    CAST(puntaje AS TEXT) AS puntaje_sucursal,
    NULL AS puntaje_restaurante
FROM 
    sucursal
WHERE 
    puntaje > 1 AND puntaje <= 5

UNION ALL

SELECT 
    'restaurante' AS entidad,
    nombre AS nombre,
    NULL AS puntaje_cliente,
    NULL AS puntaje_delivery,
    NULL AS puntaje_despachador,
    NULL AS puntaje_sucursal,
    CAST(puntaje AS TEXT) AS puntaje_restaurante
FROM 
    restaurante
WHERE 
    puntaje > 1 AND puntaje <= 5;


TODO:: DEBE ESTAR COMPLETADO EL PEDIDO RESTRICCION

"""

cur.execute(query_nine)
result = cur.fetchall()

for row in result:
    print(row)

cur.close()
conn.close()

-- 10. Dado una un alergeno seleccionado por el usuario, muestre todos los platos 
-- que lo contengan en sus ingredientes (Ejemplo: manı́).


restricciones = {
    'vegano': 1,
    'vegetariano': 2,
    'alergicos': 3,
    'celiacos': 4,
    'diabeticos': 5,
    'pescetarianos': 6,
    'vegetarianos': 7,
    'veganos': 8
}


query_ten = """
SELECT CASE
           WHEN plato.restriccion = 1 THEN 'vegano'
           WHEN plato.restriccion = 2 THEN 'vegetariano'
           WHEN plato.restriccion = 3 THEN 'alergicos'
           WHEN plato.restriccion = 4 THEN 'celiacos'
           WHEN plato.restriccion = 5 THEN 'diabeticos'
           WHEN plato.restriccion = 6 THEN 'pescetarianos'
           WHEN plato.restriccion = 7 THEN 'vegetarianos'
           WHEN plato.restriccion = 8 THEN 'veganos'
           ELSE CAST(plato.restriccion AS TEXT)
       END AS Restriccion,
       STRING_AGG(plato.nombre, ', ') AS Platos
FROM Plato
WHERE Plato.restriccion = (%s)

	GROUP BY CASE
             WHEN plato.restriccion = 1 THEN 'vegano'
             WHEN plato.restriccion = 2 THEN 'vegetariano'
             WHEN plato.restriccion = 3 THEN 'alergicos'
             WHEN plato.restriccion = 4 THEN 'celiacos'
             WHEN plato.restriccion = 5 THEN 'diabeticos'
             WHEN plato.restriccion = 6 THEN 'pescetarianos'
             WHEN plato.restriccion = 7 THEN 'vegetarianos'
             WHEN plato.restriccion = 8 THEN 'veganos'
             ELSE CAST(plato.restriccion AS TEXT)
         END,
         plato.ingredientes;
"""

cur.execute(query_ten, (restricciones['alergicos'],))
result = cur.fetchall()

for row in result:
    print(row)

cur.close()
conn.close()