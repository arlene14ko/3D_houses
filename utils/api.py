#importing requests library to get the request from the API
import requests


class API:
    """
    Class API is where we request the details of the address from the API
    It contains two functions namely:
    :get_details function where we check if the address is in the API and get the coordinates
    :get_polygon function where we get the geometry polygon of the address from the API
    """

        
    def get_details(address):
        """
        get_details function requires the address as a parameter and then it will send a request to the API
            it will save the result as a dictionary named as address_info and return the dictionary address_info
        :attrib req will get the requests from the api in a json file using the address parameter
        :attrib address_info contains the result of the request in a dictionary format
        :attrib address_info includes:
        :address_info['x_value'] contains the X coordinates in Belgian Lambert
        :address_info['y_value'] contains the Y coordinates in Belgian Lambert
        :address_info['street'] contains the street name of the address
        :address_info['house_number'] contains the house number of the address
        :address_info['postcode'] contains the postcode of the address
        :address_info['municipality'] contains the municipality of the address
        """
        req = requests.get(f"https://loc.geopunt.be/v4/Location?q={address}").json()
        address_info = {'x_value': req['LocationResult'][0]['Location']['X_Lambert72'],
                        'y_value': req['LocationResult'][0]['Location']['Y_Lambert72'],
                        'street': req['LocationResult'][0]['Thoroughfarename'],
                        'house_number': req['LocationResult'][0]['Housenumber'],
                        'postcode': req['LocationResult'][0]['Zipcode'],
                        'municipality': req['LocationResult'][0]['Municipality']}
        return address_info


    def get_polygon(address_info):
        """
        get_polygon function requires the address_info as the parameter and then it will send a request to the API
            and it will save the result as a dictionary named polygon and return the polygon
        :attrib req will get the requests from the api in a json file using the address_info parameter
        :attrib detail will request the gebouwenheden of the address from the API
        :attrib build will request the gebouw of the address from the APi
        :attrib polygon will contain the geometripolygon of the address from the API
        """
        req = requests.get("https://api.basisregisters.vlaanderen.be/v1/adresmatch",
                           params={"postcode": address_info['postcode'],
                                    "straatnaam": address_info['street'],
                                    "huisnummer": address_info['house_number']}).json()
        detail = requests.get(req['adresMatches'][0]['adresseerbareObjecten'][0]['detail']).json()
        build = requests.get(detail['gebouw']['detail']).json()
        polygon = build['geometriePolygoon']['polygon']
        
        return polygon
