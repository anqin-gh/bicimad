import json
import requests
import math
from haversine import haversine

# Levantar docker compose con:
#     Contenedor que haga el pull de los datos de la API y los guarde en la db
#     Contenedor con DB
#     Contenedor que consulte el histórico del día de la DB y calcule cuántas bicis están libres y cuáles de esas son de verdad utilizables y no rotas

# 40.435088, -3.705534 (top-left)
# 40.428025, -3.698615 (bottom-right)
class Point:
   def __init__(self, x, y):
      self.x = x
      self.y = y


class Rectangle:
  def __init__(self, top_left, bottom_right):
    assert top_left.x <= bottom_right.x
    assert top_left.y >= bottom_right.y

    self.top_left = top_left
    self.bottom_right = bottom_right

  def is_in_rectangle(self, p):
    return  p.x >= self.top_left.x and \
            p.x <= self.bottom_right.x and \
            p.y <= self.top_left.y and \
            p.y >= self.bottom_right.y


def find_stations_in_rectangle(stations, rec):
  result = []
  for station in stations:
    x = station["geometry"]["coordinates"][0]
    y = station["geometry"]["coordinates"][1]
    p = Point(x, y)
    if (rec.is_in_rectangle(p)):
      result.append(station)
  return result


def calc_distance(a, b):
  return haversine((a.x, a.y), (b.x, b.y)) * 1000


def find_station_by_id(stations, id):
  for station in stations:
    if station["id"] == id:
      return station


# Pull data from API every 5 minutes from 8am to 17:30
# 10h * 60 min / 5 = 120 db entries / day
# Store the data in one table --> Station

def main():
  home = Point(-3.701125, 40.430528)
  home_rectangle = Rectangle(Point(-3.705534, 40.435088), Point(-3.698615, 40.428025))

  response = requests.get("https://openapi.emtmadrid.es/v1/transport/bicimad/stations/")
  api_resp = response.json()
  stations = api_resp["data"]
  near_stations = find_stations_in_rectangle(stations, home_rectangle)
  near_stations.sort(key=lambda s : calc_distance(Point(s["geometry"]["coordinates"][0], s["geometry"]["coordinates"][1]), home))
  for s in near_stations:
    print(f"{s['id']}: {s['name']} - {calc_distance(Point(s['geometry']['coordinates'][0], s['geometry']['coordinates'][1]), home)}")
  print(near_stations[0])


if __name__ == '__main__':
  main()
