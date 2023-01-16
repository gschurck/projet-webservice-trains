from pysimplesoap.client import SoapClient

wsdl_url = "http://127.0.0.1:8050/"
c = SoapClient(wsdl=wsdl_url, soap_ns='soap', trace=False)
print(c.InitiateTransfer(sessionId="sid", msisdn="254722000000", amount="100", language="en"))
