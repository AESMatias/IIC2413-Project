import csv
import psycopg2
from psycopg2 import sql
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

def sanitizar_consulta(csv_path: str, table_name: str, name_consulta: str, lenght_of_rows: int = 1):
    #TODO: Hay sobre escritura de satinizado aquí, hay que optimizar.
    # Abrir el archivo CSV original y crear un archivo nuevo para escribir los datos sanitizados
    with open(csv_path, mode='r', encoding="mac_roman", errors='ignore') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        path_to_put = os.path.join(current_dir, 'csv_generados', f'{table_name}.csv')
        with open(path_to_put, mode='w', newline='', encoding='mac_roman') as new_csv_file:
            csv_writer = csv.writer(new_csv_file, delimiter=';')
            for row in csv_reader:
                # Eliminar las comillas dobles de cada elemento en la fila
                sanitizado = [elemento.replace('"', '') for elemento in row]
                #TODO:reemplazamos saltos de lineas y demás
                sanitizado = [elemento.strip() for elemento in row]
                csv_writer.writerow(sanitizado)
    # Intentar cargar los datos sanitizados a la tabla
    cargar_csv_a_tabla(path_to_put, table_name, name_consulta, lenght_of_rows)

def reemplazar_tildes(texto):
    reemplazos = {
        'á': 'a',
        'é': 'e',
        'í': 'i',
        'ó': 'o',
        'ú': 'u',
        'Á': 'A',
        'É': 'E',
        'Í': 'I',
        'Ó': 'O',
        'Ú': 'U',
        'ñ': 'n',
        'Ñ': 'N'
    }
    for original, reemplazo in reemplazos.items():
        texto = texto.replace(original, reemplazo)
    return texto


def cargar_csv_a_tabla(csv_path: str, table_name: str, name_consulta: str, lenght_of_rows: int = 1):
    try:        
        conn = psycopg2.connect(
            database="grupo37",
            user="grupo37",
            password="»6ª#uQÖq¬_½-zúÉzùÊ÷`",
            host="pavlov.ing.puc.cl"
        )

        cursor = conn.cursor()
        # Abrimos el archivo .csv y populamos las tablas
        with open(csv_path, 'r', encoding="mac_roman") as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                # print('r',row)
                if len(row) != lenght_of_rows:
                    print(f"{csv_path} Error: la fila {row} de la tabla {table_name} no tiene la cantidad de columnas esperadas ({lenght_of_rows})")
                    print(f"Saltando fila...")
                    print(len(row))
                    print('row',row)
                    for i in range(len(row)):
                        print(f"{i}: {row[i]}")
                    continue
                try:
                    # Reemplazar tildes y eñes en cada campo de la fila
                    row_sin_tildes = [reemplazar_tildes(campo) for campo in row]
                    cursor.execute(name_consulta, row_sin_tildes)
                    conn.commit()
                except psycopg2.errors.UniqueViolation as ue:
                    print(f"Clave duplicada al procesar la fila {row}: {ue}")
                    conn.rollback()  # Revertir cualquier cambio hecho por la fila actual
                except Exception as e:
                    print(f"Error al procesar la fila {row}: {e}")
                    conn.rollback()  # Revertir cualquier cambio hecho por la fila actual

        # conn.commit()

    except IndexError as e:
        print(f"INDEX ERROR al cargar datos desde {csv_path} a la tabla {table_name}: {e}")
        sanitizar_consulta(csv_path, table_name, name_consulta, lenght_of_rows)
    except Exception as e:
        print(f"Error al cargar datos desde {csv_path} a la tabla {table_name}: {e}")
    finally:
        cursor.close()
        conn.close()


################  RESECUENCIA inicio   ################

def organizar_ids(tabla_a_organizar: str):
    '''Esta función se encarga de organizar los IDs de una tabla en orden ascendente, para
    evitar que hayan saltos en la secuencia de los IDs (que un id sea 1, y el siguiente 3, por ejemplo).'''
    
    # Definir las consultas SQL
    crear_funcion_sql = f"""
    CREATE OR REPLACE FUNCTION resequence_ids_{tabla_a_organizar}()
    RETURNS TRIGGER AS $$
    BEGIN
        WITH updated AS (
        SELECT id, ROW_NUMBER() OVER (ORDER BY id) AS new_id
        FROM {tabla_a_organizar}
        )
        UPDATE {tabla_a_organizar}
        SET id = updated.new_id
        FROM updated
        WHERE {tabla_a_organizar}.id = updated.id;
        
        RETURN NULL; -- Los triggers deben retornar NULL
    END;
    $$ LANGUAGE plpgsql;
    """

    crear_trigger_sql = f"""
    CREATE TRIGGER after_insert_resequence
    AFTER INSERT ON {tabla_a_organizar}
    FOR EACH STATEMENT
    EXECUTE FUNCTION resequence_ids_{tabla_a_organizar}();
    """
    try:
        conn = psycopg2.connect(
                dbname="grupo37",
                user="grupo37",
                password="»6ª#uQÖq¬_½-zúÉzùÊ÷`",
                host="pavlov.ing.puc.cl",
                port="5432"
            )
        # Crear un cursor
        cursor = conn.cursor()
        # Ejecutar la consulta para crear la función
        cursor.execute(crear_funcion_sql)
        # Ejecutar la consulta para crear el trigger
        cursor.execute(crear_trigger_sql)
        # Confirmar los cambios
        conn.commit()
        print(f"Función y trigger de {tabla_a_organizar} creados exitosamente.")
    except Exception as e:
        # En caso de error, revertir los cambios
        conn.rollback()
        print(f"Error al crear la función y el trigger: {e}")
    finally:
        # Cerrar el cursor y la conexión
        cursor.close()
        conn.close()


