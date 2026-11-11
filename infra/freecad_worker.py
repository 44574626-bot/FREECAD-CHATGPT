# -*- coding: utf-8 -*-
"""Motor FreeCAD público de demostración. Solo genera cajas paramétricas."""
import datetime,json,os,traceback
from pathlib import Path
def run():
    import FreeCAD as App
    import Part,Sketcher
    root=Path.cwd()
    req=json.loads((root/os.environ["CAD_REQUEST"]).read_text())
    out=root/os.environ["CAD_OUTPUT"]
    out.mkdir(parents=True,exist_ok=True)
    p=req["params"]
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
    cs += [Sketcher.Constraint("Coincident",0,1,-1,1), Sketcher.Constraint("Distance",0,w), Sketcher.Constraint("Distance",1,d)]
    sk.addConstraint(cs)
    sk.setExpression("Constraints[9]","Parametros.p_WIDTH")
    sk.setExpression("Constraints[10]","Parametros.p_DEPTH")
    pad=body.newObject("PartDesign::Pad","Extrusion")
    pad.Profile=sk
    pad.Length=float(p["height_mm"])
    pad.setExpression("Length","Parametros.p_HEIGHT")
    doc.recompute()
    if pad.Shape.isNull() or not pad.Shape.isValid():raise ValueError("La geometría no es válida")
    fully=getattr(sk,"FullyConstrained",None)
    if fully is False:raise ValueError("Croquis no totalmente restringido")
    volume=pad.Shape.Volume
    filepath=out/"model.FCStd"
    doc.saveAs(str(filepath))
    result={"success":True,"operation":req["operation"],"job_id":req["job_id"],
      "model":"model.FCStd","volume_mm3":volume,"fully_constrained":fully,
      "freecad_version":".".join(map(str,App.Version()[:3])),
      "finished_utc":datetime.datetime.now(datetime.timezone.utc).isoformat()}
    App.closeDocument(doc.Name)
    return result

out=Path.cwd()/os.environ.get("CAD_OUTPUT","results/fallido")
out.mkdir(parents=True,exist_ok=True)
try:
    result=run()
except BaseException as ex:
    result={"success":False,"error":str(ex),"traceback":traceback.format_exc()[-8000:]}
(out/"status.json").write_text(json.dumps(result,ensure_ascii=False,indent=2,default=str))
print("FREECAD_RESULT",json.dumps({"success":result["success"],"error":result.get("error")}),flush=True)
try:
    from PySide import QtCore,QtGui
    application=QtGui.QApplication.instance()
    if application: QtCore.QTimer.singleShot(100,application.quit)
except Exception:
    try:
        from PySide6 import QtCore,QtWidgets
        application=QtWidgets.QApplication.instance()
        if application: QtCore.QTimer.singleShot(100,application.quit)
    except Exception:pass
