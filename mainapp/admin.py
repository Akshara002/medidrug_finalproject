from django.contrib import admin
from . models import Medicine,MedicineImage,CustomerCart,Prescription
# Register your models here.
admin.site.register(Medicine)
admin.site.register(MedicineImage)
admin.site.register(CustomerCart)
admin.site.register(Prescription)