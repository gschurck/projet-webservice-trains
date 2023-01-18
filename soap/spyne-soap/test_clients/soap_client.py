from zeep import Client

client = Client('http://localhost:8000/?wsdl')
res = client.service.say_hello("soap", 3)
print(res)
