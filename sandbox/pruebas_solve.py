import sympy as sp




def cartesian_a_uv(punto, sup):
    ecuaciones = [sp.Eq(s, p) for s, p in zip(sup, punto)]
    soluciones = sp.solve(ecuaciones, (u, v))
    return soluciones

def xyz_to_uv(parametrizacion, u, v, x0, y0, z0):
    punto = (x0, y0, z0)
    ecuaciones = [sp.Eq(s, p) for s, p in zip(parametrizacion, punto)]
    soluciones = sp.solve(ecuaciones, (u, v))
    if not soluciones:
        raise('El punto dado no esta en la superficie.')
    
    #TODO- devuelvo todas las soluciones o solo una?
    if isinstance(soluciones, dict):
        return soluciones[u] ,soluciones[v]
    else:
        return soluciones[0]

u, v = sp.symbols('u, v', real = True)
superficie_param = [sp.cos(u)*sp.cos(v), sp.cos(u)*sp.sin(v), sp.sin(u)]

u0, v0 =  xyz_to_uv([u,v,0],u,v,1,2,0)
print(u0, v0)
u0, v0 = xyz_to_uv(superficie_param,u,v,1,0,0)
print(u0, v0)
