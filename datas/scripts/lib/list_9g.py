import requests
from bs4 import BeautifulSoup

# Récupération du HTML de la page web


def getPkmInfoFromColumns(columns, indexImage, indexFrenchName, indexEnglishName):
  row_data = {}
  offset = 0

  imagePkm = columns[indexImage].find("img")
  if imagePkm is not None:
    row_data["routeImg"] = imagePkm.get("src")
  else:
    imagePkm = columns[indexImage-1].find("img")
    if imagePkm is not None:
      offset = 1
      row_data["routeImg"] = imagePkm.get("src")
    else:
      row_data["routeImg"] = columns[indexFrenchName - offset].find("a").text

  linkPkm = columns[indexFrenchName - offset].find("a")
  row_data["linkPkm"] = linkPkm.get("href")
  row_data["frName"] = linkPkm.text

  row_data["enName"] = columns[indexEnglishName - offset].find("a").text
  return row_data


def getPkmList(base_url):

  route_listPkm = "/Liste_des_Pok%C3%A9mon_dans_l%27ordre_du_Pok%C3%A9dex_de_Paldea"
  html_content = requests.get(base_url+route_listPkm).content

  # recherche de la table
  soup = BeautifulSoup(html_content, "html.parser")
  tdToFindTable = soup.find("td", id="Poussacha")
  table = tdToFindTable.find_parent("table")

  # trouver les en-têtes de colonne dans thead
  head = table.find("thead")
  headers = head.find_all("th")
  header_names = [header.text for header in headers]

  # trouver le numéro de la colonne 
  indexImage = header_names.index("Image")
  indexFrenchName = header_names.index("Nom français")
  indexEnglishName = header_names.index("Nom anglais")

  # trouver les lignes de la table dans tbody
  body = table.find("tbody")
  rows = body.find_all("tr")

  listPkm = []

  # boucle sur les lignes
  for row in rows:
    # trouver les colonnes de la ligne
    columns = row.find_all("td")
    print("COLUMN 1")
    print(columns[1])
    # initialiser un dictionnaire pour stocker les données de cette ligne
    row_data = {}
    
    listPkm.append(getPkmInfoFromColumns(columns, indexImage, indexFrenchName, indexEnglishName))

  return listPkm