organizar_ids('cliente')
organizar_ids('sucursal')
organizar_ids('restaurante')
organizar_ids('despacho')
organizar_ids('delivery')
organizar_ids('despachador')
organizar_ids('plato')
organizar_ids('administrador')
organizar_ids('direccion')
organizar_ids('pedido')
organizar_ids('calificacion')
organizar_ids('suscripcion')
organizar_ids('se_compone')
organizar_ids('delivery_de_sucursal')
    
################   RESECUENCIA FIN   ################


consulta_comuna = sql.SQL("""
INSERT INTO comuna (cut, nombre, provincia, region)
VALUES (%s, %s, %s, %s);
""")

# TODO: Falta sanitizar esta consulta maybe?
consulta_restaurante = sql.SQL("""
INSERT INTO restaurante (nombre, vigente, estilo, prec_min_repar_gratis)
VALUES (%s, %s, %s, %s);
""")

# TODO: Falta sanitizar esta consulta
consulta_sucursal = sql.SQL("""
INSERT INTO sucursal (nombre_restaurante, sucursal, direccion, telefono, area_despacho)
VALUES (%s, %s, %s, %s, %s);
""")


consulta_delivery = sql.SQL("""
INSERT INTO delivery (nombre, vigente, telefono, tiempo_despacho, precio_uni_despacho, precio_sus_mensual, precio_sus_anual)
VALUES (%s, %s, %s, %s, %s, %s, %s);
""")

consulta_despachador = sql.SQL("""
INSERT INTO despachador (nombre, telefono)
VALUES (%s, %s);
""")

consulta_platos = sql.SQL("""
INSERT INTO plato (id, nombre, descripcion, disponibilidad, estilo, restriccion,
ingredientes, porciones, precio, tiempo_preparacion, nombre_restaurante, repartomin, vigente)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
""")

consulta_datos_clientes = sql.SQL("""
INSERT INTO usuario (nombre, email, telefono, clave)
VALUES (%s, %s, %s, %s);
""")

consulta_direccion_clientes = sql.SQL("""
INSERT INTO direccion (cliente_email, direccion, comuna_cut)
VALUES (%s, %s, %s);
""")

consulta_pedidos = sql.SQL("""
INSERT INTO pedido (id, email, sucursal, nombre_delivery, nombre_despachador,
plato, fecha, hora, estado)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
""")

consulta_calificacion = sql.SQL("""
INSERT INTO calificacion (id_pedido, calificacion_pedido, calificacion_cliente)
VALUES (%s, %s, %s);
""")



path_inicial_comuna2 = os.path.join(current_dir, 'csv_iniciales', 'comuna2.csv')
path_inicial_pedidos2 = os.path.join(current_dir, 'csv_generados', 'pedidos_plus_one.csv')
path_inicial_calificacion = os.path.join(current_dir, 'csv_generados', 'calificacion_plus_one.csv')

path_generado_restaurante = os.path.join(current_dir, 'csv_generados', 'restaurantes_restaurante.csv')
path_generado_restaurantes_sucursal = os.path.join(current_dir, 'csv_generados', 'restaurantes_sucursal.csv')
path_generado_celdes_delivery = os.path.join(current_dir, 'csv_generados', 'cldeldes_delivery.csv')
path_generado_celdes_despachador = os.path.join(current_dir, 'csv_generados', 'cldeldes_despachador.csv')
path_generado_platos_int = os.path.join(current_dir, 'csv_generados', 'platos_int.csv')
path_generado_clientes_data = os.path.join(current_dir, 'csv_generados', 'clientes_data.csv')
path_generado_clientes_direccion = os.path.join(current_dir, 'csv_generados', 'clientes_direccion.csv')


#TODO: Hacer un try de todas las cargas y generar un .log del resultado de cada una de ellas en el server.
cargar_csv_a_tabla(path_inicial_comuna2, 'comuna', consulta_comuna,4)
#quizás, al cargar, hay que sanitizarlas todas todas, revisar la data!

sanitizar_consulta(path_generado_restaurante, 'restaurante', consulta_restaurante, 4)
sanitizar_consulta(path_generado_restaurantes_sucursal, 'sucursal', consulta_sucursal, 5)
sanitizar_consulta(path_generado_celdes_delivery, 'delivery', consulta_delivery, 7)
sanitizar_consulta(path_generado_celdes_despachador, 'despachador', consulta_despachador, 2)
sanitizar_consulta(path_generado_platos_int, 'platos', consulta_platos, 13)
sanitizar_consulta(path_generado_clientes_data, 'usuario', consulta_datos_clientes, 4)
sanitizar_consulta(path_generado_clientes_direccion, 'direccion', consulta_direccion_clientes, 3)
sanitizar_consulta(path_inicial_pedidos2, 'pedido', consulta_pedidos, 9)
sanitizar_consulta(path_inicial_calificacion, 'calificacion', consulta_calificacion, 3)