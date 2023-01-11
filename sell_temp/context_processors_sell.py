from .sell_temp import Selltemp


def sell(request):
    return {'sell_temp': Selltemp(request)}