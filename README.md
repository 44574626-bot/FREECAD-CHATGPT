# FreeCAD compartido para ChatGPT

Motor de ejecución CAD basado en **FreeCAD 1.1.4** y **GitHub Actions**.

## Estado
Infraestructura en despliegue. **No afirmar que FreeCAD funciona hasta obtener un job con status.json satisfactorio y model.FCStd verificable.**

## Seguridad
**Este repositorio es PÚBLICO.** Solo puede alojar scripts genéricos y ejemplos no confidenciales. No subir modelos privados, imágenes de clientes, planos, archivos de SAY, credenciales ni datos personales. Cambiar la visibilidad a `Private` en Settings → General → Danger Zone → Change repository visibility antes de incorporar el proyecto.

## Cómo utilizarlo
1. Los chats crean un JSON tipado nuevo en `jobs/requests/<job_id>.json`.
2. Al hacer commit en `main`, GitHub Actions inicia el ejecutor.
3. FreeCAD genera `results/<job_id>/model.FCStd` y `results/<job_id>/status.json`.
4. Otro chat puede usar `edit_params` sobre el archivo generado sin sobrescribir el original.
5. La instalación AppImage está verificada por SHA-256 y se extrae en caché de Actions, sujeta a expiración.

Ejemplo de solicitud:
```json
{"job_id":"prueba-box-001","operation":"create_box","params":{"width_mm":454,"depth_mm":400,"height_mm":18,"thickness_mm":18}}
```

Operaciones: `create_box`, `inspect` y `edit_params`. Se aceptan solo operaciones declaradas; no se ejecuta código Python enviado por solicitudes JSON.

**Limitaciones:** GitHub Actions usa máquinas efímeras, no un servidor FreeCAD permanentemente encendido. La caché se puede perder. Las cuotas y permisos de GitHub pueden limitar las ejecuciones.

FreeCAD oficial: https://github.com/FreeCAD/FreeCAD/releases/tag/1.1.4
