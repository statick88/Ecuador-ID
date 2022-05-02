import requests, json, signal
from tabulate import tabulate

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

banner = f"""{CYAN} ___ ___ _   _  _   ___   ___  ___    ___ ___  
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

url = "https://srienlinea.sri.gob.ec"
data = list()

def nombre():

    nombre = input(f"\n{CYAN}[+]{RESET} Nombres: ").upper().split()
    apellido = input(f"{CYAN}[+]{RESET} Apellidos: ").upper().split()
    
    try:
        if len(nombre) == 1 and len(apellido) == 1:
            r = requests.get(url + f"/movil-servicios/api/v1.0/deudas/porDenominacion/{apellido[0]}%20{nombre[0]}/?tipoPersona=N&resultados=30") 
        elif len(nombre) == 2 and len(apellido) == 1:
            r = requests.get(url + f"/movil-servicios/api/v1.0/deudas/porDenominacion/{apellido[0]}%20{nombre[0]}%20{nombre[1]}/?tipoPersona=N&resultados=30")    
        elif len(nombre) == 1 and len(apellido) == 2:
            r = requests.get(url + f"/movil-servicios/api/v1.0/deudas/porDenominacion/{apellido[0]}%20{apellido[1]}%20{nombre[0]}/?tipoPersona=N&resultados=30")   
        elif len(nombre) == 2 and len(apellido) == 2:
            r = requests.get(url + f"/movil-servicios/api/v1.0/deudas/porDenominacion/{apellido[0]}%20{apellido[1]}%20{nombre[0]}%20{nombre[1]}/?tipoPersona=N&resultados=30")     
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
            data.append([CYAN + user + RESET, GREEN + ID + RESET, WHITE + clase + RESET])
        except:
            print(f"{RED}[!]{RESET} Esta persona no existe")
            print(f"{RED}[!]{RESET} Prueba ingresar los datos sin tildes")
            exit()
        
    col_names = [f"{YELLOW}Nombre{RESET}", f"{YELLOW}ID{RESET}", f"{YELLOW}Clase{RESET}"]

    print(f'\n{tabulate(data, headers=col_names, tablefmt="fancy_grid", showindex=True)}')

def cedula():

    try:    
        intro = int(input(f"\n{CYAN}[+]{RESET} Ingrese el numero de cedula: "))
    except:
        print(f"{RED}[!]{RESET} Ingrese el numero de cedula correctamente")
        exit()
        
    r = requests.get(url + f"/movil-servicios/api/v1.0/deudas/porIdentificacion/{intro}/?tipoPersona=N&_=1651364830986")
    
    dictionary = json.loads(r.text)
    
    try:
        user = dictionary['contribuyente']['nombreComercial']
        ID = dictionary['contribuyente']['identificacion']
        clase = dictionary['contribuyente']['clase']
    except:
        print(f"{RED}[!]{RESET} Este numero de cedula no existe")
        exit()
            
    data.append([CYAN + user + RESET, GREEN + ID + RESET, WHITE + clase + RESET])
    
    col_names = [f"{YELLOW}Nombre{RESET}", f"{YELLOW}ID{RESET}", f"{YELLOW}Clase{RESET}"]
    
    print(f'\n{tabulate(data, headers=col_names, tablefmt="fancy_grid", showindex=True)}')

if __name__ == '__main__':

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
            nombre()
        if opt == 2:
            cedula()
            
