import requests


class API:
        
    def get_details(address):
        req = requests.get(f"https://loc.geopunt.be/v4/Location?q={address}").json()
        address_info = {'x_value': req['LocationResult'][0]['Location']['X_Lambert72'],
                        'y_value': req['LocationResult'][0]['Location']['Y_Lambert72'],
                        'street': req['LocationResult'][0]['Thoroughfarename'],
                        'house_number': req['LocationResult'][0]['Housenumber'],
                        'postcode': req['LocationResult'][0]['Zipcode'],
                        'municipality': req['LocationResult'][0]['Municipality']}
        return address_info
    
    def get_polygon(address_info):
        req = requests.get("https://api.basisregisters.vlaanderen.be/v1/adresmatch",
                           params={"postcode": address_info['postcode'],
                                    "straatnaam": address_info['street'],
                                    "huisnummer": address_info['house_number']}).json()
        detail = requests.get(req['adresMatches'][0]['adresseerbareObjecten'][0]['detail']).json()
        build = requests.get(detail['gebouw']['detail']).json()
        polygon = build['geometriePolygoon']['polygon']
        
        return polygon
