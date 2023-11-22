# watches/admin.py
from django.contrib import admin
from .models import Watch, Order, OrderItem, Cart, CartItem,Contact
from users.models import UserDetail
from django.utils.html import format_html

# Register your models here.

class WatchAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_featured')
    search_fields = ('name', 'description')
    list_filter = ('is_featured',)

class WatchAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'is_featured', 'display_image')
    search_fields = ('name', 'description')
    list_filter = ('is_featured',)

    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" />', obj.image.url)
        return ''
    
    display_image.allow_tags = True
    display_image.short_description = 'Image Preview'


class OrderItemInline(admin.TabularInline): 
    model = OrderItem
    extra = 0
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user' ,'created_at', 'total_price', 'status', 'payment_successful')
    search_fields = ('user__username', 'order_uuid')
    list_filter = ('status', 'payment_successful')
    inlines = [OrderItemInline]
    readonly_fields = ('get_username', 'get_email', 'get_name', 'get_address', 'get_phone_number')  # Add read-only fields here

    def get_username(self, obj):
        return obj.user.username if obj.user else ''
    get_username.short_description = 'Username'

    def get_email(self, obj):
        return obj.user.email if obj.user else ''
    get_email.short_description = 'Email'

    def get_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}" if obj.user else ''
    get_name.short_description = 'Name'

    def get_address(self, obj):
        user_detail = UserDetail.objects.filter(user=obj.user).first()
        return user_detail.address if user_detail else ''
    get_address.short_description = 'Address'

    def get_phone_number(self, obj):
        user_detail = UserDetail.objects.filter(user=obj.user).first()
        return user_detail.phone_number if user_detail else ''
    get_phone_number.short_description = 'Phone Number'



class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'watch', 'quantity', 'total_price')
    search_fields = ('order__order_uuid', 'watch__name')

class ContAdmin(admin.ModelAdmin):
    list_display=('name','email','subject','message','date')
    search_fields=('name','email','subject','message','date')
    
    #list_editable=(' ',)


admin.site.register(Watch, WatchAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Contact,ContAdmin)