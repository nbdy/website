from docxtpl import DocxTemplate
from json import load

d = DocxTemplate("x.docx")
ctx = {
    "projects": load(open("stuff.json"))
}
d.render(ctx)
d.save("o.docx")
