import json
import logging
import os

import requests

logging.basicConfig(level=logging.INFO)
from spyne import Application, rpc, ServiceBase, \
    Integer, Unicode, Date, Time
from spyne import Iterable
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

from soap_models import Train

API_URL = os.getenv("API_URL")


class SearchTrainsService(ServiceBase):
    @rpc(Unicode, Unicode, Iterable(Unicode), Date, Time, _returns=Iterable(Train))
    def search_trains(ctx, departure_station, arrival_station, seat_classes, date, time):
        # convert generator to list
        seat_classes = list(seat_classes)
        logging.info(str(seat_classes))
        logging.info(len(seat_classes))
        # split seat_classes to string and join with comma
        seat_classes = ','.join(seat_classes)
        logging.info(seat_classes)
        res = requests.get(API_URL + '/trains', params={
            'departure_station__ilike': departure_station if departure_station else None,
            'arrival_station__ilike': arrival_station if arrival_station else None,
            'departure_date': date if date else None,
            'departure_time': time if time else None,
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


class BookTicketsService(ServiceBase):
    @rpc(Integer, Integer, _returns=Unicode)
    def book_tickets(ctx, train_seat_class_id, patched_count):
        print(patched_count)
        res = requests.patch(API_URL + '/trains/class/' + str(train_seat_class_id), json={
            'available_seats_count': patched_count,
        })
        print(res.text)
        return res.text


application = Application([SearchTrainsService, BookTicketsService],
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
