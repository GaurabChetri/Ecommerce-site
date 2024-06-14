from .cart import Cart

#create context processors 
def cart(request):
    # return the default data from our cart
    return {'cart': Cart(request)}