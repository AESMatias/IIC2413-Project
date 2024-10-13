import cgi
import psycopg2
from flask import Flask, request, render_template_string, send_file

#TODO: Hay que aplicar STRIP a todos los datos entrantes.
#ENTRANTES #TODO:
app = Flask(__name__, static_url_path='/static')

conn = psycopg2.connect(
    database="db_name",
    user="username",
    password="password",
    host="hostname"
)

cursor = conn.cursor()
form = cgi.FieldStorage()

def validar_cadena_sql(cadena):
    caracteres_prohibidos = ["'", '"', ';', '--', '/*', '*/']
    for caracter in caracteres_prohibidos:
        if caracter in cadena:
            return False
    return True

@app.get('/')
def home():
    return send_file('static/index.html')

@app.get('/consultas')
def consultas():
    return send_file('static/consultas.html')

@app.get('/form_consulta_one')
def form_consulta_one():
    return send_file('static/form_consulta_one.html')

@app.get('/form_consulta_two')
def form_consulta_two():
    return send_file('static/form_consulta_two.html')

@app.get('/form_consulta_four')
def form_consulta_four():
    return send_file('static/form_consulta_four.html')

@app.get('/form_consulta_five')
def form_consulta_five():
    return send_file('static/form_consulta_five.html')

@app.get('/form_consulta_six')
def form_consulta_six():
    return send_file('static/form_consulta_six.html')

@app.get('/form_consulta_nine')
def form_consulta_nine():
    return send_file('static/form_consulta_nine.html')

@app.get('/form_consulta_ten')
def form_consulta_ten():
    return send_file('static/form_consulta_ten.html')


#TODO: This routes should be in separated modules for better organization.

