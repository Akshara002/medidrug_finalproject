from django.shortcuts import render
from . models import *
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from .models import Medicine,MedicineImage,Customer,User_tbl,CustomerCart,Ordernew,DeliveryDetail,Comments,Prescription,PrescriptionDeliveryDetail,MedicineRequest,Department,DeliveryArea,DeliveryOrder
from .forms import MedicineForm,MedicineImageForm,CustomerForm
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from django.db.models import Q
def viewPrescription(request):
    prescription=Prescription.objects.filter(user=request.session.get('userid'))
    return render(request,'customers/prescriptions.html',{"prescriptions":prescription})

def deletePrescription(request,pk):
    pres=Prescription.objects.get(id=pk)
    pres.delete()
    return redirect("/viewprescription")

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
def add_comment(request, medicine_id):
    if request.method == "POST":
        user_id=request.session.get('userid')
        user=get_object_or_404(User_tbl,id=user_id)
        medicine = get_object_or_404(Medicine, id=medicine_id)
        comt=Comments.objects.filter(user=user,medicine=medicine)
        if comt.exists():
            messages.error(request,"already comment had give to the midicine")
            return redirect("/customer")

        comment_text = request.POST.get("comment")
        rating = int(request.POST.get("rating"))
        verified = True  # Logic to check if user purchased
        sia = SentimentIntensityAnalyzer()
        def analyze_vader_sentiment(comment):
            sentiment_score = sia.polarity_scores(comment)["compound"]  # Ranges from -1 to 1

            if sentiment_score > 0.05:
                return "Positive"
            elif sentiment_score < -0.05:
                return "Negative"
            else:
                return "Neutral"

        # Get user input
        user_comment = comment_text
        sentiment = analyze_vader_sentiment(user_comment)
        msg=""
        stat=""
        if sentiment=="Positive":
            stat="yes"
            msg="comment given to medicine is positive"
        else:
            stat="no"  
            msg="comment given to medicine is negative"  
        
        comments,create= Comments.objects.get_or_create(
            medicine=medicine,
            user=user,
            comment=comment_text,
            rating=rating,
            verified_buyer=verified,
            predict=sentiment,
            statue=stat
        )
        if create:
            messages.info(request,"comment add")
        else:
            messages.info(request,"already added comment")    
        return redirect('medicine_detail', medicine_id=medicine_id)

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
        msg=""
        if sentiment=="Positive":
            stat="yes"
            msg="comment given to medicine is positive"
        else:
            stat="no"  
            msg="comment given to medicine is negative"  
        Comments.objects.create(
            medicine=medi,comment=comments,predict=sentiment,statue=stat,
            useremail="user@example.com"
           
        )
        # Print result
        print(f"Sentiment: {sentiment}")
        #return render(request,'commentview.html',{"sentiments":sentiment})
        return render(request,'commentview.html',{"sentiments":msg})
        
    else:
        return redirect("/customer")
    
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
    messages.info(request, "Medicine deleted successfully!")
    return redirect("/cartview/")

def addtoCart(request):
    if request.method=="POST":
        quantity=request.POST.get("quantity")
        userid=request.session.get("userid")
        user=User_tbl.objects.get(id=userid)
        medicineid=request.session.get("medicineid")
        medicine=Medicine.objects.get(id=medicineid)
        if medicine.is_low_stock():

            messages.info(request, "Medicine is low stock")
            return redirect("customer") 
        
        medicine.stock=medicine.stock-int(quantity)
        medicine.save()
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
        email=request.POST.get("email")
        password=request.POST.get("password")
        user=User_tbl.objects.filter(email=email,password=password).first()
        if user:
            request.session['userid']=user.id
            request.session['username']=user.name
            if user.role=="customer":
              return redirect("/customer")
            elif user.role=="supplier":
                return redirect("/supplier")
            elif user.role=="delivery":
                return redirect("/delivery")
        else:
            return render(request,'customers/login.html',{"message":"Invalid Login"})

    return render(request,'customers/login.html',{"message":""})
def logout(request):
     request.session['userid']=""
     request.session['username']=""
     messages.info(request,"Successfully Logout")
     return redirect("/login")
def customer(request):
     userid=request.session.get("userid")
     query=request.GET.get('q','')

     usertbl=User_tbl.objects.get(id=userid)
     medicines=Medicine.objects.all()
     if query:
         medicines=medicines.filter(name__icontains=query
                                    )|medicines.filter(department=query)
     comments=Comments.objects.filter(user=usertbl)
     try:
         return render(request,'customers/customer.html',{"users":usertbl,'medicines': medicines,"comments":comments})
     except usertbl.DoesNotExist:
         return redirect("/login")
def supplier(request):
     userid=request.session.get("userid")
     usertbl=User_tbl.objects.get(id=userid)
     medicines=Medicine.objects.all()
     medicinerequest=MedicineRequest.objects.order_by('-id').filter(supplier=usertbl)
     try:
         return render(request,'supplier/supplier.html',{"users":usertbl,'medicine_request': medicinerequest})
     except usertbl.DoesNotExist:
         return redirect("login")     
