from .formulas import *


TH_VEC_NORMAL = r'''Sea $(U, \varphi)$ una superficie regular y $p=(u_0, v_0)\in U$. Se llama \textbf{vector unitario normal} a la superficie en $p$ al vector:
$$'''+FORMULA_VECTOR_NORMAL+r'''$$
La recto que pasa por $\varphi(p)$ con la dirección del vector unitario normal se denomina \textbf{recta normal} a la superficie en el punto $p$.'''

TH_PLANO_TANG = r'''Sea $(u, \varphi)$ una superficie regular y $p=(u_0, v_0)\in U$. Entonces el conjunto $T_p\varphi$ de todos los vectores tangentes a la superficie en $\varphi(p)$junto con el vector cero es el subespacio vectorial de dimensión dos generado por los vectores $\{\vec{\varphi}_u, \vec{\varphi}_v\}$, evaluados ambos en $p$:
$$T_p\varphi = \mathcal{L}\{\vec{\varphi}_u, \vec{\varphi}_v\}$$
y que llamaremos \textbf{plano tangente} a la superficie en $p$.
La ecuación cartesiana del \textbf{plano tangente} $T_p\varphi$ es:
$$(\vec{\varphi}_u(p) \times \vec{\varphi}_v(p)) \cdot (x, y, z) = 0$$
El \textbf{plano afín tangente} a la superficie en $p$ es:
$$\Pi_{p}\varphi=\varphi(p) + T_p\varphi$$
Su ecuación cartesiana es:
$$'''+FORMULA_PLANO_TANG+r'$$'

TH_PFF = r'''Dada la superficie regular $(U, \varphi)$, para cada $p\in U$ se define la \textbf{primera forma bilineal fundamental} como la aplicación
$$I_p:T_p\varphi \times T_p\varphi \longrightarrow \mathbb{R}$$
definida por
$$I_p(\vec{a},\vec{b})=\vec{a} \cdot \vec{b} \text{,  para todo  } \vec{a},\vec{b} \in T_p\varphi$$
Para cualesquiera $\vec{a}=a_1\vec{\varphi}_u + a_2\vec{\varphi}_v \in T_p\varphi$ y $\vec{b}=b_1\vec{\varphi}_u + b_2\vec{\varphi}_v \in T_p\varphi$ se cumple que
$$I_p(\vec{a},\vec{b}) = \left(\begin{matrix}a_1 & a_2\end{matrix}\right) \left(\begin{matrix}E & F \\ F & G\end{matrix}\right) \left(\begin{matrix}b_1 \\ b_2\end{matrix}\right)$$
donde
$$''' + FORMULA_COMP_PFF + r'''$$
reciben el nombre de \textbf{coeficientes de la primera forma fundamental}, mientras que la matriz
$$''' + FORMULA_PFF + r'''$$
se llama \textbf{expresión matricial de la primera forma fundamental}.'''

TH_SFF = r'''Dada la superficie regular $(U, \varphi)$, para todo $p\in U$ se define la \textbf{segunda forma bilineal fundamental} como la aplicación
$$II_p:T_p\varphi \times T_p\varphi \longrightarrow \mathbb{R}$$
definida por
$$II_p(\vec{a},\vec{b})=\vec{a} \cdot W_p(\vec{b}) \text{,  para todo  } \vec{a},\vec{b} \in T_p\varphi$$
Para cualesquiera $\vec{a}=a_1\vec{\varphi}_u + a_2\vec{\varphi}_v \in T_p\varphi$ y $\vec{b}=b_1\vec{\varphi}_u + b_2\vec{\varphi}_v \in T_p\varphi$ se cumple que
$$II_p(\vec{a},\vec{b}) = \left(\begin{matrix}a_1 & a_2\end{matrix}\right) \left(\begin{matrix}e & f \\ f & g\end{matrix}\right) \left(\begin{matrix}b_1 \\ b_2\end{matrix}\right)$$
donde
$$''' + FORMULA_SFF + r'''$$

reciben el nombre de \textbf{coeficientes de la segunda forma fundamental}, mientras que la matriz
$$''' + FORMULA_COMP_SFF + r'''$$
se llama \textbf{expresión matricial de la segunda forma fundamental}.'''

TH_CURV_GAUSS = r'''Dada la superficie regular $(U, \varphi)$, $p\in U$ y $W_p:T_p\varphi \longrightarrow T_p\varphi$ la aplicación de Weingarten de la superficie cuya matriz, en la base asociada a la parametrización, es la matriz de Weingarten
$$\left[W_p\right] = \left[I_p\right]^{-1}\left[II_p\right]=\left(\begin{matrix}E & F \\ F & G\end{matrix}\right)^{-1}\left(\begin{matrix}e & f \\ f & g\end{matrix}\right)$$
Se llama \textbf{curvatura de Gauss} de la superficie en el punto $p$ al determinante de la matriz de Weingarten en dicho punto
$$K(p)=\text{det}(\left[W_p\right])=\frac{eg-f^2}{EG-F^2}$$'''