# Ruta para la primera consulta primaria solicitada en la entrega
@app.route('/consulta_primaria', methods=['POST'])
def consultar_primaria():
    # Obtener los datos del formulario
    form_atributos = request.form['atributos']
    form_tablas = request.form['tablas']
    form_condiciones = request.form['condiciones']


    # Verificamos que todos los valores sean strings y que "atributos" y "condiciones" no sean nulos.
    if (
        form_atributos is not None and isinstance(form_atributos, str) and
        isinstance(form_tablas, str) and
        form_condiciones is not None and isinstance(form_condiciones, str)
        and ((validar_cadena_sql(form_atributos)))
        and ((validar_cadena_sql(form_tablas)))
        and ((validar_cadena_sql(form_condiciones)))
    ):
        # Limpiamos las variables quitando comillas en extremos
        form_condiciones = form_condiciones.strip("'").strip('"')
        form_tablas = form_tablas.strip("'").strip('"')
        form_atributos = form_atributos.strip("'").strip('"')
        consulta = f"SELECT {form_atributos} FROM {form_tablas} WHERE {form_condiciones};"
        try:
    

            # Conexión a la base de datos mediante el cursor, nuevamente
            cursor = conn.cursor()
            # consulta = f"SELECT {form_atributos} FROM {form_tablas} WHERE {form_condiciones}"
            # Ejecutar la consulta
            cursor.execute(consulta, (form_atributos,))
            resultados = cursor.fetchall()
            cursor.close()

            def f_respuesta_html():
                print('resultados:', resultados)
                # 1 - Creamos las cabeceras de la tabla (th)
                # Separar los atributos en una lista
                atributos_lista = form_atributos.split(',')

                # Eliminar espacios en blanco de cada atributo
                atributos_lista = [atributo.strip() for atributo in atributos_lista]
                    
                html_table = """
                <div class="table-container">
                <table border="1">
                    <tr>
                """
                # Agregar las etiquetas <th> dinámicamente
                for atributo in atributos_lista:
                    if atributo == '*':
                        html_table += f"<th>{atributo}</th>"
                        continue
                    html_table += f"<th>{atributo}</th>"

                html_table += "</tr>"
                
                # 2 - Iterar sobre los resultados y agregar filas a la tabla (td and tr)
                for fila in resultados:
                    print('file:', fila)
                    html_table += "<tr>"
                    for indice, valor in enumerate(fila, start=1):
                        # Saltar el primer elemento (indice 0)
                        if indice == 0:
                            # print('valueeeeeee',valor)
                            pass
                        
                        html_table += f"<td>{valor}</td>"
                    html_table += "</tr>"

                    


                # Cerrar la tabla HTML
                html_table += '<div class="table-container">'
                html_table += "</table>"

                # Crear la respuesta HTML completa con la tabla de resultados
                respuesta_html = f"""
                <!DOCTYPE html>
                <html lang="es">

                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Fast Food</title>
                    <link rel="stylesheet" href="/static/style.css">
                    <link rel="shortcut icon" href="/static/favicon.ico">
                </head>
                <html>
                <head>
                    <title>Resultados de la Consulta</title>
                </head>
                <body>
                    <h1>Resultados de la Consulta</h1>
                    <h2>Tabla {form_tablas}</h2>
                    {html_table}
                </body>
                                <div class="container">
        <button id='advanced_queries' onclick="window.location.href='/consultas'">
            Volver hacia consultas</button>
    </div>
                </html>
                """

                # Retornar la respuesta HTML
                return respuesta_html

            return f_respuesta_html()
        except psycopg2.Error as e:
            print('porque el tipo de datos son ', type(form_atributos), type(form_tablas), type(form_condiciones))
            print(e)
            return f"""<html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Easy Food</title>
            <link rel="stylesheet" href="/static/style.css">
            <link rel="shortcut icon" href="/static/favicon.ico">
        </head>
        <body>
        <h1>Error inesperado</h1></body>
                        <div class="container">
            <button id='advanced_queries' onclick="window.location.href='/consultas'">
                Volver hacia consultas</button>
        </div>
        </html>"""
        except Exception as e:
            print('rarop exception',e)
            return f"""<html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Easy Food</title>
            <link rel="stylesheet" href="/static/style.css">
            <link rel="shortcut icon" href="/static/favicon.ico">
        </head>
        <body>
        <h1>Error inesperado</h1></body>
                        <div class="container">
            <button id='advanced_queries' onclick="window.location.href='/consultas'">
                Volver hacia consultas</button>
        </div>
        </html>"""
        finally:
            # Cerrar el cursor
            # cursor.close()
            # Cerrar la conexión también
            # conn.close()
            pass
    else:
        return f"""
            <!DOCTYPE html>
            <html lang="es">

            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Fast Food App</title>
                <link rel="stylesheet" href="/static/style.css">
            </head>
            <html>
            <head>
                <title>Resultados de la Consulta</title>
            </head>
            <body>
                <h1>Resultados de la Consulta</h1>
                <h2>Error:</h2><pre>Los datos ingresados no son válidos</pre>
            </body>
                            <div class="container">
        <button id='advanced_queries' onclick="window.location.href='/consultas'">
            Volver hacia consultas</button>
    </div>
            </html>
        """
        
@app.route('/consulta_one', methods=['POST'])
def consulta_one():
    form_platos = request.form['nombre_plato']
    # Verificamos que todos los valores sean strings y que "atributos" y "condiciones" no sean nulos.
    if (
        form_platos is not None and isinstance(form_platos, str)
        and (validar_cadena_sql(form_platos))):
        
        consulta = """
        SELECT restaurante.nombre
        FROM restaurante
        JOIN plato ON restaurante.nombre = plato.nombre_restaurante
        WHERE plato.nombre = %s AND plato.disponibilidad = TRUE;
        """

        try:
            cursor = conn.cursor()
            cursor.execute(consulta, (form_platos,))
            resultados = cursor.fetchall()
            columnas = [desc[0] for desc in cursor.description]
            cursor.close()

            # Renderizamos los resultados en formato HTML usando Flask
            return render_template_string('''
            <!DOCTYPE html>
            <html lang="es">

            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Fast Food App</title>
                <link rel="stylesheet" href="/static/style.css">
                <link rel="shortcut icon" href="/static/favicon.ico">
            </head>
            <html>
            <head>
                <title>Resultados de la Consulta</title>
            </head>
            <body>
                <h1>Resultados de la Consulta</h1>
                <table border="1">
                    <tr>
                        {% for columna in columnas %}
                        <th>{{ columna }}</th>
                        {% endfor %}
                    </tr>
                    {% for fila in resultados %}
                    <tr>
                        {% for valor in fila %}
                        <td>{{ valor }}</td>
                        {% endfor %}
                    </tr>
                    {% endfor %}
                </table>
                                <div class="container">
        <button id='advanced_queries' onclick="window.location.href='/consultas'">
            Volver hacia consultas</button>
    </div>
            </body>
            </html>
            ''', columnas=columnas, resultados=resultados)
        
        except psycopg2.Error as e:
            return f"""<html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Easy Food</title>
            <link rel="stylesheet" href="/static/style.css">
            <link rel="shortcut icon" href="/static/favicon.ico">
        </head>
        <body>
        <h1>Error inesperado</h1></body>
                        <div class="container">
            <button id='advanced_queries' onclick="window.location.href='/consultas'">
                Volver hacia consultas</button>
        </div>
        </html>"""
        except Exception as e:
            return f"""<html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Easy Food</title>
            <link rel="stylesheet" href="/static/style.css">
            <link rel="shortcut icon" href="/static/favicon.ico">
        </head>
        <body>
        <h1>Error inesperado</h1></body>
                        <div class="container">
            <button id='advanced_queries' onclick="window.location.href='/consultas'">
                Volver hacia consultas</button>
        </div>
        </html>"""
    else:
        return f"""
            <!DOCTYPE html>
            <html lang="es">

            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Fast Food App</title>
                <link rel="stylesheet" href="/static/style.css">
                <link rel="shortcut icon" href="/static/favicon.ico">
            </head>
            <html>
            <head>
                <title>Resultados de la Consulta</title>
            </head>
            <body>
                <h1>Resultados de la Consulta</h1>
                <h2>Error:</h2><pre>Los datos ingresados no son válidos</pre>
                                <div class="container">
        <button id='advanced_queries' onclick="window.location.href='/consultas'">
            Volver hacia consultas</button>
    </div>
            </body>
            </html>
        """
                                          
