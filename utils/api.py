import requests


class API:
        
    def get_coordinates(address):
        req = requests.get(f"https://loc.geopunt.be/v4/Location?q={address}").json()
        x = req['LocationResult'][0]['Location']['X_Lambert72']
        y = req['LocationResult'][0]['Location']['Y_Lambert72']
        return x, y
    
    def get_polygon(address):
        req = requests.get("https://api.basisregisters.vlaanderen.be/v1/adresmatch", params={"postcode": address.split(" ")[2], "straatnaam": address.split(" ")[0], "huisnummer": address.split(" ")[1][:-1] }).json()
        detail = requests.get(req['adresMatches'][0]['adresseerbareObjecten'][0]['detail']).json()
        build = requests.get(detail['gebouw']['detail']).json()
        #x = detail['geometriePunt']['point']['coordinates'][0]
        #y = detail['geometriePunt']['point']['coordinates'][1]
        polygon = build['geometriePolygoon']['polygon']
        
        return polygon
