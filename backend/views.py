from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives

import json
from datetime import datetime

from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import *
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from django.core.cache import cache

from .models import *
from .serializers import *

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY
# admin_email = settings.EMAIL_ADMIN
# current_admin_domain = settings.CURRENT_ADMIN_DOMAIN

# Create your views here.

def homepage(request):
    """
    Landing page view for the website
    """
    return render(request, 'homepage.html')

@api_view(['GET'])
def api_root(request):
    """
    Root API view that provides a browsable API interface
    """
    return Response({
        'categories': reverse('trucks-signs-root:categories-api', request=request),
        'lettering_item_categories': reverse('trucks-signs-root:lettering-item-categories-api', request=request),
        'products': reverse('trucks-signs-root:products-api', request=request),
        'product_color': reverse('trucks-signs-root:product-color-api', request=request),
        'truck_logo_list': reverse('trucks-signs-root:truck-logo-list-api', request=request),
        'comments': reverse('trucks-signs-root:comments-api', request=request),
        'comment_create': reverse('trucks-signs-root:comment-create-api', request=request),
        'upload_customer_image': reverse('trucks-signs-root:upload-customer-image-api', request=request),
    })

class CategoryListView(ListAPIView):
    authentication_classes = []
    serializer_class = CategorySerializer
    model = Category
    
    def get_queryset(self):
        cache_key = 'categories_list_ids'
        category_ids = cache.get(cache_key)
        if category_ids is None:
            queryset = Category.objects.all().prefetch_related('product_set')
            category_ids = list(queryset.values_list('id', flat=True))
            cache.set(cache_key, category_ids, 300)  # Cache for 5 minutes
        return Category.objects.filter(id__in=category_ids).prefetch_related('product_set')

class LetteringItemCategoryListView(ListAPIView):
    authentication_classes = []
    serializer_class = LetteringItemCategorySerializer
    model = LetteringItemCategory
    
    def get_queryset(self):
        cache_key = 'lettering_item_categories_list_queryset'
        queryset_ids = cache.get(cache_key)
        if queryset_ids is None:
            queryset = LetteringItemCategory.objects.all()
            queryset_ids = list(queryset.values_list('id', flat=True))
            cache.set(cache_key, queryset_ids, 300)  # Cache for 5 minutes
        return LetteringItemCategory.objects.filter(id__in=queryset_ids)

class ProductListView(ListAPIView):
    authentication_classes = []
    serializer_class = ProductSerializer
    model = Product
    
    def get_queryset(self):
        cache_key = 'products_list_queryset'
        queryset_ids = cache.get(cache_key)
        if queryset_ids is None:
            queryset = Product.objects.all().select_related('category')
            queryset_ids = list(queryset.values_list('id', flat=True))
            cache.set(cache_key, queryset_ids, 300)  # Cache for 5 minutes
        return Product.objects.filter(id__in=queryset_ids).select_related('category')

class ProductFromCategoryListView(ListAPIView):
    authentication_classes = []
    serializer_class = ProductSerializer
    model = Product
    lookup_url_kwarg = 'id'

    def get_queryset(self):
        category_id = self.kwargs.get(self.lookup_url_kwarg)
        return Product.objects.filter(category__id=category_id).select_related('category')


class ProductColorListView(ListAPIView):
    authentication_classes = []
    serializer_class = ProductColorSerializer
    model = ProductColor
    
    def get_queryset(self):
        cache_key = 'product_colors_list_queryset'
        queryset_ids = cache.get(cache_key)
        if queryset_ids is None:
            queryset = ProductColor.objects.all()
            queryset_ids = list(queryset.values_list('id', flat=True))
            cache.set(cache_key, queryset_ids, 300)  # Cache for 5 minutes
        return ProductColor.objects.filter(id__in=queryset_ids)