@app.route('/consulta_two', methods=['POST'])
def consulta_two():
    email_cliente = request.form['email_cliente']
    # Verificamos que todos los valores sean strings y que "atributos" y "condiciones" no sean nulos.
    if (
        email_cliente is not None and isinstance(email_cliente, str) and (validar_cadena_sql(email_cliente))):
        
        consulta = """
            SELECT usuario.email, 
                EXTRACT(MONTH FROM Pedido.fecha) AS Mes,
                COUNT(Pedido.id) AS Total_Pedidos,
                SUM(Pedido.costo) AS Gasto_Mensual
            FROM usuario
            JOIN Pedido ON usuario.email = Pedido.email
            WHERE (usuario.email = (%s) AND Pedido.estado = 'entregado a cliente')
            GROUP BY usuario.email, EXTRACT(MONTH FROM Pedido.fecha);
        """

        try:
            cursor = conn.cursor()
            cursor.execute(consulta, (email_cliente,))
            resultados = cursor.fetchall()
            columnas = [desc[0] for desc in cursor.description]
            cursor.close()

            # Renderizamos los resultados en formato HTML usando Flask
            return render_template_string('''
            <!DOCTYPE html>
            <html lang="es">

            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Entrega 2</title>
                <link rel="stylesheet" href="/static/style.css">
                <link rel="shortcut icon" href="/static/favicon.ico">
            </head>
            <html>
            <head>
                <title>Resultados de la Consulta</title>
            </head>
            <body>
                <h1>Resultados de la Consulta</h1>
                <table border="1">
                    <tr>
                        {% for columna in columnas %}
                        <th>{{ columna }}</th>
                        {% endfor %}
                    </tr>
                    {% for fila in resultados %}
                    <tr>
                        {% for valor in fila %}
                        <td>{{ valor }}</td>
                        {% endfor %}
                    </tr>
                    {% endfor %}
                </table>
                                <div class="container">
        <button id='advanced_queries' onclick="window.location.href='/consultas'">
            Volver hacia consultas</button>
    </div>
            </body>
            </html>
            ''', columnas=columnas, resultados=resultados)
        
        except psycopg2.Error as e:
            return f"""<html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Easy Food</title>
            <link rel="stylesheet" href="/static/style.css">
            <link rel="shortcut icon" href="/static/favicon.ico">
        </head>
        <body>
        <h1>Error inesperado</h1></body>
                        <div class="container">
            <button id='advanced_queries' onclick="window.location.href='/consultas'">
                Volver hacia consultas</button>
        </div>
        </html>"""
        except Exception as e:
            return f"""<html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Easy Food</title>
            <link rel="stylesheet" href="/static/style.css">
            <link rel="shortcut icon" href="/static/favicon.ico">
        </head>
        <body>
        <h1>Error inesperado</h1></body>
                        <div class="container">
            <button id='advanced_queries' onclick="window.location.href='/consultas'">
                Volver hacia consultas</button>
        </div>
        </html>"""
    else:
        return f"""
            <!DOCTYPE html>
            <html lang="es">

            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Fast Food App</title>
                <link rel="stylesheet" href="/static/style.css">
                <link rel="shortcut icon" href="/static/favicon.ico">
            </head>
            <html>
            <head>
                <title>Resultados de la Consulta</title>
            </head>
            <body>
                <h1>Resultados de la Consulta</h1>
                <h2>Error:</h2><pre>Los datos ingresados no son válidos</pre>
                                <div class="container">
        <button id='advanced_queries' onclick="window.location.href='/consultas'">
            Volver hacia consultas</button>
    </div>
            </body>
            </html>
        """

