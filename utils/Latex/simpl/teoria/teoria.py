TH_GRAFICAR = {
    'titulo' : r'Representación gráfica de una superficie implícita',
    'descripcion' : r'''La representación gráfica de superficies implícitas permite obtener una representación visual de cualquier superficie implícita y visualizar el vector normal y/o plano tangente en cualquier punto.''',
    'algoritmo': r''''''
}

TH_VEC_NORMAL = {
    'titulo' : r'Vector normal a una superficie implícita',
    'descripcion' : r'''El vetor normal a una superficie en el punto $p$ es el vector ortogonal a la superficie en ese punto.''',
    'algoritmo': r'''Sea $g:W \subset \mathbb{R}^3 \rightarrow \mathbb{R}$ una función suave con gradiente no nulo en todo punto. Entonces, un vector unitario normal, en cada punto, a la superficie de nivel $S=\{ (x,y,z) \in  \mathbb{R}^3 : g(x,y,z) = 0\}$ es
$$\vec{n} = \frac{\nabla g}{\|\nabla g\|} = \frac{(g_x, g_y, g_z)}{\sqrt{g_x^2+ g_y^2+ g_z^2}}$$'''
}

TH_PLANO_TANG = {
    'titulo' : r'Plano tangente a una superficie implícita',
    'descripcion' : r'''El plano tangente a una superficie en un punto $p$ es el plano que contiene todas las direcciones tangentes a la superficie en $p$.''',
    'algoritmo': r'''Sean $W \subset \mathbb{R}^3$,  $f:W \rightarrow \mathbb{R}$ una función suave con gradiente no nulo en todo punto, y $S=\{ (x,y,z) \in  \mathbb{R}^3 : g(x,y,z) = 0\}$ la superficie diferenciable asociada a $f$. Entonces, en cada punto $P=(x_0, y_0, z_0) \in S$  el plano afín tangente a $S$ en $P$ tiene por ecuación:
$$\nabla f(P)\left(\begin{matrix}x-x_0 \\ y-y_0 \\ z-z_0\end{matrix}\right) = 0$$
es decir,
$$f_x(P)(x-x_0) + f_y(P)(y-y_0) + f_z(P)(z-z_0)=0$$'''
}

TH_ANALISIS = {
    'titulo' : r'Análisis completo de una superficie implícita',
    'descripcion' : r'''El análisis incluye el cálculo del vector normal y del plano tangente''',
    'algoritmo': r''''''
}










