import sympy as sp

from .calc import *

SALTO_LINEA = r'\newline'
PHI_VARS = r'\vec{\varphi}(u,v)'
PHI_U = r'\vec{\varphi_u}'
PHI_V = r'\vec{\varphi_v}'
PHI_UU = r'\vec{\varphi_{uu}}'
PHI_UV = r'\vec{\varphi_{uv}}'
PHI_VV = r'\vec{\varphi_{vv}}'
PHI_U_X_PHI_V = PHI_U+r'\times'+PHI_V
NORM_PROD = r'\|'+PHI_U_X_PHI_V+r'\|'

FORM_NORMAL = r'\vec{n}=\frac{'+PHI_U_X_PHI_V+'}{'+NORM_PROD+'}'
FORM_E = 'E='+PHI_U+r'\cdot'+PHI_U
FORM_F = 'F='+PHI_U+r'\cdot'+PHI_V
FORM_G = 'G='+PHI_V+r'\cdot'+PHI_V
FORM_e = r'e='+PHI_U+r'\cdot W_p('+PHI_U+r')='+r'\vec{n} \cdot '+PHI_UU+r'=\frac{\text{det}('+PHI_U+r','+PHI_V+r','+PHI_UU+r')}{'+NORM_PROD+r'}'
FORM_f = r'f='+PHI_U+r'\cdot W_p('+PHI_V+r')='+r'\vec{n} \cdot '+PHI_UV+r'=\frac{\text{det}('+PHI_U+r','+PHI_V+r','+PHI_UV+r')}{'+NORM_PROD+r'}'
FORM_g = r'g='+PHI_V+r'\cdot W_p('+PHI_V+r')='+r'\vec{n} \cdot '+PHI_VV+r'=\frac{\text{det}('+PHI_U+r','+PHI_V+r','+PHI_VV+r')}{'+NORM_PROD+r'}'
FORM_TANG = r'('+PHI_U+r'(p)'+r'\times'+PHI_V+r'(p))\cdot ((x,y,z)-\varphi(p))=0'
FORM_CURV_GAUSS = r'K=det(\left[W_p \right])=\frac{eg-f^2}{EG-F^2}'
FORM_CURV_MEDIA = r'H=\frac{1}{2}traza(\left[W_p \right])=\frac{eG+gE-2fF}{2(EG-F^2)}'
FORM_WEINGARTEN =   r'\left[W_p\right]=\left[I_p\right]^{-1}\cdot\left[II_p\right]=\frac{1}{EG-F^2}\begin{pmatrix}eG-f F & fG-gF\\fE-eF & gE-fF\end{pmatrix}'
FORM_K1_K2 = r'k_1, k_2=H\pm\sqrt{H^2-K}'






def actualiza_variables(res):
    PHI_VARS = r'\vec{\varphi}('+str(res['u'])+','+str(res['u'])+r')'
    PHI_U = r'\vec{\varphi_{'+str(res['u'])+r'}}'
    PHI_V = r'\vec{\varphi_{'+str(res['v'])+r'}}'
    PHI_UU = r'\vec{\varphi_{'+str(res['u'])+str(res['u'])+r'}}'
    PHI_UV = r'\vec{\varphi_{'+str(res['u'])+str(res['v'])+r'}}'
    PHI_VV = r'\vec{\varphi_{'+str(res['v'])+str(res['v'])+r'}}'
    PHI_U_X_PHI_V = PHI_U+r'\times'+PHI_V
    NORM_PROD = r'\|'+PHI_U_X_PHI_V+r'\|'

    FORM_NORMAL = r'\vec{n}=\frac{'+PHI_U_X_PHI_V+'}{'+NORM_PROD+'}'
    FORM_E = 'E='+PHI_U+r'\cdot'+PHI_U
    FORM_F = 'F='+PHI_U+r'\cdot'+PHI_V
    FORM_G = 'G='+PHI_V+r'\cdot'+PHI_V
    FORM_e = r'e=\vec{n} \cdot '+PHI_UU
    FORM_f = r'f=\vec{n} \cdot '+PHI_UV
    FORM_g = r'g=\vec{n} \cdot '+PHI_VV
    FORM_TANG = r'('+PHI_U+r'(p)'+r'\times'+PHI_V+r'(p))\cdot ((x,y,z)-\varphi(p))=0'

def algoritmo_vector_normal() -> str:
    return r'Sea $(U, \varphi)$ una superficie regular y $p=(u_0, v_0)\in U$. Se llama \textbf{vector unitario normal} a la superficie en $p$ al vector:\\$$'+FORM_NORMAL+r'\\$$'