@app.route('/consulta_three', methods=['GET'])
def consulta_three():
    # Verificamos que todos los valores sean strings y que "atributos" y "condiciones" no sean nulos.
        
    consulta = """
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

    try:
        cursor = conn.cursor()
        cursor.execute(consulta,)
        resultados = cursor.fetchall()
        columnas = [desc[0] for desc in cursor.description]
        cursor.close()

        # Renderizamos los resultados en formato HTML usando Flask
        return render_template_string('''
        <!DOCTYPE html>
        <html lang="es">

        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Fast Food App</title>
            <link rel="stylesheet" href="/static/style.css">
        </head>
        <html>
        <head>
            <title>Resultados de la Consulta</title>
        </head>
        <body>
            <h1>Resultados de la Consulta</h1>
            <table border="1">
                <tr>
                    {% for columna in columnas %}
                    <th>{{ columna }}</th>
                    {% endfor %}
                </tr>
                {% for fila in resultados %}
                <tr>
                    {% for valor in fila %}
                    <td>{{ valor }}</td>
                    {% endfor %}
                </tr>
                {% endfor %}
            </table>
                            <div class="container">
        <button id='advanced_queries' onclick="window.location.href='/consultas'">
            Volver hacia consultas</button>
    </div>
        </body>
        </html>
        ''', columnas=columnas, resultados=resultados)
    
    except psycopg2.Error as e:
        return f"""<html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Easy Food</title>
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
    <h1>Error inesperado</h1></body>
                    <div class="container">
        <button id='advanced_queries' onclick="window.location.href='/consultas'">
            Volver hacia consultas</button>
    </div>
    </html>"""
    except Exception as e:
        return f"""<html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Easy Food</title>
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
    <h1>Error inesperado</h1></body>
                    <div class="container">
        <button id='advanced_queries' onclick="window.location.href='/consultas'">
            Volver hacia consultas</button>
    </div>
    </html>"""

@app.route('/consulta_four', methods=['POST'])
def consulta_thtree():
    estilo_plato = request.form['estilo_plato']
    # Verificamos que todos los valores sean strings y que "atributos" y "condiciones" no sean nulos.
    if (
        estilo_plato is not None and isinstance(estilo_plato, str)):
        
        consulta = """
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

        try:
            cursor = conn.cursor()
            cursor.execute(consulta, (estilo_plato,))
            resultados = cursor.fetchall()
            columnas = [desc[0] for desc in cursor.description]
            cursor.close()

            # Renderizamos los resultados en formato HTML usando Flask
            return render_template_string('''
            <!DOCTYPE html>
            <html lang="es">

            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Fast Food App</title>
                <link rel="stylesheet" href="/static/style.css">
            </head>
            <html>
            <head>
                <title>Resultados de la Consulta</title>
            </head>
            <body>
                <h1>Resultados de la Consulta</h1>
                <table border="1">
                    <tr>
                        {% for columna in columnas %}
                        <th>{{ columna }}</th>
                        {% endfor %}
                    </tr>
                    {% for fila in resultados %}
                    <tr>
                        {% for valor in fila %}
                        <td>{{ valor }}</td>
                        {% endfor %}
                    </tr>
                    {% endfor %}
                </table>
                                <div class="container">
        <button id='advanced_queries' onclick="window.location.href='/consultas'">
            Volver hacia consultas</button>
    </div>
            </body>
            </html>
            ''', columnas=columnas, resultados=resultados)
        
        except psycopg2.Error as e:
            return f"""<html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Easy Food</title>
            <link rel="stylesheet" href="/static/style.css">
        </head>
        <body>
        <h1>Error inesperado</h1></body>
                        <div class="container">
            <button id='advanced_queries' onclick="window.location.href='/consultas'">
                Volver hacia consultas</button>
        </div>
        </html>"""
        except Exception as e:
            return f"""<html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Easy Food</title>
            <link rel="stylesheet" href="/static/style.css">
        </head>
        <body>
        <h1>Error inesperado</h1></body>
                        <div class="container">
            <button id='advanced_queries' onclick="window.location.href='/consultas'">
                Volver hacia consultas</button>
        </div>
        </html>"""
    else:
        return f"""
            <!DOCTYPE html>
            <html lang="es">

            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Fast Food App</title>
                <link rel="stylesheet" href="/static/style.css">
            </head>
            <html>
            <head>
                <title>Resultados de la Consulta</title>
            </head>
            <body>
                <h1>Resultados de la Consulta</h1>
                <h2>Error:</h2><pre>Los datos ingresados no son válidos</pre>
                                <div class="container">
        <button id='advanced_queries' onclick="window.location.href='/consultas'">
            Volver hacia consultas</button>
    </div>
            </body>
            </html>
        """

