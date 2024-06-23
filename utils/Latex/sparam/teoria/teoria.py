from .formulas import *


TH_GRAFICAR = {
    'titulo' : r'Representación gráfica de una superficie implícita',
    'descripcion' : r'''La representación gráfica de superficies parametrizadas permite obtener una representación visual de cualquier superficie parametrizada y visualizar el vector normal, plano tangente, direcciones principales, curvaturas principales y/o direcciones asintóticas en cualquier punto.''',
    'algoritmo': r''''''
}

TH_VEC_NORMAL = {
    'titulo' : r'Vector normal a una superficie parametrizada',
    'descripcion' : r'''El vector normal a una superficie en el punto $p$ es el vector ortogonal a la superficie en ese punto.''',
    'algoritmo': r'''Sea $(U, \varphi)$ una superficie regular y $p=(u_0, v_0)\in U$. Se llama vector unitario normal a la superficie en $p$ al vector:
$$'''+FORMULA_VECTOR_NORMAL+r'''$$
La recto que pasa por $\varphi(p)$ con la dirección del vector unitario normal se denomina recta normal a la superficie en el punto $p$.'''
}

TH_PLANO_TANG = {
    'titulo' : r'Plano tangente a una superficie parametrizada',
    'descripcion' : r'''El plano tangente a una superficie en un punto $p$ es el plano que contiene todas las direcciones tangentes a la superficie en $p$.''',
    'algoritmo': r'''Sea $(u, \varphi)$ una superficie regular y $p=(u_0, v_0)\in U$. Entonces el conjunto $T_p\varphi$ de todos los vectores tangentes a la superficie en $\varphi(p)$junto con el vector cero es el subespacio vectorial de dimensión dos generado por los vectores $\{\vec{\varphi}_u, \vec{\varphi}_v\}$, evaluados ambos en $p$:
$$T_p\varphi = \mathcal{L}\{\vec{\varphi}_u, \vec{\varphi}_v\}$$
y que llamaremos \textbf{plano tangente} a la superficie en $p$.
La ecuación cartesiana del \textbf{plano tangente} $T_p\varphi$ es:
$$(\vec{\varphi}_u(p) \times \vec{\varphi}_v(p)) \cdot (x, y, z) = 0$$
El \textbf{plano afín tangente} a la superficie en $p$ es:
$$\Pi_{p}\varphi=\varphi(p) + T_p\varphi$$
Su ecuación cartesiana es:
$$'''+FORMULA_PLANO_TANG+r'$$'
}

TH_PFF = {
    'titulo' : r'Primera forma fundamental de una superficie parametrizada',
    'descripcion' : r'''La Primera Forma Fundamental es una aplicación que define un producto escalar, muy útil para calcular ángulos y longitudes.''',
    'algoritmo': r'''Dada la superficie regular $(U, \varphi)$, para cada $p\in U$ se define la \textbf{primera forma bilineal fundamental} como la aplicación
$$I_p:T_p\varphi \times T_p\varphi \longrightarrow \mathbb{R}$$
definida por
$$I_p(\vec{a},\vec{b})=\vec{a} \cdot \vec{b}$$
Para cualesquiera $\vec{a}=a_1\vec{\varphi}_u + a_2\vec{\varphi}_v \in T_p\varphi$ y $\vec{b}=b_1\vec{\varphi}_u + b_2\vec{\varphi}_v \in T_p\varphi$ se cumple que
$$I_p(\vec{a},\vec{b}) = \left(\begin{matrix}a_1 & a_2\end{matrix}\right) \left(\begin{matrix}E & F \\ F & G\end{matrix}\right) \left(\begin{matrix}b_1 \\ b_2\end{matrix}\right)$$
donde
$$''' + FORMULA_COMP_PFF + r'''$$
reciben el nombre de coeficientes de la primera forma fundamental, mientras que la matriz
$$''' + FORMULA_PFF + r'''$$
se llama expresión matricial de la primera forma fundamental.'''
}