def delivery(request):
    userid=request.session.get('userid')
    try:
        if userid:
            user=get_object_or_404(User_tbl,id=userid)
            area=DeliveryArea.objects.filter(user=user)
            city=get_object_or_404(DeliveryArea,user=user)
            delivery_order=DeliveryOrder.objects.filter(user=user)
            
            query = request.GET.get('query', '').strip()
            status=request.POST.get('status', '').strip()
            deliveryid=request.POST.get('deliveryid','').strip()
            if status:
                delivery=get_object_or_404(DeliveryOrder,id=deliveryid)
                delivery.status=status 
                delivery.save()
            if query:
                print("query",query)
                delivery_order=delivery_order.filter(user__mobile__icontains=query
                                )|delivery_order.filter(order__cart__medicine__name__icontains=query
                                                        )|delivery_order.filter(order__id__icontains=query
                                                                                )| delivery_order.filter(status__icontains=query)
                
                    
            return render(request,'delivery/dashboard.html',{'area':area,'delivery':delivery_order})
    except Exception as e:
        messages.error(request,"something went wrong")
        return redirect("/login")       
    return render(request,'delivery/dashboard.html')
def register(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        contact = request.POST.get('phone')
        password = request.POST.get('password')
        role=request.POST.get("role")
        obj=User_tbl.objects.filter(email=email).first()
        if(obj):
            return render(request, 'customers/register.html', {'message': "email already existing"})
        # Create the User_tbl object
        User_tbl.objects.create(name=name, email=email, mobile=contact, password=password,role=role)
        return redirect("login")
        
        # Render the template with a success message
        # return render(request, 'customers/register.html', {'message': "Register successfully"})
    
    # If GET method, render the template with an empty message
    return render(request, 'customers/register.html', {'message': ""})
def index(request):
    query=request.GET.get('query', '').strip()
    medicines = Medicine.objects.all()
    smedicines = Medicine.objects.all()
    department=Department.objects.all()
    if query:
        smedicines=smedicines.filter(department=query)

    return render(request,'index.html',{"medicines":medicines,"departments":department,"smedicines":smedicines,})


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
    department=Department.objects.all()
    return render(request, 'medicines/search.html', {'medicines': medicines,"departments":department})
# List all medicines
def medicine_list(request):
    medicines = Medicine.objects.all()
    low_stock=Medicine.objects.filter(stock__lt=5)
    
    return render(request, 'medicines/medicine_list.html', {'medicines': medicines,"lowstocks":low_stock})
from .models import Medicine, Comments
from django.db.models import Avg
from django.core.paginator import Paginator

def medicine_detail(request, medicine_id):
    medicine = get_object_or_404(Medicine, id=medicine_id)
    comments_list = Comments.objects.filter(medicine=medicine).order_by('-created_at')
    paginator = Paginator(comments_list, 5)  # Show 5 comments per page
    page_number = request.GET.get('page')
    comments = paginator.get_page(page_number)
    request.session['medicineid']=medicine_id
    medi=MedicineImage.objects.select_related("medicine").filter(medicine=medicine)
    rating = comments_list.aggregate(Avg('rating'))['rating__avg'] or 0
    medicine.average_rating=float(rating)
    medicine.save()
    bad_comment_count = comments_list.filter(medicine=medicine,statue="no").count()
    offerprice=round(float(medicine.price)-(float(medicine.price)* int(medicine.offer) /100))
    context = {
        'medicine': medicine,
        'comments': comments,
        'rating': round(rating, 1),
        'bad_comment': bad_comment_count,
        "medicineimage":medi,
        'offerprice':offerprice,
    }
    return render(request, 'medicines/medicine_detail.html', context)
    # medicine = get_object_or_404(Medicine, id=medicine_id)
    # request.session['medicineid']=medicine_id
    # medi=MedicineImage.objects.select_related("medicine").filter(medicine=medicine)
   
    # comments=Comments.objects.filter(medicine=medicine)
    # bad_comment=Comments.objects.filter(medicine=medicine,statue="no").count()
    # return render(request, 'medicines/medicine_detail.html', {'medicine': medicine,"medicineimage":medi,"comments":comments,"bad_comment":bad_comment})
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
    department=Department.objects.all()
    return render(request, 'medicines/add_medicine.html', {'form': form,"departments":department})

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



def add_medicine_request(request):
    if request.method == "POST":
        medicinename = request.POST.get("medicinename")
        quantity = request.POST.get("quantity")
        companyname = request.POST.get("companyname")
        description = request.POST.get("description")
        type = request.POST.get("type")
        status = request.POST.get("status")

        # Get or create the MedicineRequest object
        medicine, created = MedicineRequest.objects.get_or_create(
            medicinename=medicinename,
            defaults={
                "quantity": quantity,
                "companyname": companyname,
                "description": description,
                "type": type,
                "status": status,
            }
        )

        if created:
            message = "New Medicine Request Created Successfully!"
        else:
            message = "Medicine Request Already Exists!"
        messages.success(request,message)
        return redirect("/supplier")

    return render(request, "medicine_form.html")

def update_status(request, medicine_id):
    if request.method == "POST":
        medicine = get_object_or_404(MedicineRequest, id=medicine_id)
        new_status = request.POST.get("status")
        medicine.status = new_status
        medicine.save()
        messages.info(request,"Status Updated Successfully")
    return redirect("/supplier") 
def delete_medicinerequest(request, medicine_id):
    try:
        medicine = get_object_or_404(MedicineRequest, id=medicine_id)
        medicine.delete()
            
        messages.success(request,"data Deleted")
    except Exception as e:
        messages.error(request,"something  went wrong try again")    
    return redirect("/supplier") 
def profile(request):
    useremail=request.GET.get('useremail')
    user=User_tbl.objects.get(id=useremail)

    return render(request, 'customers/profile.html',{'users':user})
def about(request):
    return render(request, 'about.html')
def contact(request):
    return render(request, 'contact.html')
def submit_form(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        return HttpResponse(f"Thank you {name}, we have received your message!")
    return HttpResponse("Invalid request")
# def submit_form(request):
#     if request.method == "POST":
#         return HttpResponse("Form submitted successfully!")
#     else:
#         return HttpResponse("Invalid request method.")
import requests

def search_drug(request):
    query = request.GET.get('query', '')  # Get the search query from the user 
    data = None
    error = None

    if query:
        url = f"https://api.fda.gov/drug/label.json?search=openfda.brand_name:{query}&limit=1"
        try:
            response = requests.get(url)
            response.raise_for_status()
            results = response.json().get('results', [])

            if results:
                data = results[0]  # Fetch the first result
            else:
                error = "No medicine found."
        except requests.exceptions.RequestException:
            error = "Failed to fetch data from openFDA."

    return render(request, 'customers/medicine_search.html', {'query': query, 'data': data, 'error': error})
def medicineReturn(request, orderid):
    order = get_object_or_404(Ordernew, id=orderid)
    order.status = "Return"  # Use past tense for clarity
    order.save()
    
    messages.info(request, "Your refund will be processed after the medicine has been collected!")
    
    return redirect("/vieworder")
def addarea(request):
    userid=request.session.get('userid')
    user=get_object_or_404(User_tbl,id=userid)
    kerala_cities = [
    "Thiruvananthapuram", "Kochi", "Kozhikode", "Kollam", "Thrissur", "Palakkad", "Alappuzha", 
    "Kannur", "Kottayam", "Malappuram", "Pathanamthitta", "Idukki", "Wayanad", "Kasargod", 
    "Varkala", "Guruvayur", "Ponnani", "Chalakudy", "Attingal", "Kodungallur", "Nedumangad", 
    "Kunnamkulam", "Perinthalmanna", "Changanassery", "Thalassery", "Tirur", "Payyannur"
]
    if request.method=="POST":
        area=request.POST.get('area')
        company=request.POST.get('company')
        address=request.POST.get('address')
        deliveryarea,create=DeliveryArea.objects.get_or_create(
            area=area,
            company=company,
            address=address,
            user=user
        )
        if create:
            messages.info(request,"Detail is successfully registered!")
            return redirect("/delivery")
        else:
           
            messages.info(request,"Detail is already registered!")
            return redirect("/delivery")
    return render(request,'delivery/addarea.html',{'keralacities':kerala_cities})

def  area_delete(request,areaid):
    area=DeliveryArea.objects.get(id=areaid)
    area.delete()
    return redirect("/delivery")

def prescriptiondelivery(request):
    query=request.GET.get('query','').strip()
    status=request.POST.get('status')
    userid=request.session.get('userid')
    user=get_object_or_404(User_tbl,id=userid)
    area=get_object_or_404(DeliveryArea,user=user)
    perscription=PrescriptionDelivery.objects.order_by('-id').filter(delivery_company=area)
    if query:
        perscription=perscription.filter(delivery__user__mobile__icontains=query
                                         )|perscription.filter(delivery__prescription__status__icontains=query)
    if status:
        pre=get_object_or_404(PrescriptionDeliveryDetail,id=request.POST.get('deliveryid'))  
        pre.prescription.status=status 
        pre.prescription.save()
        pre.status=status
        pre.save()
        messages.info(request,"Status Updated successfully")
        return redirect("/deliveryprescription/")
    return render(request,'delivery/prescription.html',{"delivery":perscription})

def returnprescription(request,pk):
    pre=get_object_or_404(Prescription,id=pk)
    pre.status="ReturnOrder"
    pre.save()
    messages.info(request,"Your refund will be processed after the medicine has been collected!")
    return redirect("/viewprescription")
