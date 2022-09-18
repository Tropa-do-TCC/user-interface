from oct2py import Oct2Py
from scipy.io import savemat

oc = Oct2Py()

script = ""

with open("CreateShapeModel.m") as script_file:
    script = script_file.read()
with open("myScript.m", "w+") as f:
    f.write(script)

savemat("shape_model/ShapeModel11-09_76datasets.mat", oc.myScript(7))
