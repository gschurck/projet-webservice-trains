from lxml import etree
from zeep import Client, helpers
from zeep.plugins import HistoryPlugin

history = HistoryPlugin()

client = Client('http://localhost:8050/?wsdl', plugins=[history])
client.wsdl.dump()
string_list = ['first', 'standard']
emptyArrayPlaceholder = client.get_type('ns0:stringArray')
options = emptyArrayPlaceholder()

for el in string_list:
    options['string'].append(el)
res = client.service.search_trains("London", "Paris", options, "2022-01-01T12:00:00")
for hist in [history.last_sent, history.last_received]:
    print(etree.tostring(hist["envelope"], encoding="unicode", pretty_print=True))
print(res)
dict = helpers.serialize_object(res)
print(dict[0]['id'])
