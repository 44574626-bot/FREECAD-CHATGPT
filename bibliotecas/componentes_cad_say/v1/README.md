# SAY | Biblioteca de modelos FreeCAD de referencia (v1)

**40 archivos reales .FCStd, copiados bit a bit** desde [FreeCAD-library](https://github.com/FreeCAD/FreeCAD-library), instantánea del commit `f5ca01cdcaa2f69b9295a6382719c2d90628780c`. Cada archivo conserva el mismo SHA Git blob que el original; ver [CATALOGO.csv](CATALOGO.csv).

Esta colección es una **biblioteca de insumos geométricos y constructivos**, no modelos homologados para el stand SAY. **Ninguna pieza está aprobada para fabricar ni comprar.** No sustituye manuales de los fabricantes, fichas comerciales o ensayos. No hay verificación nativa de apertura/recomputación en FreeCAD 1.1.4 en esta importación.

## Contenido (40 archivos)

- 01_Tornilleria: 8 modelos de tornillos métricos ISO, diferentes tipos y largos.
- 02_Tuercas: 5 tuercas ISO 4032 métricas.
- 03_Arandelas: 4 arandelas DIN/ISO.
- 04_Uniones_y_soportes: 8 escuadras, placas y perfiles de referencia.
- 05_Rodamientos: 5 rodamientos de bolas y lineales.
- 06_Guias_lineales_NO_telescopicas: 4 componentes de guías MGN. **NO son correderas telescópicas de cajón.**
- 07_Bisagras_y_cerraduras: 2 referencias genéricas, sin SKU homologado.
- 08_Rueda_de_referencia_NO_caster: 1 rueda RC. **NO es rueda de mobiliario con freno** y no debe instalarse en SAY.
- 09_Cuerpos_de_mueble_referencia: 2 modelos de gabinete, no módulos del proyecto.
- 10_Pasadores: 1 pasador/elemento de ajuste.

## Licencia y atribución

Todos los activos proceden de **FreeCAD-library**, con **CC BY 3.0** según su [licencia de activos](https://github.com/FreeCAD/FreeCAD-library/blob/f5ca01cdcaa2f69b9295a6382719c2d90628780c/LICENSE-Assets). Los autores específicos son los autores de cada pieza: abrir el enlace de fuente por archivo en CATALOGO.csv y consultar el historial de Git de esa ruta; no atribuir la autoría de todos los modelos a SAY. Los archivos no se modificaron. Si se modifica uno, documentar cambios y conservar atribuciones.

## Uso en el diseño SAY

1. Buscar funcionalidad y medidas reales; reutilizar un modelo de referencia únicamente tras estudiar un producto/norma/ensamble pertinente.
2. Para correderas telescópicas, ruedas de mobiliario con freno, bisagras ocultas, cerraduras, conectores para melamina, vidrio y sistemas antivuelco: seleccionar SKU **real** de fabricante y geometría/ficha oficial. Consultar [Hettich CAD](https://www.hettich.com/es-es/services/hettich-cad/descargas-cad), [Blum CAD](https://www.blum.com/aa/en/services/industrial-production/cad-cam-dataservice/) y la guía SAY; la colección genérica no representa esas piezas.
3. Importar en copia del subensamble o usar enlaces; verificar unidades, colocación, interferencias, agujeros, accesos, ruta de cargas, material, abastecimiento en Huancayo y permisos antes de integrar.
4. Estado de piezas: **REFERENCIA NO HOMOLOGADA**. Valor de pruebas aquí: copia exacta SHA del archivo de origen; apertura/recomputación nativa = **NO EJECUTADA**; resistencia y ensayos físicos = **NO EJECUTADOS**.

## Organización del proyecto

Biblioteca genérica almacenada en `FREECAD-CHATGPT` público porque no contiene información privada de SAY. Los modelos finales de SAY siguen en su repositorio privado y en Drive; esta biblioteca no se deposita en `SAY_V00`.