def algoritmo_vector_tangente() -> str:
    str_inic = r'Sea $(U, \varphi)$ una superficie regular y $T_p\varphi$ su plano tangente en el punto $p\in U$.'
    str_1 = r'Se llama \textbf{base del plano tangente asociada a la superficie regular} en $p$ a la base \\ $$B_{T{p}\varphi}=\lbrace'+PHI_U+r'(p), '+PHI_V+r'(p)\rbrace$$'
    str_2 = r'La ecuaci\'on cartesiana del \textbf{plano tangente} $T_p\varphi$ es:\\ $$('+PHI_U+r'(p)'+r'\times'+PHI_V+r'(p))\cdot (x,y,z)=0 $$'
    str3 = r'El \textbf{plano af\'in tangente} a la superficie en $p$ es:\\ $$\Pi_p\varphi=\varphi(p)+T_p\varphi$$ \\ Su ecuaci\'on cartesiana es: \\ $$'+FORM_TANG+r'$$'
    return str_inic + r'\\ ' + str_1 + r'\\ ' + str_2 + r'\\ ' + str3

def algoritmo_PFF() -> str:
    str_1 = r'Dada una superficie regular $(U, \varphi)$ y un punto $p\in U$, para cualesquiera $\vec{a}=a_1\vec{'+PHI_U+r'}+a_2\vec{'+PHI_V+r'}\in T{p}\varphi$ y $\vec{b}=b_1\vec{'+PHI_U+r'}+b_2\vec{'+PHI_V+r'}\in T{p}\varphi$ se cumple que:\\ '
    str_2 = r'$$I_p(\vec{a}, \vec{b})=\begin{pmatrix} a_1 & a_2 \end{pmatrix} \begin{pmatrix} E & F \\ F & G \end{pmatrix} \begin{pmatrix} b_1 \\ b_2 \end{pmatrix}$$ '
    str_3 = r'donde: \\ $$\begin{matrix} '+FORM_E+r' & & & & '+FORM_F+r' & & & & '+FORM_G+r' \end{matrix} $$ \\ '
    str_4 = r'reciben el nombre de \textbf{coeficientes de la primera forma fundamental}, mientras que la matriz:\\ '
    str_5 = r'$$\left[I_p\right]=\begin{pmatrix} E & F \\ F & G \end{pmatrix}$$ \\ '
    str_6 = r'se llama \textbf{expresi\'on matricial de la primera forma fundamental}.'
    return str_1 + str_2 + str_3 + str_4 + str_5 + str_6    

def algoritmo_SFF() -> str:
    str_1 = r'Dada una superficie regular $(U, \varphi)$ y un punto $p\in U$, para todos $\vec{a}=a_1\vec{'+PHI_U+r'}+a_2\vec{'+PHI_V+r'}\in T{p}\varphi$ y $\vec{b}=b_1\vec{'+PHI_U+r'}+b_2\vec{'+PHI_V+r'}\in T{p}\varphi$ se cumple que:\\ '
    str_2 = r'$$II_p(\vec{a}, \vec{b})=\begin{pmatrix} a_1 & a_2 \end{pmatrix} \begin{pmatrix} e & f \\ f & g \end{pmatrix} \begin{pmatrix} b_1 \\ b_2 \end{pmatrix}$$ \\ '
    str_3 = r'donde: \\ $$ '+FORM_e+r' $$ $$ '+FORM_f+r' $$ $$ '+FORM_g+r' $$ \\ '
    str_4 = r'reciben el nombre de \textbf{coeficientes de la segunda forma fundamental}, mientras que la matriz:\\ '
    str_5 = r'$$\left[II_p\right]=\begin{pmatrix} e & f \\ f & g \end{pmatrix}$$ \\ '
    str_6 = r'se llama \textbf{expresi\'on matricial de la segunda forma fundamental}.'
    return str_1 + str_2 + str_3 + str_4 + str_5 + str_6

def algoritmo_curv_Gauss() -> str:
    str_1 = r'Sea $(U, \varphi)$ una superficie orientada, $p\in U$ y $W_p:T_p\varphi \rightarrow T_p\varphi$ la aplicaci\'on de Weingarten de la superficie cuya matriz, en la base asociada a la parametrizaci\'on, es la matriz de Weingarten: \\ '
    str_2 = r'$$ \left[W\right]=\left[I\right]^{-1}\cdot\left[II\right]=\begin{pmatrix}E & F \\ F & G\end{pmatrix}^{-1} \begin{pmatrix}e & f \\ f & g\end{pmatrix} $$ '
    str_3 = r'Se llama \textbf{curvatura de Gauss} de la superficie en el punto $p$ al determinante de la matriz de Weingarten en dicho punto: \\ '
    str_4 = r'$$'+FORM_CURV_GAUSS+r'$$'
    return str_1+str_2+str_3+str_4

def algoritmo_curv_media() -> str:
    str_1 = r'Sea $(U, \varphi)$ una superficie orientada, $p\in U$ y $W_p:T_p\varphi \rightarrow T_p\varphi$ la aplicaci\'on de Weingarten de la superficie cuya matriz, en la base asociada a la parametrizaci\'on, es la matriz de Weingarten: \\ '
    str_2 = r'$$ \left[W\right]=\left[I\right]^{-1}\cdot\left[II\right]=\begin{pmatrix}E & F \\ F & G\end{pmatrix}^{-1} \begin{pmatrix}e & f \\ f & g\end{pmatrix} $$ '
    str_3 = r'Se llama \textbf{curvatura media} de la superficie en el punto $p$ a la traza de la matriz de Weingarten en dicho punto: \\ '
    str_4 = r'$$'+FORM_CURV_MEDIA+r'$$'
    return str_1+str_2+str_3+str_4