TH_SFF = {
    'titulo' : r'Segunda forma fundamental de una superficie parametrizada',
    'descripcion' : r'''La Segunda Forma Fundamental es una herramienta que nos permite, entre otras cosas, medir cuánto se aleja una superficie de su plano tangente.''',
    'algoritmo': r'''Dada la superficie regular $(U, \varphi)$, para todo $p\in U$ se define la \textbf{segunda forma bilineal fundamental} como la aplicación
$$II_p:T_p\varphi \times T_p\varphi \longrightarrow \mathbb{R}$$
definida por
$$II_p(\vec{a},\vec{b})=\vec{a} \cdot W_p(\vec{b})$$
Para cualesquiera $\vec{a}=a_1\vec{\varphi}_u + a_2\vec{\varphi}_v \in T_p\varphi$ y $\vec{b}=b_1\vec{\varphi}_u + b_2\vec{\varphi}_v \in T_p\varphi$ se cumple que
$$II_p(\vec{a},\vec{b}) = \left(\begin{matrix}a_1 & a_2\end{matrix}\right) \left(\begin{matrix}e & f \\ f & g\end{matrix}\right) \left(\begin{matrix}b_1 \\ b_2\end{matrix}\right)$$
donde
$$''' + FORMULA_SFF + r'''$$

reciben el nombre de coeficientes de la segunda forma fundamental, mientras que la matriz
$$''' + FORMULA_COMP_SFF + r'''$$
se llama expresión matricial de la segunda forma fundamental.'''
}

TH_CURV_GAUSS = {
    'titulo' : r'Curvatura de Gauss de una superficie parametrizada',
    'descripcion' : r'''La curvatura de Gauss mide un promedio de cómo son las curvaturas en todas las direcciones de un punto de la superficie y sirve para estudiar el comportamiento local de la superficie.''',
    'algoritmo': r'''Dada la superficie regular $(U, \varphi)$, $p\in U$ y $W_p:T_p\varphi \longrightarrow T_p\varphi$ la aplicación de Weingarten de la superficie , se llama curvatura de Gauss de la superficie en el punto $p$ al determinante de la matriz de Weingarten en dicho punto
$$K(p)=\text{det}(\left[W_p\right])=\frac{eg-f^2}{EG-F^2}$$
Además, cumple que
$$K(p)=\kappa_1(p)\kappa_2(p)$$
donde $\kappa_1(p)$ y $\kappa_2(p)$ son las curvaturas principales de la superficie en $p$.'''
}

TH_CURV_MEDIA = {
    'titulo' : r'Curvatura media de una superficie parametrizada',
    'descripcion' : r'''La curvatura media mide el promedio de las curvaturas principales de un punto de la superficie y sirve para estudiar el comportamiento local de la superficie.''',
    'algoritmo': r'''Dada la superficie regular $(U, \varphi)$, $p\in U$ y $W_p:T_p\varphi \longrightarrow T_p\varphi$ la aplicación de Weingarten, se llama curvatura media de la superficie en el punto $p$ a la traza de la matriz de Weingarten en dicho punto
$$H(p)=\frac{1}{2}\text{traza}(\left[W_p\right])=\frac{eG+gE-2fF}{2(EG-F^2)}$$
Además, cumple que
$$H(p)=\frac{\kappa_1(p)+\kappa_2(p)}{2}$$
donde $\kappa_1(p)$ y $\kappa_2(p)$ son las curvaturas principales de la superficie en $p$.'''
}

TH_CURVS_PRINCIPALES = {
    'titulo' : r'Curvaturas principales de una superficie parametrizada',
    'descripcion' : r'''Las curvaturas principales son los autovectores de la matriz de Weingarten, que coinciden con las curvaturas normales máxima y mínima de la superficie en el punto $p$.''',
    'algoritmo': r'''Las curvaturas principales son los autovectores de la matriz de Weingarten. Sin embargo, también se pueden calcular mediante las siguientes fórmulas:
    $$'''+FORMULA_CURVS_PRINCIPALES+r'''$$
    donde $H$ y $K$ son la curvatura media y de Gauss de la superficie en el punto $p$.'''
}

TH_DIRS_PRINCIPALES = {
    'titulo' : r'Direcciones principales de una superficie parametrizada',
    'descripcion' : r'''Las direcciones principales son los autovectores de la matriz de Weingarten, que coinciden con las direcciones en las que las curvaturas normales de la superficie en p son máximas y mínimas (curvaturas principales)''',
}

