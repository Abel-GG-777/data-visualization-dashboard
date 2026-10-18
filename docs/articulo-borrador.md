# De Python a un dashboard público de ventas con Streamlit y Plotly

**Borrador para Medium, Dev.to o Hashnode. Pendiente de revisión; no publicado.**

Repositorio: https://github.com/Abel-GG-777/data-visualization-dashboard

Aplicación: **[PENDIENTE: insertar la URL real de Streamlit Community Cloud]**

Un dashboard permite explorar preguntas concretas: ¿cómo evolucionan las ventas?, ¿qué categorías concentran ingresos?, ¿qué regiones generan más ganancias? Este proyecto implementa ese recorrido con Python, Streamlit y Plotly, desde los datos hasta la preparación del despliegue.

## Una demostración reproducible

El punto de partida es un conjunto de 2.400 pedidos ficticios del año 2025. La función `generate_data()` utiliza una semilla fija, 42, para obtener el mismo conjunto en cada ejecución con el mismo entorno. La interfaz señala expresamente que son datos de demostración: las cifras no describen una empresa real.

Cada pedido tiene una fecha, categoría, región, cantidad de unidades, ventas y costos. Guardamos importes en céntimos enteros para sumar sin acumular errores de representación decimal. Los convertimos a soles peruanos al mostrarlos y exportarlos.

## Separar las reglas de la interfaz

`sales.py` genera los datos, aplica filtros, calcula indicadores y prepara el CSV. `app.py` se ocupa de la página y los gráficos. Esa separación facilita comprobar la lógica con ejemplos pequeños, sin depender del navegador.

Las métricas tienen definiciones explícitas: ventas es la suma de importes, ganancias es ventas menos costos, pedidos cuenta identificadores únicos y ticket promedio divide ventas entre pedidos. Si no hay pedidos, el ticket es cero. Esta simulación no incorpora impuestos ni devoluciones; las ganancias no deben interpretarse como beneficio neto contable.

## Filtrar para responder preguntas

La barra lateral permite seleccionar un período, categorías y regiones. Las condiciones se combinan: un pedido debe cumplir las tres. Las fechas incluyen los extremos y dejar una selección vacía produce un resultado vacío con un mensaje explicativo.

Los cuatro indicadores resumen la selección. Una línea presenta las ventas diarias, incluyendo ceros para los días sin operaciones. Dos gráficos de barras muestran ventas por categoría y ventas frente a ganancias por región. La tabla final permite inspeccionar los pedidos concretos y descargar exactamente esa selección en CSV con encabezados en español.

## Ejecutar y comprobar

Con Python 3.12, creamos un entorno virtual, instalamos `requirements-dev.txt` y ejecutamos `python -m streamlit run app.py` desde ese entorno. Las dependencias están fijadas para mantener un entorno definido.

La suite de pytest comprueba fórmulas con cantidades conocidas, reproducibilidad, filtros combinados, un solo día, selecciones vacías y contenido del CSV. `streamlit.testing.v1.AppTest` ejecuta la página e interactúa con sus filtros para verificar que tabla e indicadores respondan. El comando es `python -m pytest -q`. Una revisión visual en navegador complementa estas comprobaciones.

En la verificación local del 18 de octubre de 2026, con Python 3.12.14, pasaron las nueve pruebas. El servidor respondió `ok` en su endpoint de salud y `pip check` no encontró conflictos. El conjunto completo produjo 2.400 pedidos, S/ 2.437.981,88 en ventas y S/ 656.355,02 en ganancias simuladas. No había un navegador conectado para comprobar visualmente la página; esa revisión sigue pendiente, junto con la validación del despliegue público.

## Preparar la publicación con GitHub

El código se aloja en [data-visualization-dashboard](https://github.com/Abel-GG-777/data-visualization-dashboard). El archivo `.gitignore` excluye entornos virtuales, cachés, archivos `.env` y secretos de Streamlit. Esta demostración no necesita claves de API.

En Streamlit Community Cloud, el propietario debe conectar su cuenta de GitHub y crear una app con ese repositorio, la rama `main` y `app.py` como entrada. En las opciones avanzadas selecciona Python 3.12. Después debe comprobar el acceso público y copiar la URL que asigne el servicio en los marcadores de este artículo y el README.

Según la [documentación de despliegue](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy) y de [actualizaciones](https://docs.streamlit.io/deploy/streamlit-community-cloud/manage-your-app), consultada el 18 de octubre de 2026, Community Cloud refleja automáticamente los cambios enviados al repositorio conectado. Los cambios de dependencias desencadenan su reinstalación.

El workflow de GitHub Actions cumple otra función: ejecutar compilación y pruebas en pushes y pull requests. No despliega. Un fallo de Actions no impide por sí solo que Community Cloud actualice la rama conectada; para controlar ese flujo conviene trabajar con pull requests y comprobaciones obligatorias cuando estén disponibles.

## Estado antes de publicar este artículo

El proyecto incluye la implementación y la preparación del despliegue. La publicación pública y su URL siguen pendientes de los pasos del propietario de la cuenta. Antes de publicar este texto hay que añadir la URL verificada, revisar la experiencia real de despliegue y completar cualquier resultado de validación con evidencia. No se afirma que el despliegue haya ocurrido.
