import json, os, re, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
VALID_ID=re.compile(r"[a-z0-9][a-z0-9_-]{2,59}")
SOURCE_RE=re.compile(r"results/([a-z0-9][a-z0-9_-]{2,59})/model\.FCStd")
def main():
    event=os.environ.get("GITHUB_EVENT_NAME","")
    if event=="workflow_dispatch":
        p=os.environ.get("JOB_PATH") or "jobs/examples/primer_modelo.json"
    elif event=="push":
        payload=json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text())
        added=[path for c in payload.get("commits",[]) for path in c.get("added",[]) if path.startswith("jobs/requests/") and path.endswith(".json")]
        if not added:
            completed=subprocess.run(["git","diff-tree","--no-commit-id","--name-only","--diff-filter=A","-r","HEAD"],cwd=ROOT,capture_output=True,text=True,check=True)
            added=[p for p in completed.stdout.splitlines() if p.startswith("jobs/requests/") and p.endswith(".json")]
        if len(set(added))!=1: raise ValueError("Se requiere una solicitud nueva por commit: "+repr(added))
        p=added[0]
    else: raise ValueError("Evento no admitido")
    rel=Path(p)
    if rel.is_absolute() or ".." in rel.parts or not p.startswith(("jobs/examples/","jobs/requests/")):raise ValueError("Ruta de solicitud inválida")
    f=(ROOT/rel).resolve()
    if not f.is_relative_to(ROOT) or not f.is_file():raise ValueError("Solicitud no encontrada")
    if f.stat().st_size>16384:raise ValueError("Solicitud demasiado grande")
    data=json.loads(f.read_text())
    jid=data.get("job_id")
    if not isinstance(jid,str) or not VALID_ID.fullmatch(jid):raise ValueError("ID inválido")
    if p.startswith("jobs/requests/") and Path(p).stem != jid: raise ValueError("Nombre de archivo y job_id deben coincidir")
    op=data.get("operation")
    if op=="create_box":
        if set(data)!={"job_id","operation","params"}:raise ValueError("Campos inesperados")
        params=data["params"]
        if not isinstance(params,dict) or set(params)!={"width_mm","depth_mm","height_mm","thickness_mm"}:raise ValueError("Parámetros incorrectos")
    elif op in {"inspect","edit_params"}:
        if set(data)!={"job_id","operation","source","params"}:raise ValueError("Campos inesperados")
        source=data["source"]
        m=SOURCE_RE.fullmatch(source) if isinstance(source,str) else None
        if not m or m.group(1)==jid:raise ValueError("Ruta de fuente inválida")
        if not (ROOT/source).is_file():raise ValueError("Modelo fuente inexistente")
        params=data["params"]
        if op=="edit_params":
            if not isinstance(params,dict) or not params or len(params)>4 or set(params)-{"WIDTH","DEPTH","HEIGHT","THICKNESS"}:raise ValueError("Alias desconocidos")
        elif params!={}:raise ValueError("Inspect no acepta parámetros")
    else:raise ValueError("Operación no permitida")
    for v in params.values():
        if isinstance(v,bool) or not isinstance(v,(int,float)) or not (0.1<=v<=5000):raise ValueError("Dimensión inválida")
    if (ROOT/"results"/jid/"status.json").exists():raise ValueError("ID existente; crear una revisión nueva")
    with open(os.environ["GITHUB_ENV"],"a") as out:
        out.write(f"CAD_REQUEST={p}\nCAD_JOB_ID={jid}\nCAD_OUTPUT=results/{jid}\n")
    print("SOLICITUD OK:",jid,op)
if __name__=="__main__":
    try:main()
    except Exception as e:
        print("ERROR:",e,file=sys.stderr);sys.exit(1)
