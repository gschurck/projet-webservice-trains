from wsgiref.simple_server import make_server

from soapfish import xsd, soap, soap_dispatch


class GetStockPrice(xsd.ComplexType):
    company = xsd.Element(xsd.String, minOccurs=1)
    datetime = xsd.Element(xsd.DateTime)


class StockPrice(xsd.ComplexType):
    price = xsd.Element(xsd.Integer)


Schema = xsd.Schema(
    targetNamespace='http://code.google.com/p/soapfish/stock.xsd',  # should be unique, can be any string.
    complexTypes=[GetStockPrice, StockPrice],
    elements={
        'getStockPrice': xsd.Element(GetStockPrice),
        'stockPrice': xsd.Element(StockPrice),
    },
)


def get_stock_price(request, gsp):
    print(gsp.company)
    return StockPrice(price=139)


def get_stock_price2(request):
    return StockPrice(price=139)


get_stock_price_method = xsd.Method(
    function=get_stock_price,
    soapAction='http://code.google.com/p/soapfish/stock/get_stock_price',
    input='getStockPrice',
    output='stockPrice',
    operationName='GetStockPrice',
)
SERVICE = soap.Service(
    targetNamespace='http://code.google.com/p/soapfish/stock.wsdl',
    location='http://127.0.0.1:8000/stock',  # where request should be sent.
    schemas=[Schema],
    methods=[get_stock_price_method],
)

dispatcher = soap_dispatch.SOAPDispatcher(SERVICE)
# app = soap_dispatch.WsgiSoapApplication({'/ChargePoint/services/chargePointService': dispatcher})
app = soap_dispatch.WsgiSoapApplication(dispatcher)

print('Serving HTTP on port 8000...')
httpd = make_server('', 8000, app)
httpd.serve_forever()
