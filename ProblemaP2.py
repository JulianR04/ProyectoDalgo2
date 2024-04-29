from queue import Queue
import sys
import time
import heapq


## Para poder ejecutar el codigo usar el comando python ProblemP2.py P0.in P0.out sin necesidad de los <>


class Vertice:
    def __init__(self, masa, carga):
        self.masa = masa
        self.carga = carga
        self.pareja = None
        self.tipo = "libre"
    
    def add_pareja(self, vertice):
        self.pareja = vertice
        self.tipo = "fundamental"
        
    def es_opuesto(self, vertice):
        return self.masa == vertice.masa and self.carga != vertice.carga  

    def __repr__(self):
        self.tipo = "fundamental" if self.pareja is not None else "libre" 
        return f"Vertice(masa={self.masa}, carga={self.carga}), tipo={self.tipo}"

    def __eq__(self, other):
        if not isinstance(other, Vertice) or (self.pareja is None and other.pareja is not None) or (self.pareja is not None and other.pareja is None):
            return False
        
        elif self.pareja is None and other.pareja is None:
            return self.masa == other.masa and self.carga == other.carga
        
        else:
            return self.masa == other.masa and self.carga == other.carga \
                and self.pareja.masa == other.pareja.masa and self.pareja.carga == other.pareja.carga

    def __hash__(self):
        return hash((self.masa, self.carga))
    
class Conexion:
    def __init__(self, origen, destino, costo):
        self.origen = origen
        self.destino = destino
        self.costo=costo
        self.tipo = ""
    def get_costo (self, vertice1, vertice2):
        if (vertice1 == self.origen or vertice1 == self.destino) and (vertice2 == self.origen or vertice2 == self.destino):
            return self.costo

    def __repr__(self):
        return f"Conexion(origen={self.origen}, destino={self.destino}, costo={self.costo})"  
    
