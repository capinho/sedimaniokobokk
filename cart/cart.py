from decimal import Decimal
from django.http import HttpResponse

from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages

from shop.models import Product
from orders.models import *

class Cart(object):
    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            #enregistrer un panier vide dans la session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        """
        Ajouter un produit au panier ou mettre à jour sa quantité.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                    'price': str(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # mettre à jour le panier de la session
        self.session[settings.CART_SESSION_ID] = self.cart
        # marquer la session comme "modifiée" pour s'assurer qu'elle est sauvegardée
        self.session.modified = True

    def remove(self, product):
        """
        Supprimer un produit du panier
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
    Itérer sur les articles dans le panier et obtenir les produits de la base de données.
        """
        product_ids = self.cart.keys()
        # récupérer les objets du produit et les ajouter au panier
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Compter tous les articles dans le panier.
        """
        #
        #product_ids = self.cart.keys()
        #products = Product.objects.filter(id__in=product_ids)
        return sum(item['quantity'] for item in self.cart.values())
        #return products.count()

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def get_total_item(self):
        for item in self.cart:
            return item

    def clear(self):
        # retirer le panier de la session
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