@app.route('/consulta_five', methods=['POST'])
def consulta_five():
    estilo_plato = request.form['estilo_plato']
    # Verificamos que todos los valores sean strings y que "atributos" y "condiciones" no sean nulos.
    if (
        estilo_plato is not None and isinstance(estilo_plato, str)):
        
        consulta = """
            SELECT plato.restriccion AS restriccion,
                string_agg(plato.nombre, ', ') AS platos
            FROM plato
            WHERE plato.estilo = (%s) 
            GROUP BY plato.restriccion;
            """

        try:
            cursor = conn.cursor()
            cursor.execute(consulta, (estilo_plato,))
            resultados = cursor.fetchall()
            columnas = [desc[0] for desc in cursor.description]
            cursor.close()

            # Renderizamos los resultados en formato HTML usando Flask
            return render_template_string('''
            <!DOCTYPE html>
            <html lang="es">

            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Fast Food App</title>
                <link rel="stylesheet" href="/static/style.css">
            </head>
            <html>
            <head>
                <title>Resultados de la Consulta</title>
            </head>
            <body>
                <h1>Resultados de la Consulta</h1>
    <div class="container2">
        <h5>vegano: 1</h5>
        <h5>vegetariano: 2</h5>
        <h5>alergicos: 3</h5>
        <h5>celiacos: 4</h5>
        <h5>diabeticos: 5</h5>
        <h5>pescetarianos: 6</h5>
        <h5>vegetarianos: 7</h5>
        <h5>veganos: 8</h5>
        
        
    </div>
                <table border="1">
                    <tr>
                        {% for columna in columnas %}
                        <th>{{ columna }}</th>
                        {% endfor %}
                    </tr>
                    {% for fila in resultados %}
                    <tr>
                        {% for valor in fila %}
                        <td>{{ valor }}</td>
                        {% endfor %}
                    </tr>
                    {% endfor %}
                </table>
                                <div class="container">
        <button id='advanced_queries' onclick="window.location.href='/consultas'">
            Volver hacia consultas</button>
    </div>
            </body>
            </html>
            ''', columnas=columnas, resultados=resultados)
        
        except psycopg2.Error as e:
            return f"""<html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Easy Food</title>
            <link rel="stylesheet" href="/static/style.css">
        </head>
        <body>
        <h1>Error inesperado</h1></body>
                        <div class="container">
            <button id='advanced_queries' onclick="window.location.href='/consultas'">
                Volver hacia consultas</button>
        </div>
        </html>"""
        except Exception as e:
            return f"""<html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Easy Food</title>
            <link rel="stylesheet" href="/static/style.css">
        </head>
        <body>
        <h1>Error inesperado</h1></body>
                        <div class="container">
            <button id='advanced_queries' onclick="window.location.href='/consultas'">
                Volver hacia consultas</button>
        </div>
        </html>"""
    else:
        return f"""
            <!DOCTYPE html>
            <html lang="es">

            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Entrega 2</title>
                <link rel="stylesheet" href="/static/style.css">
            </head>
            <html>
            <head>
                <title>Resultados de la Consulta</title>
            </head>
            <body>
                <h1>Resultados de la Consulta</h1>
                <h2>Error:</h2><pre>Los datos ingresados no son válidos</pre>
                                <div class="container">
        <button id='advanced_queries' onclick="window.location.href='/consultas'">
            Volver hacia consultas</button>
    </div>
            </body>
            </html>
        """

