import React from 'react';

const Producto = ({ nombre, datosQuery, marketsDiferentes, rangoPrecios, ultimoMenorPrecioActivo }) => (
    <div>
        <h2>Nombre del Producto: {nombre}</h2>
        <p>Rango de Precios: {rangoPrecios}</p>
        <p>Cantidad de Markets Diferentes: {marketsDiferentes}</p>
        <div>
            <h3>Datos de la Query:</h3>
            <ul>
                {datosQuery.map((dato, idx) => (
                    <li key={idx}>{dato}</li>
                ))}
            </ul>
        </div>
        <hr />
    </div>
);

export default Producto;
