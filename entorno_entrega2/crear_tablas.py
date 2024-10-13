import subprocess
import csv
import os
import psycopg2

# comando_eliminar = f'psql -U postgres -d grupo37 -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;" -p 5555 -W {password}'
# subprocess.run(comando_eliminar, shell=True)


def limpiar_tablas():

    ##### BORRAMOS TODAS LAS TABLAS PRIMERO:

    conn = psycopg2.connect(
        database="db_name",
        user="username",
        password="password",
        host="hostname",
    )
    cursor = conn.cursor()

    # Ejecutar el script para borrar todas las tablas del esquema public, sin DROPEARLO directamente
    try:
        cursor.execute("""
            DO $$
            DECLARE
                tabla_name text;
            BEGIN
                FOR tabla_name IN
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = 'public'
                LOOP
                    EXECUTE 'DROP TABLE IF EXISTS public.' || tabla_name || ' CASCADE;';
                END LOOP;
            END $$;
        """)
        conn.commit()
        print("Todas las tablas eliminadas correctamente.")
    except Exception as e:
        conn.rollback()
        print(f"Error al eliminar tablas: {e}")

    # Cerrar cursor y conexión
    cursor.close()
    conn.close()


def crear_tablas(password: str):
    archivo_sql = 'creacion_tablas.sql'
    comando_psql = f'psql -U grupo37 -d grupo37 -a -f {archivo_sql} -p 5432 -W {password}'
    subprocess.run(comando_psql, shell=True)
    