class Grafo:
    def __init__(self):
        self.vertices = []
        self.conexiones = []
        self.matriz_ady=[]
        self.diccionario_indices = {}
    def add_conexion(self, conexion):
        self.conexiones.append(conexion)
        if conexion.origen not in self.vertices:
            self.vertices.append(conexion.origen)
        if conexion.destino not in self.vertices:
            self.vertices.append(conexion.destino)          

    def add_vertice(self,vertice):
        self.vertices.append(vertice)          
    

    def crear_matriz_ady(self):
        n = len(self.vertices)
        self.matriz_ady = [[0] * n for _ in range(n)]
        self.diccionario_indices = {vertice: index for index, vertice in enumerate(self.vertices)}

        for conexion in self.conexiones:
            v1 = self.diccionario_indices[conexion.origen]
            v2 = self.diccionario_indices[conexion.destino]

            if self.matriz_ady[v1][v2] == 0: 
                self.matriz_ady[v1][v2] = conexion.costo
            if self.matriz_ady[v2][v1] == 0:  
                self.matriz_ady[v2][v1] = conexion.costo

        return self.matriz_ady, self.diccionario_indices

    def determinar_si_se_puede_y_grafo_euleriano(self):
        conteo  = {}
        grafo_euleriano = {}
        for conexion in self.conexiones:
            origen = str(conexion.origen.carga) + str(conexion.origen.masa)
            destino = str(conexion.destino.carga)+ str(conexion.destino.masa)

            if  origen not in conteo.keys():
                conteo[origen] = 1
                grafo_euleriano[origen] = [destino]

            else:
                conteo[origen] +=1
                grafo_euleriano[origen].append(destino)

            if destino not in conteo.keys():
                conteo[destino] = 1
                grafo_euleriano[destino] = [origen]

            else:
                conteo[destino] +=1
                grafo_euleriano[destino].append(origen)

        source = None
        impares = 0
        mayor_grado_impar = 0
        for key, val in conteo.items():
            if val % 2 != 0:
                impares +=1
                if val > mayor_grado_impar:
                    mayor_grado_impar = val
                    source = key

        if impares > 2: 
            return False, None, None 
        return True, grafo_euleriano, source  

    def es_alcanzable_BFS(self, origen, destino, grafo_euleriano):
        if len(grafo_euleriano[origen]) > 0:
            visitados = set()
            visitados.add(origen)
            cola = Queue()
            cola.put(origen)
            while not cola.empty():
                actual = cola.get()
                if actual == destino:
                    return True
                for vecino in grafo_euleriano[actual]:
                    if vecino not in visitados:
                        visitados.add(vecino)
                        cola.put(vecino)
        else:
            return True

    def encontrar_camino_euleriano(self, inicio, numero_elementos, grafo_euleriano):
        camino = []
        actual = inicio
        for _ in range(numero_elementos):
            vecinos = grafo_euleriano[actual].copy()
            for siguiente in vecinos:
                grafo_euleriano[actual].remove(siguiente)
                grafo_euleriano[siguiente].remove(actual)
                if self.es_alcanzable_BFS(actual,siguiente,grafo_euleriano):
                    camino.append((actual,siguiente))
                    actual = siguiente
                    break
                else: 
                    grafo_euleriano[actual].append(siguiente)
                    grafo_euleriano[siguiente].append(actual)   
        return camino


    def dijkstra(self, nodo_inicio, nodo_destino):
        distancias = [float('inf')] * len(self.vertices)
        distancias[nodo_inicio] = 0
        visitados = [False] * len(self.vertices)
        caminos = [[] for _ in range(len(self.vertices))]
        
        heap = []
        heapq.heappush(heap, (0, nodo_inicio))
        
        while heap:
            min_distancia, min_vertice = heapq.heappop(heap)
            visitados[min_vertice] = True
            
            if min_vertice == nodo_destino:
                break
            
            for v in range(len(self.vertices)):
                if not visitados[v] and self.matriz_ady[min_vertice][v] != 0:
                    nueva_distancia = min_distancia + self.matriz_ady[min_vertice][v]
                    if nueva_distancia < distancias[v]:
                        distancias[v] = nueva_distancia
                        caminos[v] = caminos[min_vertice] + [min_vertice]
                        heapq.heappush(heap, (nueva_distancia, v))

        return distancias, caminos
     
    def vertices_fundamentales_repetidos(self):
        cuenta_masa_carga = {}
        vertices_unicos = {}

        for vertice in self.vertices:
            if vertice.tipo == "fundamental": 
                clave = (vertice.masa, vertice.carga)
                if clave in cuenta_masa_carga:
                    cuenta_masa_carga[clave] += 1
                    if clave not in vertices_unicos:
                        vertices_unicos[clave] = vertice
                else:
                    cuenta_masa_carga[clave] = 1
                    vertices_unicos[clave] = vertice

        vertices_repetidos = []
        for clave, cantidad in cuenta_masa_carga.items():
            if cantidad > 1:  
                vertices_repetidos.append(vertices_unicos[clave])

        return vertices_repetidos

    def encontrar_opuesto_libre(self, vertice):
        carga_opuesta = "-" if vertice.carga == "+" else "+"
        for candidato in self.vertices:
            if candidato.masa == vertice.masa and candidato.carga == carga_opuesta and candidato.tipo == "libre":
                return candidato
        return None

    
    def dijkstra_para_fundamentales_repetidos(self):
        vertices_repetidos = self.vertices_fundamentales_repetidos()
        resultados_dijkstra = {}
        costo_final = 0

        for vertice in vertices_repetidos:
            nodo_inicio = self.diccionario_indices[vertice]
            vertice_opuesto = self.encontrar_opuesto_libre(vertice)

            if vertice_opuesto is not None:
                nodo_destino = self.diccionario_indices[vertice_opuesto]
                distancias, caminos = self.dijkstra(nodo_inicio, nodo_destino)
                costo_final+= distancias[nodo_destino]

                camino = caminos[nodo_destino]
                camino_formateado = [f"{self.vertices[n].carga}{self.vertices[n].masa}" for n in camino] + [f"{vertice_opuesto.carga}{vertice_opuesto.masa}"]

                camino_formateado = camino_formateado[1:]  
                clave = f"{vertice.carga}{vertice.masa}"
                resultados_dijkstra[clave] = camino_formateado

        return resultados_dijkstra, costo_final

    def generar_camino_conectado(self, camino_euleriano, dijkstra_paths):
        camino_mapa = {}

        
        for i in range(len(camino_euleriano) - 1):
            ele_fund = camino_euleriano[i]
            vertice_inicio = ele_fund[0]
            vertice_final = ele_fund[1]

            tupla_segmento = (vertice_inicio, vertice_final)

            if vertice_final in dijkstra_paths:
                camino_con_dijkstra = dijkstra_paths[vertice_final]
                camino_mapa[tupla_segmento] = camino_con_dijkstra
        ultimo_segmento = camino_euleriano[-1]
        clave_ultimo_segmento = (ultimo_segmento[0], ultimo_segmento[1])
        camino_mapa[clave_ultimo_segmento] = None

        return camino_mapa

    def formatear_camino_final(self, camino_mapa, costo_total):
        resultado = []

        def formato_vertice(vertice_str):
            if vertice_str[0] == '+':
                return vertice_str[1:] 
            return vertice_str  

        for (vertice_inicio, vertice_final), camino_intermedio in camino_mapa.items():
            inicio_formato = formato_vertice(vertice_inicio)
            final_formato = formato_vertice(vertice_final)
            elemento_fundamental = f"({inicio_formato},{final_formato})"
            resultado.append(elemento_fundamental)

            if camino_intermedio is not None:
                intermedios = ",".join([formato_vertice(v) for v in camino_intermedio])
                resultado.append(intermedios)
        resultado_final = ",".join(resultado) + f" {costo_total}"
        return resultado_final


    
    def __repr__(self):
        return f"Vertices: \n" + "\n".join([str(vertice) for vertice in self.vertices]) + "\n" \
                + "Conexiones: \n" + "\n".join([str(conexion) for conexion in self.conexiones]) + "\n"


