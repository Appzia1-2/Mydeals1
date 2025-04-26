from .models import *
from django import forms

class adminform(forms.Form):
    username=forms.CharField(max_length=50)
    password=forms.CharField()


from django.core.exceptions import ValidationError
from .models import CustomUser  # Make sure to import your CustomUser model

class CustomUserRegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        label='Confirm Password'
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        label='Email'
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']  # Add email to fields list
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username__iexact=username).exists():
            raise ValidationError("A user with this username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match.")
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Hash the password
        user.email = self.cleaned_data['email']  # Save the email
        if commit:
            user.save()
        return user



class CustomUserProfileForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        label='Email'
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone', 'address', 'dob', 'nationality', 'gender', 'image','whatsapp']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Address'}),
            'dob': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Date of Birth', 'type': 'date'}),
            'nationality': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nationality'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username__iexact=username).exclude(pk=self.instance.pk).exists():
            raise ValidationError("A user with this username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError("A user with this email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        # Save the updated profile fields
        if commit:
            user.save()
        return user

from django import forms
from django.contrib.auth.forms import AuthenticationForm

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        label='Username'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        label='Password'
    )


from django import forms
from django.core.exceptions import ValidationError
from oman_app.models import CustomUser  # Adjusted import to reference your custom user model
from django.contrib.auth.forms import PasswordResetForm

class CustomPasswordResetForm(PasswordResetForm):
    username = forms.CharField(max_length=150, required=True, label="Username")
    
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        username = cleaned_data.get("username")

        # Check if a user with both the email and username exists
        if email and username:
            try:
                user = CustomUser.objects.get(email=email, username=username)  # Use CustomUser model
            except CustomUser.DoesNotExist:
                raise ValidationError("No user found with the provided email and username combination.")
        return cleaned_data

class nearbylocationForm(forms.ModelForm):
    class Meta:
        model = NearbyLocation
        fields = '__all__'

class mainamenitiesForm(forms.ModelForm):
    class Meta:
        model = MainAmenities
        fields = '__all__'

class additionalamenitiesForm(forms.ModelForm):
    class Meta:
        model = AdditionalAmenities
        fields = '__all__'


from django import forms
from .models import Land, NearbyLocation