def generar_nuevos_csv():
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Separamos el archivo cldeldes en tres, segun sus columnas:
    cliente_file = os.path.join(current_dir, 'csv_generados', 'cldeldes_cliente.csv')
    delivery_file = os.path.join(current_dir, 'csv_generados', 'cldeldes_delivery.csv')
    despachador_file = os.path.join(current_dir, 'csv_generados', 'cldeldes_despachador.csv')

    cldeldes_path = os.path.join(current_dir, 'csv_iniciales', 'cldeldes.csv')

    # Abrir los archivos de salida para escribir
    try:
        with open(cldeldes_path, 'r', encoding="mac_roman", errors='ignore') as main_file, \
            open(cliente_file, 'w', newline='', encoding="mac_roman", errors='ignore') as cliente_csv, \
            open(delivery_file, 'w', newline='', encoding="mac_roman", errors='ignore') as delivery_csv, \
            open(despachador_file, 'w', newline='', encoding="mac_roman", errors='ignore') as despachador_csv:
            
            reader = csv.reader(main_file, delimiter=';')
            next(reader)  # Saltar la cabecera

            # Creamos los writer para los archivos de salida qie seran escritos
            cliente_writer = csv.writer(cliente_csv, delimiter=';')
            delivery_writer = csv.writer(delivery_csv, delimiter=';')
            despachador_writer = csv.writer(despachador_csv, delimiter=';')

            # Los escribimos con sus respectivas cabeceras
            cliente_writer.writerow(['clientenombre', 'clienteemail', 'clientetelefono', 'clienteclave'])
            delivery_writer.writerow(['deliverynombre', 'deliveryvigente', 'deliverytelefono', 'deliverytiempo', 'deliverypreciounitario', 'deliverypreciomensual', 'deliveryprecioanual'])
            despachador_writer.writerow(['despachadornombre', 'despachadortelefono'])

            # Iterar sobre cada fila del archivo de entrada
            for row in reader:
                try:
                    #Cambiamos el telefono, le agregamos el +
                    row[6] = str("+" + row[6])
                    row[12] = str("+" + row[12])
                    
                    
                    # Extraer datos para cada tabla
                    cliente_data = row[:4]
                    delivery_data = row[4:11]
                    despachador_data = row[11:]

                    # Escribimos los datos en los archivos correspondientes
                    cliente_writer.writerow(cliente_data)
                    delivery_writer.writerow(delivery_data)
                    despachador_writer.writerow(despachador_data)
                except IndexError as e:
                    print(f"Error al procesar la row {row}: {e}")
                except Exception as e:
                    print(f"Error inesperado al procesar la row {row}: {e}")
                    
            print("Datos separados y escritos en los archivos correspondientes correctamente.")
            #Dado que with open es un context manager, se maneja automaticamente el cerrado de los archivos
            
    except FileNotFoundError as fnfe:
        print(f"Error: No se pudo encontrar el archivo 'cldeldes.csv': {fnfe}")
        print('ruta actual>', current_dir)
        print('cldeldes_path', cldeldes_path)
    except PermissionError as pe:
        print(f"Error: Permiso denegado al acceder a uno de los archivos: {pe}")
    except Exception as e:
        print(f"Error inesperado: {e}")

    # Similarmente a arriba, separamos en dos partes el archivo restaurantes.csv, para
    # luego popular, con esos datos, las tablas restaurante y sucursal.

    restaurante_file = os.path.join(current_dir, 'csv_generados', 'restaurantes_restaurante.csv')
    sucursal_file = os.path.join(current_dir, 'csv_generados', 'restaurantes_sucursal.csv')

    restaurantes2_path = os.path.join(current_dir, 'csv_iniciales', 'restaurantes2.csv')

    try:
        with open(restaurantes2_path, 'r', encoding="mac_roman", errors='ignore') as main_file, \
            open(restaurante_file, 'w', newline='', encoding="mac_roman", errors='ignore') as restaurante_resta, \
            open(sucursal_file, 'w', newline='', encoding="mac_roman", errors='ignore') as restaurante_sucursal:
            
            reader = csv.reader(main_file, delimiter=';')
            next(reader)  # Saltar la cabecera

            # Creamos los writer para los archivos de salida qie seran escritos
            resta_writer = csv.writer(restaurante_resta, delimiter=';')
            sucursal_writer = csv.writer(restaurante_sucursal, delimiter=';')

            # Los escribimos con sus respectivas cabeceras
            resta_writer.writerow(['nombre', 'vigente', 'estilo', 'prec_min_repar_gratis'])
            sucursal_writer.writerow(['nombre_restaurante','sucursal','direccion','telefono', 'area_despacho'])

            # Iterar sobre cada fila del archivo de entrada
            for row in reader:
                try:
                    #Cambiamos el telefono, le agregamos el +
                    row[6] = str("+" + row[6])
                    
                    # Extraer datos para cada tabla
                    restaurante_data = [row[i] for i in [0, 1, 2,3]]
                    sucursal_data = [row[i] for i in [0, 4, 5, 6, 7]]

                    # Escribimos los datos en los archivos correspondientes
                    resta_writer.writerow(restaurante_data)
                    sucursal_writer.writerow(sucursal_data)
                except IndexError as e:
                    print(f"Error al procesar la row {row}: {e}")
                except Exception as e:
                    print(f"Error inesperado al procesar la row {row}: {e}")
                    
            print("Datos separados y escritos en los archivos correspondientes correctamente.")
            #Dado que with open es un context manager, se maneja automaticamente el cerrado de los archivos
            
    except FileNotFoundError as fnfe:
        print(f"Error: No se pudo encontrar el archivo 'cldeldes.csv': {fnfe}")
    except PermissionError as pe:
        print(f"Error: Permiso denegado al acceder a uno de los archivos: {pe}")
    except Exception as e:
        print(f"Error inesperado: {e}")
        
        
    platos_path = os.path.join(current_dir, 'csv_iniciales', 'platos.csv')
    platos_int_path = os.path.join(current_dir, 'csv_generados', 'platos_int.csv')
        
    # Transformamos los valores de la columna restricciones en csv de platos, de string a int
    try:
        restriccion_mapping = {
        'vegano': 1,
        'vegetariano': 2,
        'alergicos': 3,
        'celiacos': 4,
        'diabeticos': 5,
        'pescetarianos': 6,
        'vegetarianos': 7,
        'veganos': 8,
        }
        
        with open(platos_path, 'r', encoding="mac_roman", errors='ignore') as main_file, \
            open(platos_int_path, 'w', newline='', encoding="mac_roman", errors='ignore') as platos_csv:
            
            reader = csv.reader(main_file, delimiter=';')
            next(reader)  # Saltar la cabecera

            # Creamos los writer para los archivos de salida qie seran escritos
            platos_writer = csv.writer(platos_csv, delimiter=';')

            # Los escribimos con sus respectivas cabeceras
            platos_writer.writerow(['id', 'nombre', 'descripcion', 'disponibilidad', 'estilo', 
                        'restriccion', 'ingredientes', 'porciones', 'precio', 
                        'tiempo_preparacion', 'nombre_restaurante', 'repartomin', 'vigente'])
            # Iterar sobre cada fila del archivo de entrada
            for row in reader:
                try:
                    platos_data = [row[i] for i in range(len(row))]
                    # Transformar restricción a su correspondiente entero si está en el mapeo
                    if platos_data[5] in restriccion_mapping.keys():
                        platos_data[5] = restriccion_mapping[platos_data[5]]
                    # Escribimos los datos en los archivos correspondientes
                    platos_writer.writerow(platos_data)
                except IndexError as e:
                    print(f"Error al procesar la row {row}: {e}")
                except Exception as e:
                    print(f"Error inesperado al procesar la row {row}: {e}")
                    
            print("Datos separados y escritos en los archivos correspondientes correctamente.")

    except FileNotFoundError as e:
        print(f"Error: No se pudo encontrar el archivo 'cldeldes.csv': {e}")
    except PermissionError as e:
        print(f"Error: Permiso denegado al acceder a uno de los archivos: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")
        # Convertimos los valores de la columna restricciones en csv de platos, de string a int


    cliente_path = os.path.join(current_dir, 'csv_iniciales', 'clientes.csv')
    clientes_data = os.path.join(current_dir, 'csv_generados', 'clientes_data.csv')
    clientes_direccion = os.path.join(current_dir, 'csv_generados', 'clientes_direccion.csv')

    # Separamos clientes.csv en dos archivos, para luego popular las tablas direccion y cliente
    try:
        with open(cliente_path, 'r', encoding='mac_roman' ) as main_file, \
            open(clientes_data, 'w', newline='', encoding='mac_roman') as cliente_datos_csv, \
            open(clientes_direccion, 'w', newline='', encoding='mac_roman') as cliente_direccion_csv:
            
            reader = csv.reader(main_file, delimiter=';')
            next(reader)  # Saltar la cabecera

            # Creamos los writer para los archivos de salida qie seran escritos
            cliente_datos_writer = csv.writer(cliente_datos_csv, delimiter=';')
            cliente_direccion_writer = csv.writer(cliente_direccion_csv, delimiter=';')

            # Los escribimos con sus respectivas cabeceras
            
            cliente_datos_writer.writerow(['nombre','email','telefono','clave'])
            cliente_direccion_writer.writerow(['email','direccion','comuna'])

            # Iterar sobre cada fila del archivo de entrada
            for row in reader:
                try:
                    
                    #Cambiamos el telefono, le agregamos el +
                    row[2] = str("+" + row[2])
                    
                    # Extraer datos para cada tabla, leugo de haber cambiado el teléfono.
                    cliente_data = row[:4]
                    direccion_data = [row[i] for i in [1,4, 5]]

                    # Escribimos los datos en los archivos correspondientes
                    cliente_datos_writer.writerow(cliente_data)
                    cliente_direccion_writer.writerow(direccion_data)
                except IndexError as e:
                    print(f"Error al procesar la row {row}: {e}")
                except Exception as e:
                    print(f"Error inesperado al procesar la row {row}: {e}")
                    
            print("Datos separados y escritos en los archivos correspondientes correctamente.")
            # Dado que with open es un context manager, se maneja automaticamente el cerrado de los archivos
            
    except FileNotFoundError as fnfe:
        print(f"Error: No se pudo encontrar el archivo 'cldeldes.csv': {fnfe}")
    except PermissionError as pe:
        print(f"Error: Permiso denegado al acceder a uno de los archivos: {pe}")
    except Exception as e:
        print(f"Error inesperado: {e}")