class Caso:
    def __init__(self, case_id, n, w1, w2, lineas, output_file):
        self.case_id = case_id
        self.n = n
        self.w1 = w1
        self.w2 = w2
        self.lineas = lineas
        self.output_file = output_file
        
        self.grafo, self.vertices_fundamentales, self.num_elementos_fund = self.cargar_grafo(lineas) #1
        rpsta, grafo_euleriano, source_eulerian = self.grafo.determinar_si_se_puede_y_grafo_euleriano() #2

        if rpsta == False:
            self.escribir_resultado("NO SE PUEDE", output_file)
        else:

            camino_euleriano = self.grafo.encontrar_camino_euleriano(source_eulerian, self.num_elementos_fund, grafo_euleriano)

            self.grafo, self.vertices_libres = self.grafo_vertices_libres(self.grafo)
                        
            self.grafo_completo = self.crear_grafo_completo(self.grafo)
            self.matriz_grafo, self.diccionario_indices = self.grafo_completo.crear_matriz_ady()  
            caminos_fundamentales, costo = self.grafo_completo.dijkstra_para_fundamentales_repetidos()
            
            camino_final = self.grafo_completo.generar_camino_conectado(camino_euleriano, caminos_fundamentales)
            resultado_final = self.grafo_completo.formatear_camino_final( camino_final, costo)
            self.escribir_resultado(resultado_final, output_file)
            
            
    def calcular_costo(self, vertice1, vertice2):
        return (1 + abs(vertice1.masa-vertice2.masa) % self.w1) if (vertice1.carga == vertice2.carga) else (self.w2 - abs(vertice1.masa-vertice2.masa) % self.w2)
    
    def cargar_grafo(self, lineas):
        index = 0
        cant_casos = self.n
        vertices_fundamentales = []
        grafo = Grafo()
        for _ in range(cant_casos):
            origen, destino = map(int, lineas[index].split())
            
            masa_origen = abs(origen)
            carga_origen = "-" if origen < 0 else "+"
            origen = Vertice(masa_origen,carga_origen)
            masa_destino = abs(destino)
            carga_destino = "-" if destino < 0 else "+"
            destino = Vertice(masa_destino,carga_destino)
            
            origen.add_pareja(destino)
            destino.add_pareja(origen)
            vertices_fundamentales.append(origen)
            vertices_fundamentales.append(destino)
                    
            costo =  sys.maxsize
            conexion = Conexion(origen, destino,costo)
            grafo.add_conexion(conexion)
            index += 1
        num_elementos_fund = index
        return grafo, vertices_fundamentales, num_elementos_fund

    def grafo_vertices_libres(self, grafo):
            original_vertices = set(grafo.vertices)
            vertices_libres = []
            for vertice in original_vertices:
                carga_opuesta = "-" if vertice.carga == "+" else  "+"
                vertice_opuesto = Vertice(vertice.masa, carga_opuesta)
                if vertice_opuesto not in original_vertices and vertice_opuesto not in grafo.vertices:
                    grafo.add_vertice(vertice_opuesto)
                    vertices_libres.append(vertice_opuesto)
                
                vertice_real_libre = Vertice(vertice.masa, vertice.carga)
                if vertice_real_libre not in original_vertices and vertice_real_libre not in grafo.vertices:
                    grafo.add_vertice(vertice_real_libre)
                    vertices_libres.append(vertice_real_libre)
                
                
            return grafo, vertices_libres
    
    
    def crear_grafo_completo(self, grafo):
        vertices_por_masa = {}
        for vertice in self.vertices_fundamentales + self.vertices_libres:
            if vertice.masa not in vertices_por_masa:
                vertices_por_masa[vertice.masa] = []
            vertices_por_masa[vertice.masa].append(vertice)

        conexiones_existentes = set((conexion.origen, conexion.destino) for conexion in grafo.conexiones)
        conexiones_existentes.update((conexion.destino, conexion.origen) for conexion in grafo.conexiones)

        for v_fund in self.vertices_fundamentales:
            for masa, vertices in vertices_por_masa.items():
                if masa != v_fund.masa:
                    for v_libre in vertices:
                        if (v_fund, v_libre) not in conexiones_existentes:
                            costo = self.calcular_costo(v_fund, v_libre)
                            conexion = Conexion(v_fund, v_libre, costo)
                            grafo.add_conexion(conexion)
                            conexiones_existentes.add((v_fund, v_libre))
                            conexiones_existentes.add((v_libre, v_fund))

        for masa, vertices in vertices_por_masa.items():
            for i in range(len(vertices)):
                for j in range(i + 1, len(vertices)):
                    if vertices[i].masa != vertices[j].masa:
                        if (vertices[i], vertices[j]) not in conexiones_existentes:
                            costo = self.calcular_costo(vertices[i], vertices[j])
                            conexion = Conexion(vertices[i], vertices[j], costo)
                            grafo.add_conexion(conexion)
                            conexiones_existentes.add((vertices[i], vertices[j]))
                            conexiones_existentes.add((vertices[j], vertices[i]))

        return grafo


    
    def escribir_camino_minimo(self, distancias, output_file):
        with open(output_file, 'a') as f:
            f.write(f"Case {self.case_id}: {distancias}\n")
        
    
    def escribir_resultado(self, result, output_file):
        with open(output_file, 'a') as f:
            f.write(f"Case {self.case_id}: {result}\n")

        
