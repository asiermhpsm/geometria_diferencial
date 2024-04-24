from formulas import *


ALG_WEINGARTEN = [
    r'''Calcular el vector normal
$$'''+FORMULA_VECTOR_NORMAL+r'$$',
    r'''Calcular la primera forma fundamental
$$''' + FORMULA_PFF + r'$$',
    r'''Calcular la segunda forma fundamental
$$''' + FORMULA_SFF + r'$$',
    r'''Calcular la matriz de Weingarten
$$''' + FORMULA_WEINGARTEN + r'$$'
]

ALG_VECTOR_NORMAL = [
    r'''Calcular el vector normal
$$'''+FORMULA_VECTOR_NORMAL+r'$$'
]

ALG_SFF = [
    r'''Calcular el vector normal
$$'''+FORMULA_VECTOR_NORMAL+r'$$',
    r'''Calcular la segunda forma fundamental
$$''' + FORMULA_SFF + r'''$$
donde
$$''' + FORMULA_COMP_SFF + r'$$'
]

ALG_PTO_UMBILICO = [
    r'''Calcular el vector normal
$$'''+FORMULA_VECTOR_NORMAL+r'$$',
    r'''Calcular la primera forma fundamental
$$''' + FORMULA_PFF + r'$$',
    r'''Calcular la segunda forma fundamental
$$''' + FORMULA_SFF + r'$$',
    r'''Calcular la curvatura de Gauss
$$''' + FORMULA_CURV_GAUSS + r'$$',
    r'''Calcular la curvatura media
$$''' + FORMULA_CURV_MEDIA + r'$$',
    r'''Calcular las curvaturas principales
$$''' + FORMULA_CURVS_PRINCIPALES + r'$$',
    r'''Calcular los puntos umbílicos, que cumplen
$$\kappa_1 = \kappa_2$$'''
]

ALG_PLANO_TANGENTE = [
    r'''Calcular el plano tangente
$$'''+FORMULA_PLANO_TANG+r'$$'
]

ALG_PFF = [
    r'''Calcular la primera forma fundamental
$$''' + FORMULA_PFF + r'''$$
donde
$$''' + FORMULA_COMP_PFF + r'$$'
]

ALG_DIRS_PRINCIPALES = [
    r'''Calcular el vector normal
$$'''+FORMULA_VECTOR_NORMAL+r'$$',
    r'''Calcular la primera forma fundamental
$$''' + FORMULA_PFF + r'$$',
    r'''Calcular la segunda forma fundamental
$$''' + FORMULA_SFF + r'$$',
    r'''Calcular la matriz de Weingarten
$$''' + FORMULA_WEINGARTEN + r'$$',
    r'''Calcular las direcciones principales con la matriz de Weingarten. Sean $\kappa_1, \kappa_2$ los autovalores de la matriz de Weingarten y $\vec{v}=(\vec{v}_1, \vec{v}_2), \vec{w}=(\vec{w}_1, \vec{w}_2)$ sus autovectores, entonces las direcciones principales son
$$d_1 = \vec{v}_1\cdot\varphi_u + \vec{v}_2\cdot\varphi_v$$
$$d_2 = \vec{w}_1\cdot\varphi_u + \vec{w}_2\cdot\varphi_v$$'''
]

ALG_CURV_PRINCIPALES = [
    r'''Calcular el vector normal
$$'''+FORMULA_VECTOR_NORMAL+r'$$',
    r'''Calcular la primera forma fundamental
$$''' + FORMULA_PFF + r'$$',
    r'''Calcular la segunda forma fundamental
$$''' + FORMULA_SFF + r'$$',
    r'''Calcular la curvatura de Gauss
$$''' + FORMULA_CURV_GAUSS + r'$$',
    r'''Calcular la curvatura media
$$''' + FORMULA_CURV_MEDIA + r'$$',
    r'''Calcular las curvaturas principales
$$''' + FORMULA_CURVS_PRINCIPALES + r'$$'
]

ALG_CURV_MEDIA = [
    r'''Calcular el vector normal
$$'''+FORMULA_VECTOR_NORMAL+r'$$',
    r'''Calcular la primera forma fundamental
$$''' + FORMULA_PFF + r'$$',
    r'''Calcular la segunda forma fundamental
$$''' + FORMULA_SFF + r'$$',
    r'''Calcular la curvatura media
$$''' + FORMULA_CURV_MEDIA + r'$$'
]