#  Nuevos id de pedidos aumentados en +1 para que hagan match con calificaciones:
    pedidos_path = os.path.join(current_dir, 'csv_iniciales', 'pedidos.csv')
    pedidos_plus_one = os.path.join(current_dir, 'csv_generados', 'pedidos_plus_one.csv')

    # Separamos clientes.csv en dos archivos, para luego popular las tablas direccion y cliente
    try:
        # TODO: Esto no sirve!
        with open(pedidos_path, 'r', encoding='mac_roman', errors='ignore') as main_file, \
            open(pedidos_plus_one, 'w', newline='', encoding='mac_roman') as pedidos_one_csv:
            
            reader = csv.reader(main_file, delimiter=';')
            next(reader)  # Saltar la cabecera

            # Creamos los writer para los archivos de salida qie seran escritos
            pedidos_one_writer = csv.writer(pedidos_one_csv, delimiter=';')

            # Los escribimos con sus respectivas cabeceras
            pedidos_one_writer.writerow(['id','cliente','sucursal','delivery','despachador','plato','fecha','hora','estado'])
            # Iterar sobre cada fila del archivo de entrada
            for row in reader:
                try:
                    #TODO:SANITIZAR DATOS
                    #Cambiamos el telefono, le agregamos el +
                    row[2] = str("+" + row[2])
                    # Extraer datos para cada tabla, leugo de haber cambiado el teléfono.
                    cliente_data = row[:4]
                    # Escribimos los datos en los archivos correspondientes
                    pedidos_one_writer.writerow(cliente_data)
                except IndexError as e:
                    print(f"Error al procesar la row {row}: {e}")
                except Exception as e:
                    print(f"Error inesperado al procesar la row {row}: {e}")
                    
            print("Datos separados y escritos en los archivos correspondientes correctamente.")

    except FileNotFoundError as fnfe:
        print(f"Error: No se pudo encontrar el archivo 'cldeldes.csv': {fnfe}")
    except PermissionError as pe:
        print(f"Error: Permiso denegado al acceder a uno de los archivos: {pe}")
    except Exception as e:
        print(f"Error inesperado: {e}")
        
