from django import forms
from .models import Medicine,MedicineImage,Customer,Department,DeliveryDetail, DeliveryArea,PrescriptionDeliveryDetail

class MedicineForm(forms.ModelForm):
    image = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': False}), required=False)
    department = forms.ModelChoiceField(queryset=Department.objects.all(), widget=forms.Select, empty_label="Select a Department")

    class Meta:
        model = Medicine
        fields = ['name', 'category', 'price', 'stock', 'expiry_date', 'department', 'description', 'offer', 'image']


class MedicineImageForm(forms.ModelForm):
    images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': False}), required=False)

    class Meta:
        model = MedicineImage
        fields = ['images']

class CustomerForm(forms.ModelForm):
     class Meta:
         model=Customer
         fields=['name','contact','email','password']




class DeliveryDetailForm(forms.ModelForm):
    companyname = forms.ChoiceField(choices=[])

    class Meta:
        model = DeliveryDetail
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(DeliveryDetailForm, self).__init__(*args, **kwargs)
        companies = DeliveryArea.objects.values_list('company', flat=True).distinct()
        self.fields['companyname'].choices = [(company, company) for company in companies]

class PrescriptionDeliveryDetailForm(forms.ModelForm):
    companyname = forms.ChoiceField(choices=[])

    class Meta:
        model = PrescriptionDeliveryDetail
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(PrescriptionDeliveryDetailForm, self).__init__(*args, **kwargs)
        companies = DeliveryArea.objects.values_list('company', flat=True).distinct()
        self.fields['companyname'].choices = [(company, company) for company in companies]