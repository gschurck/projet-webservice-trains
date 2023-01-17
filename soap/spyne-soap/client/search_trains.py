from zeep import Client

client = Client('http://localhost:8050/?wsdl')
client.wsdl.dump()
string_list = ['first', 'standard']
emptyArrayPlaceholder = client.get_type('ns0:stringArray')
options = emptyArrayPlaceholder()

for el in string_list:
    options['string'].append(el)
res = client.service.search_trains("London", "Paris", options, "2022-01-01T12:00:00")
print(res)
