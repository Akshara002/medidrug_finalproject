from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Medicine,MedicineImage,Customer,User_tbl,CustomerCart,Ordernew,DeliveryDetail,Comments,Prescription,PrescriptionDeliveryDetail
from .forms import MedicineForm,MedicineImageForm,CustomerForm
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from django.db.models import Q
def viewPrescription(request):
    prescription=Prescription.objects.filter(user=request.session.get('userid'))
    return render(request,'customers/prescriptions.html',{"prescriptions":prescription})
def prescriptionUpload(request):
    if request.method=="POST":
        prescription=request.FILES.get('prescription')
        user=User_tbl.objects.get(id=request.session.get('userid'))
        pres=Prescription.objects.create(user=user,prescription=prescription)
        request.session['prescriptionid']=pres.id
    else:    
        prescription=Prescription.objects.order_by('-created_at').filter(user=request.session.get('userid'))
        return render(request,'customers/prescriptions.html',{"prescriptions":prescription})
    return redirect('/viewprescription')
def comments(request):
    if request.method=="POST":
        comments=request.POST.get('comment')
        medicineid=request.POST.get("medicineid")
        medi=Medicine.objects.get(id=medicineid)
        

        # Initialize Sentiment Analyzer
        sia = SentimentIntensityAnalyzer()

        # Function to analyze sentiment
        def analyze_vader_sentiment(comment):
            sentiment_score = sia.polarity_scores(comment)["compound"]  # Ranges from -1 to 1

            if sentiment_score > 0.05:
                return "Positive"
            elif sentiment_score < -0.05:
                return "Negative"
            else:
                return "Neutral"

        # Get user input
        user_comment = comments
        sentiment = analyze_vader_sentiment(user_comment)
        Comments.objects.create(
            medicine=medi,comment=comments,predict=sentiment,statue="no",
            useremail="user@example.com"
           
        )
        # Print result
        print(f"Sentiment: {sentiment}")
        return render(request,'commentview.html',{"sentiments":sentiment})
    return render(request,'commentview.html',{"sentiments":""})
def sendOTP(request):

    return render(request,'comments.html')
def viewOrder(request):
    user=User_tbl.objects.get(id=request.session.get('userid'))
    order=Ordernew.objects.select_related('user','cart').filter(user=user)
    return render(request,'customers/vieworder.html',{"orders":order})
def Checkout(request):
    if request.method=="POST":
        orderid=request.session.get('orderid')
        userid=request.session.get('userid')
        user=User_tbl.objects.get(id=userid)
        order=Ordernew.objects.get(id=orderid)
        houseno=request.POST.get("houseno")
        street=request.POST.get("street")
        city=request.POST.get("city")
        state=request.POST.get("state")
        country=request.POST.get("country")
        zipcode=request.POST.get("zipcode")
        DeliveryDetail.objects.create(
            order=order,user=user,
            houseno=houseno,
            street=street,
            city=city,
            state=state,
            country=country,
            zipcode=zipcode
        )
    return redirect("customer")    

        
        
    
def prescriptionCheckout(request):
    if request.method=="POST":
        prescriptionid=request.session.get('prescriptionid')
        userid=request.session.get('userid')
        user=User_tbl.objects.get(id=userid)
        prescription=Prescription.objects.get(id=prescriptionid)
        prescription.status="Payment Completed"
        prescription.save()
        houseno=request.POST.get("houseno")
        street=request.POST.get("street")
        city=request.POST.get("city")
        state=request.POST.get("state")
        country=request.POST.get("country")
        zipcode=request.POST.get("zipcode")
        PrescriptionDeliveryDetail.objects.create(
            prescription=prescription,user=user,
            houseno=houseno,
            street=street,
            city=city,
            state=state,
            country=country,
            zipcode=zipcode
        )
        return redirect("/viewprescription")
    return render(request,'customers/prescriptioncheckout.html')    

        
        
    
def  order(request):
    if request.method=="GET":
        cartid=request.GET.get("cartid")
        qty=request.GET.get("qty")
        cartitem=CustomerCart.objects.select_related('medicine').filter(id=cartid).first()
        totalamount=float(qty)*float(cartitem.medicine.price)
        user=User_tbl.objects.get(id=request.session.get('userid'))
        order= Ordernew.objects.create(
            user=user,total_amount=totalamount,qty=qty,cart=cartitem
            
        )
        print(order.id)
        request.session['orderid']=order.id
        cartitem.status="order"
        cartitem.save()
        orderdetail=Ordernew.objects.select_related('user','cart').get(id=order.id)
    return  render(request,'customers/checkout.html',{"orders":order})
