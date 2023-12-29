import sqlite3 as db

# Creacion de la base de datos
conexionBD=db.connect("pruebaTecnicaBD")

# Gracias a este cursor podremos modificar la base de datos
cursorBD = conexionBD.cursor()

# Creacion tabla precio
crearTablaPrecio = '''
    CREATE TABLE PRICE (
                 PRICE_ID INTEGER PRIMARY KEY,
                 NORMAL_PRICE INTEGER,
                 DISCOUNT_PRICE INTEGER,
                 ACTIVE BOOLEAN,
                 CREATE_DATE DATE
                 )
'''

# Ejecutamos
cursorBD.execute(crearTablaPrecio)

# Creacion tabla producto
crearTablaProducto = '''
    CREATE TABLE PRODUCT (
                 SKU VARCHAR(8) PRIMARY KEY,
                 NAME VARCHAR(20),
                 EAN INTEGER,
                 PRICE_ID INTEGER,
                 FOREIGN KEY(PRICE_ID) REFERENCES PRICE(PRICE_ID)
                 )
'''

# Ejecutamos
cursorBD.execute(crearTablaProducto)

# Creacion tabla mercado
crearTablaMercado = '''
    CREATE TABLE MARKET (
                 NAME VARCHAR(50),
                 SKU VARCHAR(8),
                 FOREIGN KEY(SKU) REFERENCES PRODUCT(SKU)
                 )
'''

# Ejecutamos
cursorBD.execute(crearTablaMercado)

# Agregamos datos a tabla Price
cursorBD.execute("INSERT INTO PRICE VALUES(1, 14990, 9990, 1, '2023-12-28')")
cursorBD.execute("INSERT INTO PRICE VALUES(2, 19990, 17990, 1, '2023-12-28')")
cursorBD.execute("INSERT INTO PRICE VALUES(3, 12990, 9990, 0, '2023-12-28')")
cursorBD.execute("INSERT INTO PRICE VALUES(4, 11990, 7990, 1, '2023-12-28')")

# Agregamos datos a tabla Product
cursorBD.execute("INSERT INTO PRODUCT VALUES('Z12GS34E', 'Botella', 7805688518182, 1)")
cursorBD.execute("INSERT INTO PRODUCT VALUES('Z12GS34F', 'Botella Roja', 7805688518182, 1)")
cursorBD.execute("INSERT INTO PRODUCT VALUES('HS23JKA1', 'Caja Organizadora', 7800478112321, 2)")
cursorBD.execute("INSERT INTO PRODUCT VALUES('12GAS69S', 'Juego de mesa genérico', 7811805656723, 3)")
cursorBD.execute("INSERT INTO PRODUCT VALUES('YU1352IA', 'Libreta', 7867216351516, 4)")

# Agregamos datos a tabla Market
cursorBD.execute("INSERT INTO MARKET VALUES('LIDER', 'Z12GS34E')")
cursorBD.execute("INSERT INTO MARKET VALUES('CASAIDEAS', 'HS23JKA1')")
cursorBD.execute("INSERT INTO MARKET VALUES('RIPLEY', '12GAS69S')")
cursorBD.execute("INSERT INTO MARKET VALUES('RIPLEY', 'Z12GS34F')")
cursorBD.execute("INSERT INTO MARKET VALUES('CONTRAPUNTO LIBROS', 'YU1352IA')")

# vemos los resultados

cursorBD.execute("SELECT * FROM PRODUCT") 

results = cursorBD.fetchall()

print("Datos de tabla Product: ",results)

# Cerrar la conexión a la base de datos
conexionBD.commit()
conexionBD.close()






