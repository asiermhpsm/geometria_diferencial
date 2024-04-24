from app import app
import json

server = app.test_client()
#response = server.get('/param_surf/vector_normal?superficie=[u,v,u**2%2Bv^2]')
response = server.get('/param_surf/vector_normal?superficie=[s,t,s**2%2Bt^2]&var1=s&var2=t')
res = json.loads(response.data)

pasos = r"""\documentclass{article}
\usepackage{amsmath}
\begin{document}"""
for i, paso in enumerate(res):
    pasos = pasos + f"""
Paso {i+1}

{paso['descripcion']}
$${paso['pasoLatex']}$$

"""

pasos = pasos + r"""

\end{document}"""
print(pasos)