class LandForm(forms.ModelForm):
    nearby_location = forms.ModelMultipleChoiceField(
        queryset=NearbyLocation.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    class Meta:
        model = Land
        fields = [
            'property_title', 
            'price', 
            'plot_area', 
            'description', 
            'regions',
            'cities',
            'latitude',
            'longitude',
            'images',
            'listing_type',  
            'zoned_for',
            'lister_type',  
            'property_mortgage',
            'facade',
            'rental_period',
            'nearby_location',  # Added nearby locations
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'listing_type': forms.Select(choices=Land.LISTING_TYPE_CHOICES),
        }



class Villaform(forms.ModelForm):
    nearby_location = forms.ModelMultipleChoiceField(
        queryset=NearbyLocation.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    main_amenities = forms.ModelMultipleChoiceField(
        queryset=MainAmenities.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    additional_amenities = forms.ModelMultipleChoiceField(
        queryset=AdditionalAmenities.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    class Meta:
        model = Villa
        fields = [
            'property_title', 
            'price', 
            'plot_area',
            'surface_area', 
            'bedrooms',
            'bathrooms',
            'description',
            'building',  # Added building age
            'regions',
            'cities',
            'latitude',
            'longitude', 
            'lister_type',  # Added Agent or Landlord selection
            'property_mortgage',  # Added mortgage Yes/No
            'facade',  # Added facade choices
            'furnished',  # Added furnished choice
            'images',
            'listing_type',
            'rental_period',
            'nearby_location',
            'additional_amenities',
            'main_amenities',
            'floors',
        ]
        
class categoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class jobcategoryForm(forms.ModelForm):
    class Meta:
        model = JobCategory
        fields = '__all__'

class advertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = '__all__'

class userForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = '__all__'

class regionForm(forms.ModelForm):
    class Meta:
        model = Region
        fields = '__all__'

class cityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = '__all__'

class CommercialForm(forms.ModelForm):
    nearby_location = forms.ModelMultipleChoiceField(
        queryset=NearbyLocation.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    main_amenities = forms.ModelMultipleChoiceField(
        queryset=MainAmenities.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    additional_amenities = forms.ModelMultipleChoiceField(
        queryset=AdditionalAmenities.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    class Meta:
        model = Commercial
        fields = [
            'property_title',
            'price',
            'plot_area',
            'description',
            'regions',
            'cities',
            'latitude',
            'longitude',
           
            'images',
            'listing_type',  # Add this field
            
            'furnished',  # Added furnished choice
            'property',
           
             
            'lister_type',  # Added Agent or Landlord selection
            
            'property_mortgage',  # Added mortgage Yes/No
            'nearby_location',
            'additional_amenities',
            'main_amenities',
            'floors',
            
            'rental_period',
        ]

class FarmForm(forms.ModelForm):
    nearby_location = forms.ModelMultipleChoiceField(
        queryset=NearbyLocation.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    main_amenities = forms.ModelMultipleChoiceField(
        queryset=MainAmenities.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    additional_amenities = forms.ModelMultipleChoiceField(
        queryset=AdditionalAmenities.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    class Meta:
        model = Farm
        fields = [
            'property_title',
            'price',
            'surface_area',
            'plot_area',
            'regions',
            'cities',
            'latitude',
            'longitude',
            'description',
            'images',
            'listing_type',  # Add this field
            'bedrooms',
            'bathrooms',
            'building',  # Added building age
            'lister_type',  # Added Agent or Landlord selection
            'property_mortgage',  # Added mortgage Yes/No
            'facade',  # Added facade choices
            'furnished',  # Added furnished choice
            'nearby_location',
            'additional_amenities',
            'main_amenities',
            'rental_period',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class ChaletForm(forms.ModelForm):
    class Meta:
        model = Chalet
        fields = [
            'property_title',
            'price',
            'location',
            'plot_area',
            'bedrooms',
            'bathrooms',
            'description',
            'amenities',
            'regions',
            'cities',
            'latitude',
            'longitude',
            'proximity_to_activities',
            'tenancy_information',
            'contact_details',
            'additional_information',
            'listing_type',  # Add this field
            'images',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'amenities': forms.Textarea(attrs={'rows': 3}),
            'proximity_to_activities': forms.Textarea(attrs={'rows': 3}),
            'contact_details': forms.Textarea(attrs={'rows': 3}),
            'additional_information': forms.Textarea(attrs={'rows': 3}),
        }

class FashionForm(forms.ModelForm):
    class Meta:
        model = Fashion
        fields = [
            'brand', 
            'category', 
            'size', 
            'gender', 
            'color', 
            'material',
            'condition', 
            'price', 
            'location', 
            'description',
            'regions',
             'cities',
             'latitude',
             'longitude',
            'contact_details',  # Assuming you add 'contact_details' field for fashion items
            
            'images',
        ]

class ToysForm(forms.ModelForm):
    class Meta:
        model = Toys
        fields = [
            'category', 
            'product_name',
            'brand', 
            'platform', 
            'age_group', 
            'condition', 
            'price', 
            'location', 
            'images',
            'description',
            'regions',
            'cities',
            'latitude',
            'longitude',
           
        ]

class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = [
            'product_name',
            'product_type',
            'brand',
            'quantity',
            'expiration_date',
            'price',
            'location',
            'dietary_info',
            'images',
            'description',
            'regions',
            'cities',
            'latitude',
            'longitude',
        ]

class FitnessForm(forms.ModelForm):
    class Meta:
        model = Fitness
        fields = [
            'product_name',
            'category',
            'brand',
            'description',
            'regions',
            'cities',
            'latitude',
            'longitude',
            'condition',
            'price',
            'warranty_status',
            'location',
            'images',
            ]
        
class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['pet_type', 'breed', 'age', 'price', 'vaccinated', 'location', 'images','description','regions','cities','latitude','longitude','pet_name']

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['category', 'genre', 'condition', 'price', 'location', 'images','description',
            'regions',
            'cities',
            'latitude',
            'longitude',
            'book_name',]

class ApplianceForm(forms.ModelForm):
    class Meta:
        model = Appliance
        fields = ['appliance_type', 'brand', 'model_number', 'condition', 'warranty_status', 'price', 'location', 'images','regions','description',
            'cities',
            'latitude',
            'longitude',
            'product_name',]



class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = ['category', 'brand', 'condition', 'price', 'warranty_status', 'location', 'description','regions','cities','latitude','longitude','images']
        
class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['course_type', 'subject', 'duration', 'price', 'location', 'instructor_name', 'qualification', 'experience', 'description','regions','cities','latitude','longitude','images']
       

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['service_type', 'provider_name', 'price_range', 'contact_info', 'location', 'description','regions','cities','latitude','longitude','images']


class MobileForm(forms.ModelForm):
    class Meta:
        model = Mobile
        fields = [ 'brand', 'model_number', 'operating_system', 'screen_size',
            'storage_capacity', 'ram_size', 'battery_capacity', 
            'price', 'condition', 'location', 'description','images',
            'regions',
            'cities',
            'latitude',
            'longitude','product_name',]

       
class ComputerForm(forms.ModelForm):
    class Meta:
        model = Computer
        fields = [
          'brand', 'model_number', 'operating_system', 'screen_size',
            'storage_capacity', 'ram_size', 'processor', 'graphics_card', 
            'battery_life', 'price', 'condition', 'location','images','description',
            'regions',
            'cities',
            'latitude',
            'longitude','product_name',
        ]
        

class SoundForm(forms.ModelForm):
    class Meta:
        model = Sound
        fields = [
            'brand', 'model_number', 'connectivity', 'output_power',
            'channels', 'has_smart_assistant', 'price', 'condition',
            'location','images','description',
            'regions',
            'cities',
            'latitude',
            'longitude','product_name'
        ]
       
class CompanyRegistrationForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['company_name', 'company_type', 'trade_license', 'contact_name', 'logo', 'website', 'description','company_size','email','industry','phone','instagram','youtube','linkedin','facebook','regions',
             'cities',
             'latitude',
             'longitude']
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.user = self.user  # Assign the logged-in user
        if commit:
            instance.save()
        return instance



class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPost
        fields = [
            "title", "description", "job_type", "job_category", 
            "salary_range", "work_location", "number_of_vacancies", 
            "contact_email", "qualifications", "skills_required", 
            "experience_required", "application_deadline", "working_hours","cities","regions"
        ]
        widgets = {
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
            "qualifications": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "skills_required": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "application_deadline": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        }


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['name', 'email', 'phone', 'resume']
        widgets = {
            'name': forms.TextInput(attrs={
                'id': 'name', 
                'name': 'name', 
                'required': True, 
                'type': 'text'
            }),
            'email': forms.EmailInput(attrs={
                'id': 'email', 
                'name': 'email', 
                'required': True, 
                'type': 'email'
            }),
            'phone': forms.TextInput(attrs={
                'id': 'phone', 
                'name': 'phone', 
                'type': 'text'
            }),
            'resume': forms.ClearableFileInput(attrs={
                'id': 'resume', 
                'name': 'resume', 
                'type': 'file'
            }),
        }
        labels = {
            'name': 'Full Name',
            'email': 'Email',
            'phone': 'Phone Number',
            'resume': 'Upload Resume',
        }



import os
    
class ChatForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['message']



from django import forms
from .models import Automobile, Motorcycle, AutoAccessoryPart, HeavyVehicle, Boat, NumberPlate







class CarForm(forms.ModelForm):
    class Meta:
        model = Automobile
        fields = [
            # Basic information
            'name', 'make', 'year', 'body_type', 'condition','rental_period',
            
            # Technical specifications
            'fuel_type', 'engine_capacity', 'transmission', 
            'regional_spec', 'number_of_seats', 'vin_chassis_number',
            
            # Appearance
            'exterior_color',
            
            # Pricing and listing
            'price', 'listing_type',
            
            # Location
            'regions', 'cities', 'latitude', 'longitude', 'location',
            
            # Additional information
            'description', 'warranty_status',
            
            # Media
            'images'
        ]
        # You might want to add widgets or labels for better UX

class BikeForm(forms.ModelForm):
    class Meta:
        model = Motorcycle
        fields = [
            'name', 'make', 'model', 'year', 'body_type', 
            'engine_capacity', 'price', 'condition', 'description', 
            'regions', 'cities', 'latitude', 'longitude', 'location', 'images', 'listing_type'
        ]

class AccessoryForm(forms.ModelForm):
    class Meta:
        model = AutoAccessoryPart
        fields = [
            'name', 'description', 'price', 'regions', 
            'cities', 'latitude', 'longitude', 'images','type','provide','condition'
        ]
class HeavyVehicleForm(forms.ModelForm):
    class Meta:
        model = HeavyVehicle
        fields = [
            'name', 'description', 'manufacturer', 'year', 
             
            'price',  'condition', 'make',
            'regions', 'cities', 'latitude', 'longitude',  'images','listing_type'
        ]

class BoatForm(forms.ModelForm):
    class Meta:
        model = Boat
        fields = [
            'name', 'description', 'manufacturer', 
             'price', 'condition', 
            'regions', 'cities', 'latitude', 'longitude',  'images','listing_type'
        ]

class NumberPlateForm(forms.ModelForm):
    class Meta:
        model = NumberPlate
        fields = [
            'number', 'price', 'description', 
            'regions', 'cities', 'latitude', 'longitude', 'location','listing_type','letter_english', 'letter_arabic', 'plate_type' , 'seller_name'
        ]

from django import forms
from .models import UploadedImage

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedImage
        fields = ['image']

from django import forms
from .models import DrivingTraining

class DrivingTrainingForm(forms.ModelForm):
    class Meta:
        model = DrivingTraining
        fields = [
            'trainer_name', 'trainer_gender', 'transmission', 'price',
            'body_type', 'model_year', 'description', 'regions', 'cities',
             'location', 'language', 'about_instructor', 'images',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'about_instructor': forms.Textarea(attrs={'rows': 3}),
        }

# -------------------------------------------------------------

class ApartmentForm(forms.ModelForm):
    nearby_location = forms.ModelMultipleChoiceField(
        queryset=NearbyLocation.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    main_amenities = forms.ModelMultipleChoiceField(
        queryset=MainAmenities.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    additional_amenities = forms.ModelMultipleChoiceField(
        queryset=AdditionalAmenities.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    class Meta:
        model = Apartment
        fields = [
            'property_title',
            'price',
            'plot_area',
            'regions',
            'cities',
            'latitude',
            'longitude',
            'description',
            'property_mortgage',
            'listing_type',
            'floors',
            'images',
            'building',  
            'lister_type',  
            'property_mortgage',  
            'facade', 
            'furnished', 
            'nearby_location',
            'additional_amenities',
            'main_amenities', 
            'bedrooms',
            'bathrooms',
            'rental_period',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            
        }

class FactoryForm(forms.ModelForm):
    nearby_location = forms.ModelMultipleChoiceField(
        queryset=NearbyLocation.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    main_amenities = forms.ModelMultipleChoiceField(
        queryset=MainAmenities.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    additional_amenities = forms.ModelMultipleChoiceField(
        queryset=AdditionalAmenities.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    class Meta:
        model = Factory
        fields = [
            'property_title',
            'price',
            'plot_area',
            'regions',
            'cities',
            'latitude',
            'longitude',
            'description',
            'nearby_location',
            'additional_amenities',
            'main_amenities',
            'property_mortgage',
            'listing_type',
            'lister_type',  # Added Agent or Landlord selection
            'images',
            'rental_period',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            
        }




class ComplexForm(forms.ModelForm):
    nearby_location = forms.ModelMultipleChoiceField(
        queryset=NearbyLocation.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    main_amenities = forms.ModelMultipleChoiceField(
        queryset=MainAmenities.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    additional_amenities = forms.ModelMultipleChoiceField(
        queryset=AdditionalAmenities.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    class Meta:
        model = Complex
        fields = [
            'property_title',
            'price',
            'plot_area',
            'regions',
            'cities',
            'latitude',
            'longitude',
            'description',
            'property_mortgage',
            'listing_type',
            'lister_type',  # Added Agent or Landlord selection
            'images',
            'property',
            'nearby_location',
            'additional_amenities',
            'main_amenities',
            'floors','rental_period',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            
        }

class ClinicForm(forms.ModelForm):
    nearby_location = forms.ModelMultipleChoiceField(
        queryset=NearbyLocation.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    main_amenities = forms.ModelMultipleChoiceField(
        queryset=MainAmenities.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    additional_amenities = forms.ModelMultipleChoiceField(
        queryset=AdditionalAmenities.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    class Meta:
        model = Clinic
        fields = [
            'property_title',
            'price',
            'plot_area',
            'regions',
            'cities',
            'latitude',
            'longitude',
            'furnished', 
            'description',
            'property_mortgage',
            'listing_type',
            'lister_type',  # Added Agent or Landlord selection
            'nearby_location',
            'additional_amenities',
            'main_amenities',
            'images',
            'property',
            'floors','rental_period',
            ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            
        }

class HostelForm(forms.ModelForm):
    nearby_location = forms.ModelMultipleChoiceField(
        queryset=NearbyLocation.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    main_amenities = forms.ModelMultipleChoiceField(
        queryset=MainAmenities.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    additional_amenities = forms.ModelMultipleChoiceField(
        queryset=AdditionalAmenities.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    class Meta:
        model = Hostel
        fields = [
            'property_title',
            'price',
            'plot_area',
            'regions',
            'cities',
            'latitude',
            'longitude',
            'description',
            'property_mortgage',
            'listing_type',
            'lister_type',  # Added Agent or Landlord selection
            'images',
            'property',
            'bedrooms',
            'floors',
            'nearby_location',
            'additional_amenities',
            'main_amenities',
            'furnished', 'rental_period',
            
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            
        }



class OfficeForm(forms.ModelForm):
    nearby_location = forms.ModelMultipleChoiceField(
        queryset=NearbyLocation.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    main_amenities = forms.ModelMultipleChoiceField(
        queryset=MainAmenities.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    additional_amenities = forms.ModelMultipleChoiceField(
        queryset=AdditionalAmenities.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    class Meta:
        model = Office
        fields = [
            'property_title',
            'price',
            'plot_area',
            'regions',
            'cities',
            'latitude',
            'longitude',
            'description',
            'property_mortgage',
            'listing_type',
            'lister_type',  # Added Agent or Landlord selection
            'images',
            'property',
            'floors',
            'nearby_location',
            'additional_amenities',
            'main_amenities',
            'furnished','rental_period',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            
        }



class ShopForm(forms.ModelForm):
    nearby_location = forms.ModelMultipleChoiceField(
        queryset=NearbyLocation.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    main_amenities = forms.ModelMultipleChoiceField(
        queryset=MainAmenities.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    additional_amenities = forms.ModelMultipleChoiceField(
        queryset=AdditionalAmenities.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    class Meta:
        model = Shop
        fields = [
            'property_title',
            'price',
            'plot_area',
            'regions',
            'cities',
            'latitude',
            'longitude',
            'description',
            'property_mortgage',
            'listing_type',
            'lister_type',  # Added Agent or Landlord selection            
            'images',
            'nearby_location',
            'additional_amenities',
            'main_amenities','rental_period',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            
        }

class CafeForm(forms.ModelForm):
    nearby_location = forms.ModelMultipleChoiceField(
        queryset=NearbyLocation.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    main_amenities = forms.ModelMultipleChoiceField(
        queryset=MainAmenities.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    additional_amenities = forms.ModelMultipleChoiceField(
        queryset=AdditionalAmenities.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    class Meta:
        
        model = Cafe
        fields = [
            'property_title',
            'price',
            'plot_area',
             'regions',
             'cities',
             'latitude',
             'longitude',
            
            'description',
            'property_mortgage',
            'listing_type',
            'lister_type',  # Added Agent or Landlord selection
            
            
            'images',
            'property',           
            'nearby_location',
            'additional_amenities',
            'main_amenities','rental_period',      
            
            
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            
        }


class StaffForm(forms.ModelForm):
    nearby_location = forms.ModelMultipleChoiceField(
        queryset=NearbyLocation.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    main_amenities = forms.ModelMultipleChoiceField(
        queryset=MainAmenities.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    additional_amenities = forms.ModelMultipleChoiceField(
        queryset=AdditionalAmenities.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    class Meta:
        model = Staff
        fields = [
            'property_title',
            'price',
            'plot_area',
             'regions',
             'cities',
             'latitude',
             'longitude',
            
            'description',
            'property_mortgage',
            'listing_type',
            'lister_type',  # Added Agent or Landlord selection
            'nearby_location',
            'additional_amenities',
            'main_amenities',
            
            'images',
            'property',
            'bedrooms',
            
            'floors','rental_period',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            
        }



class WarehouseForm(forms.ModelForm):
    nearby_location = forms.ModelMultipleChoiceField(
        queryset=NearbyLocation.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    main_amenities = forms.ModelMultipleChoiceField(
        queryset=MainAmenities.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    additional_amenities = forms.ModelMultipleChoiceField(
        queryset=AdditionalAmenities.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    class Meta:
        model = Warehouse
        fields = [
            'property_title',
            'price',
            'plot_area',
             'regions',
             'cities',
             'latitude',
             'longitude',
            'description',
            'property_mortgage',
            'listing_type',
            'lister_type',  # Added Agent or Landlord selection
            'nearby_location',
            'additional_amenities',
            'main_amenities',
            'images',
            'property','rental_period',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            
        }

class Townhouseform(forms.ModelForm):
    nearby_location = forms.ModelMultipleChoiceField(
        queryset=NearbyLocation.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    main_amenities = forms.ModelMultipleChoiceField(
        queryset=MainAmenities.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    additional_amenities = forms.ModelMultipleChoiceField(
        queryset=AdditionalAmenities.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    class Meta:
        model = Townhouse
        fields = [
            'property_title', 
            'price', 
            'plot_area', 
            'surface_area', 
            'bedrooms',
            'bathrooms',
            'floors',
            'description',
            'building',  # Added building age
             'regions',
             'cities',
             'latitude',
             'longitude', 
              'lister_type',  # Added Agent or Landlord selection
            
            'property_mortgage',  # Added mortgage Yes/No
            'facade',  # Added facade choices
             'furnished',  # Added furnished choice
            'nearby_location',
            'additional_amenities',
            'main_amenities',
             
            'images',
            'listing_type','rental_period',
            
        ]



class Fullfloorsform(forms.ModelForm):
    nearby_location = forms.ModelMultipleChoiceField(
        queryset=NearbyLocation.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    main_amenities = forms.ModelMultipleChoiceField(
        queryset=MainAmenities.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    additional_amenities = forms.ModelMultipleChoiceField(
        queryset=AdditionalAmenities.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    class Meta:
        model = Fullfloors
        fields = [
            'property_title', 
            'price', 
            'plot_area', 
            'floors',
            'description',
            'regions',
            'cities',
            'latitude',
            'longitude', 
            'lister_type',  # Added Agent or Landlord selection
            'property_mortgage',  # Added mortgage Yes/No
            'property',
            
            'nearby_location',
            'additional_amenities',
            'main_amenities',
            'images',
            'listing_type','rental_period',
            
        ]

class Showroomsform(forms.ModelForm):
    nearby_location = forms.ModelMultipleChoiceField(
        queryset=NearbyLocation.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    main_amenities = forms.ModelMultipleChoiceField(
        queryset=MainAmenities.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    additional_amenities = forms.ModelMultipleChoiceField(
        queryset=AdditionalAmenities.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    class Meta:
        model = Showrooms
        fields = [
            'property_title', 
            'price', 
            'plot_area', 
            'description',
             'regions',
             'cities',
             'latitude',
             'longitude', 
              'lister_type',  # Added Agent or Landlord selection
            'property_mortgage',  # Added mortgage Yes/No
           'property', 
            'nearby_location',
            'additional_amenities',
            'main_amenities', 
            'images',
            'listing_type','rental_period',
            
        ]
class Wholebuildingform(forms.ModelForm):
    nearby_location = forms.ModelMultipleChoiceField(
        queryset=NearbyLocation.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    class Meta:
        model = Wholebuilding
        fields = [
            'property_title', 
            'price', 
            'plot_area',
            'surface_area', 
            'floors',
            'building',  # Added building age
            'nearby_location',
            'description',
            'facade',
            'regions',
            'cities',
            'latitude',
            'longitude', 
            'lister_type',  # Added Agent or Landlord selection
            'property_mortgage',  # Added mortgage Yes/No
            'property', 
            'images',
            'listing_type','rental_period',
        ]

class Supermarketform(forms.ModelForm):
    nearby_location = forms.ModelMultipleChoiceField(
        queryset=NearbyLocation.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    main_amenities = forms.ModelMultipleChoiceField(
        queryset=MainAmenities.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    additional_amenities = forms.ModelMultipleChoiceField(
        queryset=AdditionalAmenities.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    class Meta:
        model = Supermarket
        fields = [
            'property_title', 
            'price', 
            'plot_area', 
            'nearby_location',
            'additional_amenities',
            'main_amenities', 
            'description',
            'regions',
            'cities',
            'latitude',
            'longitude', 
            'lister_type',  # Added Agent or Landlord selection
            'property_mortgage',  # Added mortgage Yes/No
            'property',  
            'images',
            'listing_type','rental_period',
            
        ]
class Foreignform(forms.ModelForm):
    nearby_location = forms.ModelMultipleChoiceField(
        queryset=NearbyLocation.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    class Meta:
        model = Foreign
        fields = [
            'property_title', 
            'price', 
            'country', 
            'description',
            'regions',
            'cities',
            'nearby_location',
            'latitude',
            'longitude', 
            'lister_type',  # Added Agent or Landlord selection
            'property_mortgage',  # Added mortgage Yes/No
            'estate_type',
            'images',
            'listing_type',  'rental_period', 
        ]


class Sharedform(forms.ModelForm):
    
    class Meta:
        model = Shared
        fields = [
            'property_title', 
            'price', 
            
            'description',
           
            'regions',
            'cities',
            'latitude',
            'longitude', 
            
            'furnished',  # Added furnished choice
            'images',
            'listing_type',
            'rental_period',
            
        ]


class Suitsform(forms.ModelForm):
    
    class Meta:
        model = Suits
        fields = [
            'property_title', 
            'price', 
            
            'description',
           
            'regions',
            'cities',
            'latitude',
            'longitude', 
            
            'furnished',  # Added furnished choice
            'images',
            'listing_type',
            'rental_period',
            
        ]

# ------------------------------------------------------Motors------------------------------------------------------------
from django import forms
from .models import Part

class PartForm(forms.ModelForm):
    types = forms.ChoiceField(choices=[
        ('batteries', 'Batteries'),
        ('bodyparts', 'Body Parts'),
        ('mechanical', 'Mechanical Parts'),
        ('spareparts', 'Spare Parts'),
        ('other', 'Other'),
    ], required=True)

    class Meta:
        model = Part
        fields = [
            'name', 'description', 'price', 'regions', 'cities', 'latitude', 'longitude', 
            'provide', 'condition', 'subtype', 'images',
        ]
      

class SportsCarForm(forms.ModelForm):  # Renamed
    class Meta:
        model = SportsCar  # Updated model reference
        fields = [
            'make', 'year', 'description',
            'bodytype', 'top_speed', 'top_speed_unit',
            'acceleration', 'drivetrain',
            'regions', 'cities',
            'rental_period', 'rental_price',
            'horsepower', 'torque',
            'images', 'latitude', 'longitude'
        ]
