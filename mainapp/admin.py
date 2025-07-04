from django.contrib import admin
from .models import *
from .forms import DeliveryDetailForm,PrescriptionDeliveryDetailForm

class DeliveryDetailAdmin(admin.ModelAdmin):
    form = DeliveryDetailForm

admin.site.register(DeliveryDetail, DeliveryDetailAdmin)

class PrescriptionDeliveryDetailAdmin(admin.ModelAdmin):
    form = PrescriptionDeliveryDetailForm

admin.site.register(PrescriptionDeliveryDetail, PrescriptionDeliveryDetailAdmin)

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "stock", "expiry_date", "department", "offer")
    list_filter = ("category", "department", "expiry_date", "stock")

@admin.register(MedicineImage)
class MedicineImageAdmin(admin.ModelAdmin):
    list_display = ("medicine", "image")
    list_filter = ("medicine",)

@admin.register(User_tbl)
class UserAdmin(admin.ModelAdmin):
    list_display = ("name", "mobile", "email", "role")
    list_filter = ("role",)

# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ("user", "total_amount", "status", "created_at")
#     list_filter = ("status", "created_at")

@admin.register(Ordernew)
class OrdernewAdmin(admin.ModelAdmin):
    list_display = ("user","cart", "total_amount", "qty", "status", "created_at")
    list_filter = ("status", "created_at")

# @admin.register(DeliveryDetail)
# class DeliveryDetailAdmin(admin.ModelAdmin):
#     list_display = ("user", "order", "city", "state", "country", "zipcode")
#     list_filter = ("city", "state", "country")

@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ("medicine", "user", "rating", "likes", "verified_buyer")
    list_filter = ("rating", "verified_buyer")

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ("id","user", "created_at", "status", "total_amount", "remarks","deliverydate")
    list_filter = ("status", "created_at")

@admin.register(MedicineRequest)
class MedicineRequestAdmin(admin.ModelAdmin):
    list_display = ("medicinename", "quantity", "companyname", "type", "status", "medicine_date")
    list_filter = ("status", "type", "medicine_date")

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("department",)
    list_filter = ("department",)
@admin.register(DeliveryArea)
class AreaAdmin(admin.ModelAdmin):
    list_display=("id","area","company","user")    
    list_filter=("area","user")

# @admin.register(DeliveryOrder)
# class DelivaryorderAdmin(admin.ModelAdmin):
#     list_display=("order","area","user","status")    
#     list_filter=("area","user","order")
# @admin.register(PrescriptionDeliveryDetail)  
# class PrescriptionDeliveryDetailAdmin(admin.ModelAdmin):
#     list_display=("id","user","status","created_at")  
#     list_filter=("created_at","user","status")
# @admin.register(PrescriptionDelivery)
# class PrescriptionDeliveryAdmin(admin.ModelAdmin):
#     list_display=("id","delivery","delivery_company","created_at",)
#     list_filter=("created_at","delivery","delivery_company")
class OrderAdmin(admin.ModelAdmin):
    list_display=("id","user","total_amount","created_at")
    list_filter=("user","id")

admin.site.register(Order,OrderAdmin) 
class OrderItemAdmin(admin.ModelAdmin):
    list_display=("id","order","total_qty","total_price")
admin.site.register(OrderItem,OrderItemAdmin)
class CustomerCartAdmin(admin.ModelAdmin):
    list_display=("id","medicine","total","quantity","status")
admin.site.register(CustomerCart,CustomerCartAdmin)