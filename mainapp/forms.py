from django import forms
from .models import Medicine,MedicineImage,Customer,Department

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