def algoritmo_Weingarten() -> str:
    str_1 = r'Sea $(U, \varphi)$ una superficie orientada. Se llama \textbf{aplicai\'on de Weingarten} de $(U, \varphi)$ en $p\in U$ al endomorfismo: \\ '
    str_2 = r'$$ W_p:T_p\varphi \rightarrow T_p\varphi \text{  que verifica:  }  \begin{cases} W_p(\vec{\varphi_u})=-\vec{n}_u \\ W_p(\vec{\varphi_v})=-\vec{n}_v \end{cases} $$'
    str_3 = r'Usando los valores de la primera y segunda forma fundamental se da que \\ '
    str_4 = r'$$' + FORM_WEINGARTEN + r'$$'
    return str_1+str_2+str_3+str_4

def algoritmo_curv_princ() -> str:
    str_1 = r'Sea $(U, \varphi)$ una superficie orientada y $p\in U$. Lo autovalores $k_1$ y $k_2$ de aplicaci\'on de la Weingarten se denominan \textbf{curvaturas principales}. \\ '
    str_2 = r'Usando la la curvatura de Gauss $K$ y la curvatura media $H$ en $p$, se cumple: \\ '
    str_3 = r'$$\begin{matrix} K=k_1k_2 & & & & H=\frac{k_1+k_2}{2} & & & & k_1, k_2=H\pm\sqrt{H^2-K} \end{matrix}$$ \\ '
    return str_1+str_2+str_3

def algoritmo_dir_princ() -> str:
    return r'Sea $(U, \varphi)$ una superficie orientada y $p\in U$. Lo autovectores de la aplicaci\'on de Weingarten se denominan \textbf{vectores principales}. \\ '




def todas_formulas():
    funcs = [algoritmo_vector_normal, algoritmo_vector_tangente, algoritmo_PFF, algoritmo_SFF, algoritmo_curv_Gauss, algoritmo_curv_media, 
            algoritmo_Weingarten, algoritmo_curv_princ, algoritmo_dir_princ]
    res = 'TEORIA'
    for func in funcs:
        res = res + '\n' + r'\\ FORMULA NUEVA \\' + '\n' +func()
    return res

def imprime_resultados(json):
    res = r'TEOR\'iA \\'
    for i, paso in enumerate(json):
        res = res + r'\textbf{Paso '+str(i)+r':} \\ ' + paso['descripcion'] + r' \\ ' + paso['pasoLatex'] + r' \\ '

    return res




def res_normal(res) -> dict:
    pasos = [
        {
            "descripcion" : r'Se va a calcular el vector normal de la superficie parametrizada $' + sp.latex(res['sup'], mat_delim='(') + r'$',
            "paso" : "",
            "pasoLatex" : ""
        },
        {
            "descripcion" : r'C\'alculo de la \textbf{derivada parcial de con respecto a ' + str(res['u']) + r'}: El vector $\vec{\varphi_'+str(res['u'])+r'}$ de la superficie es',
            "paso" : "",
            "pasoLatex" : r'$\varphi_{'+str(res['u'])+r'}='+sp.latex(res['du'], mat_delim='(')+r'$'
        },
        {
            "descripcion" : r'C\'alculo de la \textbf{derivada parcial de con respecto a ' + str(res['v']) + r'}: El vector $\vec{\varphi_'+str(res['v'])+r'}$ de la superficie es',
            "paso" : "",
            "pasoLatex" : r'$\varphi_{'+str(res['v'])+r'}='+sp.latex(res['dv'], mat_delim='(')+r'$'
        },
        {
            "descripcion" : r'C\'alculo del \textbf{producto vectorial de las derivadas parciales}: El vector producto vectorial de las derivadas parciales de la superficie es',
            "paso" : "",
            "pasoLatex" : r'$\varphi_'+str(res['u'])+r' \times'+r' \varphi_'+str(res['v'])+r'='+sp.latex(res['duXdv'], mat_delim='(')+r'$'
        },
        {
            "descripcion" : r'C\'alculo de la \textbf{norma del producto vectorial}: La norma del producto vectorial de las derivadas parciales de la superficie es',
            "paso" : "",
            "pasoLatex" : r'$\|\varphi_'+str(res['u'])+r' \times'+r' \varphi_'+str(res['v'])+r'\|='+sp.latex(res['norma'], mat_delim='(')+r'$'
        },
        {
            "descripcion" : r'C\'alculo del \textbf{vector normal}: El vector normal de la superficie en un punto genérico es',
            "paso" : "",
            "pasoLatex" : r'$\vec{n}='+sp.latex(res['normal'], mat_delim='(')+r'$'
        }
    ]

    return pasos