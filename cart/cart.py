from store.models import Product, Profile

class Cart():
    def __init__(self, request):
        self.session = request.session
        #Get request
        self.request = request
        #Get the current session if it exits
        cart = self.session.get('session_key')
        #if user is new, no session key! create one
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        #Make sure cart is avaible on all pages
        self.cart = cart

    def db_add(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)
            #Logic
        if product_id in self.cart:
            pass
        else:
                # self.cart[product_id] = {'price':str(product.price)}
            self.cart[product_id] = int(product_qty)
        self.session.modified = True

            #Deal with looged in user
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            #Convert {'3':2} to {"3":2}:
            carty =str(self.cart)
            carty= carty.replace("\'", "\"")
            #Save carty to the Profile Model
            current_user.update(old_cart=str(carty))



    
    
    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)
        #Logic
        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {'price':str(product.price)}
            self.cart[product_id] = int(product_qty)
        self.session.modified = True

        #Deal with looged in user
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            #Convert {'3':2} to {"3":2}:
            carty =str(self.cart)
            carty= carty.replace("\'", "\"")
            #Save carty to the Profile Model
            current_user.update(old_cart=str(carty))

    def __len__(self):
        return len(self.cart)
    
    def get_prods(self):
        #Get ids from cart
        products_ids = self.cart.keys()
        #use ids to lookup productsin database model
        products = Product.objects.filter(id__in= products_ids)
        return products 

    def get_quants(self):
        quantities = self.cart
        return quantities 

    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)

        #Get cart
        ourcart = self.cart
        #Update Dictionary/Cart
        ourcart[product_id] = product_qty
        self.session.modified = True
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            #Convert {'3':2} to {"3":2}:
            carty =str(self.cart)
            carty= carty.replace("\'", "\"")
            #Save carty to the Profile Model
            current_user.update(old_cart=str(carty))
        thing = self.cart
        return thing
    

    def delete(self, product):
        product_id = str(product)
        #Delete from Dict/Cart
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            #Convert {'3':2} to {"3":2}:
            carty =str(self.cart)
            carty= carty.replace("\'", "\"")
            #Save carty to the Profile Model
            current_user.update(old_cart=str(carty))

    def cart_total(self):
        #Get product IDS
        product_ids =self.cart.keys()
        #Look up those keys in or products DB
        products = Product.objects.filter(id__in = product_ids)
        quantities =self.cart
        total = 0
        for key, value in quantities.items():
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total = total+ (product.sale_price * value)
                    else:
                        total = total+ (product.price * value)
        return total