class LogoListView(ListAPIView):
    authentication_classes = []
    serializer_class = ProductSerializer
    model = Product
    
    def get_queryset(self):
        # Cache the category lookup to avoid filtering by title
        cache_key = 'truck_sign_category_id'
        category_id = cache.get(cache_key)
        if category_id is None:
            try:
                category = Category.objects.get(title='Truck Sign')
                category_id = category.id
                cache.set(cache_key, category_id, 3600)  # Cache for 1 hour
            except Category.DoesNotExist:
                return Product.objects.none()
        
        cache_key_products = f'logo_list_{category_id}'
        queryset_ids = cache.get(cache_key_products)
        if queryset_ids is None:
            queryset = Product.objects.filter(category_id=category_id, is_uploaded=False).select_related('category')
            queryset_ids = list(queryset.values_list('id', flat=True))
            cache.set(cache_key_products, queryset_ids, 300)  # Cache for 5 minutes
        return Product.objects.filter(id__in=queryset_ids, category_id=category_id, is_uploaded=False).select_related('category')


class ProductDetail(RetrieveAPIView):
    authentication_classes = []
    serializer_class = ProductSerializer
    model = Product
    lookup_field = 'id'
    queryset = Product.objects.all().select_related('category')




class ProductVariationRetrieveView(RetrieveAPIView):
    authentication_classes = []
    serializer_class = ProductVariationSerializer
    model = ProductVariation
    lookup_field = 'id'
    
    def get_queryset(self):
        return ProductVariation.objects.select_related(
            'product', 
            'product__category',
            'product_color'
        ).prefetch_related(
            'lettering_item_variation_set__lettering_item_category'
        )




class CreateOrder(GenericAPIView):
    authentication_classes = []
    serializer_class = OrderSerializer

    def post(self, request, id, format=None):
        data = request.data

        product = Product.objects.get(id=id)

        product_variation = ProductVariation(product=product)
        product_variation.save()

        lettering_items = data['lettering_items']
        for custom_lettering_item in lettering_items:
            if custom_lettering_item['text'] and custom_lettering_item['text'].strip():
                item_category = LetteringItemCategory.objects.get(title=custom_lettering_item['title'])
                item_category.save()
                lettering_item = LetteringItemVariation(lettering_item_category=item_category, lettering=custom_lettering_item['text'], product_variation=product_variation)
                lettering_item.save()

        try:
            product_color = ProductColor.objects.get(id=data['product_color_id'])
        except:
            product_color = None
        product_variation.product_color = product_color
        product_variation.amount = 1
        product_variation.save()

        order_serializer = OrderSerializer(data=data['order'])
        order_serializer.is_valid(raise_exception=True)
        order = order_serializer.save(product=product_variation, payment=None)
        order_serializer = OrderSerializer(order)

        return Response({"Result":order_serializer.data}, status=status.HTTP_200_OK)




class RetrieveOrder(RetrieveAPIView):
    authentication_classes = []
    serializer_class = OrderSerializer
    model = Order
    lookup_field = 'id'
    
    def get_queryset(self):
        return Order.objects.select_related(
            'product',
            'product__product',
            'product__product__category',
            'product__product_color',
            'payment'
        ).prefetch_related(
            'product__lettering_item_variation_set__lettering_item_category'
        )




