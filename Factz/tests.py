from django.test import TestCase

def buildZeroRequestObject():
    request = HttpRequest()
    request.POST = QueryDict('float=0&int=0&string=0')
    return request
    
def buildBlankRequestObject():
    request = HttpRequest()
    request.POST = QueryDict('')
    return request

class ApiTestCases(TestCase):
    
    def test_intFromPost_1(self):
        request = buildValidRequestObject()
        value = intFromPost(request,'int')
        self.assertEqual(type(value),type(int(1)))
        