@app.route('/consulta_six', methods=['POST'])
def consulta_six():
    email_cliente = request.form['email_cliente']
    # Verificamos que todos los valores sean strings y que "atributos" y "condiciones" no sean nulos.
    if (
        email_cliente is not None and isinstance(email_cliente, str)):
        
        consulta = """
        SELECT usuario.email AS usuario,
            string_agg(restaurante.nombre,', ') AS restaurante
        FROM usuario

        JOIN suscripcion 
            ON usuario.id = suscripcion.id_cliente
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

        WHERE suscripcion.estado = 'Vigente' AND usuario.email = (%s)
        GROUP BY usuario.email;
            """

        try:
            cursor = conn.cursor()
            cursor.execute(consulta, (email_cliente,))
            resultados = cursor.fetchall()
            columnas = [desc[0] for desc in cursor.description]
            cursor.close()

            # Renderizamos los resultados en formato HTML usando Flask
            return render_template_string('''
            <!DOCTYPE html>
            <html lang="es">

            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Entrega 2</title>
                <link rel="stylesheet" href="/static/style.css">
            </head>
            <html>
            <head>
                <title>Resultados de la Consulta</title>
            </head>
            <body>
                <h1>Resultados de la Consulta</h1>
                <table border="1">
                    <tr>
                        {% for columna in columnas %}
                        <th>{{ columna }}</th>
                        {% endfor %}
                    </tr>
                    {% for fila in resultados %}
                    <tr>
                        {% for valor in fila %}
                        <td>{{ valor }}</td>
                        {% endfor %}
                    </tr>
                    {% endfor %}
                </table>
                                <div class="container">
        <button id='advanced_queries' onclick="window.location.href='/consultas'">
            Volver hacia consultas</button>
    </div>
            </body>
            </html>
            ''', columnas=columnas, resultados=resultados)
        
        except psycopg2.Error as e:
            return f"""<html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Easy Food</title>
            <link rel="stylesheet" href="/static/style.css">
        </head>
        <body>
        <h1>Error inesperado</h1></body>
                        <div class="container">
            <button id='advanced_queries' onclick="window.location.href='/consultas'">
                Volver hacia consultas</button>
        </div>
        </html>"""
        except Exception as e:
            return f"""<html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Easy Food</title>
            <link rel="stylesheet" href="/static/style.css">
        </head>
        <body>
        <h1>Error inesperado</h1></body>
                        <div class="container">
            <button id='advanced_queries' onclick="window.location.href='/consultas'">
                Volver hacia consultas</button>
        </div>
        </html>"""
    else:
        return f"""
            <!DOCTYPE html>
            <html lang="es">

            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Entrega 2</title>
                <link rel="stylesheet" href="/static/style.css">
            </head>
            <html>
            <head>
                <title>Resultados de la Consulta</title>
            </head>
            <body>
                <h1>Resultados de la Consulta</h1>
                <h2>Error:</h2><pre>Los datos ingresados no son válidos</pre>
                            <div class="container">
        <button id='advanced_queries' onclick="window.location.href='/consultas'">
            Volver hacia consultas</button>
    </div>
            </body>
            
            </html>
        """