#  Nuevos id de calificaciones aumentados en +1 para que hagan match correcamente:
    calificaciones_path = os.path.join(current_dir, 'csv_iniciales', 'calificacion.csv')
    calificaciones_plus_one = os.path.join(current_dir, 'csv_generados', 'calificacion_plus_one.csv')

    # Separamos clientes.csv en dos archivos, para luego popular las tablas direccion y cliente
    try:
        with open(calificaciones_path, 'r', encoding='mac_roman', errors='ignore') as main_file, \
            open(calificaciones_plus_one, 'w', newline='', encoding='mac_roman', errors='ignore') as cal_csv:
            
            reader = csv.reader(main_file, delimiter=';')
            next(reader)  # Saltar la cabecera

            # Creamos los writer para los archivos de salida qie seran escritos
            calificaciones_plus_one_writer = csv.writer(cal_csv, delimiter=';')

            # Los escribimos con sus respectivas cabeceras
            calificaciones_plus_one_writer.writerow(['pedido','resdel','cliente'])
            # Iterar sobre cada fila del archivo de entrada
            for row in reader:
                try:
                    #TODO:Sanitizar los datos!
                    # Escribimos los datos en los archivos correspondientes
                    row[0] = str(int(row[0]) + 1)
                    calificaciones_plus_one_writer.writerow(row)
                except IndexError as e:
                    print(f"Error al procesar la row {row}: {e}")
                except Exception as e:
                    print(f"Error inesperado al procesar la row {row}: {e}")
                    
            print("Datos separados y escritos en los archivos correspondientes correctamente.")

    except FileNotFoundError as fnfe:
        print(f"Error: No se pudo encontrar el archivo 'cldeldes.csv': {fnfe}")
    except PermissionError as pe:
        print(f"Error: Permiso denegado al acceder a uno de los archivos: {pe}")
    except Exception as e:
        print(f"Error inesperado: {e}")
        


    pedidos_path = os.path.join(current_dir, 'csv_iniciales', 'pedidos.csv')
    pedidos_plus_one = os.path.join(current_dir, 'csv_generados', 'pedidos_plus_one.csv')

    try:
        with open(pedidos_path, 'r', encoding='mac_roman', errors='ignore') as main_file, \
                open(pedidos_plus_one, 'w', newline='', encoding='mac_roman', errors='ignore') as pedidos_csv:

            reader = csv.reader(main_file, delimiter=';')
            next(reader)  # Saltar la cabecera

            # Creamos los writer para los archivos de salida que serán escritos
            pedidos_plus_one_writer = csv.writer(pedidos_csv, delimiter=';')

            # Escribimos la cabecera en el archivo de salida
            pedidos_plus_one_writer.writerow(['id', 'cliente', 'sucursal', 'delivery', 'despachador', 'plato', 'fecha', 'hora', 'estado'])
            
            # Iterar sobre cada fila del archivo de entrada
            for row in reader:
                try:
                    # Convertir la fecha de formato "DD-MM-YY" a "DD-MM-YYYY"
                    fecha_actual = row[6][0:6] + "20" + row[6][6:8]
                    row[6] = fecha_actual
                    row[7] = row[7] + "-03"
                    # Convertir la fecha de formato DD-MM-YYYY a YYYY-MM-DD
                    fecha = row[6].split("-")
                    fecha = fecha[2] + "-" + fecha[1] + "-" + fecha[0]
                    row[6] = fecha
                    
                    # Escribimos los datos en el archivo de salida
                    pedidos_plus_one_writer.writerow(row)
                except IndexError as e:
                    print(f"Error al procesar la fila {row}: {e}")
                except Exception as e:
                    print(f"Error inesperado al procesar la fila {row}: {e}")

            print("Datos procesados y escritos en el archivo 'pedidos_plus_one.csv' correctamente.")

    except FileNotFoundError as fnfe:
        print(f"Error: No se pudo encontrar el archivo 'pedidos.csv': {fnfe}")
    except PermissionError as pe:
        print(f"Error: Permiso denegado al acceder a uno de los archivos: {pe}")
    except Exception as e:
        print(f"Error inesperado: {e}")


limpiar_tablas()
crear_tablas('')
generar_nuevos_csv()