import React, { useState, useEffect } from 'react';
import Producto from './Producto';

const App = () => {
  const [productosOriginales, setProductosOriginales] = useState([]);
  const [productos, setProductos] = useState([]);
  const [filtro, setFiltro] = useState('');

  useEffect(() => {
    // Realizar solicitud a app.py al montar el componente
    fetch('http://localhost:5000/api/datos_agrupados')
      .then(response => response.json())
      .then(data => {
        setProductosOriginales(data);
        setProductos(data);
      })
      .catch(error => console.error('Error al cargar productos:', error));
  }, []);

  const filtrarProductos = () => {
    // Aplicar el filtrado a la copia original de productos
    const filtrados = productosOriginales.filter(producto =>
      producto["nombre_de_producto"].toLowerCase().includes(filtro.toLowerCase())
    );
    setProductos(filtrados);
  };

  const limpiarFiltro = () => {
    setFiltro('');
    setProductos(productosOriginales); // Restablecer productos al estado original
  };

  const procesarFiltrado = () => {
    // Aplicar el filtro cuando se hace clic en Buscar
    filtrarProductos();
  };

  return (
    <div>
      <input
        type="text"
        placeholder="Filtrar por nombre"
        value={filtro}
        onChange={(e) => setFiltro(e.target.value)}
      />
      <button onClick={procesarFiltrado}>Buscar</button>
      <button onClick={limpiarFiltro}>Limpiar Filtro</button>
      {productos.map((producto, index) => (
        <Producto
          key={index}
          nombre={producto["nombre_de_producto"]}
          datosQuery={producto["datos_query"]}
          marketsDiferentes={producto["cantidad_markets_diferentes"]}
          rangoPrecios={producto["rango_precios"]}
          ultimoMenorPrecioActivo={producto["ultimo_menor_precio_activo"]}
        />
      ))}
    </div>
  );
};

export default App;
