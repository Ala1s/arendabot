class CyanRequest(object):
    deal_type = ''
    metro = 0
    maxprice = 0
    minprice = 0
    offer_type = ''
    room1 = 0
    room2 = 0
    room3 = 0
    room4 = 0
    region = 0
    room9 = 0
    type = 0

    def __init__(self):
        self.deal_type = 'rent'
        self.offer_type = 'flat'
        self.type = 4
        self.region = 1


class DomofondRequest(object):
    PropertyTypeDescription = ''
    PriceFrom = 0
    PriceTo = 0
    RentalRate = ''

    def __init__(self):
        self.RentalRate = 'Month'
        self.PropertyTypeDescription = 'kvartiry'


class AvitoRequest(object):
    pmax = 0
    pmin = 0
    metro = 0
