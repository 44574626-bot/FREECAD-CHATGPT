# -*- coding: utf-8 -*-
"""Ejecutor compartido FreeCAD, operaciones tipadas y sin Python arbitrario."""
import datetime,json,os,traceback
from pathlib import Path

ROOT=Path.cwd()
def analyze(doc):
    import FreeCAD as App
    doc.recompute()
    sketches=[o for o in doc.Objects if o.TypeId=="Sketcher::SketchObject"]
    pads=[o for o in doc.Objects if o.TypeId=="PartDesign::Pad"]
    if not pads:raise ValueError("Sin extrusión PartDesign")
    if any(p.Shape.isNull() or not p.Shape.isValid() for p in pads):raise ValueError("Sólido nulo o inválido")
    if any(getattr(s,"FullyConstrained",None) is False for s in sketches):raise ValueError("Hay croquis sin restringir")
    return {"volume_mm3":pads[-1].Shape.Volume,
        "fully_constrained":all(getattr(s,"FullyConstrained",False) for s in sketches),
        "objects":len(doc.Objects),"freecad_version":".".join(map(str,App.Version()[:3]))}

def make_model(p):
    import FreeCAD as App
    import Part,Sketcher
    doc=App.newDocument("FreeCAD_Compartido")
    sheet=doc.addObject("Spreadsheet::Sheet","Parametros")
    sheet.set("A1","Parametro");sheet.set("B1","Dimensiones mm")
    for n,(alias,key) in enumerate([("p_WIDTH","width_mm"),("p_DEPTH","depth_mm"),("p_HEIGHT","height_mm"),("p_THICKNESS","thickness_mm")],2):
        sheet.set("A"+str(n),alias)
        sheet.set("B"+str(n),str(float(p[key]))+" mm")
        sheet.setAlias("B"+str(n),alias)
    doc.recompute()
    body=doc.addObject("PartDesign::Body","Cuerpo")
    sk=doc.addObject("Sketcher::SketchObject","PerfilRectangular")
    body.addObject(sk)
    w=float(p["width_mm"]);d=float(p["depth_mm"])
    v=[(0,0),(w,0),(w,d),(0,d)]
    for i in range(4):
        a,b=v[i],v[(i+1)%4]
        sk.addGeometry(Part.LineSegment(App.Vector(a[0],a[1],0),App.Vector(b[0],b[1],0)),False)
    cs=[Sketcher.Constraint("Coincident",i,2,(i+1)%4,1) for i in range(4)]
    cs += [Sketcher.Constraint("Horizontal",0),Sketcher.Constraint("Vertical",1),Sketcher.Constraint("Horizontal",2),Sketcher.Constraint("Vertical",3)]
    cs += [Sketcher.Constraint("Coincident",0,1,-1,1),Sketcher.Constraint("Distance",0,w),Sketcher.Constraint("Distance",1,d)]
    sk.addConstraint(cs)
    sk.setExpression("Constraints[9]","Parametros.p_WIDTH")
    sk.setExpression("Constraints[10]","Parametros.p_DEPTH")
    pad=body.newObject("PartDesign::Pad","Extrusion")
    pad.Profile=sk
    pad.Length=float(p["height_mm"])
    pad.setExpression("Length","Parametros.p_HEIGHT")
    doc.recompute()
    return doc

def open_model(source):
    import FreeCAD as App
    # Validación secundaria: ningún camino absoluto ni referencias fuera de results/
    parts=Path(source).parts
    if len(parts)!=3 or parts[0]!="results" or parts[2]!="model.FCStd" or ".." in parts:raise ValueError("Fuente no autorizada")
    return App.openDocument(str(ROOT/source))

def perform(req,out):
    import FreeCAD as App
    op=req["operation"]
    if op=="create_box":doc=make_model(req["params"])
    else:doc=open_model(req["source"])
    try:
        if op=="edit_params":
            sheet=doc.getObject("Parametros")
            if sheet is None:raise ValueError("No existe hoja Parametros")
            for name,val in req["params"].items():
                alias="p_"+name
                matches=[row for row in range(2,200) if sheet.getAlias("B"+str(row))==alias]
                if len(matches)!=1:raise ValueError("Alias inexistente: "+alias)
                sheet.set("B"+str(matches[0]),str(float(val))+" mm")
            doc.recompute()
        info=analyze(doc)
        if op!="inspect":
            doc.saveAs(str(out/"model.FCStd"))
            info["model"]="model.FCStd"
        else:info["model"]=None
        if "source" in req:info["source"]=req["source"]
        if op=="edit_params":info["modified"]=req["params"]
        return info
    finally:
        App.closeDocument(doc.Name)

out=ROOT/os.environ.get("CAD_OUTPUT","results/fallido")
out.mkdir(parents=True,exist_ok=True)
try:
    req=json.loads((ROOT/os.environ["CAD_REQUEST"]).read_text())
    details=perform(req,out)
    result={"success":True,"operation":req["operation"],"job_id":req["job_id"],**details,
     "finished_utc":datetime.datetime.now(datetime.timezone.utc).isoformat()}
except BaseException as ex:
    result={"success":False,"error":str(ex),"traceback":traceback.format_exc()[-8000:]}
(out/"status.json").write_text(json.dumps(result,ensure_ascii=False,indent=2,default=str))
print("FREECAD_RESULT",json.dumps({"success":result["success"],"error":result.get("error")}),flush=True)
try:
    from PySide import QtCore,QtGui
    application=QtGui.QApplication.instance()
    if application:QtCore.QTimer.singleShot(100,application.quit)
except Exception:
    try:
        from PySide6 import QtCore,QtWidgets
        application=QtWidgets.QApplication.instance()
        if application:QtCore.QTimer.singleShot(100,application.quit)
    except Exception:pass
