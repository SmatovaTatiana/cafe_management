from .doc_temp import Doctemp


def doc(request):
    return {'doc_temp': Doctemp(request)}
