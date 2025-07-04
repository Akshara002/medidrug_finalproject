from django.db import models

# Create your models here.
from django.db import models
from django.utils.timezone import now


    

    
class Medicine(models.Model):
    name = models.CharField(max_length=200)
    average_rating=models.DecimalField(max_digits=3,decimal_places=2)
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
    role=models.CharField(max_length=100,default="customer")
    is_Active=models.BooleanField(default=False)
    def __str__(self):
        return f"Name:{self.name}-Role:{self.role}"
    


class CustomerCart(models.Model):
    user = models.ForeignKey(User_tbl, on_delete=models.CASCADE,related_name="user_cart")
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE,related_name="medicine_cart")
    total=models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=1)
    status=models.CharField(max_length=100)

    def total_price(self):
        return self.quantity * self.medicine.price    
    def __str__(self):
        return self.medicine.name 
    
    

class Order(models.Model):
    user = models.ForeignKey(User_tbl, on_delete=models.CASCADE,related_name="user_order")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=[("Pending", "Pending"), ("Completed", "Completed"),("Paid","Paid")], default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)
    deliverydate=models.CharField(max_length=100,default="with in 24hour",null=True, blank=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.name}"    


class Ordernew(models.Model):
    user = models.ForeignKey(User_tbl, on_delete=models.CASCADE,related_name="user_order_new")
    cart=models.ForeignKey(CustomerCart, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    qty=models.CharField(max_length=100)
    status = models.CharField(max_length=50, choices=[("Pending", "Pending"), ("Completed", "Completed"),("Return","return"),("ReturnCompleted","returncompleted")], default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order id:{self.id} by {self.user.name} item:{self.cart.medicine.name}"      

class DeliveryDetail(models.Model):
    user = models.ForeignKey(User_tbl, on_delete=models.CASCADE,related_name="user_delivery")
    order=models.ForeignKey(Order, on_delete=models.CASCADE,related_name="order_delivery")
    houseno=models.CharField(max_length=100)
    street=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    country=models.CharField(max_length=100)
    zipcode=models.CharField(max_length=100)
    landmark=models.CharField(max_length=100)
    companyname=models.CharField(max_length=100,default="companyname")
    created_at = models.DateTimeField(auto_now_add=True)
    deliverydate=models.CharField(max_length=100,default="with in 48 hour")
    def __str__(self):
        return f"delivery Area {self.city} for {self.user.name}"   

class Payment(models.Model):
    user=models.ForeignKey(User_tbl, on_delete=models.CASCADE,related_name="user_payment")
    order=models.ForeignKey(Ordernew, on_delete=models.CASCADE,related_name="order_payment")
    status=models.CharField(max_length=100,default="payment")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"delivery {self.id} by {self.user.name}"   
class Comments(models.Model):
    medicine = models.ForeignKey('Medicine', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User_tbl, on_delete=models.CASCADE,related_name="user_comment")
    comment = models.TextField()
    predict=models.CharField(max_length=100)
    rating = models.IntegerField(default=5)  # 1 to 5 stars
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)
    statue=models.CharField(max_length=100,default="")
    verified_buyer = models.BooleanField(default=False)
    

    def __str__(self):
        return f"{self.user.name} - {self.medicine.name}"  
    
class Prescription(models.Model):
    user=models.ForeignKey(User_tbl,on_delete=models.CASCADE,related_name="userprescription") 
    created_at=models.DateField(auto_now=True) 
    prescription=models.FileField(upload_to="prescriptions/")
    status=models.CharField(max_length=100,default='start')  
    total_amount=models.CharField(max_length=100,default='0')
    remarks=models.TextField(max_length=200,default='no remarks')
    deliverydate=models.CharField(max_length=100,default='with in 48hours',blank=True)
    def __str__(self):
        return f"prescription id: {self.id} by {self.user.name} status:{self.status}" 
    
class DeliveryArea(models.Model):
    area=models.CharField(max_length=100) 
    company=models.CharField(max_length=100) 
    address=models.TextField(max_length=100)
    user=models.ForeignKey(User_tbl,on_delete=models.CASCADE) 
    def __str__(self):
        return f"id:{self.id}delivering Area:{self.area}-company:{self.company}-role:{self.user.role}"  
    
class PrescriptionDeliveryDetail(models.Model):
    user = models.ForeignKey(User_tbl, on_delete=models.CASCADE,related_name="user_pres_delivery")
    prescription=models.ForeignKey(Prescription, on_delete=models.CASCADE,related_name="presc_delivery")
    houseno=models.CharField(max_length=100)
    street=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    country=models.CharField(max_length=100)
    zipcode=models.CharField(max_length=100)
    landmark=models.CharField(max_length=100)
    status=models.CharField(max_length=100,default="pending")
    companyname=models.CharField(max_length=100,default="companyname")
    created_at = models.DateTimeField(auto_now_add=True)
    deliverydate=models.CharField(max_length=100,default="with in 48hours",null=True, blank=True)
    
    def __str__(self):
        return f"Id:{self.id} Prescription by {self.user.name} and its Status is {self.prescription.status}"   
    
class PrescriptionDelivery(models.Model):
    delivery_company=models.ForeignKey(DeliveryArea,on_delete=models.CASCADE,related_name="perscription_company")
    delivery=models.ForeignKey(PrescriptionDeliveryDetail,on_delete=models.CASCADE,related_name="perscription_delivery")  
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Prescription by {self.delivery.user.name} Status:{self.delivery.prescription.status} Assign By:{self.delivery_company.company}"       
    
class MedicineRequest(models.Model):
        STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Processing", "Processing"),
        ("Completed", "Completed"),
        ("Rejected", "Rejected"),
        ]
        Type_CHOICES = [
        ("order", "Order"),
        ("return", "Return"),
        
        ]
        medicinename=models.CharField(max_length=100)
        quantity=models.CharField(max_length=100)
        companyname=models.CharField(max_length=100)
        description=models.CharField(max_length=100)
        type=models.CharField(max_length=100, choices=Type_CHOICES, default="Request")
        status=models.CharField(max_length=100, choices=STATUS_CHOICES, default="Pending")
        medicine_date=models.DateTimeField(auto_now=True)
        supplier=models.ForeignKey(User_tbl,on_delete=models.CASCADE)
        def __str__(self):
            return f"Medicine Name:${self.medicinename}-status ${self.status}"
class Department(models.Model):
    department=models.CharField(max_length=100)
    def __str__(self):
        return f"department:{self.department}"

STATUS_delivery = [
        ("Pending", "Pending"),
        ("Processing", "Processing"),
        ("Delivered", "Delivered"),
        ("Rejected", "Rejected"),
        ("NoContact","NoContact"),

        ]
class DeliveryOrder(models.Model):
    user=models.ForeignKey(User_tbl,on_delete=models.CASCADE,related_name="user_deliv_order")
    area=models.ForeignKey(DeliveryArea,on_delete=models.CASCADE,related_name="deliv_area_order")
    order=models.ForeignKey(Ordernew,on_delete=models.CASCADE,related_name="order_delivery_order")
    delivery=models.ForeignKey(DeliveryDetail,on_delete=models.CASCADE,related_name="deliv_order_detail")
    status=models.CharField(max_length=100, choices=STATUS_delivery, default="Pending")
    def __str__(self):
        return f"Delivery{self.user.name}"

class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name="order_item_order")
    medicine=models.ForeignKey(Medicine,on_delete=models.CASCADE,related_name="order_medicine")
    total_qty=models.IntegerField()
    total_price=models.CharField(max_length=100)
     