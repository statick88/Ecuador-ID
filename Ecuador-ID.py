import requests, json, signal
from tabulate import tabulate
from datetime import datetime

BLACK = '\033[30m'
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
WHITE = '\033[37m'
RESET = '\033[39m'

def ctrl_c(sig, frame):
    print(f"\n{RED}[!] Saliendo...{RESET}")
    exit()

signal.signal(signal.SIGINT, ctrl_c)

class process():

    def __init__(self):

        self.url = "https://srienlinea.sri.gob.ec"
        self.data = list()
        self.col_names = [f"{YELLOW}Nombre{RESET}", f"{YELLOW}ID{RESET}", f"{YELLOW}Clase{RESET}", f"{YELLOW}Ciudad{RESET}"]
        self.ciudades = {'01' : 'Azuay','02' : 'Bolívar','03' : 'Cañar','04' : 'Carchi','05' : 'Cotopaxi', '06' : 'Chimborazo','07' : 'El Oro', '08' : 'Esmeraldas', '09' : 'Guayas', '10' : 'Imbabura', '11' : 'Loja', '12' : 'Los Ríos', '13' : 'Manabí', '14' : 'Morona Santiago', '15' : 'Napo', '16' : 'Pastaza', '17' :'Pichincha', '18' : 'Tungurahua', '19' : 'Zamora Chinchipe', '20' : 'Galápagos', '21' : 'Sucumbíos', '22' : 'Orellana', '23' :'Santo Domingo', '24' : 'Santa Elena'}
        self.cedula = None
        
    def banner(self):
        banner = f"""{CYAN}         ___ ___ _   _  _   ___   ___  ___    ___ ___  
        | __/ __| | | |/_\ |   \ / _ \| _ \__|_ _|   \ 
        | _| (__| |_| / _ \| |) | (_) |   /___| || |) |
        |___\___|\___/_/ \_\___/ \___/|_|_\  |___|___/ 
        ⠀⠀⠀            {MAGENTA}BY: Alcatraz2033{GREEN}⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣠⣼⣷⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣾⣿⣿⣿⣿⣿⣿⣿⣿⣶⣤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣤⣤⣴⣶⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡅⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡂⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠁⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⢼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠉⠻⣿⠫⠛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠏⣸⣿⣿⣿⣿⣿⣿⣿⡿⠟⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⣴⣿⣿⣿⣿⣿⣿⣿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⡿⠻⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣿⡟⠁{RESET}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀                                     
        """

        print(banner)
        print(f"{CYAN}1) Busqueda por nombre\n2) Busqueda por cedula{RESET}")

    def time_convert(self, time_serial):

        fecha_hora_original = time_serial
        fecha_hora_parseada = datetime.strptime(fecha_hora_original, "%Y-%m-%dT%H:%M:%S.%f%z")
        fecha_hora_legible = fecha_hora_parseada.strftime("%Y-%m-%d %H:%M:%S %Z")

        return fecha_hora_legible
    
    def nombre(self):
        cedula2 = list()
        nombre = input(f"\n{CYAN}[+]{RESET} Nombres: ").upper().split()
        apellido = input(f"{CYAN}[+]{RESET} Apellidos: ").upper().split()
        
        try:
            if len(nombre) == 1 and len(apellido) == 1:
                r = requests.get(self.url + f"/movil-servicios/api/v1.0/deudas/porDenominacion/{apellido[0]}%20{nombre[0]}/?tipoPersona=N&resultados=30") 
            elif len(nombre) == 2 and len(apellido) == 1:
                r = requests.get(self.url + f"/movil-servicios/api/v1.0/deudas/porDenominacion/{apellido[0]}%20{nombre[0]}%20{nombre[1]}/?tipoPersona=N&resultados=30")    
            elif len(nombre) == 1 and len(apellido) == 2:
                r = requests.get(self.url + f"/movil-servicios/api/v1.0/deudas/porDenominacion/{apellido[0]}%20{apellido[1]}%20{nombre[0]}/?tipoPersona=N&resultados=30")   
            elif len(nombre) == 2 and len(apellido) == 2:
                r = requests.get(self.url + f"/movil-servicios/api/v1.0/deudas/porDenominacion/{apellido[0]}%20{apellido[1]}%20{nombre[0]}%20{nombre[1]}/?tipoPersona=N&resultados=30")     
            elif len(nombre) == 0 or len(apellido) == 0:
                print(f"{RED}[!]{RESET} Campos incompletos")
                exit()
        except:
            print(f"{RED}[!]{RESET} Ingrese dos nombres y dos apellidos")
            exit()

        for i in json.loads(r.text):
            try:
                user = i['nombreComercial']
                ID  = i['identificacion']
                clase  = i['clase']

                if len(ID) > 10:
                    ciudad = "No registrada"
                else:
                    ciudad = self.ciudades[ID[:2]]

                self.data.append([CYAN + user + RESET, GREEN + ID + RESET, WHITE + clase + RESET, CYAN + ciudad + RESET])
                cedula2.append(ID)

            except:
                print(f"{RED}[!]{RESET} Esta persona no existe")
                print(f"{RED}[!]{RESET} Prueba ingresar los datos sin tildes")
                exit()

        print(f'\n{tabulate(self.data, headers=self.col_names, tablefmt="fancy_grid", showindex=True)}')
        print(f'\n{CYAN}[*]{RESET} Descubre informacion extra')
        selec = int(input(f"{GREEN}[PERSONA NUMERO]─►{RESET} "))
        self.cedula = cedula2[selec]

    def cedulas(self):
        cedula2 = list()
        try:    
            intro = int(input(f"\n{CYAN}[+]{RESET} Ingrese el numero de cedula: "))
        except:
            print(f"{RED}[!]{RESET} Ingrese el numero de cedula correctamente")
            exit()
            
        r = requests.get(self.url + f"/movil-servicios/api/v1.0/deudas/porIdentificacion/{intro}/?tipoPersona=N&_=1651364830986")
        dictionary = json.loads(r.text)

        try:
            user = dictionary['contribuyente']['nombreComercial']
            ID = dictionary['contribuyente']['identificacion']
            clase = dictionary['contribuyente']['clase']

            if len(ID) > 10:
                ciudad = "No registrada"
            else:
                ciudad = self.ciudades[ID[:2]]

            self.data.append([CYAN + user + RESET, GREEN + ID + RESET, WHITE + clase + RESET, CYAN + ciudad + RESET])
            cedula2.append(ID)
            
        except:
            print(f"{RED}[!]{RESET} Este numero de cedula no existe")
            exit()
        
        print(f'\n{tabulate(self.data, headers=self.col_names, tablefmt="fancy_grid", showindex=True)}')
        print(f'\n{CYAN}[*]{RESET} Descubre informacion extra')
        selec = int(input(f"{GREEN}[PERSONA NUMERO]─►{RESET} "))
        self.cedula = cedula2[selec]
        
    # def denuncias(self):
