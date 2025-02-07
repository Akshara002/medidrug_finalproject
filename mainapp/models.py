from django.db import models

# Create your models here.
from django.db import models
from django.utils.timezone import now


    

    
class Medicine(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    expiry_date = models.DateField()
    department=models.CharField(max_length=100)
    description=models.CharField(max_length=100)
    offer=models.CharField(max_length=100)
    image= models.ImageField(upload_to='medicine_images/', null=True, blank=True)

    def is_expired(self):
        return self.expiry_date < now().date()

    def is_low_stock(self):
        return self.stock < 5  # Alert when stock is below 5

    def __str__(self):
        return self.name



class MedicineImage(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name="Medicine")
    image = models.ImageField(upload_to="medicine_images/")

    def __str__(self):
        return f"Image for {self.medicine.name}"

class Customer(models.Model):
    name=models.CharField(max_length=100)
    contact=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    password=models.CharField(max_length=100)
    def __str__(self):
        return self.name
class User_tbl(models.Model):
    name=models.CharField(max_length=100)
    mobile=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user = models.ForeignKey(User_tbl, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.quantity * self.medicine.price

class CustomerCart(models.Model):
    user = models.ForeignKey(User_tbl, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    total=models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=1)
    status=models.CharField(max_length=100)

    def total_price(self):
        return self.quantity * self.medicine.price    

class Order(models.Model):
    user = models.ForeignKey(User_tbl, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=[("Pending", "Pending"), ("Completed", "Completed")], default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"    


class Ordernew(models.Model):
    user = models.ForeignKey(User_tbl, on_delete=models.CASCADE)
    cart=models.ForeignKey(CustomerCart, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    qty=models.CharField(max_length=100)
    status = models.CharField(max_length=50, choices=[("Pending", "Pending"), ("Completed", "Completed")], default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"      

class DeliveryDetail(models.Model):
    user = models.ForeignKey(User_tbl, on_delete=models.CASCADE)
    order=models.ForeignKey(Ordernew, on_delete=models.CASCADE)
    houseno=models.CharField(max_length=100)
    street=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    country=models.CharField(max_length=100)
    zipcode=models.CharField(max_length=100)
    landmark=models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"delivery {self.id} by {self.user.username}"   

class Payment(models.Model):
    user=models.ForeignKey(User_tbl, on_delete=models.CASCADE)
    order=models.ForeignKey(Ordernew, on_delete=models.CASCADE)
    status=models.CharField(max_length=100,default="payment")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"delivery {self.id} by {self.user.username}"   
class Comments(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name="Medicinecomment")
    comment=models.TextField(max_length=100)
    predict=models.CharField(max_length=100)
    statue=models.CharField(max_length=100)
    useremail=models.CharField(max_length=100)
    created_at=models.DateField(auto_now=True)
    def __str__(self):
        return f"comments {self.id} by {self.medicine.name}"   
class Prescription(models.Model):
    user=models.ForeignKey(User_tbl,on_delete=models.CASCADE,related_name="userprescription") 
    created_at=models.DateField(auto_now=True) 
    prescription=models.FileField(upload_to="prescriptions/")
    status=models.CharField(max_length=100,default='start')  
    total_amount=models.CharField(max_length=100,default='0')
    remarks=models.TextField(max_length=200,default='no remarks')
    def __str__(self):
        return f"prescription {self.id} by {self.user.name}" 

class PrescriptionDeliveryDetail(models.Model):
    user = models.ForeignKey(User_tbl, on_delete=models.CASCADE)
    prescription=models.ForeignKey(Prescription, on_delete=models.CASCADE)
    houseno=models.CharField(max_length=100)
    street=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    country=models.CharField(max_length=100)
    zipcode=models.CharField(max_length=100)
    landmark=models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"delivery {self.id} by {self.user.username}"      