@app.route('/consulta_seven', methods=['GET'])
def consulta_seven():
    # Verificamos que todos los valores sean strings y que "atributos" y "condiciones" no sean nulos.

    consulta = """
    SELECT usuario.email AS usuario,
        COALESCE(SUM(pedido.costo), 0) AS suma_gastada
    FROM usuario

    LEFT JOIN pedido
        ON pedido.email = usuario.email
    JOIN suscripcion
        ON suscripcion.id_cliente = usuario.id AND (suscripcion.estado = 'Cancelada' OR suscripcion IS NULL)
    GROUP BY usuario.email;
        """

    try:
        cursor = conn.cursor()
        cursor.execute(consulta,)
        resultados = cursor.fetchall()
        columnas = [desc[0] for desc in cursor.description]
        cursor.close()

        # Renderizamos los resultados en formato HTML usando Flask
        return render_template_string('''
        <!DOCTYPE html>
        <html lang="es">

        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Entrega 2</title>
            <link rel="stylesheet" href="/static/style.css">
        </head>
        <html>
        <head>
            <title>Resultados de la Consulta</title>
        </head>
        <body>
            <h1>Resultados de la Consulta</h1>
            <table border="1">
                <tr>
                    {% for columna in columnas %}
                    <th>{{ columna }}</th>
                    {% endfor %}
                </tr>
                {% for fila in resultados %}
                <tr>
                    {% for valor in fila %}
                    <td>{{ valor }}</td>
                    {% endfor %}
                </tr>
                {% endfor %}
            </table>
                            <div class="container">
        <button id='advanced_queries' onclick="window.location.href='/consultas'">
            Volver hacia consultas</button>
    </div>
        </body>
        </html>
        ''', columnas=columnas, resultados=resultados)
    
    except psycopg2.Error as e:
        return f"""<html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Easy Food</title>
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
    <h1>Error inesperado</h1></body>
                    <div class="container">
        <button id='advanced_queries' onclick="window.location.href='/consultas'">
            Volver hacia consultas</button>
    </div>
    </html>"""
    except Exception as e:
        return f"""<html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Easy Food</title>
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
    <h1>Error inesperado</h1></body>
                    <div class="container">
        <button id='advanced_queries' onclick="window.location.href='/consultas'">
            Volver hacia consultas</button>
    </div>
    </html>"""

@app.route('/consulta_eight', methods=['GET'])
def consulta_eight():
    consulta = """
        SELECT plato.nombre AS plato,
            string_agg(restaurante.nombre,', ') AS restaurante
        FROM plato

        JOIN Restaurante 
            ON plato.nombre_restaurante = restaurante.nombre
        GROUP BY plato.nombre;
        """

    try:
        cursor = conn.cursor()
        cursor.execute(consulta,)
        resultados = cursor.fetchall()
        columnas = [desc[0] for desc in cursor.description]
        cursor.close()

        # Renderizamos los resultados en formato HTML usando Flask
        return render_template_string('''
        <!DOCTYPE html>
        <html lang="es">

        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Entrega 2</title>
            <link rel="stylesheet" href="/static/style.css">
        </head>
        <html>
        <head>
            <title>Resultados de la Consulta</title>
        </head>
        <body>
            <h1>Resultados de la Consulta</h1>
            <table border="1">
                <tr>
                    {% for columna in columnas %}
                    <th>{{ columna }}</th>
                    {% endfor %}
                </tr>
                {% for fila in resultados %}
                <tr>
                    {% for valor in fila %}
                    <td>{{ valor }}</td>
                    {% endfor %}
                </tr>
                {% endfor %}
            </table>
                            <div class="container">
        <button id='advanced_queries' onclick="window.location.href='/consultas'">
            Volver hacia consultas</button>
    </div>
        </body>
        </html>
        ''', columnas=columnas, resultados=resultados)
    
    except psycopg2.Error as e:
        return f"""<html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Easy Food</title>
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
    <h1>Error inesperado</h1></body>
                    <div class="container">
        <button id='advanced_queries' onclick="window.location.href='/consultas'">
            Volver hacia consultas</button>
    </div>
    </html>"""
    except Exception as e:
        return f"""<html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Easy Food</title>
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
    <h1>Error inesperado</h1></body>
                    <div class="container">
        <button id='advanced_queries' onclick="window.location.href='/consultas'">
            Volver hacia consultas</button>
    </div>
    </html>"""