TH_CURV_MEDIA = r'''Dada la superficie regular $(U, \varphi)$, $p\in U$ y $W_p:T_p\varphi \longrightarrow T_p\varphi$ la aplicación de Weingarten de la superficie cuya matriz, en la base asociada a la parametrización, es la matriz de Weingarten
$$\left[W_p\right] = \left[I_p\right]^{-1}\left[II_p\right]=\left(\begin{matrix}E & F \\ F & G\end{matrix}\right)^{-1}\left(\begin{matrix}e & f \\ f & g\end{matrix}\right)$$
Se llama \textbf{curvatura media} de la superficie en el punto $p$ a la traza de la matriz de Weingarten en dicho punto
$$H(p)=\frac{1}{2}\text{traza}(\left[W_p\right])=\frac{eG+gE-2fF}{2(EG-F^2)}$$'''

TH_CURVS_PRINCIPALES = r'''Sean $(U, \varphi)$ una superficie orientada y $p\in U$, los autovalores $\kappa_1$ y $\kappa_2$ de la aplicación de Weingarten se denominan \textbf{curvaturas principales}. \\
Geométricamente, las curvaturas principales son los valores máximo y mínimo que la curvatura normal puede alcanzar en cualquier punto de la superficie, es decir
$$\kappa_1 \leq \kappa_n(\vec{\omega}) \leq \kappa_2 \text{, para todo } \omega \in T_p\varphi$$'''

TH_DIRS_PRINCIPALES = r'''Sean $(U, \varphi)$ una superficie orientada y $p\in U$, los autovalores de la aplicación de Weingarten de denominan \textbf{vectores o direcciones principales}.\\
Geométricamente, las curvaturas principales son los valores máximo y mínimo que la curvatura normal puede alcanzar en cualquier punto de la superficie y esos valores se alcanzan en la dirección de los vectores principales.'''

TH_WEINGARTEN = r'''Sea $(U, \varphi)$ una superficie orientada. Se llama \textbf{aplicación de Weingarten} de $(U, \varphi)$ en $p \in U$ el endomorfismo
$$W_p : T_p\varphi \longrightarrow T_p\varphi$$
que verifica
$$ \left\{W_p(\vec{\varphi}_u) = -\vec{n}_u \atop W_p(\vec{\varphi}_v) = -\vec{n}_v\right.$$
La matriz del endomorfismo de Weingarten $W_p$ en la base asociada del plano tangente $B_{T_p\varphi} = \{\vec{\varphi}_u, \vec{\varphi}_v\}$, llamada \textbf{matriz de Weingarten}, es
$$\left[W_p\right] = \left[I_p\right]^{-1}\left[II_p\right]=\left(\begin{matrix}E & F \\ F & G\end{matrix}\right)^{-1}\left(\begin{matrix}e & f \\ f & g\end{matrix}\right)=\frac{1}{EG-F^2}\left(\begin{matrix}eG-fF & fG-gF \\ fG-gF & gE-fF\end{matrix}\right)$$'''

TH_PTS_UMBILICOS = r'''Sean $(U, \varphi)$ una superficie orientada y $p\in U$, cuando los autovalores coinciden ($\kappa_1=\kappa_2$), se dice que $p$ es un \textbf{punto umbílico} de la superficie. Notese que cuando $\kappa_1=\kappa_2=\kappa$, la aplicación de Weingarten verifica que
$$W_p(\vec{\omega})=\kappa\vec{\omega} \text{, para todo } \vec{\omega} \in T_p\varphi$$
En consecuencia, un punto es umbílico si y sólo si la aplicación de Weingarten es un múltiplo escalar de la identidad, y en ese caso todo vector no nulo del plano tangente es una vector principal.'''

TH_CLASIFICACION_PTOS = r'''Sea $(U, \varphi)$ una superficie orientada, $p\in U$ y $\kappa_1, \kappa_2 \in \mathbb{R}$ las cruvaturas principales de la superficie en $p$, entonces
\begin{enumerate}
    \item Si $\kappa_1\kappa_2>0$ se dice que $p$ es un \textbf{punto elíptico}.
    \item Si $\kappa_1\kappa_2<0$ se dice que $p$ es un \textbf{punto hiperbólico}.
    \item Si $\kappa_1\kappa_2=0$ y $\kappa_1 \neq \kappa_2$ se dice que $p$ es un \textbf{punto parabólico}.
    \item Si $\kappa_1=\kappa_2=0$ se dice que $p$ es un \textbf{punto planar}.
\end{enumerate}'''

TH_ANALISIS = r'''La forma y el comportamiento de una superficie diferenciable y orientada se puede mediante varias de sus características, entre las que destacan, su vector nomal, su primera y segunda forma fundamental, su cruvatura de Gauss y media o sus curvaturas y direcciones principales. Todas estas características nos ayudan a conocer localmente el comportamiento de una superficie.'''

