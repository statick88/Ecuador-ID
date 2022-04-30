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
    exit(1)

signal.signal(signal.SIGINT, ctrl_c)

banner = f"""
{GREEN} /$$$$$$$$  /$$$$$$  /$$   /$$  /$$$$$$  /$$$$$$$   /$$$$$$  /$$$$$$$ 
| $$_____/ /$$__  $$| $$  | $$ /$$__  $$| $$__  $$ /$$__  $$| $$__  $$
| $$      | $$  \__/| $$  | $$| $$  \ $$| $$  \ $$| $$  \ $$| $$  \ $$
| $$$$$   | $$      | $$  | $$| $$$$$$$$| $$  | $$| $$  | $$| $$$$$$$/
| $$__/   | $$      | $$  | $$| $$__  $$| $$  | $$| $$  | $$| $$__  $$
| $$      | $$    $$| $$  | $$| $$  | $$| $$  | $$| $$  | $$| $$  \ $$
| $$$$$$$$|  $$$$$$/|  $$$$$$/| $$  | $$| $$$$$$$/|  $$$$$$/| $$  | $$
|________/ \______/  \______/ |__/  |__/|_______/  \______/ |__/  |__/
                           {CYAN}BY: Alcatraz2033{GREEN}
 /$$$$$$ /$$$$$$$        /$$$$$$$   /$$$$$$  /$$   /$$                
|_  $$_/| $$__  $$      | $$__  $$ /$$__  $$| $$  / $$                
  | $$  | $$  \ $$      | $$  \ $$| $$  \ $$|  $$/ $$/                
  | $$  | $$  | $$      | $$  | $$| $$  | $$ \  $$$$/                 
  | $$  | $$  | $$      | $$  | $$| $$  | $$  >$$  $$                 
  | $$  | $$  | $$      | $$  | $$| $$  | $$ /$$/\  $$                
 /$$$$$$| $$$$$$$/      | $$$$$$$/|  $$$$$$/| $$  \ $$                
|______/|_______/       |_______/  \______/ |__/  |__/{RESET}                                                       
"""

print(banner)
intro = input(f"{CYAN}[+]{RESET} Ingrese el nombre y apellido: ").upper().split()

url = "https://srienlinea.sri.gob.ec"

try:
    r = requests.get(url + f"/movil-servicios/api/v1.0/deudas/porDenominacion/{intro[1]}%20{intro[0]}/?tipoPersona=N&resultados=30")
except:
    print(f"{RED}[!]{RESET} Ingrese el nombre y apellido correctamente")
    exit(1)
    
data = list()

for i in json.loads(r.text):
    try:
        user = i['nombreComercial']
        ID  = i['identificacion']
        clase  = i['clase']
        identify = i['tipoIdentificacion']
        data.append([CYAN + user + RESET, GREEN + ID + RESET, WHITE + clase + RESET])
    except:
        print(f"{RED}[!]{RESET} Ingrese el primer nombre y apellido sin tildes")
        exit(1)
    
col_names = [f"{YELLOW}Nombre{RESET}", f"{YELLOW}ID{RESET}", f"{YELLOW}Clase{RESET}"]

print(f'\n{tabulate(data, headers=col_names, tablefmt="fancy_grid", showindex=True)}')