TH_WEINGARTEN = {
    'titulo' : r'Aplicación de Weingarten de una superficie parametrizada',
    'descripcion' : r'''La aplicación de Weingarten es una herramienta que permite estudiar el comportamiento de las superficies además de definir y calcular otros elementos de la superficie.''',
    'algoritmo': r'''Sea $(U, \varphi)$ una superficie orientada. Se llama aplicación de Weingarten de $(U, \varphi)$ en $p \in U$ el endomorfismo W_p : T_p\varphi \longrightarrow T_p\varphi que verifica
$$ \left\{W_p(\vec{\varphi}_u) = -\vec{n}_u \atop W_p(\vec{\varphi}_v) = -\vec{n}_v\right.$$
La matriz del endomorfismo de Weingarten $W_p$ en la base asociada del plano tangente $B_{T_p\varphi} = \{\vec{\varphi}_u, \vec{\varphi}_v\}$, llamada matriz de Weingarten, es
$$\left[W_p\right] = \left[I_p\right]^{-1}\left[II_p\right]=\frac{1}{EG-F^2}\left(\begin{matrix}eG-fF & fG-gF \\ fG-gF & gE-fF\end{matrix}\right)$$'''
}

TH_PTS_UMBILICOS = {
    'titulo' : r'Puntos umbílicos de una superficie parametrizada',
    'descripcion' : r'''Los puntos umbílicos son aquellos puntos de la superficie en los que las curvaturas principales coinciden, y definen punto de la superficie en los que, sin importar la dirección que se tome, la curvatura será simepre la misma.''',
    'algoritmo': r'''Sean $(U, \varphi)$ una superficie orientada y $p\in U$, se dice que $p$ es un punto umbílico si cumple que
    $$\kappa_1(p)=\kappa_2(p)$$'''

}

TH_CLASIFICACION_PTOS = {
    'titulo' : r'Clasificación de un punto de una superficie parametrizada',
    'descripcion' : r'''Los puntos de una superficie se pueden clasificar en cuatro tipos para conocer la forma local de la superficie.''',
    'algoritmo': r'''Sea $(U, \varphi)$ una superficie orientada, $p\in U$ y $\kappa_1, \kappa_2 \in \mathbb{R}$ las cruvaturas principales de la superficie en $p$, entonces:
    Si $\kappa_1\kappa_2>0$ se dice que $p$ es un punto elíptico.
    Si $\kappa_1\kappa_2<0$ se dice que $p$ es un punto hiperbólico.
    Si $\kappa_1\kappa_2=0$ y $\kappa_1 \neq \kappa_2$ se dice que $p$ es un punto parabólico.
    Si $\kappa_1=\kappa_2=0$ se dice que $p$ es un punto planar.
'''
}

TH_DIRS_ASINTOTICAS = {
    'titulo' : r'Direcciones asintóticas de una superficie parametrizada',
    'descripcion' : r'''Las direcciones asintóticas marcan la dirección que toman las curvas contenidas en la superficie que pasan por el punto p y que tienen curvatura nula en p''',
    'algoritmo': r'''Dada una superficie regular $S=(U, \varphi)$ y un punto $p$ de $S$, una dirección $\vec{w}=(x, y)$ se denomina \textbf{asintótica} si la curva contenida en $S$ que pasa por $p$ y tiene dirección $w$ tiene curvatura $0$; o lo que es lo mismo si
$$II_p(\vec{w}, \vec{w}) = \left(\begin{matrix}x & y\end{matrix}\right) \left(\begin{matrix}e & f \\ f & g\end{matrix}\right) \left(\begin{matrix}x \\ y\end{matrix}\right)=0$$
Si se analiza la ecuación anterior, se reducen a los siguientes casos secuenciales:

Si $e = f = g = 0$, entonces el punto el planar y todas las direcciones son asintótica
Si $e = 0, g \neq 0$, entonces las coordenadas de las direcciones con respeto a a base $\{\varphi_u, \varphi_v\}$ son 
$$\{(1, 0),(-g, 2f)\}$$
Si $e \neq 0, g = 0$, entonces las coordenadas de las direcciones con respeto a a base $\{\varphi_u, \varphi_v\}$ son 
$$\{(0, 1),(-2f, e)\}$$
Si $f^2 - ge < 0$, entonces estamos ante un punto elíptico y por lo tanto no hay direcciones asintóticas
En el resto de casos, las coordenadas de las direcciones con respeto a la base $\{\varphi_u, \varphi_v\}$ son 
$$\{(g, -f + \sqrt{f^2 - ge}), (g, -f - \sqrt{f^2 - ge})\}$$'''
}

TH_ANALISIS = {
    'titulo' : r'Análisis completo de una superficie parametrizada',
    'descripcion' : r'''El análisis incluye el cálculo de todos los elementos posibles.''',
    'algoritmo': r''''''
}