def respuesta_dijkstra(grafo, distancias, caminos):
    for i, distancia in enumerate(distancias):
        if i < len(grafo.vertices):
            vertice_info = (f"Nodo {i} (masa={grafo.vertices[i].masa}, "
                            f"carga={grafo.vertices[i].carga}, "
                            f"tipo={grafo.vertices[i].tipo}): {distancia}")
        else:
            vertice_info = f"Nodo {i}: {distancia}"
        print(vertice_info)

    for i, camino in enumerate(caminos):
        camino_descripcion = [f"nodo {j} (masa={grafo.vertices[j].masa}, "
                              f"carga={grafo.vertices[j].carga}, "
                              f"tipo={grafo.vertices[j].tipo})" for j in camino + [i]]


    
def resolver_casos( input_file, output_file):
    
    with open(input_file, 'r') as f:
        data = f.read()
        
    with open(output_file, 'w') as f:
        f.write("")
        
    lineas = data.strip().split("\n") 
    index = 0
    cant_casos = int(lineas[index]) 
    index += 1 
    
    case_count = 0
    for _ in range(cant_casos):
        n, w1, w2 = map(int, lineas[index].split())
        index += 1
        case = lineas[index:index+n]
        index += n
        caso_actual = Caso(case_count, n, w1, w2, case, output_file)
        case_count += 1
    

        
if __name__ == "__main__":


    if len(sys.argv) != 3:
        print("Entradas esperadas: python script.py archivo_entrada.in archivo_salida.out\nIntente otravez")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]


    resolver_casos(input_file, output_file)


