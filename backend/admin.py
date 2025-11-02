from django.contrib import admin
from .models import *

# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'user_email',
        'id',
        'ordered',
        'get_product_variation_id',
        'get_product',
        'get_product_category',
        'ordered_date',
    ]
    
    list_select_related = (
        'product',
        'product__product',
        'product__product__category',
        'product__product_color',
        'payment'
    )
    
    list_prefetch_related = (
        'product__lettering_item_variation_set__lettering_item_category',
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related(
            'product',
            'product__product',
            'product__product__category',
            'product__product_color',
            'payment'
        ).prefetch_related(
            'product__lettering_item_variation_set__lettering_item_category'
        )

    def get_product_variation_id(self, obj):
        try:
            return obj.product.id
        except:
            return 'No customized product'
    get_product_variation_id.short_description = 'Customized Product ID'
    get_product_variation_id.admin_order_field = 'product__id'

    def get_product(self, obj):
        try:
            return obj.product.product.id
        except:
            return 'No base product'
    get_product.short_description = 'Base Product ID'
    get_product.admin_order_field = 'product__product__id'

    def get_product_category(self, obj):
        try:
            return obj.product.product.category
        except:
            return 'No category'
    get_product_category.short_description = 'Product Category'
    get_product_category.admin_order_field = 'product__product__category'

    search_fields = ['user_email', 'id']





class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'base_price',
        'max_amount_of_lettering_items',
        'height',
        'width',
        'id',
    ]
    search_fields = ['title', 'id']
    
    list_per_page = 50  # Limit items per page for better performance
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Prefetch products to avoid N+1 queries if needed
        return qs.prefetch_related('product_set')





class LetteringItemCategoryAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'price',
        'id',
    ]
    search_fields = ['title', 'id']
    list_per_page = 50  # Limit items per page for better performance






class ProductColorAdmin(admin.ModelAdmin):
    list_display = [
        'color_nickname',
        'color_in_hex',
        'id',
    ]
    search_fields = ['color_nickname', 'color_in_hex', 'id']
    list_per_page = 50  # Limit items per page for better performance





class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'category',
        'is_uploaded',
        'id',
    ]
    search_fields = ['title', 'id']
    list_filter = ['category', 'is_uploaded']
    list_select_related = ('category',)
    
    list_per_page = 50  # Limit items per page for better performance
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('category')





class ProductVariationAdmin(admin.ModelAdmin):
    list_display = [
        'product',
        'get_amount_of_lettering',
        'product_color',
        'get_amount',
        'id',
    ]
    
    list_select_related = (
        'product',
        'product__category',
        'product_color'
    )
    
    list_prefetch_related = (
        'lettering_item_variation_set__lettering_item_category',
    )
    
    list_per_page = 50  # Limit items per page for better performance

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related(
            'product',
            'product__category',
            'product_color'
        ).prefetch_related(
            'lettering_item_variation_set__lettering_item_category'
        )

    def get_amount(self, obj):
        try:
            return obj.amount
        except:
            return '0'

    get_amount.short_description = "Amount of Product"
    get_amount.admin_order_field = "amount"


    def get_amount_of_lettering(self, obj):
        try:
            # Use cached prefetch instead of calling get_all_lettering_items()
            return obj.lettering_item_variation_set.count()
        except:
            return '0'
    get_amount_of_lettering.short_description = 'Amount of Lettering'
    get_amount_of_lettering.admin_order_field = 'lettering_item_variation_set__count'

    search_fields = ['id']




class LetteringItemVariationAdmin(admin.ModelAdmin):
    list_display = [
        'get_lettering_item_category',
        'lettering',
        'get_product_variation',
        'id',
    ]
    
    list_select_related = (
        'lettering_item_category',
        'product_variation',
        'product_variation__product',
        'product_variation__product__category'
    )
    
    list_per_page = 50  # Limit items per page for better performance

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related(
            'lettering_item_category',
            'product_variation',
            'product_variation__product',
            'product_variation__product__category'
        )

    def get_lettering_item_category(self, obj):
        try:
            return obj.lettering_item_category
        except:
            return "---"
    get_lettering_item_category.short_description = 'Category'


    def get_product_variation(self, obj):
        try:
            return obj.product_variation
        except:
            return "---"
    get_product_variation.short_description = 'Product Variation'

    search_fields = ['lettering', 'id']






class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        'user_email',
        'get_amount',
        'timestamp',
        'id',
    ]

    def get_amount(self, obj):
        try:
            return str(obj.amount / 100.0) + ' USD'
        except:
            return "---"

        get_amount.short_description = 'Amount'

    search_fields = ['user_email', 'id']





class CommentAdmin(admin.ModelAdmin):
    list_display = [
        'user_email',
        'text',
        'visible',
        'id',
    ]
    list_filter = ['visible']
    search_fields = ['user_email', 'id']
    list_per_page = 50  # Limit items per page for better performance



admin.site.register(Category, CategoryAdmin)
admin.site.register(LetteringItemCategory, LetteringItemCategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductColor, ProductColorAdmin)
admin.site.register(ProductVariation, ProductVariationAdmin)
admin.site.register(LetteringItemVariation, LetteringItemVariationAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Comment, CommentAdmin)