@app.route('/consulta_nine', methods=['POST'])
def consulta_nine():
    puntaje = request.form['puntaje']
    # Verificamos que todos los valores sean strings y que "atributos" y "condiciones" no sean nulos.
    consulta = """
        SELECT 'usuario' AS tabla,
        email AS nombre, usuario.id as puntaje
        FROM usuario
        WHERE puntaje > (%s)

        UNION ALL

        SELECT 'delivery' AS tabla,
        nombre AS nombre, puntaje
        FROM delivery
        WHERE puntaje > (%s)

        UNION ALL

        SELECT 'despachador' AS tabla,
        nombre AS nombre, puntaje
        FROM despachador
        WHERE puntaje > (%s)

        UNION ALL

        SELECT 'sucursal' AS tabla,
        sucursal AS nombre, puntaje
        FROM sucursal
        WHERE puntaje > (%s)

        UNION ALL

        SELECT 'restaurante' AS tabla,
        nombre AS nombre, puntaje
        FROM restaurante
        WHERE puntaje > (%s);
        """

    try:
        cursor = conn.cursor()
        cursor.execute(consulta, (puntaje,))
        resultados = cursor.fetchall()
        columnas = [desc[0] for desc in cursor.description]
        cursor.close()

        # Renderizamos los resultados en formato HTML usando Flask
        return render_template_string('''
        <!DOCTYPE html>
        <html lang="es">

        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>¡Easy Food App!</title>
            <link rel="stylesheet" href="/static/style.css">
        </head>
        <html>
        <head>
            <title>Resultados de la Consulta</title>
        </head>
        <body>
            <h1>Resultados de la Consulta</h1>
            <table border="1">
                <tr>
                    {% for columna in columnas %}
                    <th>{{ columna }}</th>
                    {% endfor %}
                </tr>
                {% for fila in resultados %}
                <tr>
                    {% for valor in fila %}
                    <td>{{ valor }}</td>
                    {% endfor %}
                </tr>
                {% endfor %}
            </table>
                            <div class="container">
        <button id='advanced_queries' onclick="window.location.href='/consultas'">
            Volver hacia consultas</button>
    </div>
        </body>
        </html>
        ''', columnas=columnas, resultados=resultados)
    
    except psycopg2.Error as e:
        return f"""<html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Easy Food</title>
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
    <h1>Error inesperado</h1></body>
                    <div class="container">
        <button id='advanced_queries' onclick="window.location.href='/consultas'">
            Volver hacia consultas</button>
    </div>
    </html>"""
    except Exception as e:
        return f"""<html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Easy Food</title>
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
    <h1>Error inesperado</h1></body>
                    <div class="container">
        <button id='advanced_queries' onclick="window.location.href='/consultas'">
            Volver hacia consultas</button>
    </div>
    </html>"""


@app.route('/consulta_ten', methods=['POST'])
def consulta_ten():
    plato_restriccion = request.form['plato_restriccion']
    # Verificamos que todos los valores sean strings y que "atributos" y "condiciones" no sean nulos.
    consulta = """
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

    try:
        cursor = conn.cursor()
        cursor.execute(consulta, (plato_restriccion,))
        resultados = cursor.fetchall()
        columnas = [desc[0] for desc in cursor.description]
        cursor.close()

        # Renderizamos los resultados en formato HTML usando Flask
        return render_template_string('''
        <!DOCTYPE html>
        <html lang="es">

        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Entrega 2</title>
            <link rel="stylesheet" href="/static/style.css">
        </head>
        <html>
        <head>
            <title>Resultados de la Consulta</title>
        </head>
        <body>
            <h1>Resultados de la Consulta</h1>
            <table border="1">
                <tr>
                    {% for columna in columnas %}
                    <th>{{ columna }}</th>
                    {% endfor %}
                </tr>
                {% for fila in resultados %}
                <tr>
                    {% for valor in fila %}
                    <td>{{ valor }}</td>
                    {% endfor %}
                </tr>
                {% endfor %}
            </table>
                <div class="container">
        <button id='advanced_queries' onclick="window.location.href='/consultas'">
            Volver hacia consultas</button>
    </div>
        </body>
        </html>
        ''', columnas=columnas, resultados=resultados)
    
    except psycopg2.Error as e:
        return f"""<html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Easy Food</title>
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
    <h1>Error inesperado</h1></body>
                    <div class="container">
        <button id='advanced_queries' onclick="window.location.href='/consultas'">
            Volver hacia consultas</button>
    </div>
    </html>"""
    except Exception as e:
        return f"""<html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Easy Food</title>
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
    <h1>Error inesperado</h1></body>
                    <div class="container">
        <button id='advanced_queries' onclick="window.location.href='/consultas'">
            Volver hacia consultas</button>
    </div>
    </html>"""


if __name__ == '__main__':
    app.run(debug=True, port=8037) #This port should be defined above and in the .env!