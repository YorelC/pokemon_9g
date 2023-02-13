from lib import list_9g

base_url = "https://www.pokepedia.fr"

pkmList = list_9g.getPkmList(base_url)
print(pkmList)