ALG_CURV_GAUSS = [
    r'''Calcular el vector normal
$$'''+FORMULA_VECTOR_NORMAL+r'$$',
    r'''Calcular la primera forma fundamental
$$''' + FORMULA_PFF + r'$$',
    r'''Calcular la segunda forma fundamental
$$''' + FORMULA_SFF + r'$$',
    r'''Calcular la curvatura de Gauss
$$''' + FORMULA_CURV_GAUSS + r'$$'
]

ALG_CLASIFICACION_PTO = [
    r'''Calcular el vector normal
$$'''+FORMULA_VECTOR_NORMAL+r'$$',
    
    r'''Calcular la primera forma fundamental
$$''' + FORMULA_PFF + r'$$',
    r'''Calcular la segunda forma fundamental
$$''' + FORMULA_SFF + r'$$',
    r'''Calcular la curvatura de Gauss
$$''' + FORMULA_CURV_GAUSS + r'$$',
    r'''Calcular la curvatura media
$$''' + FORMULA_CURV_MEDIA + r'$$',
    r'''Calcular las curvaturas principales
$$''' + FORMULA_CURVS_PRINCIPALES + r'$$',
    r'''Clasificar el punto $p=\varphi(u_0, v_0)$.
\begin{enumerate}
    \item Si $\kappa_1\kappa_2>0$ se dice que $p$ es un \textbf{punto elíptico}.
    \item Si $\kappa_1\kappa_2<0$ se dice que $p$ es un \textbf{punto hiperbólico}.
    \item Si $\kappa_1\kappa_2=0$ y $\kappa_1 \neq \kappa_2$ se dice que $p$ es un \textbf{punto parabólico}.
    \item Si $\kappa_1=\kappa_2=0$ se dice que $p$ es un \textbf{punto planar}.
\end{enumerate}'''
]

ALG_ANALISIS_COMPLETO = [
    r'''Calcular el vector normal
$$'''+FORMULA_VECTOR_NORMAL+r'$$',

    r'''Calcular el plano tangente
$$'''+FORMULA_PLANO_TANG+r'$$',

    r'''Calcular la primera forma fundamental
$$''' + FORMULA_PFF + r'''$$ 
donde
$$''' + FORMULA_COMP_PFF + r'$$',

    r'''Calcular la segunda forma fundamental
$$''' + FORMULA_SFF + r'''$$
donde
$$''' + FORMULA_COMP_SFF + r'$$',

    r'''Calcular la curvatura de Gauss
$$''' + FORMULA_CURV_GAUSS + r'$$',

    r'''Calcular la curvatura media
$$''' + FORMULA_CURV_MEDIA + r'$$',

    r'''Calcular la matriz de Weingarten
$$''' + FORMULA_WEINGARTEN + r'$$',

    r'''Calcular las curvaturas principales y las direcciones principales con la matriz de Weingarten. Sean $\kappa_1, \kappa_2$ los autovalores de la matriz de Weingarten y $\vec{v}=(\vec{v}_1, \vec{v}_2), \vec{w}=(\vec{w}_1, \vec{w}_2)$ sus autovectores, entonces las curvaturas principales son $\kappa_1, \kappa_2$ y las direcciones principales son
$$d_1 = \vec{v}_1\cdot\varphi_u + \vec{v}_2\cdot\varphi_v$$
$$d_2 = \vec{w}_1\cdot\varphi_u + \vec{w}_2\cdot\varphi_v$$''',

    r'''Calcular los puntos umbílicos, que cumplen
$$\kappa_1 = \kappa_2$$''',

    r'''Clasificar el punto $p=\varphi(u_0, v_0)$.
\begin{enumerate}
    \item Si $\kappa_1\kappa_2>0$ se dice que $p$ es un \textbf{punto elíptico}.
    \item Si $\kappa_1\kappa_2<0$ se dice que $p$ es un \textbf{punto hiperbólico}.
    \item Si $\kappa_1\kappa_2=0$ y $\kappa_1 \neq \kappa_2$ se dice que $p$ es un \textbf{punto parabólico}.
    \item Si $\kappa_1=\kappa_2=0$ se dice que $p$ es un \textbf{punto planar}.
\end{enumerate}'''
]


for paso, i in enumerate(ALG_ANALISIS_COMPLETO):
    print(f'Paso {paso+1}: {i}')