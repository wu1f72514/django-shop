# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.formats import localize
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from shop.views import dashboard
from shop.views.dashboard import router

from myshop.models import Product, SmartCard, SmartPhoneModel


class ProductSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()
    product_code = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'product_name', 'product_code', 'price', 'active']

    def get_product_code(self, product):
        return getattr(product, 'product_code', _("n.a."))

    def get_price(self, product):
        price = product.get_price(self.context['request'])
        return localize(price)


class SmartCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmartCard
        fields = '__all__'


class SmartPhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmartPhoneModel
        fields = '__all__'


class ProductsDashboard(dashboard.ProductsDashboard):
    list_display = ['product_name', 'product_code', 'price', 'active']
    list_display_links = ['product_name']
    list_serializer_class = ProductSerializer
    detail_serializer_classes = {
        'myshop.smartcard': SmartCardSerializer,
        'myshop.smartphonemodel': SmartPhoneSerializer,
    }

router.register('products', ProductsDashboard)