class PaymentView(GenericAPIView):

    authentication_classes = []
    serializer_class = PaymentSerializer

    def get(self, post, id, format=None):
        order = Order.objects.select_related(
            'product',
            'product__product',
            'product__product__category',
            'product__product_color',
            'payment'
        ).prefetch_related(
            'product__lettering_item_variation_set__lettering_item_category'
        ).get(id=id)
        order_serializer = OrderSerializer(order)
        return Response({"Order": order_serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, id, format=None):

        try:
        # if True:
            order = Order.objects.select_related(
                'product',
                'product__product',
                'product__product__category',
                'product__product_color',
                'payment'
            ).prefetch_related(
                'product__lettering_item_variation_set__lettering_item_category'
            ).get(id=id)
            try:
                order_serializer = OrderSerializer(order, data=request.data['order'], partial=True)
                order_serializer.is_valid(raise_exception=True)
                order = order_serializer.save()
            except:
                pass

            card_num = request.data['card_num']
            exp_month = request.data['exp_month']
            exp_year = request.data['exp_year']
            cvc = request.data['cvc']

            token = stripe.Token.create(
                card={
                    "number": card_num,
                    "exp_month": int(exp_month),
                    "exp_year": int(exp_year),
                    "cvc": cvc
                },
            )

            amount = int(order.get_total_price() * 100)

            charge = stripe.Charge.create(
                amount=amount,
                currency="usd",
                source=token
            )


            stripe_charge_id = charge['id']
            payment = Payment(user_email = order.user_email, stripe_charge_id=stripe_charge_id, amount=amount)
            payment.save()
            order.ordered = True
            order.payment = payment
            order.save()

            # Send Email to user
            # email_subject="Purchase made."
            # message=render_to_string('purchase-made.html', {
            #     'user': order.user_email,
            #     'image': order.product.product.image,
            #     'amount_of_product': str(order.product.amount),
            #     'total_amount':str("{:.2f}".format(order.get_total_price())),
            # })
            # to_email = order.user_email
            # email = EmailMultiAlternatives(email_subject, to=[to_email])
            # email.attach_alternative(message, "text/html")
            # email.send()
            #
            # admin_message=render_to_string('admin-purchase-made.html',{
            #     'user': order.user_email,
            #     'order': order.id,
            #     'current_admin_domain':current_admin_domain,
            # })

            # to_admin_email = admin_email
            # email = EmailMultiAlternatives(email_subject, to=[to_admin_email])
            # email.attach_alternative(admin_message, "text/html")
            # email.send()

            return Response({"Result": "Success"}, status=status.HTTP_200_OK)

        # else:
        #     pass
        except stripe.error.CardError as e:
            return Response({"Result":"Error with card during payment"}, status=status.HTTP_400_BAD_REQUEST)

        except stripe.error.RateLimitError as e:
            return Response({"Result":"Rate Limit error during payment"}, status=status.HTTP_400_BAD_REQUEST)

        except stripe.error.InvalidRequestError as e:
            return Response({"Result":"Invalid request error during payment"}, status=status.HTTP_400_BAD_REQUEST)

        except stripe.error.AuthenticationError as e:
            return Response({"Result":"Authentication error during payment"}, status=status.HTTP_400_BAD_REQUEST)

        except stripe.error.APIConnectionError as e:
            return Response({"Result":"API connection error during payment"}, status=status.HTTP_400_BAD_REQUEST)

        except stripe.error.StripeError as e:
            return Response({"Result":"Something went wrong during payment"}, status=status.HTTP_400_BAD_REQUEST)

        except:
            return Response({"Result":"Error during payment"}, status=status.HTTP_400_BAD_REQUEST)




class CommentsView(ListAPIView):
    authentication_classes = []
    serializer_class = CommentSerializer
    model = Comment
    
    def get_queryset(self):
        cache_key = 'comments_list_queryset'
        queryset_ids = cache.get(cache_key)
        if queryset_ids is None:
            queryset = Comment.objects.filter(visible=True)
            queryset_ids = list(queryset.values_list('id', flat=True))
            cache.set(cache_key, queryset_ids, 300)  # Cache for 5 minutes
        return Comment.objects.filter(id__in=queryset_ids, visible=True)


class CommentCreateView(CreateAPIView):
    authentication_classes = []
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    
    def perform_create(self, serializer):
        instance = serializer.save()
        # Invalidate comments cache when a new comment is created
        cache.delete('comments_list_queryset')
        return instance


class UploadCustomerImage(GenericAPIView):
    authentication_classes = []

    def post(self, request, form=None):
        data = request.data
        product_title = "Customer-Image-" + str(datetime.now())
        category = Category.objects.select_related().get(title="Truck Sign")
        product = Product(category=category, title=product_title, is_uploaded=True)
        product.save()

        product_serializer = ProductSerializer(product, data=data, partial=True)
        product_serializer.is_valid(raise_exception=True)
        product = product_serializer.save()
        product.detail_image = product.image
        product.save()
        product_serializer = ProductSerializer(product)
        return Response({"Result": product_serializer.data}, status=status.HTTP_200_OK)