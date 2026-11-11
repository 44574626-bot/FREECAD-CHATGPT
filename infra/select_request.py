import json, os, re, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
def main():
    event=os.environ.get("GITHUB_EVENT_NAME","")
    if event=="workflow_dispatch":
        p=os.environ.get("JOB_PATH") or "jobs/examples/primer_modelo.json"
    elif event=="push":
        payload=json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text())
        added=[path for c in payload.get("commits",[]) for path in c.get("added",[]) if path.startswith("jobs/requests/") and path.endswith(".json")]
        if len(added)!=1: raise ValueError("Una solicitud nueva por push")
        p=added[0]
    else: raise ValueError("Evento no admitido")
    rel=Path(p)
    if rel.is_absolute() or ".." in rel.parts or not p.startswith(("jobs/examples/","jobs/requests/")):raise ValueError("Ruta de solicitud inválida")
    f=(ROOT/rel).resolve()
    if not f.is_relative_to(ROOT) or not f.is_file():raise ValueError("Solicitud no encontrada")
    data=json.loads(f.read_text())
    jid=data.get("job_id")
    if not isinstance(jid,str) or not re.fullmatch(r"[a-z0-9][a-z0-9_-]{2,59}",jid):raise ValueError("ID inválido")
    if data.get("operation")!="create_box":raise ValueError("Solo create_box disponible en la demostración pública")
    if set(data)!={"job_id","operation","params"}:raise ValueError("Campos inesperados")
    params=data["params"]
    if not isinstance(params,dict) or set(params)!={"width_mm","depth_mm","height_mm","thickness_mm"}:raise ValueError("Parámetros incorrectos")
    for v in params.values():
        if isinstance(v,bool) or not isinstance(v,(int,float)) or not (0.1<=v<=5000):raise ValueError("Dimensión inválida")
    if (ROOT/"results"/jid/"status.json").exists():raise ValueError("ID usado, crear una nueva revisión")
    with open(os.environ["GITHUB_ENV"],"a") as out:
        out.write(f"CAD_REQUEST={p}\nCAD_JOB_ID={jid}\nCAD_OUTPUT=results/{jid}\n")
    print("SOLICITUD OK:",jid)
if __name__=="__main__":
    try:main()
    except Exception as e:
        print("ERROR:",e,file=sys.stderr);sys.exit(1)
