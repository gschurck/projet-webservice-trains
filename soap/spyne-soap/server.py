import json
import logging
import os

import requests

logging.basicConfig(level=logging.INFO)
from spyne import Application, rpc, ServiceBase, \
    Integer, Unicode, DateTime
from spyne import Iterable
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

from soap_models import CustomModel, Train

API_URL = os.getenv("API_URL")


class HelloWorldService(ServiceBase):
    @rpc(Unicode, Integer, DateTime, _returns=Iterable(CustomModel))
    def say_hello(ctx, name, times, date):
        ret = []
        for i in range(times):
            # yield 'Hello, %s' % name
            ret.append(CustomModel(name='Hello, %s' % name))
        return ret


class SearchTrainsService(ServiceBase):
    @rpc(Unicode, Unicode, Iterable(Unicode), DateTime, _returns=Iterable(Train))
    def search_trains(ctx, departure_station, arrival_station, seat_classes, date):
        # convert generator to list
        seat_classes = list(seat_classes)
        logging.info(str(seat_classes))
        logging.info(len(seat_classes))
        # split seat_classes to string and join with comma
        seat_classes = ','.join(seat_classes)
        logging.info(seat_classes)
        res = requests.get(API_URL + '/trains', params={
            'departure_station': departure_station if departure_station else None,
            'arrival_station': arrival_station if arrival_station else None,
            'train__seat_class__in': seat_classes if seat_classes else None,
        })
        logging.info(type(res))
        logging.info(json.dumps(res.json(), indent=4))
        trains = json.loads(res.text)
        logging.info(type(trains))
        for train in trains:
            res = requests.get(API_URL + '/trains/' + str(train['id']) + '/classes')
            train['classes'] = json.loads(res.text)
        logging.info(json.dumps(trains, indent=4))
        return trains


application = Application([HelloWorldService, SearchTrainsService],
                          tns='soap.trains',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11()
                          )
if __name__ == '__main__':
    # You can use any Wsgi server. Here, we chose
    # Python's built-in wsgi server but you're not
    # supposed to use it in production.
    from wsgiref.simple_server import make_server

    wsgi_app = WsgiApplication(application)
    server = make_server('0.0.0.0', 8050, wsgi_app)
    server.serve_forever()