def cartDelete(request,itemid):
    cart= get_object_or_404(CustomerCart,id=itemid)
    cart.delete()
    messages.success(request, "Medicine deleted successfully!")
    return redirect("cartview")

def addtoCart(request):
    if request.method=="POST":
        quantity=request.POST.get("quantity")
        userid=request.session.get("userid")
        user=User_tbl.objects.get(id=userid)
        medicineid=request.session.get("medicineid")
        medicine=Medicine.objects.get(id=medicineid)
        CustomerCart.objects.create(
            user=user,medicine=medicine,quantity=quantity
        )
        return redirect("viewCart")
    else:
        return  redirect("customer")
       
def viewCart(request):
    userid=request.session.get("userid")
    user=User_tbl.objects.get(id=userid)
    obj=CustomerCart.objects.select_related("medicine","user").filter(~Q(status="order"),user=user)
   
        
    return render(request,'customers/cartview.html',{'cart':obj})
    
def login(request):
    if request.method=="POST":
        email=request.POST.get("eml")
        password=request.POST.get("password")
        user=User_tbl.objects.filter(email=email,password=password).first()
        if user:
            request.session['userid']=user.id
            request.session['username']=user.name
            return redirect("customer")
        else:
            return render(request,'customers/login.html',{"message":"Invalid Login"})

    return render(request,'customers/login.html',{"message":""})
def customer(request):
     userid=request.session.get("userid")
     usertbl=User_tbl.objects.get(id=userid)
     medicines=Medicine.objects.all()
     try:
         return render(request,'customers/customer.html',{"users":usertbl,'medicines': medicines})
     except usertbl.DoesNotExist:
         return redirect("login")

def register(request):
    if request.method == "POST":
        name = request.POST.get('fname')
        email = request.POST.get('eml')
        contact = request.POST.get('mobile')
        password = request.POST.get('password')
        obj=User_tbl.objects.filter(email=email).first()
        if(obj):
            return render(request, 'customers/register.html', {'message': "email already existing"})
        # Create the User_tbl object
        User_tbl.objects.create(name=name, email=email, mobile=contact, password=password)
        return redirect("login")
        
        # Render the template with a success message
        # return render(request, 'customers/register.html', {'message': "Register successfully"})
    
    # If GET method, render the template with an empty message
    return render(request, 'customers/register.html', {'message': ""})
def index(request):
    medicines = Medicine.objects.all()

    return render(request,'index.html',{"medicines":medicines})


def search_medicine(request):
    medicines = Medicine.objects.all()

    name = request.GET.get('name', '')
    department = request.GET.get('department', '')
    expiry_date = request.GET.get('expiry_date', '')

    if name:
        medicines = medicines.filter(name__icontains=name)
    if department:
        medicines = medicines.filter(department__icontains=department)
    if expiry_date:
        medicines = medicines.filter(expiry_date=expiry_date)

    return render(request, 'medicines/search.html', {'medicines': medicines})
# List all medicines
def medicine_list(request):
    medicines = Medicine.objects.all()
    low_stock=Medicine.objects.filter(stock__lt=5)
    
    return render(request, 'medicines/medicine_list.html', {'medicines': medicines,"lowstocks":low_stock})

def medicine_detail(request, medicine_id):
    medicine = get_object_or_404(Medicine, id=medicine_id)
    request.session['medicineid']=medicine_id
    medi=MedicineImage.objects.select_related("medicine").filter(medicine=medicine)
   
    comments=Comments.objects.filter(medicine=medicine)
    return render(request, 'medicines/medicine_detail.html', {'medicine': medicine,"medicineimage":medi,"comments":comments})
# Add a new medicine
def add_medicine(request):
    if request.method == "POST":
        form = MedicineForm(request.POST, request.FILES)
        images = request.FILES.getlist('images')  # Get multiple images

        if form.is_valid():
            medicine = form.save()

            for img in images:
                MedicineImage.objects.create(medicine=medicine, image=img)

            return redirect('medicine_list')  # Redirect to the medicine list page

    else:
        form = MedicineForm()
    
    return render(request, 'medicines/add_medicine.html', {'form': form})

# Update medicine details
def update_medicine(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    if request.method == 'POST':
        form = MedicineForm(request.POST, request.FILES, instance=medicine)
        if form.is_valid():
            form.save()
            messages.success(request, "Medicine updated successfully!")
            return redirect('medicine_list')
    else:
        form = MedicineForm(instance=medicine)
    return render(request, 'medicines/update_medicine.html', {'form': form})

# Delete medicine
def delete_medicine(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    medicine.delete()
    messages.success(request, "Medicine deleted successfully!")
    return redirect('medicine_list')