# 
        # data = list()
        # col_names = [f"{YELLOW}Nombre{RESET}", f"{YELLOW}Juicio Numero{RESET}", f"{YELLOW}Delito{RESET}", f"{YELLOW}Fecha{RESET}", f"{YELLOW}Lugar{RESET}"]
        # url = 'https://consultas.funcionjudicial.gob.ec'
        # send = {"parametro":f"{self.cedula}","paginaIncial":1,"paginaFinal":10,"origen":"cedula"}
# 
        # s = requests.session()
# 
        # r = s.post(url + f'/informacionjudicialindividual/api/defensorPenal/buscarPorNombreCedula/{self.cedula}/1/10/cedula', json=send)
# 
        # dictionary = json.loads(r.text); dictionary = dictionary['respuesta']
# 
        # for i in dictionary:
            # nombre = i['nombre']
            # juicio = i['idJuicio']
            # delito = i['nombreDelito']
            # fecha = i['fechaProvidencia']
            # lugar = i['nombreProvincia']
# 
            # data.append([CYAN + nombre + RESET, GREEN + juicio + RESET, RED + delito + RESET, WHITE + fecha + RESET, CYAN + lugar + RESET])
        # print(f'\n{tabulate(data, headers=col_names, tablefmt="fancy_grid", showindex=True)}')


    def denuncias(self):

        col_names = [f"{YELLOW}Fecha de Ingreso{RESET}", f"{YELLOW}No. Proceso{RESET}", f"{YELLOW}Accion/Infraccion{RESET}"]
        data = list()
        url = "https://api.funcionjudicial.gob.ec"

        headers = {
            "Content-Type": "application/json"
        }

        data_j = {
            "numeroCausa": "",
            "actor": {
                "cedulaActor": "",
                "nombreActor": ""
            },
            "demandado": {
                "cedulaDemandado": f"{self.cedula}",
                "nombreDemandado": ""
            },
            "provincia": "",
            "numeroFiscalia": "",
            "recaptcha": "verdad"
        }
        json_data = json.dumps(data_j)

        r = requests.post(url + '/informacion/buscarCausas?page=1&size=100', data=json_data, headers=headers)

        dictionary = json.loads(r.text)
        for i in dictionary:
            juicio = i['idJuicio']
            delito = i['nombreDelito'].rstrip()
            fecha = self.time_convert(i['fechaIngreso'])

            data.append([CYAN + fecha + RESET, GREEN + juicio + RESET, RED + delito + RESET])
        print(f'\n{tabulate(data, headers=col_names, tablefmt="fancy_grid", showindex=True)}')


ecuador = process()
ecuador.banner()
try:
    opt = int(input(f"{GREEN}[Opcion]─►{RESET} "))
except:
    print(f"{RED}[!]{RESET} Solo puede ingresar numeros")
    exit()
            
if opt not in (1, 2):
    print(f"{RED}[!]{RESET} Solo puede seleccionar 1 o 2")
    exit()

else:
    if opt == 1:
        ecuador.nombre()
        ecuador.denuncias()
        
    if opt == 2:
        ecuador.cedulas()
        ecuador.denuncias()
