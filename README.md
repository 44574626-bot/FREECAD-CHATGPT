# FreeCAD compartido para ChatGPT

**Estado: prueba funcional completada el 11/11/2026.** Motor real FreeCAD **1.1.4**, sobre GitHub Actions con caché recuperada entre ejecuciones.

## Resultados verificados

1. [Ejecución 2](https://github.com/44574626-bot/FREECAD-CHATGPT/actions/runs/43123404371): primera generación de `results/demo-publico-002/model.FCStd`. Croquis restringido y volumen **3 268 800 mm³** (454 × 400 × 18 mm).
2. [Ejecución 3](https://github.com/44574626-bot/FREECAD-CHATGPT/actions/runs/43123807848): edición de `WIDTH = 500 mm` sobre la versión 2. Nuevo archivo `results/demo-edicion-003/model.FCStd`, croquis restringido, volumen **3 600 000 mm³**. El original sigue intacto.
3. En la tercera ejecución GitHub confirma **cache hit**, sin descargar nuevamente el AppImage desde el sitio de FreeCAD.

## Funcionamiento para varios chats

El chat crea un archivo **nuevo** en `jobs/requests/<job_id>.json` usando la conexión GitHub. El commit en `main` dispara `.github/workflows/freecad.yml`. El ejecutor abre FreeCAD, trabaja sobre un archivo nativo y publica un resultado propio en `results/<job_id>/`.

**Crear un modelo**:
```json
{"job_id":"ejemplo-001","operation":"create_box","params":{"width_mm":454,"depth_mm":400,"height_mm":18,"thickness_mm":18}}
```

**Modificar sin sobrescribir**:
```json
{"job_id":"ejemplo-002","operation":"edit_params","source":"results/ejemplo-001/model.FCStd","params":{"WIDTH":500}}
```

**Inspeccionar un modelo previo**:
```json
{"job_id":"ejemplo-003","operation":"inspect","source":"results/ejemplo-002/model.FCStd","params":{}}
```

Actualmente las operaciones permitidas son **create_box**, **edit_params** (WIDTH, DEPTH, HEIGHT, THICKNESS) e **inspect**. El acceso se realiza mediante archivos JSON restringidos, **sin ejecución de código Python arbitrario desde el chat**.

Los modelos siguen bajo control de versiones Git, y el motor es reproducible. El caché no es permanente: puede expirar o eliminarse.

## Seguridad: repositorio PÚBLICO

**IMPORTANTE: ESTE REPOSITORIO ES PÚBLICO.** Aquí hay exclusivamente infraestructura genérica y geometría de prueba. **No subir `STAND.FCStd`, `Pieza1.ipt`, imágenes de la clienta, archivos CAD de SAY, planos privados ni credenciales.**

Antes de incorporar los archivos del proyecto SAY, el titular debe cambiarlo a privado desde **Settings → General → Danger Zone → Change repository visibility → Make private**. Es una acción que debe realizar el titular desde GitHub.

## Alcance y restricciones

- No es un servidor permanentemente encendido: GitHub Actions utiliza una máquina temporal por trabajo.
- FreeCAD 1.1.4 se ejecuta realmente y sus archivos nativos se conservan.
- Solo está probada la generación y edición de un cuerpo rectangular simple. **Todavía no se ha habilitado la construcción completa de R06, ensamblajes o planos**.
- Al ejecutar sobre un repositorio público, cualquier archivo generado será público. Los trabajos pasan por GitHub Actions, no por Codex.
- Tras convertir el repositorio a privado, habrá que verificar las políticas de Actions y la cuota disponible según el plan.

## Enlaces

- [Ejecuciones GitHub Actions](https://github.com/44574626-bot/FREECAD-CHATGPT/actions)
- [Modelos de demostración](https://github.com/44574626-bot/FREECAD-CHATGPT/tree/main/results)
- [FreeCAD 1.1.4 oficial](https://github.com/FreeCAD/FreeCAD/releases/tag/1.1.4)
