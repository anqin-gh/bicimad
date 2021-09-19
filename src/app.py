import json
import requests

# Levantar docker compose con:
#     Contenedor que haga el pull de los datos de la API y los guarde en la db
#     Contenedor con DB
#     Contenedor que consulte el histórico del día de la DB y calcule cuántas bicis están libres y cuáles de esas son de verdad utilizables y no rotas

# Pull data from API every 5 minutes from 8am to 17:30
# 10h * 60 min / 5 = 120 db entries / day
# Store the data in one table --> Station

def main():
  response = requests.get("https://openapi.emtmadrid.es/v1/transport/bicimad/stations/")
  api_resp = response.json()
  stations = api_resp["data"]


if __name__ == '__main__':
  main()
