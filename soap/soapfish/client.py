from test import InitiateTransfer, TransServerServiceStub

i = InitiateTransfer(sessionId="sid", msisdn="254722000000", amount="100", language="en")
TransServerServiceStub().InitiateTransfer(i)
