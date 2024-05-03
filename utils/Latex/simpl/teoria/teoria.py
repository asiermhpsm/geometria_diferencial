TH_VEC_NORMAL = r'''Sea $g:W \subset \mathbb{R}^3 \rightarrow \mathbb{R}$ una función suave con gradiente no nulo en todo punto. Entonces, un vector unitario normal, en cada punto, a la superficie de nivel
$$S=\Biggl\{ \left(\begin{matrix}x \\ y \\ z\end{matrix}\right) \in  \mathbb{R}^3 : g(x,y,z) = 0\Biggr\} \text{ es } \vec{n} = \frac{\nabla g}{\|\nabla g\|} = \frac{(g_x, g_y, g_z)}{\sqrt{g_x^2+ g_y^2+ g_z^2}}$$'''

TH_PLANO_TANG = r'''Sean $W \subset \mathbb{R}^3$,  $f:W \rightarrow \mathbb{R}$ una función suave con gradiente no nulo en todo punto, y 
$$S=\Biggl\{ \left(\begin{matrix}x \\ y \\ z\end{matrix}\right) \in  W : f(x,y,z) = 0\Biggr\}$$
la superficie diferenciable asociada a $f$. Entonces, en cada punto $P=(x_0, y_0, z_0) \in S$, un vector ortogonal al plano tangente a $S$ en $P$ es el vector gradiente
$$\nabla f(P) = (f_x(P), f_y(P), f_z(P))$$
el plano tangente a $S$ en $P$ tiene por ecuación:
$$\nabla f(P)\left(\begin{matrix}x \\ y \\ z\end{matrix}\right) = 0$$
es decir,
$$f_x(P)x + f_y(P)y + f_z(P)z=0$$
y el plano afín tangente a $S$ en $P$ tiene por ecuación:
$$\nabla f(P)\left(\begin{matrix}x-x_0 \\ y-y_0 \\ z-z_0\end{matrix}\right) = 0$$
es decir,
$$f_x(P)(x-x_0) + f_y(P)(y-y_0) + f_z(P)(z-z_0)=0$$'''