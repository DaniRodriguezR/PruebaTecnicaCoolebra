from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3 as db

app = Flask(__name__)

# Habilitamos CORS para poder pasar valores del backend al frontend
CORS(app)

def consulta():
    conexionBD=db.connect("pruebaTecnicaBD")
    cursorBD = conexionBD.cursor()

    query = '''
        SELECT P.SKU, P.NAME, P.EAN, PR.NORMAL_PRICE, MIN(PR.DISCOUNT_PRICE) AS "ULTIMO MENOR PRECIO ACTIVO",
        M.NAME AS NOMBRE_MERCADO
        FROM PRODUCT AS P
        JOIN
        PRICE AS PR ON P.PRICE_ID = PR.PRICE_ID
        JOIN
        MARKET AS M ON P.SKU = M.SKU
        
        /* PR.ACTIVE INDICANDO SI EL PRECIO ESTA ACTIVO 
        SIENDO 1 QUE SI LO ESTÁ Y 0 QUE NO LO ESTÁ*/
        WHERE PR.ACTIVE = 1
        GROUP BY P.SKU
        ORDER BY P.SKU
    '''

    cursorBD.execute(query)

    # Obtener los resultados
    resultados = cursorBD.fetchall()

    # Cerrar la conexión y el cursor
    cursorBD.close()
    conexionBD.close()

    return resultados

@app.route('/api/datos_agrupados', methods=['GET'])
def obtener_datos_agrupados():

    resultados = consulta()

    resultados_agrupados = {}

    # Recorrer resultados
    for resultado in resultados:
        sku, nombre_producto, ean, precio_normal, precio_descto, nombre_mercado = resultado

        # Actualizar el diccionario con datos del producto
        if sku not in resultados_agrupados:
            resultados_agrupados[sku] = {
                "Nombre del producto": nombre_producto,
                "Datos Query":[],
                "Markets": set(),
                "Rango de precios": {"menor": precio_descto, "mayor": precio_normal},
                "Ultimo Menor Precio Activo": precio_descto,
            }
        
        # Agregar los datos de la query al diccionario
        resultados_agrupados[sku]["Datos Query"].append(f"SKU: {sku}, Ean:{ean}, Precio: {precio_descto}, Mercado: {nombre_mercado}")

        # Actualizar la cantidad de markets diferentes
        resultados_agrupados[sku]["Markets"].add(nombre_mercado)

        # Actualizar el rango de precios
        if precio_normal > resultados_agrupados[sku]["Rango de precios"]["mayor"]:
            resultados_agrupados[sku]["Rango de precios"]["mayor"] = precio_normal
        elif precio_descto < resultados_agrupados[sku]["Rango de precios"]["menor"]:
            resultados_agrupados[sku]["Rango de precios"]["menor"] = precio_descto

    # Calcular la cantidad de markets diferentes
    for sku, datos_producto in resultados_agrupados.items():
        datos_producto["Cantidad Markets Diferentes"] = len(datos_producto["Markets"])

    # Convertir el diccionario a la lista de diccionarios solicitada
    lista_resultados_agrupados = [{
        "Nombre Producto": datos["Nombre del producto"],
        "Datos Query": datos["Datos Query"],
        "Cantidad de Markets Diferentes": datos["Cantidad Markets Diferentes"],
        "Rango de Precios": f"{datos['Rango de precios']['mayor']} - {datos['Rango de precios']['menor']}",
        "Ultimo Menor Precio Activo": datos["Rango de precios"]["menor"]
    } for datos in resultados_agrupados.values()]

    return jsonify(lista_resultados_agrupados)

if __name__ == '__main__':
    app.run(debug=True)
            
