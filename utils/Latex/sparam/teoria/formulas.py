FORMULA_VECTOR_NORMAL = r"""\vec{n}=\frac{\vec{\varphi}_u \times \vec{\varphi}_v}{\|\vec{\varphi}_u \times \vec{\varphi}_v\|}"""
FORMULA_PLANO_TANG = r"""(\vec{\varphi}_u(p) \times \vec{\varphi}_v(p)) \cdot ((x, y, z)-\varphi(p)) = 0"""
FORMULA_COMP_PFF = r"""E=\vec{\varphi}_u \cdot \vec{\varphi}_u \qquad F=\vec{\varphi}_u \cdot \vec{\varphi}_v \qquad G=\vec{\varphi}_v \cdot \vec{\varphi}_v"""
FORMULA_PFF = r"""\left[I_p\right]=\left(\begin{matrix}E & F \\ F & G\end{matrix}\right) """
FORMULA_COMP_SFF = r"""e=\vec{n}\cdot \vec{\varphi}_{uu} \qquad f=\vec{n}\cdot \vec{\varphi}_{uv} \qquad g=\vec{n}\cdot \vec{\varphi}_{vv}"""
FORMULA_SFF = r"""\left[II_p\right]=\left(\begin{matrix}e & f \\ f & g\end{matrix}\right)"""
FORMULA_CURV_GAUSS = r"""\frac{eg-f^2}{EG-F^2}"""
FORMULA_CURV_MEDIA = r"""\frac{eG+gE-2fF}{2(EG-F^2)}"""
FORMULA_CURVS_PRINCIPALES = r"""\kappa_1, \kappa_2 = H \pm \sqrt{H^2-K}"""
FORMULA_WEINGARTEN = r"""\left[W_p\right] = \frac{1}{EG-F^2}\left(\begin{matrix}eG-fF & fG-gF \\ fG-gF & gE-fF\end{matrix}\right)"""



