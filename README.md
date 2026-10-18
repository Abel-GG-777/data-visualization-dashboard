# data-visualization-dashboard

Dashboard de ventas en español con Python, Streamlit y Plotly. **Datos de demostración: todas las operaciones son ficticias.**

Repositorio: https://github.com/Abel-GG-777/data-visualization-dashboard

Aplicación pública: **[PENDIENTE: añadir la URL real después del despliegue]**.

## Instalación y ejecución

Usa Python 3.12 (también utilizado en CI). En Windows, si `python` no está en el PATH, utiliza `py -3.12` para crear el entorno.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

En Linux/macOS:

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python -m streamlit run app.py
```

Abre http://localhost:8501. Para solo ejecutar la aplicación basta instalar `requirements.txt`; `requirements-dev.txt` agrega pytest. Detén el servidor con Ctrl+C.

## Datos y uso

- 2.400 pedidos únicos entre el 1 de enero y el 31 de diciembre de 2025, generados con `random.Random(42)`. No dependen de la fecha del equipo ni de servicios externos.
- Cada fila es un pedido con categoría, región, unidades, venta y costo. Los cálculos base usan céntimos enteros; la presentación y el CSV usan soles (PEN).
- Ventas = suma de importes; ganancias = ventas menos costos simulados; pedidos = identificadores únicos; ticket promedio = ventas / pedidos. No se modelan impuestos, descuentos ni devoluciones.
- Los tres filtros se combinan con AND. El período incluye ambos extremos. Una categoría o región vacía devuelve cero pedidos. Los días sin ventas aparecen como cero en la evolución.
- La tabla y la descarga reflejan los mismos filtros. CSV con encabezados incluso sin resultados, codificación UTF-8 con BOM, coma como separador y punto decimal.

`sales.py` contiene los datos y cálculos; `app.py` construye la interfaz. `.streamlit/config.toml` define el tema. No se necesitan credenciales ni secretos.

## Verificación

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m compileall -q app.py sales.py
```

Las pruebas verifican reproducibilidad, identidades contables, indicadores con valores conocidos, límites inclusivos de fechas, combinación de filtros, resultados vacíos, CSV y ejecución de Streamlit mediante `AppTest` con interacciones. Esta ejecución comprueba elementos y comportamiento de la app; no sustituye una revisión visual en navegador.

Validación local realizada el 18 de octubre de 2026 con Python 3.12.14:

- `pytest -q`: **9 pruebas aprobadas**.
- Compilación de `app.py` y `sales.py` correcta; `pip check`: sin dependencias incompatibles.
- Servidor Streamlit iniciado en `127.0.0.1:8501`; `/_stcore/health` respondió `ok`.
- Conjunto completo: ventas **S/ 2.437.981,88**, ganancias **S/ 656.355,02**, **2.400 pedidos**, ticket mostrado **S/ 1.015,83**.
- Revisión visual en navegador pendiente: no había un navegador conectado disponible en el entorno de trabajo. No se ha verificado un despliegue público ni una ejecución de Actions en GitHub.

## Despliegue público en Streamlit Community Cloud

Instrucciones contrastadas con la documentación oficial el 18 de octubre de 2026. Pasos que debe completar el propietario de la cuenta:

1. Revisa los cambios y súbelos a la rama `main` del repositorio de GitHub. Desde esta carpeta, puedes usar `git add .`, `git commit -m "Construir dashboard de ventas"` y `git push origin main`. El `.gitignore` excluye el entorno, cachés y secretos locales.
2. Entra en https://share.streamlit.io, inicia sesión y vincula GitHub con los permisos solicitados para el repositorio. Selecciona el espacio de trabajo de `Abel-GG-777`.
3. Pulsa **Create app**, luego **Yup, I have an app**. Selecciona repositorio `Abel-GG-777/data-visualization-dashboard`, rama `main` y archivo de entrada `app.py`.
4. En **Advanced settings**, elige Python **3.12**. No agregues secretos: esta aplicación no los usa. El subdominio es opcional y depende de disponibilidad.
5. Despliega y revisa los registros. Comprueba indicadores, filtros y CSV. En la configuración de uso compartido confirma el acceso público; abre el enlace en una ventana sin sesión para verificarlo.
6. Copia la URL real en este README y en el borrador del artículo. La URL no se puede confirmar antes de que el servicio cree la aplicación.

Después del primer despliegue, los cambios enviados a la rama configurada se reflejan automáticamente en Community Cloud; cambios en dependencias provocan su reinstalación y pueden tardar más. No se requiere un workflow de despliegue ni un token de Streamlit en GitHub.

**GitHub Actions solo comprueba el código.** `.github/workflows/checks.yml` instala dependencias, compila y ejecuta las pruebas en cada push y pull request. No publica la app ni el artículo. Community Cloud despliega por separado y no espera necesariamente a que Actions termine: ejecuta las pruebas antes de subir cambios o utiliza protección de rama y pull requests con comprobaciones obligatorias si tu cuenta/repositorio lo permite.

Documentación oficial:

- [Crear y desplegar una app](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy)
- [Actualizar la app y sus dependencias](https://docs.streamlit.io/deploy/streamlit-community-cloud/manage-your-app)
- [Dependencias](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies)
- [Compartir la aplicación](https://docs.streamlit.io/deploy/streamlit-community-cloud/share-your-app)

## Artículo

El borrador editable está en [docs/articulo-borrador.md](docs/articulo-borrador.md). Está pendiente de revisión y publicación autorizada. No se ha creado video, guion ni envío a Telegram.
