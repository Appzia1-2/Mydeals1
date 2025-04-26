from django.db import models
from django.utils import timezone


class Advertisement(models.Model):
    image = models.ImageField(upload_to='advertisements/')
    url = models.URLField(max_length=500, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Advertisement {self.id}"


class Region(models.Model):
    name = models.CharField(max_length=100, unique=True)
 
    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=100, unique=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='cities')
 

    def __str__(self):
        return self.name
    


    
class Category(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=100, help_text="Enter the Font Awesome class for the icon, e.g., 'fas fa-tshirt'.")
    def _str_(self):
        return self.name

class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.category.name} - {self.name}"
    
class JobCategory(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=100, help_text="Enter the Font Awesome class for the icon, e.g., 'fas fa-tshirt'.")
    def _str_(self):
        return self.name



class NearbyLocation(models.Model):
    name = models.CharField(max_length=255, verbose_name="Location Name")
    def __str__(self):
        return self.name     
    
class MainAmenities(models.Model):
    name = models.CharField(max_length=255, verbose_name="Location Name")
    def __str__(self):
        return self.name     
    
class AdditionalAmenities(models.Model):
    name = models.CharField(max_length=255, verbose_name="Location Name")
    def __str__(self):
        return self.name     


from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError

from django.db import models
from django.conf import settings

class Land(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout', 'Soldout')
    ]
    RENTAL_PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]
    LISTING_TYPE_CHOICES = [
        ('sell', 'Sell'),
        ('rent', 'Rent')
    ]
    LISTER_TYPE_CHOICES = [
        ('agent', 'Agent'),
        ('landlord', 'Landlord'),
    ]
    PROPERTY_MORTGAGE_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    FACADE_CHOICES = [
        ('northern', 'Northern'),
        ('southern', 'Southern'),
        ('eastern', 'Eastern'),
        ('western', 'Western'),
        ('northeast', 'Northeast'),
        ('southeast', 'Southeast'),
        ('northwest', 'Northwest'),
        ('southwest', 'Southwest'),

    ]
    ZONED_FOR_CHOICES = [
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('farm', 'Farm'),
        ('industrial', 'Industrial'),
        ('mixed use', 'Mixed Use')
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='lands'
    )
    property_title = models.CharField(max_length=255, verbose_name="Property Title")
    image = models.ImageField(upload_to='land/', verbose_name="Main Image")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    REGION_CHOICES = [
        ('MS', 'Muscat'),
        ('DH', 'Dhofar'),
        ('BT', 'Al Batinah'),
        ('DA', 'Al Dakhiliya'),
        ('SH', 'Al Sharqiya'),
        ('BR', 'Al Buraimi'),
        ('ZU', 'Al Dhahirah'),
        ('MW', 'Musandam'),
        ('WR', 'Al Wusta'),
    ]
    
    regions = models.CharField(
        max_length=250,
        choices=REGION_CHOICES,
        default='MS'  
    )
    
    cities = models.TextField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    created_at = models.DateTimeField(default=timezone.now)
    plot_area = models.CharField(max_length=100, verbose_name="Land Area")
    description = models.TextField(verbose_name="Property Description")
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    
    # New field for listing type
    listing_type = models.CharField(
        max_length=10,
        choices=LISTING_TYPE_CHOICES,
        default='sell',
        verbose_name="Listing Type"
    )
    rental_period = models.CharField(
        max_length=10,
        choices=RENTAL_PERIOD_CHOICES,
        null=True,
        blank=True,
        verbose_name="Rental Period"
    )
    lister_type = models.CharField(
        max_length=10,
        choices=LISTER_TYPE_CHOICES,
        verbose_name="Lister Type"
    )
    
    
    property_mortgage = models.CharField(
        max_length=3, 
        choices=PROPERTY_MORTGAGE_CHOICES, 
        default='no', 
        verbose_name="Property Mortgage"
    )
    facade = models.CharField(
        max_length=10, 
        choices=FACADE_CHOICES, 
        verbose_name="Facade"
    )
    zoned_for = models.CharField(
        max_length=100, 
        choices=ZONED_FOR_CHOICES, 
        verbose_name="Zoned For"
    )
    nearby_location = models.ManyToManyField(NearbyLocation) 
    images = models.ManyToManyField(
        'LandImage', 
        blank=True, 
        related_name='land', 
        verbose_name="Images"
    )
    
    videos = models.ManyToManyField(
        'LandVideo', 
        blank=True, 
        related_name='land', 
        verbose_name="Videos"
    )

     
    def get_region_display(self):
        return dict(self.REGION_CHOICES).get(self.regions, self.regions)

class LandImage(models.Model):
    image = models.ImageField(upload_to='land/images/', verbose_name="Image")

    def __str__(self):
        return f"Image {self.id}"

class LandVideo(models.Model):
    video = models.FileField(upload_to='land/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"
   
#villa    
class Villa(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout','Soldout')
    ]
    TRANSACTION_CHOICES = [
        ('sell', 'Sell'),
        ('rent', 'Rent'),
    ]
    RENTAL_PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]
    FURNISHED_CHOICES = [
        ('furnished', 'Furnished'),
        ('semi_furnished', 'Semi-Furnished'),
        ('unfurnished', 'Unfurnished'),
    ]
    BUILDING_AGE_CHOICES = [
        ('under_construction', 'Under Construction'),
        ('0-11_months', '0-11 Months'),
        ('1-5_years', '1-5 Years'),
        ('6-9_years', '6-9 Years'),
        ('10-19_years', '10-19 Years'),
        ('20+_years', '20+ Years'),
    ]
    LISTER_TYPE_CHOICES = [
        ('agent', 'Agent'),
        ('landlord', 'Landlord'),
    ]
    PROPERTY_MORTGAGE_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    FACADE_CHOICES = [
        ('northern', 'Northern'),
        ('southern', 'Southern'),
        ('eastern', 'Eastern'),
        ('western', 'Western'),
        ('northeast', 'Northeast'),
        ('southeast', 'Southeast'),
        ('northwest', 'Northwest'),
        ('southwest', 'Southwest'),
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='villas'
    )
    nearby_location = models.ManyToManyField(NearbyLocation) 
    main_amenities = models.ManyToManyField(MainAmenities)
    additional_amenities = models.ManyToManyField(AdditionalAmenities)  
    property_title = models.CharField(max_length=255, verbose_name="Property Title")
    image = models.ImageField(upload_to='villa/', verbose_name="Main Image")
    created_at = models.DateTimeField(default=timezone.now)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    REGION_CHOICES = [
        ('MS', 'Muscat'),
        ('DH', 'Dhofar'),
        ('BT', 'Al Batinah'),
        ('DA', 'Al Dakhiliya'),
        ('SH', 'Al Sharqiya'),
        ('BR', 'Al Buraimi'),
        ('ZU', 'Al Dhahirah'),
        ('MW', 'Musandam'),
        ('WR', 'Al Wusta'),
    ]

    regions = models.CharField(
        max_length=250,
        choices=REGION_CHOICES,
        default='MS'  
    )
    FLOOR_CHOICES = [
    ('1_floor', '1 Floor'),
    ('2_floor', '2 Floors'),  # Fixed
    ('3_floor', '3 Floors'),  # Fixed
    ('4_floor', '4 Floors'),  # Fixed
    ('5_floor', '5+ Floors'),  # Fixed
    ]

    floors = models.CharField(
       max_length=250,
       choices=FLOOR_CHOICES,
       default='1_floor'  # Fixed
    )

    cities=models.TextField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    plot_area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Land Area")
    surface_area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Surface Area")
    bedrooms = models.CharField(
        max_length=10,
        choices=[
            ('studio', 'Studio'),
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4'),
            ('5', '5'),
            ('6+', '6+'),
        ],
        verbose_name="Number of Bedrooms"
    )
    bathrooms = models.CharField(
        max_length=10,
        choices=[
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4'),
            ('5', '5'),
            ('6+', '6+'),
        ],
        verbose_name="Number of Bathrooms"
    )
    description = models.TextField(verbose_name="Property Description")
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    furnished = models.CharField(
        max_length=20, 
        choices=FURNISHED_CHOICES, 
        default='unfurnished', 
        verbose_name="Furnished"
    )
    building = models.CharField(max_length=20, choices=BUILDING_AGE_CHOICES,default='under_construction',  verbose_name="Building Age")
    
    listing_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_CHOICES,
        default='sell',
        verbose_name="Listing Type"
    )
    rental_period = models.CharField(
        max_length=10,
        choices=RENTAL_PERIOD_CHOICES,
        null=True,
        blank=True,
        verbose_name="Rental Period"
    )
    lister_type = models.CharField(
        max_length=10,
        choices=LISTER_TYPE_CHOICES,
        verbose_name="Lister Type"
    )
    
    
    property_mortgage = models.CharField(
        max_length=3, 
        choices=PROPERTY_MORTGAGE_CHOICES, 
        default='no', 
        verbose_name="Property Mortgage"
    )
    facade = models.CharField(
        max_length=10, 
        choices=FACADE_CHOICES, 
        verbose_name="Facade"
    )

    images = models.ManyToManyField(
        'VillaImage', 
        blank=True, 
        related_name='villa', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'VillaVideo', 
        blank=True, 
        related_name='villa', 
        verbose_name="Videos"
    )

    def get_region_display(self):
        return dict(self.REGION_CHOICES).get(self.regions, self.regions)
    
class VillaImage(models.Model):
    image = models.ImageField(upload_to='villa/images/', verbose_name="Image")

    def __str__(self):
        return f"Image {self.id}"
class VillaVideo(models.Model):
    video = models.FileField(upload_to='villa/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"
    

class Commercial(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout', 'Soldout'),
    ]
    
    TRANSACTION_CHOICES = [
        ('sell', 'Sell'),
        ('rent', 'Rent'),
    ]
    RENTAL_PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]
    FURNISHED_CHOICES = [
        ('furnished', 'Furnished'),
        ('semi_furnished', 'Semi-Furnished'),
        ('unfurnished', 'Unfurnished'),
    ]
    PROPERTY_MORTGAGE_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    LISTER_TYPE_CHOICES = [
        ('agent', 'Agent'),
        ('landlord', 'Landlord'),
    ]

    PROPERTY_CHOICES = [
        ('complete', 'Complete'),
        ('under_construction', 'Under Construction'),
            ]
    nearby_location = models.ManyToManyField(NearbyLocation) 
    main_amenities = models.ManyToManyField(MainAmenities)
    additional_amenities = models.ManyToManyField(AdditionalAmenities)  
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='commercial'
    )
    property_title = models.CharField(max_length=255, verbose_name="Property Title")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    nearby_location = models.ManyToManyField(NearbyLocation) 
    main_amenities = models.ManyToManyField(MainAmenities)
    additional_amenities = models.ManyToManyField(AdditionalAmenities)  
    REGION_CHOICES = [
        ('MS', 'Muscat'),
        ('DH', 'Dhofar'),
        ('BT', 'Al Batinah'),
        ('DA', 'Al Dakhiliya'),
        ('SH', 'Al Sharqiya'),
        ('BR', 'Al Buraimi'),
        ('ZU', 'Al Dhahirah'),
        ('MW', 'Musandam'),
        ('WR', 'Al Wusta'),
    ]
    regions = models.CharField(
        max_length=250,
        choices=REGION_CHOICES,
        default='MS'  
    )
    cities = models.TextField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    created_at = models.DateTimeField(default=timezone.now)
    plot_area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Surface Area (sq ft/m²)")
    description = models.TextField(verbose_name="Property Description")
    FLOOR_CHOICES = [
    ('1_floor', '1 Floor'),
    ('2_floor', '2 Floors'),  # Fixed
    ('3_floor', '3 Floors'),  # Fixed
    ('4_floor', '4 Floors'),  # Fixed
    ('5_floor', '5+ Floors'),  # Fixed
    ]

    floors = models.CharField(
       max_length=250,
       choices=FLOOR_CHOICES,
       default='1_floor'  # Fixed
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    listing_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_CHOICES,
        default='sell',
        verbose_name="Listing Type"
    )
    rental_period = models.CharField(
        max_length=10,
        choices=RENTAL_PERIOD_CHOICES,
        null=True,
        blank=True,
        verbose_name="Rental Period"
    )
    furnished = models.CharField(
        max_length=20, 
        choices=FURNISHED_CHOICES, 
        default='unfurnished', 
        verbose_name="Furnished"
    )
    property_mortgage = models.CharField(
        max_length=3, 
        choices=PROPERTY_MORTGAGE_CHOICES, 
        default='no', 
        verbose_name="Property Mortgage"
    )
    lister_type = models.CharField(
        max_length=10,
        choices=LISTER_TYPE_CHOICES,
        verbose_name="Lister Type"
    )
    property = models.CharField(
        max_length=20,
        choices=PROPERTY_CHOICES,
         default='under_construction', 
        verbose_name="Property Status"
    )

    images = models.ManyToManyField(
        'ComImage', 
        blank=True, 
        related_name='Commercial', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'ComVideo',
        blank=True,
        related_name='Commercial',
        verbose_name="Videos"
    )
    
    def __str__(self):
        return self.property_title
    
    def get_region_display(self):
        return dict(self.REGION_CHOICES).get(self.regions, self.regions)


class ComImage(models.Model):
    image = models.ImageField(upload_to='Commercial/images/', verbose_name="Image")

    def __str__(self):
        return f"Image {self.id}"

class ComVideo(models.Model):
    video = models.FileField(upload_to='Commercial/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"


class Farm(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout','Soldout')
    ]
    TRANSACTION_CHOICES = [
        ('sell', 'Sell'),
        ('rent', 'Rent'),
    ]
    RENTAL_PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
        ]
    BUILDING_AGE_CHOICES = [
        ('under_construction', 'Under Construction'),
        ('0-11_months', '0-11 Months'),
        ('1-5_years', '1-5 Years'),
        ('6-9_years', '6-9 Years'),
        ('10-19_years', '10-19 Years'),
        ('20+_years', '20+ Years'),
    ]
    LISTER_TYPE_CHOICES = [
        ('agent', 'Agent'),
        ('landlord', 'Landlord'),
    ]
    FURNISHED_CHOICES = [
        ('furnished', 'Furnished'),
        ('semi_furnished', 'Semi-Furnished'),
        ('unfurnished', 'Unfurnished'),
    ]
    PROPERTY_MORTGAGE_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    FACADE_CHOICES = [
        ('northern', 'Northern'),
        ('southern', 'Southern'),
        ('eastern', 'Eastern'),
        ('western', 'Western'),
        ('northeast', 'Northeast'),
        ('southeast', 'Southeast'),
        ('northwest', 'Northwest'),
        ('southwest', 'Southwest'),

    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='farm'
    )
    property_title = models.CharField(max_length=255, verbose_name="Property Title")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    surface_area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Surface Area")
    bedrooms = models.CharField(
        max_length=10,
        choices=[
            ('studio', 'Studio'),
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4'),
            ('5', '5'),
            ('6+', '6+'),
        ],
        verbose_name="Number of Bedrooms"
    )
    bathrooms = models.CharField(
        max_length=10,
        choices=[
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4'),
            ('5', '5'),
            ('6+', '6+'),
        ],
        verbose_name="Number of Bathrooms"
    )
    created_at = models.DateTimeField(default=timezone.now)
    REGION_CHOICES = [
        ('MS', 'Muscat'),
        ('DH', 'Dhofar'),
        ('BT', 'Al Batinah'),
        ('DA', 'Al Dakhiliya'),
        ('SH', 'Al Sharqiya'),
        ('BR', 'Al Buraimi'),
        ('ZU', 'Al Dhahirah'),
        ('MW', 'Musandam'),
        ('WR', 'Al Wusta'),
    ]

    regions = models.CharField(
        max_length=250,
        choices=REGION_CHOICES,
        default='MS'  
    )
    cities=models.TextField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    plot_area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Land Area")
    nearby_location = models.ManyToManyField(NearbyLocation) 
    main_amenities = models.ManyToManyField(MainAmenities)
    additional_amenities = models.ManyToManyField(AdditionalAmenities) 
    listing_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_CHOICES,
        default='sell',
        verbose_name="Listing Type"
    )
    description = models.TextField(verbose_name="Property Description")
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    furnished = models.CharField(
        max_length=20, 
        choices=FURNISHED_CHOICES, 
        default='unfurnished', 
        verbose_name="Furnished"
    )
    building = models.CharField(max_length=20, choices=BUILDING_AGE_CHOICES,default='under_construction',  verbose_name="Building Age")
    lister_type = models.CharField(
        max_length=10,
        choices=LISTER_TYPE_CHOICES,
        verbose_name="Lister Type"
    )
    rental_period = models.CharField(
        max_length=10,
        choices=RENTAL_PERIOD_CHOICES,
        null=True,
        blank=True,
        verbose_name="Rental Period")
    
    
    property_mortgage = models.CharField(
        max_length=3, 
        choices=PROPERTY_MORTGAGE_CHOICES, 
        default='no', 
        verbose_name="Property Mortgage"
    )
    facade = models.CharField(
        max_length=10, 
        choices=FACADE_CHOICES, 
        verbose_name="Facade"
    )

    images = models.ManyToManyField(
        'FarmImage', 
        blank=True, 
        related_name='Farm', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'FarmVideo',
        blank=True,
        related_name='Farm',
        verbose_name="Videos"
    )

    def __str__(self):
        return self.property_title
    
    def get_region_display(self):
        return dict(self.REGION_CHOICES).get(self.regions, self.regions)

class FarmImage(models.Model):
    image = models.ImageField(upload_to='Farm/images/', verbose_name="Image")

    def __str__(self):
        return f"Image {self.id}"

class FarmVideo(models.Model):
    video = models.FileField(upload_to='Farm/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"

class Chalet(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout','Soldout')
    ]
    TRANSACTION_CHOICES = [
        ('sell', 'Sell'),
        ('rent', 'Rent'),
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='chalet'
    )
    property_title = models.CharField(max_length=255, verbose_name="Property Title")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    created_at = models.DateTimeField(default=timezone.now)
    REGION_CHOICES = [
        ('MS', 'Muscat'),
        ('DH', 'Dhofar'),
        ('BT', 'Batinah'),
        ('DA', 'Dakhiliyah'),
        ('SH', 'Sharqiyah'),
        ('BR', 'Buraimi'),
        ('ZU', 'Zufar'),
        ('MW', 'Musandam'),
        ('WR', 'Wusta'),
    ]

    regions = models.CharField(
        max_length=250,
        choices=REGION_CHOICES,
        default='MS'  
    )
    cities=models.TextField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    location=models.TextField(max_length=250)
    plot_area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Plot Area")
    bedrooms = models.IntegerField(verbose_name="Number of Bedrooms")
    bathrooms = models.IntegerField(verbose_name="Number of Bathrooms")
    description = models.TextField(verbose_name="Property Description")
    amenities = models.TextField(verbose_name="Amenities (e.g., Fireplace, Jacuzzi, Sauna)")
    proximity_to_activities = models.TextField(verbose_name="Proximity to Skiing/Outdoor Activities")
    tenancy_information = models.CharField(
        max_length=100, 
        choices=[('rented', 'Rented'), ('owner_occupied', 'Owner Occupied')], 
        verbose_name="Tenancy Information"
    )
    listing_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_CHOICES,
        default='sell',
        verbose_name="Listing Type"
    )
    contact_details = models.TextField(verbose_name="Contact Details")
    additional_information = models.TextField(verbose_name="Additional Information")
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    images = models.ManyToManyField(
        'ChaletImage', 
        blank=True, 
        related_name='Chalet', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'ChaletVideo',
        blank=True,
        related_name='Chalet',
        verbose_name="Videos"
    )

    def __str__(self):
        return self.property_title
    
    def get_region_display(self):
        return dict(self.REGION_CHOICES).get(self.regions, self.regions)

class ChaletImage(models.Model):
    image = models.ImageField(upload_to='Chalet/images/', verbose_name="Image")

    def __str__(self):
        return f"Image {self.id}"

class ChaletVideo(models.Model):
    video = models.FileField(upload_to='Chalet/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"


    
#Job
class Job(models.Model):
    job_title = models.CharField(max_length=255, verbose_name="Job Title")
    company_name = models.CharField(max_length=255, verbose_name="Company Name")
    job_type = models.CharField(
        max_length=50, 
        choices=[
            ('full_time', 'Full-time'), 
            ('part_time', 'Part-time'), 
            ('freelance', 'Freelance'), 
            ('contract', 'Contract'), 
            ('temporary', 'Temporary')
        ], 
        verbose_name="Job Type"
    )
    industry = models.CharField(
        max_length=50, 
        choices=[('IT', 'IT'), ('marketing', 'Marketing'), ('finance', 'Finance'), ('designing', 'Designing')], 
        verbose_name="Industry"
    )
    experience_level = models.CharField(
        max_length=50, 
        choices=[('entry', 'Entry-level'), ('mid', 'Mid-level'), ('senior', 'Senior')], 
        verbose_name="Experience Level"
    )
    salary_range = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Salary Range (OMR)")
    education_level = models.CharField(
        max_length=50, 
        choices=[('diploma', 'Diploma'), ('bachelor', 'Bachelor\'s'), ('postgraduate', 'Post Graduate'), ('phd', 'PHD')], 
        verbose_name="Education Level"
    )
    REGION_CHOICES = [
        ('MS', 'Muscat'),
        ('DH', 'Dhofar'),
        ('BT', 'Batinah'),
        ('DA', 'Dakhiliyah'),
        ('SH', 'Sharqiyah'),
        ('BR', 'Buraimi'),
        ('ZU', 'Zufar'),
        ('MW', 'Musandam'),
        ('WR', 'Wusta'),
    ]

    regions = models.CharField(
        max_length=250,
        choices=REGION_CHOICES,
        default='MS'  
    )
    cities=models.TextField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    location=models.TextField(max_length=250)
    skills_required = models.TextField(verbose_name="Skills Required")
    description = models.TextField(verbose_name="Property Description")
#JobSeeker
class JobSeeker(models.Model):
    full_name = models.CharField(max_length=255, verbose_name="Full Name")
    contact_number = models.CharField(max_length=20, verbose_name="Contact Number")
    email_address = models.EmailField(verbose_name="Email Address")
    address = models.CharField(max_length=255, verbose_name="Current Address")
    summary = models.TextField(verbose_name="Professional Summary")
    
    job_title = models.CharField(max_length=255, verbose_name="Previous Job Title")
    company_name = models.CharField(max_length=255, verbose_name="Company Name")
    job_location = models.CharField(max_length=255, verbose_name="Company Location")
    start_date = models.DateField(verbose_name="Job Start Date")
    end_date = models.DateField(verbose_name="Job End Date", null=True, blank=True)
    responsibilities = models.TextField(verbose_name="Responsibilities and Achievements")

    degree = models.CharField(max_length=255, verbose_name="Degree")
    institution = models.CharField(max_length=255, verbose_name="Institution Name")
    institution_location = models.URLField(verbose_name="Institution Location")
    start_date_education = models.DateField(verbose_name="Education Start Date")
    end_date_education = models.DateField(verbose_name="Education End Date")
    
    skills = models.TextField(verbose_name="Skills")
    certification_name = models.CharField(max_length=255, verbose_name="Certification Name")
    issuing_organization = models.CharField(max_length=255, verbose_name="Issuing Organization")
    date_obtained = models.DateField(verbose_name="Certification Date")
    
    languages = models.CharField(max_length=255, verbose_name="Languages Spoken")
    proficiency_level = models.CharField(
        max_length=50, 
        choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')], 
        verbose_name="Language Proficiency"
    )

    project_title = models.CharField(max_length=255, verbose_name="Project Title")
    project_description = models.TextField(verbose_name="Project Description")
    role = models.CharField(max_length=255, verbose_name="Project Role")
    project_duration = models.CharField(max_length=255, verbose_name="Project Duration")


# authenticated user
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username must be set')
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)  # Normalize the email address
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)  # Hashes the password
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        # Add required fields for superuser only
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('email', 'admin@example.com')  # Default email for superuser

        # You can avoid asking for 'email' or 'name' explicitly
        return self.create_user(username, password=password, **extra_fields)

from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django_countries.fields import CountryField
class CustomUser(AbstractBaseUser):
    is_admin = models.BooleanField(default=False)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True, blank=True)

    # Non-mandatory fields
    phone = models.CharField(max_length=15, null=True, blank=True)  # Allows phone to be optional
    whatsapp = models.CharField(max_length=15, null=True, blank=True)  # Allows phone to be optional
    address = models.TextField(null=True, blank=True)              # Allows address to be optional
    dob = models.DateField(null=True, blank=True)                  # Allows dob to be optional
    nationality = CountryField(blank=True, null=True)
    gender = models.CharField(
        max_length=10,
        choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')],
        null=True,
        blank=True
    )  # Allows gender to be optional
    image = models.ImageField(
    upload_to='user/images/', 
    verbose_name="user Image", 
    blank=True, 
    null=True
)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


# Fashion model
class Fashion(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout','Soldout')
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='fashion'
    )
    product_name=models.TextField(max_length=250)
    REGION_CHOICES = [
        ('MS', 'Muscat'),
        ('DH', 'Dhofar'),
        ('BT', 'Batinah'),
        ('DA', 'Dakhiliyah'),
        ('SH', 'Sharqiyah'),
        ('BR', 'Buraimi'),
        ('ZU', 'Zufar'),
        ('MW', 'Musandam'),
        ('WR', 'Wusta'),
    ]

    regions = models.CharField(
        max_length=250,
        choices=REGION_CHOICES,
        default='MS'  
    )
    cities=models.TextField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    location=models.TextField(max_length=250)
    name=models.TextField(max_length=250)
    category = models.CharField(
        max_length=50, 
        choices=[
            ('clothing', 'Clothing'), 
            ('footwear', 'Footwear'), 
            ('accessories', 'Accessories')
        ], 
        verbose_name="Category"
    )
    brand = models.CharField(max_length=100, verbose_name="Brand")
    size = models.CharField(
        max_length=10, 
        choices=[('S', 'Small'), ('M', 'Medium'), ('L', 'Large'), ('XL', 'XL')], 
        verbose_name="Size"
    )
    gender = models.CharField(
        max_length=10, 
        choices=[('male', 'Male'), ('female', 'Female'), ('unisex', 'Unisex')], 
        verbose_name="Gender"
    )
    color = models.CharField(max_length=50, verbose_name="Color")
    material = models.CharField(max_length=100, verbose_name="Material")
    condition = models.CharField(
        max_length=10, 
        choices=[('used', 'Used'), ('like_new', 'Like New')], 
        verbose_name="Condition"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    contact_details = models.TextField(verbose_name="Contact Details")
    created_at = models.DateTimeField(default=timezone.now)
    description = models.TextField(verbose_name="Property Description")
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    images = models.ManyToManyField(
        'FashionImage', 
        blank=True, 
        related_name='fashion', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'FashionVideo', 
        blank=True, 
        related_name='fashion', 
        verbose_name="Videos"
    )
class FashionImage(models.Model):
    image = models.ImageField(upload_to='Fashion/images/', verbose_name="Image")

    def _str_(self):
        return f"Image {self.id}"
    
class FashionVideo(models.Model):
    video = models.FileField(upload_to='Fashion/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"

class Toys(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout','Soldout')
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='toys'
    )
    product_name = models.CharField(max_length=250)
    REGION_CHOICES = [
        ('MS', 'Muscat'),
        ('DH', 'Dhofar'),
        ('BT', 'Batinah'),
        ('DA', 'Dakhiliyah'),
        ('SH', 'Sharqiyah'),
        ('BR', 'Buraimi'),
        ('ZU', 'Zufar'),
        ('MW', 'Musandam'),
        ('WR', 'Wusta'),
    ]

    regions = models.CharField(
        max_length=250,
        choices=REGION_CHOICES,
        default='MS'  
    )
    cities=models.TextField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    location=models.TextField(max_length=250)
    created_at = models.DateTimeField(default=timezone.now)
    description = models.TextField(verbose_name="Property Description")
    category = models.CharField(
        max_length=50, 
        choices=[('video_games', 'Video Games'), ('consoles', 'Consoles'), ('toys', 'Toys')], 
        verbose_name="Category"
    )
    brand = models.CharField(max_length=100, verbose_name="Brand")
    platform = models.CharField(
        max_length=20, 
        choices=[('ps5', 'PS5'), ('xbox', 'Xbox'), ('pc', 'PC')], 
        verbose_name="Gaming Platform"
    )
    age_group = models.CharField(
        max_length=20, 
        choices=[
            ('3-5_years', '3-5 years'), 
            ('6-10_years', '6-10 years'), 
            ('11-16_years', '11-16 years'), 
            ('above_16_years', 'Above 16 years')
        ], 
        verbose_name="Age Group"
    )
    condition = models.CharField(
        max_length=11, 
        choices=[('new', 'New'), ('used', 'Used'), ('refurbished', 'Refurbished')], 
        verbose_name="Condition"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    images = models.ManyToManyField(
        'ToysImage', 
        blank=True, 
        related_name='toys', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'ToysVideo', 
        blank=True, 
        related_name='toys', 
        verbose_name="Videos"
    )

class ToysImage(models.Model):
    image = models.ImageField(upload_to='Toys/images/', verbose_name="Image")

    def _str_(self):
        return f"Image {self.id}"
    
class ToysVideo(models.Model):
    video = models.FileField(upload_to='Toys/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"

    

#Food and Supplements
class Food(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout','Soldout')
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='food'
    )
    product_type = models.CharField(
        max_length=50, 
        choices=[
            ('food', 'Food'), 
            ('vitamin', 'Vitamin'), 
            ('herbal', 'Herbal Supplements'), 
            ('protein', 'Protein Supplements'), 
            ('fatty_acids', 'Fatty Acids & Omega-3s')
        ], 
        verbose_name="Product Type"
    )
    product_name=models.TextField(max_length=250)
    brand = models.CharField(max_length=100, verbose_name="Brand")
    description = models.TextField(verbose_name="Property Description")
    created_at = models.DateTimeField(default=timezone.now)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Quantity (grams/liters/capsules)")
    expiration_date = models.DateField(verbose_name="Expiration Date")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    REGION_CHOICES = [
        ('MS', 'Muscat'),
        ('DH', 'Dhofar'),
        ('BT', 'Batinah'),
        ('DA', 'Dakhiliyah'),
        ('SH', 'Sharqiyah'),
        ('BR', 'Buraimi'),
        ('ZU', 'Zufar'),
        ('MW', 'Musandam'),
        ('WR', 'Wusta'),
    ]

    regions = models.CharField(
        max_length=250,
        choices=REGION_CHOICES,
        default='MS'  
    )
    cities=models.TextField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    location=models.TextField(max_length=250)
    dietary_info = models.TextField(verbose_name="Dietary Information (e.g., Gluten-Free, Vegan)")
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    images = models.ManyToManyField(
        'FoodImage', 
        blank=True, 
        related_name='food', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'FoodVideo', 
        blank=True, 
        related_name='food', 
        verbose_name="Videos"
    )

class FoodImage(models.Model):
    image = models.ImageField(upload_to='Food/images/', verbose_name="Image")

    def _str_(self):
        return f"Image {self.id}"
    
class FoodVideo(models.Model):
    video = models.FileField(upload_to='Food/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"

    

# SportsFitness model
class Fitness(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout','Soldout')
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='fitness'
    )
    category = models.CharField(
        max_length=50, 
        choices=[
            ('equipment', 'Equipment'), 
            ('apparel', 'Apparel'), 
            ('team_sports', 'Team Sports'), 
            ('individual_sports', 'Individual Sports'), 
            ('athletics', 'Athletics/Track and Field')
        ], 
        verbose_name="Category"
    )
    product_name=models.TextField(max_length=250)
    brand = models.CharField(max_length=100, verbose_name="Brand")
    description = models.TextField(verbose_name="Property Description")
    created_at = models.DateTimeField(default=timezone.now)
    condition = models.CharField(
        max_length=11, 
        choices=[('new', 'New'), ('used', 'Used')], 
        verbose_name="Condition"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    warranty_status = models.CharField(
        max_length=10, 
        choices=[('yes', 'Yes'), ('no', 'No')], 
        verbose_name="Warranty Status"
    )
    REGION_CHOICES = [
        ('MS', 'Muscat'),
        ('DH', 'Dhofar'),
        ('BT', 'Batinah'),
        ('DA', 'Dakhiliyah'),
        ('SH', 'Sharqiyah'),
        ('BR', 'Buraimi'),
        ('ZU', 'Zufar'),
        ('MW', 'Musandam'),
        ('WR', 'Wusta'),
    ]

    regions = models.CharField(
        max_length=250,
        choices=REGION_CHOICES,
        default='MS'  
    )
    cities=models.TextField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    location=models.TextField(max_length=250)
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    images = models.ManyToManyField(
        'FitnessImage', 
        blank=True, 
        related_name='fitness', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'FitnessVideo', 
        blank=True, 
        related_name='fitness', 
        verbose_name="Videos"
    )

class FitnessImage(models.Model):
    image = models.ImageField(upload_to='Fitness/images/', verbose_name="Image")

    def _str_(self):
        return f"Image {self.id}"
    
class FitnessVideo(models.Model):
    video = models.FileField(upload_to='Fitness/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"

#Pets
class Pet(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout','Soldout')
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='pet'
    )
    pet_type = models.CharField(
        max_length=50, 
        choices=[
            ('dog', 'Dog'), 
            ('cat', 'Cat'), 
            ('fish', 'Fish'), 
            ('rabbit', 'Rabbit'), 
            ('hamster', 'Hamster'), 
            ('hedgehog', 'Hedgehog'), 
            ('bird', 'Lovebird'), 
            ('tortoise', 'Tortoise')
        ], 
        verbose_name="Pet Type"
    )
    pet_name=models.TextField(max_length=250)
    breed = models.CharField(max_length=100, verbose_name="Breed")
    created_at = models.DateTimeField(default=timezone.now)
    age = models.IntegerField(verbose_name="Age (months/years)")
    description = models.TextField(verbose_name="Property Description")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    vaccinated = models.CharField(
        max_length=3, 
        choices=[('yes', 'Yes'), ('no', 'No')], 
        verbose_name="Vaccination Status"
    )
    REGION_CHOICES = [
        ('MS', 'Muscat'),
        ('DH', 'Dhofar'),
        ('BT', 'Batinah'),
        ('DA', 'Dakhiliyah'),
        ('SH', 'Sharqiyah'),
        ('BR', 'Buraimi'),
        ('ZU', 'Zufar'),
        ('MW', 'Musandam'),
        ('WR', 'Wusta'),
    ]

    regions = models.CharField(
        max_length=250,
        choices=REGION_CHOICES,
        default='MS'  
    )
    cities=models.TextField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    location=models.TextField(max_length=250)
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    images = models.ManyToManyField(
        'PetImage', 
        blank=True, 
        related_name='pet', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'PetVideo', 
        blank=True, 
        related_name='pet', 
        verbose_name="Videos"
    )

class PetImage(models.Model):
    image = models.ImageField(upload_to='Pet/images/', verbose_name="Image")

    def _str_(self):
        return f"Image {self.id}"

class PetVideo(models.Model):
    video = models.FileField(upload_to='Pet/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"

    
class Book(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout','Soldout')
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='book'
    )
    category = models.CharField(
        max_length=50, 
        choices=[
            ('fiction', 'Fiction'), 
            ('non_fiction', 'Non-Fiction'), 
            ('children_books', 'Children’s Books'), 
            ('graphic_novels', 'Graphic Novels and Comics'), 
            ('poetry', 'Poetry'), 
            ('textbooks', 'Textbooks and Educational Materials'), 
            ('arts_crafts', 'Arts and Crafts'), 
            ('music', 'Music'), 
            ('photography', 'Photography')
        ], 
        verbose_name="Category"
    )
    book_name=models.TextField(max_length=250)
    genre = models.CharField(max_length=100, verbose_name="Genre (for books)")
    created_at = models.DateTimeField(default=timezone.now)
    description = models.TextField(verbose_name="Property Description")
    condition = models.CharField(
        max_length=11, 
        choices=[('new', 'New'), ('used', 'Used')], 
        verbose_name="Condition"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    REGION_CHOICES = [
        ('MS', 'Muscat'),
        ('DH', 'Dhofar'),
        ('BT', 'Batinah'),
        ('DA', 'Dakhiliyah'),
        ('SH', 'Sharqiyah'),
        ('BR', 'Buraimi'),
        ('ZU', 'Zufar'),
        ('MW', 'Musandam'),
        ('WR', 'Wusta'),
    ]

    regions = models.CharField(
        max_length=250,
        choices=REGION_CHOICES,
        default='MS'  
    )
    cities=models.TextField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    location=models.TextField(max_length=250)
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    images = models.ManyToManyField(
        'BookImage', 
        blank=True, 
        related_name='book', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'BookVideo', 
        blank=True, 
        related_name='book', 
        verbose_name="Videos"
    )

class BookImage(models.Model):
    image = models.ImageField(upload_to='Book/images/', verbose_name="Image")

    def _str_(self):
        return f"Image {self.id}"
    
class BookVideo(models.Model):
    video = models.FileField(upload_to='Book/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"

# Home Appliance model
class Appliance(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout','Soldout')
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='appliance'
    )
    appliance_type = models.CharField(
        max_length=100, 
        choices=[
            ('refrigerator', 'Refrigerator'), 
            ('washing_machine', 'Washing Machine'), 
            ('oven', 'Oven'), 
            ('microwave', 'Microwave'), 
            ('clothes_dryer', 'Clothes Dryer'), 
            ('vacuum_cleaner', 'Vacuum Cleaner'), 
            ('air_conditioner', 'Air Conditioner')
        ], 
        verbose_name="Appliance Type"
    )
    product_name=models.TextField(max_length=250)
    image = models.ImageField(upload_to='Home Appliances/', verbose_name="Home Appliance Image")
    brand = models.CharField(max_length=100, verbose_name="Brand")
    created_at = models.DateTimeField(default=timezone.now)
    model_number = models.CharField(max_length=100, verbose_name="Model Number")
    description = models.TextField(verbose_name="Property Description")
    condition = models.CharField(
        max_length=11,  # Increased max_length to 11
        choices=[('new', 'New'), ('used', 'Used'), ('refurbished', 'Refurbished')], 
        verbose_name="Condition"
    )
    warranty_status = models.CharField(
        max_length=10, 
        choices=[('yes', 'Yes'), ('no', 'No')], 
        verbose_name="Warranty Status"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    REGION_CHOICES = [
        ('MS', 'Muscat'),
        ('DH', 'Dhofar'),
        ('BT', 'Batinah'),
        ('DA', 'Dakhiliyah'),
        ('SH', 'Sharqiyah'),
        ('BR', 'Buraimi'),
        ('ZU', 'Zufar'),
        ('MW', 'Musandam'),
        ('WR', 'Wusta'),
    ]

    regions = models.CharField(
        max_length=250,
        choices=REGION_CHOICES,
        default='MS'  
    )
    cities=models.TextField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    location=models.TextField(max_length=250)
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    images = models.ManyToManyField(
        'ApplianceImage', 
        blank=True, 
        related_name='appliance', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'ApplianceVideo', 
        blank=True, 
        related_name='appliance', 
        verbose_name="Videos"
    )

class ApplianceImage(models.Model):
    image = models.ImageField(upload_to='Appliance/images/', verbose_name="Image")

    def _str_(self):
        return f"Image {self.id}"
    
class ApplianceVideo(models.Model):
    video = models.FileField(upload_to='Appliance/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"

# ----------------------------------------------------community---------------------------------------------------------

#Business Equipments
class Business(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout','Soldout')
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='business'
    )
    category = models.CharField(
        max_length=50, 
        choices=[
            ('computers', 'Computers and Accessories'), 
            ('furniture', 'Office Furniture'), 
            ('telecommunication', 'Telecommunication Equipment'), 
            ('office_supplies', 'Office Supplies'), 
            ('audio_visual', 'Audio-Visual Equipment'), 
            ('storage_solutions', 'Storage Solutions')
        ], 
        verbose_name="Category"
    )
    product_name=models.TextField(max_length=250)
    brand = models.CharField(max_length=100, verbose_name="Brand")
    description = models.TextField(verbose_name="Property Description")
    created_at = models.DateTimeField(default=timezone.now)
    condition = models.CharField(max_length=11, 
        choices=[('new', 'New'), ('used', 'Used'), ('refurbished', 'Refurbished')], 
        verbose_name="Condition"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    warranty_status = models.CharField(
        max_length=10, 
        choices=[('yes', 'Yes'), ('no', 'No')], 
        verbose_name="Warranty Status"
    )
    REGION_CHOICES = [
        ('MS', 'Muscat'),
        ('DH', 'Dhofar'),
        ('BT', 'Batinah'),
        ('DA', 'Dakhiliyah'),
        ('SH', 'Sharqiyah'),
        ('BR', 'Buraimi'),
        ('ZU', 'Zufar'),
        ('MW', 'Musandam'),
        ('WR', 'Wusta'),
    ]

    regions = models.CharField(
        max_length=250,
        choices=REGION_CHOICES,
        default='MS'  
    )
    cities=models.TextField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    location=models.TextField(max_length=250)
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    images = models.ManyToManyField(
        'BusinessImage', 
        blank=True, 
        related_name='business', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'BusinessVideo', 
        blank=True, 
        related_name='business', 
        verbose_name="Videos"
    )

    def __str__(self):
        return self.brand

class BusinessImage(models.Model):
    image = models.ImageField(upload_to='Business/images/', verbose_name="Image")

    def __str__(self):
        return f"Image {self.id}"

class BusinessVideo(models.Model):
    video = models.FileField(upload_to='Business/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"
    


#Education & Training
class Education(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout','Soldout')
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='education'
    )
    course_type = models.CharField(
        max_length=50, 
        choices=[
            ('online', 'Online Learning'), 
            ('in_person', 'In-person'), 
            ('bootcamp', 'Coding Bootcamps')
        ], 
        verbose_name="Course Type"
    )
    subject = models.CharField(max_length=100, verbose_name="Course Subject")
    duration = models.IntegerField(verbose_name="Duration (weeks/months)")
    created_at = models.DateTimeField(default=timezone.now)
    description = models.TextField(verbose_name="Property Description")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Course Fee (OMR)")
    REGION_CHOICES = [
        ('MS', 'Muscat'),
        ('DH', 'Dhofar'),
        ('BT', 'Batinah'),
        ('DA', 'Dakhiliyah'),
        ('SH', 'Sharqiyah'),
        ('BR', 'Buraimi'),
        ('ZU', 'Zufar'),
        ('MW', 'Musandam'),
        ('WR', 'Wusta'),
    ]

    regions = models.CharField(
        max_length=250,
        choices=REGION_CHOICES,
        default='MS'  
    )
    cities=models.TextField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    location=models.TextField(max_length=250)
    instructor_name = models.CharField(max_length=255, verbose_name="Instructor Name")
    qualification = models.CharField(max_length=255, verbose_name="Instructor Qualification")
    experience = models.TextField(verbose_name="Instructor Experience")
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    images = models.ManyToManyField(
        'EducationImage', 
        blank=True, 
        related_name='education', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'EducationVideo', 
        blank=True, 
        related_name='education', 
        verbose_name="Videos"
    )

    def __str__(self):
        return self.subject

class EducationImage(models.Model):
    image = models.ImageField(upload_to='Education/images/', verbose_name="Image")

    def __str__(self):
        return f"Image {self.id}"

class EducationVideo(models.Model):
    video = models.FileField(upload_to='Education/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"


# Service Provider
class Service(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout','Soldout')
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='service'
    )
    service_type = models.CharField(
        max_length=50, 
        choices=[
            ('cleaning', 'Cleaning'), 
            ('maintenance', 'Maintenance'), 
            ('consulting', 'Consulting'), 
            ('legal', 'Legal Services'), 
            ('human_resources', 'Human Resources Services'), 
            ('medical', 'Medical Services'), 
            ('fitness', 'Fitness Services')
        ], 
        verbose_name="Service Type"
    )
    provider_name = models.CharField(max_length=255, verbose_name="Service Provider Name")
    price_range = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price Range (OMR)")
    created_at = models.DateTimeField(default=timezone.now)
    description = models.TextField(verbose_name="Property Description")
    contact_info = models.TextField(verbose_name="Contact Information")
    REGION_CHOICES = [
        ('MS', 'Muscat'),
        ('DH', 'Dhofar'),
        ('BT', 'Batinah'),
        ('DA', 'Dakhiliyah'),
        ('SH', 'Sharqiyah'),
        ('BR', 'Buraimi'),
        ('ZU', 'Zufar'),
        ('MW', 'Musandam'),
        ('WR', 'Wusta'),
    ]

    regions = models.CharField(
        max_length=250,
        choices=REGION_CHOICES,
        default='MS'  
    )
    cities=models.TextField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    location=models.TextField(max_length=250)
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    images = models.ManyToManyField(
        'ServiceImage', 
        blank=True, 
        related_name='service', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'ServiceVideo', 
        blank=True, 
        related_name='service', 
        verbose_name="Videos"
    )

    def __str__(self):
        return self.provider_name

class ServiceImage(models.Model):
    image = models.ImageField(upload_to='Service/images/', verbose_name="Image")

    def __str__(self):
        return f"Image {self.id}"
    
class ServiceVideo(models.Model):
    video = models.FileField(upload_to='Service/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"
    

# --------------------------------------------------------Mobile -----------------------------------------


# Computer and Mobile model
class Mobile(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout','Soldout')
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='mobile'
    )
    product_name=models.TextField(max_length=250)
    brand = models.CharField(max_length=100, verbose_name="Brand")
    description = models.TextField(verbose_name="Property Description")
    model_number = models.CharField(max_length=100, verbose_name="Model Number")
    created_at = models.DateTimeField(default=timezone.now)
    operating_system = models.CharField(
        max_length=50, 
        choices=[
            ('android', 'Android'),
            ('iOS', 'iOS'),
            ('windows', 'Windows'),
            ('other', 'Other')
        ], 
        verbose_name="Operating System"
    )
    screen_size = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Screen Size (inches)")
    storage_capacity = models.IntegerField(verbose_name="Storage Capacity (GB)")
    ram_size = models.IntegerField(verbose_name="RAM Size (GB)")
    battery_capacity = models.IntegerField(verbose_name="Battery Capacity (mAh)", null=True, blank=True)
    
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    condition = models.CharField(
        max_length=11, 
        choices=[
            ('new', 'New'),
            ('used', 'Used'),
            ('refurbished', 'Refurbished')
        ], 
        verbose_name="Condition"
    )
    REGION_CHOICES = [
        ('MS', 'Muscat'),
        ('DH', 'Dhofar'),
        ('BT', 'Batinah'),
        ('DA', 'Dakhiliyah'),
        ('SH', 'Sharqiyah'),
        ('BR', 'Buraimi'),
        ('ZU', 'Zufar'),
        ('MW', 'Musandam'),
        ('WR', 'Wusta'),
    ]

    regions = models.CharField(
        max_length=250,
        choices=REGION_CHOICES,
        default='MS'  
    )
    cities=models.TextField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    location=models.TextField(max_length=250)
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    images = models.ManyToManyField(
        'MobileImage', 
        blank=True, 
        related_name='mobile', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'MobileVideo', 
        blank=True, 
        related_name='mobile', 
        verbose_name="Videos"
    )

    def __str__(self):
        return self.brand

class MobileImage(models.Model):
    image = models.ImageField(upload_to='Mobile/images/', verbose_name="Image")

    def __str__(self):
        return f"Image {self.id}"
    
class MobileVideo(models.Model):
    video = models.FileField(upload_to='Mobile/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"

class Computer(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout','Soldout')
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='computer'
    )
    product_name=models.TextField(max_length=250)
    brand = models.CharField(max_length=100, verbose_name="Brand")
    created_at = models.DateTimeField(default=timezone.now)
    description = models.TextField(verbose_name="Property Description")
    model_number = models.CharField(max_length=100, verbose_name="Model Number")
    operating_system = models.CharField(
        max_length=50, 
        choices=[
            ('windows', 'Windows'),
            ('macOS', 'macOS'),
            ('linux', 'Linux'),
            ('other', 'Other')
        ], 
        verbose_name="Operating System"
    )
    screen_size = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Screen Size (inches)")
    storage_capacity = models.IntegerField(verbose_name="Storage Capacity (GB)")
    ram_size = models.IntegerField(verbose_name="RAM Size (GB)")
    processor = models.CharField(max_length=100, verbose_name="Processor Type")
    graphics_card = models.CharField(max_length=100, verbose_name="Graphics Card", null=True, blank=True)
    battery_life = models.CharField(max_length=50, verbose_name="Battery Life (hours)", null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    condition = models.CharField(
        max_length=11, 
        choices=[
            ('new', 'New'),
            ('used', 'Used'),
            ('refurbished', 'Refurbished')
        ], 
        verbose_name="Condition"
    )
    REGION_CHOICES = [
        ('MS', 'Muscat'),
        ('DH', 'Dhofar'),
        ('BT', 'Batinah'),
        ('DA', 'Dakhiliyah'),
        ('SH', 'Sharqiyah'),
        ('BR', 'Buraimi'),
        ('ZU', 'Zufar'),
        ('MW', 'Musandam'),
        ('WR', 'Wusta'),
    ]

    regions = models.CharField(
        max_length=250,
        choices=REGION_CHOICES,
        default='MS'  
    )
    cities=models.TextField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    location=models.TextField(max_length=250)
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    images = models.ManyToManyField(
        'ComputerImage', 
        blank=True, 
        related_name='computer', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'ComputerVideo', 
        blank=True, 
        related_name='computer', 
        verbose_name="Videos"
    )

    def __str__(self):
        return self.brand

class ComputerImage(models.Model):
    image = models.ImageField(upload_to='Mobile/computer/images/', verbose_name="Image")

    def __str__(self):
        return f"Image {self.id}"
    
class ComputerVideo(models.Model):
    video = models.FileField(upload_to='Computer/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"

class Sound(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout','Soldout')
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='sound'
    )
    product_name=models.TextField(max_length=250)
    brand = models.CharField(max_length=100, verbose_name="Brand")
    model_number = models.CharField(max_length=100, verbose_name="Model Number")
    created_at = models.DateTimeField(default=timezone.now)
    description = models.TextField(verbose_name="Property Description")
    connectivity = models.CharField(
        max_length=50, 
        choices=[
            ('bluetooth', 'Bluetooth'),
            ('wifi', 'Wi-Fi'),
            ('aux', 'AUX'),
            ('usb', 'USB'),
            ('other', 'Other')
        ], 
        verbose_name="Connectivity"
    )
    output_power = models.CharField(max_length=50, verbose_name="Output Power (e.g., 20W)")
    channels = models.CharField(max_length=50, verbose_name="Audio Channels (e.g., 2.1, 5.1)", null=True, blank=True)
    has_smart_assistant = models.BooleanField(default=False, verbose_name="Smart Assistant Support")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    condition = models.CharField(
        max_length=11, 
        choices=[
            ('new', 'New'),
            ('used', 'Used'),
            ('refurbished', 'Refurbished')
        ], 
        verbose_name="Condition"
    )
    REGION_CHOICES = [
        ('MS', 'Muscat'),
        ('DH', 'Dhofar'),
        ('BT', 'Batinah'),
        ('DA', 'Dakhiliyah'),
        ('SH', 'Sharqiyah'),
        ('BR', 'Buraimi'),
        ('ZU', 'Zufar'),
        ('MW', 'Musandam'),
        ('WR', 'Wusta'),
    ]

    regions = models.CharField(
        max_length=250,
        choices=REGION_CHOICES,
        default='MS'  
    )
    cities=models.TextField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    location=models.TextField(max_length=250)
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    images = models.ManyToManyField(
        'DeviceImage', 
        blank=True, 
        related_name='sound', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'SoundVideo', 
        blank=True, 
        related_name='sound', 
        verbose_name="Videos"
    )

    def __str__(self):
        return self.brand
   
class DeviceImage(models.Model):
    image = models.ImageField(upload_to='Mobile/devices/images/', verbose_name="Image")

    def __str__(self):
        return f"Image {self.id}"
    
class SoundVideo(models.Model):
    video = models.FileField(upload_to='Mobile/devices/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"
                                                                                                                                                                                               
                                                                                                                                                                                              
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

class Favorite(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Using the custom user model from settings
        on_delete=models.CASCADE,
        related_name='favorites'  # You can change the related name as needed
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def _str_(self):
        return f"{self.user} - {self.content_object}"


# joib hiring
from django.db import models
from django.conf import settings

class Company(models.Model):
    COMPANY_TYPES = [
        ('private', 'Private'),
        ('partnership', 'Partnership'),
        ('civil_company', 'Civil Company'),
        ('public', 'Public'),
    ]

    INDUSTRIES = [
        ('agriculture', 'Agriculture'),
        ('accounting', 'Accounting'),
        ('it', 'IT'),
        ('education', 'Education'),
        ('healthcare', 'Healthcare'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='companies'
    )
    company_name = models.CharField(max_length=255,unique=True)
    company_type = models.CharField(max_length=20, choices=COMPANY_TYPES)
    trade_license = models.CharField(max_length=50)
    contact_name = models.CharField(max_length=255)
    linkedin = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    industry = models.CharField(max_length=50, choices=INDUSTRIES)
    company_size = models.PositiveIntegerField()
    phone = models.CharField(max_length=20)
    logo = models.ImageField(upload_to='company_logos/')
    website = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)
    description = models.TextField()
    email = models.EmailField()
    REGION_CHOICES = [
        ('MS', 'Muscat'),
        ('DH', 'Dhofar'),
        ('BT', 'Batinah'),
        ('DA', 'Dakhiliyah'),
        ('SH', 'Sharqiyah'),
        ('BR', 'Buraimi'),
        ('ZU', 'Zufar'),
        ('MW', 'Musandam'),
        ('WR', 'Wusta'),
    ]
    
    regions = models.CharField(
        max_length=250,
        choices=REGION_CHOICES,
        default='MS'  
    )
    
    cities = models.TextField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    
    def __str__(self):
        return self.company_name
    def get_region_display(self):
        return dict(self.REGION_CHOICES).get(self.regions, self.regions)

class JobPost(models.Model):
    title = models.CharField(max_length=200, help_text="Job Title (e.g., Software Developer)")
    description = models.TextField(help_text="Detailed description of the role, responsibilities, and expectations.")
    job_type = models.CharField(
        max_length=50,
        choices=[
            ("full-time", "Full-time"),
            ("part-time", "Part-time"),
            ("contract", "Contract"),
            ("temporary", "Temporary"),
            ("freelance", "Freelance"),
            ("internship", "Internship"),
        ],
        default="full-time",
    )
    job_category = models.ForeignKey(JobCategory, on_delete=models.CASCADE, related_name="job_posts")
    salary_range = models.CharField(max_length=100, blank=True, null=True)
    work_location = models.CharField(max_length=255)
    number_of_vacancies = models.PositiveIntegerField(default=1)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    contact_email = models.EmailField()
    qualifications = models.TextField()
    skills_required = models.TextField()
    experience_required = models.CharField(max_length=100)
    application_deadline = models.DateField()
    working_hours = models.CharField(max_length=100, blank=True, null=True)
    posted_on = models.DateTimeField(auto_now_add=True)
    cities = models.TextField(max_length=250)
    regions = models.TextField(max_length=250)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='jobs'
    )
    def __str__(self):
        return self.title

class JobApplication(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Link to the custom user model
        on_delete=models.CASCADE,  # Delete applications if the user is deleted
        related_name='job_applications',  # Related name for reverse access
        verbose_name="User"
    )
    job = models.ForeignKey(
        JobPost,
        on_delete=models.CASCADE,
        related_name='applications',
        verbose_name="Job"
    )
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="Full Name")
    email = models.EmailField(verbose_name="Email Address")
    phone = models.CharField(max_length=15, verbose_name="Phone Number")
    resume = models.FileField(upload_to='resumes/', verbose_name="Upload Resume")
    applied_on = models.DateTimeField(auto_now_add=True, verbose_name="Applied On")

    def __str__(self):
        return f"{self.name} ({self.email})"



from django.conf import settings
from django.db import models
from django.utils.timezone import now

class ChatMessage(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()
    timestamp = models.DateTimeField(default=now)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username} - {self.message[:30]}"
    

   
class Automobile(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout', 'Soldout')
    ]
    TRANSACTION_CHOICES = [
        ('sell', 'Sell'),
        ('rent', 'Rent'),
    ]
    REGIONAL_SPEC_CHOICES = [
        ('gcc', 'GCC Spec'),
        ('euro', 'European Spec'),
        ('usa', 'USA Spec'),
        ('japan', 'Japanese Spec'),
        ('other', 'Other'),
    ]
    RENTAL_PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cars')
    name = models.CharField(max_length=100, verbose_name="Name")
    make = models.CharField(max_length=100, verbose_name="Car Manufacturer")
    year = models.CharField(max_length=100,verbose_name="Year of Manufacture")
    body_type = models.CharField(max_length=100, verbose_name="Car Body Type")
    created_at = models.DateTimeField(default=timezone.now)
    fuel_type = models.CharField(
        max_length=50,
        choices=[('petrol', 'Petrol'), ('diesel', 'Diesel'), ('electric', 'Electric'), ('hybrid', 'Hybrid')],
        verbose_name="Fuel Type"
    )
    engine_capacity = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Engine Capacity (cc)")
    transmission = models.CharField(
        max_length=50,
        choices=[('automatic', 'Automatic'), ('manual', 'Manual')],
        verbose_name="Transmission Type"
    )
    
    exterior_color = models.CharField(max_length=50, verbose_name="Exterior Color")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    REGION_CHOICES = [
        ('MS', 'Muscat'),
        ('DH', 'Dhofar'),
        ('BT', 'Al Batinah'),
        ('DA', 'Al Dakhiliya'),
        ('SH', 'Al Sharqiya'),
        ('BR', 'Al Buraimi'),
        ('ZU', 'Al Dhahirah'),
        ('MW', 'Musandam'),
        ('WR', 'Al Wusta'),
    ]

    regions = models.CharField(
        max_length=250,
        choices=REGION_CHOICES,
        default='MS'  
    )
    listing_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_CHOICES,
        default='sell',
        verbose_name="Listing Type"
    )
    cities=models.TextField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    location=models.TextField(max_length=250)
    description = models.TextField(verbose_name="Description")
    warranty_status = models.CharField(
        max_length=10,
        choices=[('yes', 'Yes'), ('no', 'No')],
        verbose_name="Warranty Status"
    )
    condition = models.CharField(
        max_length=10,
        choices=[('new', 'New'), ('used', 'Used'), ('import', 'Import')],
        verbose_name="Condition"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Approval Status"
    )
    # New fields added
    regional_spec = models.CharField(
        max_length=20,
        choices=REGIONAL_SPEC_CHOICES,
        default='gcc',
        verbose_name="Regional Specification"
    )
    number_of_seats = models.PositiveIntegerField(
        verbose_name="Number of Seats",
        null=True,
        blank=True
    )
    vin_chassis_number = models.CharField(
        max_length=50,
        verbose_name="VIN/Chassis Number",
        blank=True,
        null=True,
        unique=True
    )
    rental_period = models.CharField(
        max_length=10,
        choices=RENTAL_PERIOD_CHOICES,
        null=True,
        blank=True,
        verbose_name="Rental Period"
        )
    images = models.ManyToManyField(
        'AutomobileImage', 
        blank=True, 
        related_name='automobile', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'AutomobileVideo', 
        blank=True, 
        related_name='automobile', 
        verbose_name="Videos"
    )

    def get_region_display(self):
        return dict(self.REGION_CHOICES).get(self.regions, self.regions)

class AutomobileImage(models.Model):
    image = models.ImageField(upload_to='automobile/images/', verbose_name="Image")

    def __str__(self):
        return f"Image {self.id}"

class AutomobileVideo(models.Model):
    video = models.FileField(upload_to='automobile/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"
  

    
# Motorcycles Model
class Motorcycle(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout', 'Soldout')
    ]
    TRANSACTION_CHOICES = [
        ('sell', 'Sell'),
        ('rent', 'Rent'),
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='motorcycles'
    )
    make = models.CharField(max_length=100, verbose_name="Manufacturer")
    name = models.CharField(max_length=100, verbose_name="Name")
    model = models.CharField(max_length=100, verbose_name="Model")
    created_at = models.DateTimeField(default=timezone.now)
    year = models.CharField(max_length=100,verbose_name="Year of Manufacture")
    description = models.TextField(verbose_name="Description")
    REGION_CHOICES = [
        ('MS', 'Muscat'),
        ('DH', 'Dhofar'),
        ('BT', 'Al Batinah'),
        ('DA', 'Al Dakhiliya'),
        ('SH', 'Al Sharqiya'),
        ('BR', 'Al Buraimi'),
        ('ZU', 'Al Dhahirah'),
        ('MW', 'Musandam'),
        ('WR', 'Al Wusta'),
    ]

    regions = models.CharField(
        max_length=250,
        choices=REGION_CHOICES,
        default='MS'  
    )
    cities=models.TextField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    location=models.TextField(max_length=250)
    body_type = models.CharField(max_length=100, verbose_name="Motorcycle Type")
    listing_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_CHOICES,
        default='sell',
        verbose_name="Listing Type"
    )
    engine_capacity = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Engine Capacity (cc)")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    condition = models.CharField(
        max_length=10,
        choices=[('new', 'New'), ('used', 'Used')],
        verbose_name="Condition"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Approval Status"
    )
    images = models.ManyToManyField(
        'MotorcycleImage', 
        blank=True, 
        related_name='motorcycle', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'MotorcycleVideo', 
        blank=True, 
        related_name='motorcycle', 
        verbose_name="Videos"
    )

    def get_region_display(self):
        return dict(self.REGION_CHOICES).get(self.regions, self.regions)

class MotorcycleImage(models.Model):
    image = models.ImageField(upload_to='Motorcycle/images/', verbose_name="Image")

    def __str__(self):
        return f"Image {self.id}"

class MotorcycleVideo(models.Model):
    video = models.FileField(upload_to='Motorcycle/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"

# Auto Accessories & Parts Model
class AutoAccessoryPart(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='auto_accessories'
    )
    # Type choices
    TYPE_CHOICES = [
        ('ALARM', 'Alarm System'),
        ('CAMERA', 'Cameras & Sensors'),
        ('CLEANING', 'Cleaning Tools and Fresheners'),
        ('FLOORS', 'Floors and Covers'),
        ('GPS', 'GPS'),
        ('KEYS', 'Keys'),
        ('PHONE', 'Phone Holders and Accessories'),
        ('RECORDER', 'Recorders'),
        ('SCREEN', 'Screens'),
        ('SOUND', 'Sound System'),
        ('SPARK', 'Spark Plug'),
        ('SPEAKER', 'Speakers'),
        ('WINDOW', 'Window Tint-Stickers'),
        ('WIPER', 'Windshield Wipers'),
        ('OTHER', 'Other'),
    ]
    PROVIDE_DELIVERY_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    type = models.CharField(
        max_length=110, 
        choices=TYPE_CHOICES, 
        default='OTHER',
        verbose_name="Type"
    )
    provide = models.CharField(
        max_length=3, 
        choices=PROVIDE_DELIVERY_CHOICES, 
        default='no', 
        verbose_name="Delivery"
    )
    

    name = models.CharField(max_length=100, verbose_name="Accessory/Part Name")
    description = models.TextField(verbose_name="Description")
    created_at = models.DateTimeField(default=timezone.now)
    REGION_CHOICES = [
         ('MS', 'Muscat'),
        ('DH', 'Dhofar'),
        ('BT', 'Al Batinah'),
        ('DA', 'Al Dakhiliya'),
        ('SH', 'Al Sharqiya'),
        ('BR', 'Al Buraimi'),
        ('ZU', 'Al Dhahirah'),
        ('MW', 'Musandam'),
        ('WR', 'Al Wusta'),
    ]
    

    regions = models.CharField(
        max_length=250,
        choices=REGION_CHOICES,
        default='MS'  
    )
    condition = models.CharField(
        max_length=10, 
        choices=[('used', 'Used'), ('like_new', 'Like New')], 
        verbose_name="Condition"
    )
    cities=models.CharField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
   
    
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')],
        default='pending',
        verbose_name="Approval Status"
    )

    def get_region_display(self):
        return dict(self.REGION_CHOICES).get(self.regions, self.regions)
    
    images = models.ManyToManyField(
        'AutoAccessoryPartImage', 
        blank=True, 
        related_name='accessoriesparts', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'AutoAccessoryPartVideo', 
        blank=True, 
        related_name='accessoriesparts', 
        verbose_name="Videos"
    )

class AutoAccessoryPartImage(models.Model):
    image = models.ImageField(upload_to='accessoriesparts/images/', verbose_name="Image")

    def __str__(self):
        return f"Image {self.id}"

class AutoAccessoryPartVideo(models.Model):
    video = models.FileField(upload_to='accessoriesparts/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"

class HeavyVehicle(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout', 'Soldout')
    ]
    TRANSACTION_CHOICES = [
        ('sell', 'Sell'),
        ('rent', 'Rent'),
    ]
    CONDITION_CHOICES = [
        ('new', 'New'),
        ('used', 'Used')
    ]
     
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='heavy_vehicles'
    )
    listing_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_CHOICES,
        default='sell',
        verbose_name="Listing Type"
    )
    name = models.CharField(max_length=255, verbose_name="Vehicle Name")
    description = models.TextField(verbose_name="Description")
    REGION_CHOICES = [
         ('MS', 'Muscat'),
        ('DH', 'Dhofar'),
        ('BT', 'Al Batinah'),
        ('DA', 'Al Dakhiliya'),
        ('SH', 'Al Sharqiya'),
        ('BR', 'Al Buraimi'),
        ('ZU', 'Al Dhahirah'),
        ('MW', 'Musandam'),
        ('WR', 'Al Wusta'),
    ]

    regions = models.CharField(
        max_length=250,
        choices=REGION_CHOICES,
        default='MS'  
    )
    cities=models.TextField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    
    manufacturer = models.CharField(max_length=100, verbose_name="Manufacturer")
    make = models.CharField(max_length=100, verbose_name="Make")
    created_at = models.DateTimeField(default=timezone.now)
    year = models.PositiveIntegerField(verbose_name="Year of Manufacture")
    
    transmission = models.CharField(
        max_length=50,
        choices=[('automatic', 'Automatic'), ('manual', 'Manual')],
        verbose_name="Transmission Type"
    )
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Price (OMR)")
   
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, verbose_name="Condition")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Approval Status")
  
    images = models.ManyToManyField(
        'HeavyVehicleImage', 
        blank=True, 
        related_name='heavyvehicle', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'HeavyVehicleVideo', 
        blank=True, 
        related_name='heavyvehicle', 
        verbose_name="Videos"
    )
    
    def get_region_display(self):
        return dict(self.REGION_CHOICES).get(self.regions, self.regions)
    
class HeavyVehicleImage(models.Model):
    image = models.ImageField(upload_to='heavyvehicle/images/', verbose_name="Image")

    def __str__(self):
        return f"Image {self.id}"

class HeavyVehicleVideo(models.Model):
    video = models.FileField(upload_to='heavyvehicle/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"

class Boat(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout', 'Soldout')
    ]
    TRANSACTION_CHOICES = [
        ('sell', 'Sell'),
        ('rent', 'Rent'),
    ]
    CONDITION_CHOICES = [
        ('new', 'New'),
        ('used', 'Used')
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='boats'
    )
    listing_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_CHOICES,
        default='sell',
        verbose_name="Listing Type"
    )
    name = models.CharField(max_length=255, verbose_name="Boat Name")
    description = models.TextField(verbose_name="Description")
    manufacturer = models.CharField(max_length=100, verbose_name="Manufacturer")
    created_at = models.DateTimeField(default=timezone.now)
   
    REGION_CHOICES = [
        ('MS', 'Muscat'),
        ('DH', 'Dhofar'),
        ('BT', 'Al Batinah'),
        ('DA', 'Al Dakhiliya'),
        ('SH', 'Al Sharqiya'),
        ('BR', 'Al Buraimi'),
        ('ZU', 'Al Dhahirah'),
        ('MW', 'Musandam'),
        ('WR', 'Al Wusta'),
    ]

    regions = models.CharField(
        max_length=250,
        choices=REGION_CHOICES,
        default='MS'  
    )
    cities=models.TextField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
   
   
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Price (OMR)")
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, verbose_name="Condition")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Approval Status")
   

    images = models.ManyToManyField(
        'BoatImage', 
        blank=True, 
        related_name='boat', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'BoatVideo', 
        blank=True, 
        related_name='boat', 
        verbose_name="Videos"
    )

    def get_region_display(self):
        return dict(self.REGION_CHOICES).get(self.regions, self.regions)

class BoatImage(models.Model):
    image = models.ImageField(upload_to='boat/images/', verbose_name="Image")

    def __str__(self):
        return f"Image {self.id}"

class BoatVideo(models.Model):
    video = models.FileField(upload_to='boat/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"
    



from django.utils.translation import gettext_lazy as _

# Number Plates Model
class NumberPlate(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='number_plates'
    )
    class PlateType(models.TextChoices):
        COMMERCIAL = "commercial", _("Commercial")
        DRIVING_TRAINING = "driving_training", _("Driving Training")
        MOTORCYCLE = "motorcycle", _("Motorcycle")
        PERSONAL = "personal", _("Personal")
        RENTAL = "rental", _("Rental")
        TAXI_BUSES = "taxi_buses", _("Taxi Buses")
        TAXI_SEDAN = "taxi_sedan", _("Taxi Sedan")

    TRANSACTION_CHOICES = [
        ('sell', 'Sell'),
        ('rent', 'Rent'),
        ('wanted', 'Wanted')
    ]
    listing_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_CHOICES,
        default='sell',
        verbose_name="Listing Type"
    )
    number = models.CharField(max_length=20, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    letter_english = models.CharField(max_length=10)
    letter_arabic = models.CharField(max_length=10)
    plate_type = models.CharField(max_length=20, choices=PlateType.choices)
    created_at = models.DateTimeField(default=timezone.now)
    seller_name = models.CharField(max_length=100)
    description = models.TextField(verbose_name="Description")
    REGION_CHOICES = [
        ('MS', 'Muscat'),
        ('DH', 'Dhofar'),
        ('BT', 'Al Batinah'),
        ('DA', 'Al Dakhiliya'),
        ('SH', 'Al Sharqiya'),
        ('BR', 'Al Buraimi'),
        ('ZU', 'Al Dhahirah'),
        ('MW', 'Musandam'),
        ('WR', 'Al Wusta'),
    ]

    regions = models.CharField(
        max_length=250,
        choices=REGION_CHOICES,
        default='MS'  
    )
    cities=models.TextField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    location=models.TextField(max_length=250)
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')],
        default='pending',
        verbose_name="Approval Status"
    )
    
    def get_region_display(self):
        return dict(self.REGION_CHOICES).get(self.regions, self.regions)
    
    def __str__(self):
        return f"{self.number} - {self.plate_type}"
    
    def get_plate_design(self):
        return f"[ {self.letter_arabic} | {self.letter_english} | {self.number} | {self.plate_type} ]"



from django.db import models

class UploadedImage(models.Model):
    image = models.ImageField(upload_to='images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image uploaded at {self.uploaded_at}"


from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.conf import settings

class DrivingTraining(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='driving_trainings'
    )

    trainer_name = models.CharField(max_length=255)
    trainer_gender = models.CharField(
        max_length=10, 
        choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]
    )
    transmission = models.CharField(
        max_length=10, 
        choices=[('Automatic', 'Automatic'), ('Manual', 'Manual')]
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    body_type = models.CharField(
        max_length=20, 
        choices=[('Sedan', 'Sedan'), ('Hatchback', 'Hatchback'), ('Small Truck', 'Small Truck'), ('Large Truck', 'Large Truck'), ('Motorcycle', 'Motorcycle')]
    )
    model_year = models.PositiveIntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    description = models.TextField(verbose_name="Description")
    REGION_CHOICES = [
        ('MS', 'Muscat'),
        ('DH', 'Dhofar'),
        ('BT', 'Batinah'),
        ('DA', 'Dakhiliyah'),
        ('SH', 'Sharqiyah'),
        ('BR', 'Buraimi'),
        ('ZU', 'Zufar'),
        ('MW', 'Musandam'),
        ('WR', 'Wusta'),
    ]
    regions = models.CharField(
        max_length=250,
        choices=REGION_CHOICES,
        default='MS'  
    )
    cities = models.TextField(max_length=250)
    
    location = models.TextField(max_length=250)
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')],
        default='pending',
        verbose_name="Approval Status"
    )
    language = models.CharField(max_length=100)
    about_instructor = models.TextField()
    images = models.ManyToManyField(
        'DrivingTrainingImage', 
        blank=True, 
        related_name='driving_training', 
        verbose_name="Images"
    )

    def _str_(self):
        return f"{self.trainer_name} - {self.body_type} ({self.model_year})"

class DrivingTrainingImage(models.Model):
    image = models.ImageField(upload_to='driving_training/images/', verbose_name="Image")

    def _str_(self):
        return f"Image {self.id}"
    

# -----------------------------------------------------------------------------

class Apartment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout','Soldout')
    ]
    TRANSACTION_CHOICES = [
        ('sell', 'Sell'),
        ('rent', 'Rent'),
    ]
    RENTAL_PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
        ]
    BUILDING_AGE_CHOICES = [
        ('under_construction', 'Under Construction'),
        ('0-11_months', '0-11 Months'),
        ('1-5_years', '1-5 Years'),
        ('6-9_years', '6-9 Years'),
        ('10-19_years', '10-19 Years'),
        ('20+_years', '20+ Years'),
    ]
    FURNISHED_CHOICES = [
        ('furnished', 'Furnished'),
        ('semi_furnished', 'Semi-Furnished'),
        ('unfurnished', 'Unfurnished'),
    ]
    LISTER_TYPE_CHOICES = [
        ('agent', 'Agent'),
        ('landlord', 'Landlord'),
    ]
    PROPERTY_MORTGAGE_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    FACADE_CHOICES = [
        ('northern', 'Northern'),
        ('southern', 'Southern'),
        ('eastern', 'Eastern'),
        ('western', 'Western'),
        ('northeast', 'Northeast'),
        ('southeast', 'Southeast'),
        ('northwest', 'Northwest'),
        ('southwest', 'Southwest'),

    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='apartment'
    )
    property_title = models.CharField(max_length=255, verbose_name="Property Title")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    created_at = models.DateTimeField(default=timezone.now)
    REGION_CHOICES = [
        ('MS', 'Muscat'),
        ('DH', 'Dhofar'),
        ('BT', 'Al Batinah'),
        ('DA', 'Al Dakhiliya'),
        ('SH', 'Al Sharqiya'),
        ('BR', 'Al Buraimi'),
        ('ZU', 'Al Dhahirah'),
        ('MW', 'Musandam'),
        ('WR', 'Al Wusta'),
    ]
    regions = models.CharField(
        max_length=250,
        choices=REGION_CHOICES,
        default='MS'  
    )
    cities=models.TextField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    plot_area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Surface Area")
    bedrooms = models.CharField(
        max_length=10,
        choices=[
            ('studio', 'Studio'),
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4'),
            ('5', '5'),
            ('6+', '6+'),
        ],
        verbose_name="Number of Bedrooms"
    )
    bathrooms = models.CharField(
        max_length=10,
        choices=[
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4'),
            ('5', '5'),
            ('6+', '6+'),
        ],
        verbose_name="Number of Bathrooms"
    )
    description = models.TextField(verbose_name="Property Description")
    FLOOR_CHOICES = [
    ('1_floor', '1 Floor'),
    ('2_floor', '2 Floors'),  # Fixed
    ('3_floor', '3 Floors'),  # Fixed
    ('4_floor', '4 Floors'),  # Fixed
    ('5_floor', '5+ Floors'),  # Fixed
    ]

    floors = models.CharField(
       max_length=250,
       choices=FLOOR_CHOICES,
       default='1_floor'  # Fixed
    )
    listing_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_CHOICES,
        default='sell',
        verbose_name="Listing Type"
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    furnished = models.CharField(
        max_length=20, 
        choices=FURNISHED_CHOICES, 
        default='unfurnished', 
        verbose_name="Furnished"
    )
    rental_period = models.CharField(
        max_length=10,
        choices=RENTAL_PERIOD_CHOICES,
        null=True,
        blank=True,
        verbose_name="Rental Period"
        )
    building = models.CharField(max_length=20, choices=BUILDING_AGE_CHOICES,default='under_construction',  verbose_name="Building Age")
    lister_type = models.CharField(
        max_length=10,
        choices=LISTER_TYPE_CHOICES,
        verbose_name="Lister Type"
    )  
    property_mortgage = models.CharField(
        max_length=3, 
        choices=PROPERTY_MORTGAGE_CHOICES, 
        default='no', 
        verbose_name="Property Mortgage"
    )
    nearby_location = models.ManyToManyField(NearbyLocation) 
    main_amenities = models.ManyToManyField(MainAmenities)
    additional_amenities = models.ManyToManyField(AdditionalAmenities) 
    facade = models.CharField(
        max_length=10, 
        choices=FACADE_CHOICES, 
        verbose_name="Facade"
    )
    images = models.ManyToManyField(
        'ApartmentImage', 
        blank=True, 
        related_name='Apartment', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'ApartmentVideo',
        blank=True,
        related_name='Apartment',
        verbose_name="Videos"
    )

    def __str__(self):
        return self.property_title
    
    def get_region_display(self):
        return dict(self.REGION_CHOICES).get(self.regions, self.regions)

class ApartmentImage(models.Model):
    image = models.ImageField(upload_to='Apartment/images/', verbose_name="Image")

    def __str__(self):
        return f"Image {self.id}"

class ApartmentVideo(models.Model):
    video = models.FileField(upload_to='Apartment/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"
    
class Factory(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout','Soldout')
    ]
    TRANSACTION_CHOICES = [
        ('sell', 'Sell'),
        ('rent', 'Rent'),
    ]

    RENTAL_PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
        ]
    PROPERTY_MORTGAGE_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    LISTER_TYPE_CHOICES = [
        ('agent', 'Agent'),
        ('landlord', 'Landlord'),
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='factory'
    )
    property_title = models.CharField(max_length=255, verbose_name="Property Title")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    created_at = models.DateTimeField(default=timezone.now)
    nearby_location = models.ManyToManyField(NearbyLocation) 
    main_amenities = models.ManyToManyField(MainAmenities)
    additional_amenities = models.ManyToManyField(AdditionalAmenities) 
    REGION_CHOICES = [
        ('MS', 'Muscat'),
        ('DH', 'Dhofar'),
        ('BT', 'Al Batinah'),
        ('DA', 'Al Dakhiliya'),
        ('SH', 'Al Sharqiya'),
        ('BR', 'Al Buraimi'),
        ('ZU', 'Al Dhahirah'),
        ('MW', 'Musandam'),
        ('WR', 'Al Wusta'),
    ]

    regions = models.CharField(
        max_length=250,
        choices=REGION_CHOICES,
        default='MS'  
    )
    cities=models.TextField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    plot_area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Surface Area")
    description = models.TextField(verbose_name="Property Description")
    listing_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_CHOICES,
        default='sell',
        verbose_name="Listing Type"
    )
  
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    property_mortgage = models.CharField(
        max_length=3, 
        choices=PROPERTY_MORTGAGE_CHOICES, 
        default='no', 
        verbose_name="Property Mortgage"
    )
    images = models.ManyToManyField(
        'FactoryImage', 
        blank=True, 
        related_name='Factory', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'FactoryVideo',
        blank=True,
        related_name='Factory',
        verbose_name="Videos"
    )
    rental_period = models.CharField(
        max_length=10,
        choices=RENTAL_PERIOD_CHOICES,
        null=True,
        blank=True,
        verbose_name="Rental Period"
        )
    lister_type = models.CharField(
        max_length=10,
        choices=LISTER_TYPE_CHOICES,
        verbose_name="Lister Type"
    )

    def __str__(self):
        return self.property_title
    
    def get_region_display(self):
        return dict(self.REGION_CHOICES).get(self.regions, self.regions)

class FactoryImage(models.Model):
    image = models.ImageField(upload_to='Factory/images/', verbose_name="Image")

    def __str__(self):
        return f"Image {self.id}"

class FactoryVideo(models.Model):
    video = models.FileField(upload_to='Factory/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"
    

class Complex(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout','Soldout')
    ]
    TRANSACTION_CHOICES = [
        ('sell', 'Sell'),
        ('rent', 'Rent'),
    ]
    RENTAL_PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
        ]
    PROPERTY_MORTGAGE_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    LISTER_TYPE_CHOICES = [
        ('agent', 'Agent'),
        ('landlord', 'Landlord'),
    ]
    PROPERTY_CHOICES = [
        ('complete', 'Complete'),
        ('under_construction', 'Under Construction'),
            ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='complex'
    )
    property_title = models.CharField(max_length=255, verbose_name="Property Title")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    created_at = models.DateTimeField(default=timezone.now)
    REGION_CHOICES = [
        ('MS', 'Muscat'),
        ('DH', 'Dhofar'),
        ('BT', 'Al Batinah'),
        ('DA', 'Al Dakhiliya'),
        ('SH', 'Al Sharqiya'),
        ('BR', 'Al Buraimi'),
        ('ZU', 'Al Dhahirah'),
        ('MW', 'Musandam'),
        ('WR', 'Al Wusta'),
    ]

    regions = models.CharField(
        max_length=250,
        choices=REGION_CHOICES,
        default='MS'  
    )
    cities=models.TextField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    plot_area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Surface Area")
    nearby_location = models.ManyToManyField(NearbyLocation) 
    main_amenities = models.ManyToManyField(MainAmenities)
    additional_amenities = models.ManyToManyField(AdditionalAmenities)
    description = models.TextField(verbose_name="Property Description")
    FLOOR_CHOICES = [
    ('1_floor', '1 Floor'),
    ('2_floor', '2 Floors'),  # Fixed
    ('3_floor', '3 Floors'),  # Fixed
    ('4_floor', '4 Floors'),  # Fixed
    ('5_floor', '5+ Floors'),  # Fixed
    ]

    floors = models.CharField(
       max_length=250,
       choices=FLOOR_CHOICES,
       default='1_floor'  # Fixed
    )
    listing_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_CHOICES,
        default='sell',
        verbose_name="Listing Type"
    )
  
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    rental_period = models.CharField(
        max_length=10,
        choices=RENTAL_PERIOD_CHOICES,
        null=True,
        blank=True,
        verbose_name="Rental Period"
        )
    property_mortgage = models.CharField(
        max_length=3, 
        choices=PROPERTY_MORTGAGE_CHOICES, 
        default='no', 
        verbose_name="Property Mortgage"
    )
    images = models.ManyToManyField(
        'ComplexImage', 
        blank=True, 
        related_name='Complex', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'ComplexVideo',
        blank=True,
        related_name='Complex',
        verbose_name="Videos"
    )
    lister_type = models.CharField(
        max_length=10,
        choices=LISTER_TYPE_CHOICES,
        verbose_name="Lister Type"
    )
    property = models.CharField(
        max_length=20,
        choices=PROPERTY_CHOICES,
         default='under_construction', 
        verbose_name="Property Status"
    )

    def __str__(self):
        return self.property_title
    
    def get_region_display(self):
        return dict(self.REGION_CHOICES).get(self.regions, self.regions)

class ComplexImage(models.Model):
    image = models.ImageField(upload_to='Complex/images/', verbose_name="Image")

    def __str__(self):
        return f"Image {self.id}"

class ComplexVideo(models.Model):
    video = models.FileField(upload_to='Complex/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"
    
class Clinic(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout','Soldout')
    ]
    TRANSACTION_CHOICES = [
        ('sell', 'Sell'),
        ('rent', 'Rent'),
    ]
    RENTAL_PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
        ]
    PROPERTY_MORTGAGE_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    LISTER_TYPE_CHOICES = [
        ('agent', 'Agent'),
        ('landlord', 'Landlord'),
    ]
    PROPERTY_CHOICES = [
        ('complete', 'Complete'),
        ('under_construction', 'Under Construction'),
            ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='clinic'
    )
    property_title = models.CharField(max_length=255, verbose_name="Property Title")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    created_at = models.DateTimeField(default=timezone.now)
    REGION_CHOICES = [
        ('MS', 'Muscat'),
        ('DH', 'Dhofar'),
        ('BT', 'Al Batinah'),
        ('DA', 'Al Dakhiliya'),
        ('SH', 'Al Sharqiya'),
        ('BR', 'Al Buraimi'),
        ('ZU', 'Al Dhahirah'),
        ('MW', 'Musandam'),
        ('WR', 'Al Wusta'),
    ]

    regions = models.CharField(
        max_length=250,
        choices=REGION_CHOICES,
        default='MS'  
    )
    cities=models.TextField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    nearby_location = models.ManyToManyField(NearbyLocation) 
    main_amenities = models.ManyToManyField(MainAmenities)
    additional_amenities = models.ManyToManyField(AdditionalAmenities)
    plot_area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Surface Area")
   
    description = models.TextField(verbose_name="Property Description")
    FLOOR_CHOICES = [
    ('basement_floor', 'Basement Floor'),
    ('semiground_floor', 'Semi Ground Floor'),
    ('ground_floor', 'Ground Floor'),
    ('1_floor', '1 Floor'),
    ('2_floor', '2 Floors'),
    ('3_floor', '3 Floors'),
    ('4_floor', '4 Floors'),
    ('5_floor', '5 Floors'),
    ('6_floor', '6 Floors'),
    ('7_floor', '7 Floors'),
    ('8_floor', '8 Floors'),
    ('lastfloorwith_roof', 'Last Floor with Roof'),
]
    FURNISHED_CHOICES = [
        ('furnished', 'Furnished'),
        ('semi_furnished', 'Semi-Furnished'),
        ('unfurnished', 'Unfurnished'),
    ]
    furnished = models.CharField(
        max_length=20, 
        choices=FURNISHED_CHOICES, 
        default='unfurnished', 
        verbose_name="Furnished"
    )
    floors = models.CharField(
       max_length=250,
       choices=FLOOR_CHOICES,
       default='1_floor'  # Fixed
    )
    listing_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_CHOICES,
        default='sell',
        verbose_name="Listing Type"
    )
    rental_period = models.CharField(
        max_length=10,
        choices=RENTAL_PERIOD_CHOICES,
        null=True,
        blank=True,
        verbose_name="Rental Period"
        )
  
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    property_mortgage = models.CharField(
        max_length=3, 
        choices=PROPERTY_MORTGAGE_CHOICES, 
        default='no', 
        verbose_name="Property Mortgage"
    )
    images = models.ManyToManyField(
        'ClinicImage', 
        blank=True, 
        related_name='Clinic', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'ClinicVideo',
        blank=True,
        related_name='Clinic',
        verbose_name="Videos"
    )
    lister_type = models.CharField(
        max_length=10,
        choices=LISTER_TYPE_CHOICES,
        verbose_name="Lister Type"
    )
    property = models.CharField(
        max_length=20,
        choices=PROPERTY_CHOICES,
         default='under_construction', 
        verbose_name="Property Status"
    )

    def __str__(self):
        return self.property_title
    
    def get_region_display(self):
        return dict(self.REGION_CHOICES).get(self.regions, self.regions)

class ClinicImage(models.Model):
    image = models.ImageField(upload_to='Clinic/images/', verbose_name="Image")

    def __str__(self):
        return f"Image {self.id}"

class ClinicVideo(models.Model):
    video = models.FileField(upload_to='Clinic/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"
    
class Hostel(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout','Soldout')
    ]
    TRANSACTION_CHOICES = [
        ('sell', 'Sell'),
        ('rent', 'Rent'),
    ]
    RENTAL_PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
        ]
    PROPERTY_MORTGAGE_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    LISTER_TYPE_CHOICES = [
        ('agent', 'Agent'),
        ('landlord', 'Landlord'),
    ]
    PROPERTY_CHOICES = [
        ('complete', 'Complete'),
        ('under_construction', 'Under Construction'),
            ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='Hostel'
    )
    property_title = models.CharField(max_length=255, verbose_name="Property Title")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    created_at = models.DateTimeField(default=timezone.now)
    nearby_location = models.ManyToManyField(NearbyLocation) 
    main_amenities = models.ManyToManyField(MainAmenities)
    additional_amenities = models.ManyToManyField(AdditionalAmenities)
    bedrooms = models.CharField(
        max_length=10,
        choices=[
            ('studio', 'Studio'),
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4'),
            ('5', '5'),
            ('6+', '6+'),
        ],
        verbose_name="Number of Bedrooms"
    )
    REGION_CHOICES = [
        ('MS', 'Muscat'),
        ('DH', 'Dhofar'),
        ('BT', 'Al Batinah'),
        ('DA', 'Al Dakhiliya'),
        ('SH', 'Al Sharqiya'),
        ('BR', 'Al Buraimi'),
        ('ZU', 'Al Dhahirah'),
        ('MW', 'Musandam'),
        ('WR', 'Al Wusta'),
    ]

    regions = models.CharField(
        max_length=250,
        choices=REGION_CHOICES,
        default='MS'  
    )
    FURNISHED_CHOICES = [
        ('furnished', 'Furnished'),
        ('semi_furnished', 'Semi-Furnished'),
        ('unfurnished', 'Unfurnished'),
    ]
    furnished = models.CharField(
        max_length=20, 
        choices=FURNISHED_CHOICES, 
        default='unfurnished', 
        verbose_name="Furnished"
    )
    cities=models.TextField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    plot_area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Surface Area")
    description = models.TextField(verbose_name="Property Description")
    FLOOR_CHOICES = [
    ('1_floor', '1 Floor'),
    ('2_floor', '2 Floors'),  # Fixed
    ('3_floor', '3 Floors'),  # Fixed
    ('4_floor', '4 Floors'),  # Fixed
    ('5_floor', '5+ Floors'),  # Fixed
    ]

    floors = models.CharField(
       max_length=250,
       choices=FLOOR_CHOICES,
       default='1_floor'  # Fixed
    )
    listing_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_CHOICES,
        default='sell',
        verbose_name="Listing Type"
    )
    rental_period = models.CharField(
        max_length=10,
        choices=RENTAL_PERIOD_CHOICES,
        null=True,
        blank=True,
        verbose_name="Rental Period"
        )
  
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    property_mortgage = models.CharField(
        max_length=3, 
        choices=PROPERTY_MORTGAGE_CHOICES, 
        default='no', 
        verbose_name="Property Mortgage"
    )
    images = models.ManyToManyField(
        'HostelImage', 
        blank=True, 
        related_name='Hostel', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'HostelVideo',
        blank=True,
        related_name='Hostel',
        verbose_name="Videos"
    )
    lister_type = models.CharField(
        max_length=10,
        choices=LISTER_TYPE_CHOICES,
        verbose_name="Lister Type"
    )
    property = models.CharField(
        max_length=20,
        choices=PROPERTY_CHOICES,
         default='under_construction', 
        verbose_name="Property Status"
    )

    def __str__(self):
        return self.property_title
    
    def get_region_display(self):
        return dict(self.REGION_CHOICES).get(self.regions, self.regions)

class HostelImage(models.Model):
    image = models.ImageField(upload_to='Hostel/images/', verbose_name="Image")

    def __str__(self):
        return f"Image {self.id}"

class HostelVideo(models.Model):
    video = models.FileField(upload_to='Hostel/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"
    


class Office(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout','Soldout')
    ]
    TRANSACTION_CHOICES = [
        ('sell', 'Sell'),
        ('rent', 'Rent'),
    ]
    RENTAL_PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
        ]
    PROPERTY_MORTGAGE_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    LISTER_TYPE_CHOICES = [
        ('agent', 'Agent'),
        ('landlord', 'Landlord'),
    ]
    PROPERTY_CHOICES = [
        ('complete', 'Complete'),
        ('under_construction', 'Under Construction'),
            ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='Office'
    )
    property_title = models.CharField(max_length=255, verbose_name="Property Title")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    created_at = models.DateTimeField(default=timezone.now)
    FURNISHED_CHOICES = [
        ('furnished', 'Furnished'),
        ('semi_furnished', 'Semi-Furnished'),
        ('unfurnished', 'Unfurnished'),
    ]
    furnished = models.CharField(
        max_length=20, 
        choices=FURNISHED_CHOICES, 
        default='unfurnished', 
        verbose_name="Furnished"
    )
    nearby_location = models.ManyToManyField(NearbyLocation) 
    main_amenities = models.ManyToManyField(MainAmenities)
    additional_amenities = models.ManyToManyField(AdditionalAmenities)
    REGION_CHOICES = [
        ('MS', 'Muscat'),
        ('DH', 'Dhofar'),
        ('BT', 'Al Batinah'),
        ('DA', 'Al Dakhiliya'),
        ('SH', 'Al Sharqiya'),
        ('BR', 'Al Buraimi'),
        ('ZU', 'Al Dhahirah'),
        ('MW', 'Musandam'),
        ('WR', 'Al Wusta'),
    ]

    regions = models.CharField(
        max_length=250,
        choices=REGION_CHOICES,
        default='MS'  
    )
    cities=models.TextField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    plot_area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Surface Area")
   
    description = models.TextField(verbose_name="Property Description")
    FLOOR_CHOICES = [
    ('basement_floor', 'Basement Floor'),
    ('semiground_floor', 'Semi Ground Floor'),
    ('ground_floor', 'Ground Floor'),
    ('1_floor', '1 Floor'),
    ('2_floor', '2 Floors'),
    ('3_floor', '3 Floors'),
    ('4_floor', '4 Floors'),
    ('5_floor', '5 Floors'),
    ('6_floor', '6 Floors'),
    ('7_floor', '7 Floors'),
    ('8_floor', '8 Floors'),
    ('lastfloorwith_roof', 'Last Floor with Roof'),
]

    floors = models.CharField(
       max_length=250,
       choices=FLOOR_CHOICES,
       default='1_floor'  # Fixed
    )
    listing_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_CHOICES,
        default='sell',
        verbose_name="Listing Type"
    )
  
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    rental_period = models.CharField(
        max_length=10,
        choices=RENTAL_PERIOD_CHOICES,
        null=True,
        blank=True,
        verbose_name="Rental Period"
        )
    property_mortgage = models.CharField(
        max_length=3, 
        choices=PROPERTY_MORTGAGE_CHOICES, 
        default='no', 
        verbose_name="Property Mortgage"
    )
    images = models.ManyToManyField(
        'OfficeImage', 
        blank=True, 
        related_name='Office', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'OfficeVideo',
        blank=True,
        related_name='Office',
        verbose_name="Videos"
    )
    lister_type = models.CharField(
        max_length=10,
        choices=LISTER_TYPE_CHOICES,
        verbose_name="Lister Type"
    )
    property = models.CharField(
        max_length=20,
        choices=PROPERTY_CHOICES,
         default='under_construction', 
        verbose_name="Property Status"
    )

    def __str__(self):
        return self.property_title
    
    def get_region_display(self):
        return dict(self.REGION_CHOICES).get(self.regions, self.regions)

class OfficeImage(models.Model):
    image = models.ImageField(upload_to='Office/images/', verbose_name="Image")

    def __str__(self):
        return f"Image {self.id}"

class OfficeVideo(models.Model):
    video = models.FileField(upload_to='Office/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"
    

class Shop(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout','Soldout')
    ]
    TRANSACTION_CHOICES = [
        ('sell', 'Sell'),
        ('rent', 'Rent'),
    ]
    RENTAL_PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
        ]
    PROPERTY_MORTGAGE_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    LISTER_TYPE_CHOICES = [
        ('agent', 'Agent'),
        ('landlord', 'Landlord'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='Shop'
    )
    property_title = models.CharField(max_length=255, verbose_name="Property Title")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    created_at = models.DateTimeField(default=timezone.now)
    nearby_location = models.ManyToManyField(NearbyLocation) 
    main_amenities = models.ManyToManyField(MainAmenities)
    additional_amenities = models.ManyToManyField(AdditionalAmenities)
    REGION_CHOICES = [
        ('MS', 'Muscat'),
        ('DH', 'Dhofar'),
        ('BT', 'Al Batinah'),
        ('DA', 'Al Dakhiliya'),
        ('SH', 'Al Sharqiya'),
        ('BR', 'Al Buraimi'),
        ('ZU', 'Al Dhahirah'),
        ('MW', 'Musandam'),
        ('WR', 'Al Wusta'),
    ]

    regions = models.CharField(
        max_length=250,
        choices=REGION_CHOICES,
        default='MS'  
    )
    cities=models.TextField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    plot_area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Surface Area")
   
    description = models.TextField(verbose_name="Property Description")
    
    listing_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_CHOICES,
        default='sell',
        verbose_name="Listing Type"
    )
  
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    property_mortgage = models.CharField(
        max_length=3, 
        choices=PROPERTY_MORTGAGE_CHOICES, 
        default='no', 
        verbose_name="Property Mortgage"
    )
    rental_period = models.CharField(
        max_length=10,
        choices=RENTAL_PERIOD_CHOICES,
        null=True,
        blank=True,
        verbose_name="Rental Period"
        )
    images = models.ManyToManyField(
        'ShopImage', 
        blank=True, 
        related_name='Shop', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'ShopVideo',
        blank=True,
        related_name='Shop',
        verbose_name="Videos"
    )
    lister_type = models.CharField(
        max_length=10,
        choices=LISTER_TYPE_CHOICES,
        verbose_name="Lister Type"
    )
   
    def __str__(self):
        return self.property_title
    
    def get_region_display(self):
        return dict(self.REGION_CHOICES).get(self.regions, self.regions)

class ShopImage(models.Model):
    image = models.ImageField(upload_to='Shop/images/', verbose_name="Image")

    def __str__(self):
        return f"Image {self.id}"

class ShopVideo(models.Model):
    video = models.FileField(upload_to='Shop/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"
    

class Cafe(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout','Soldout')
    ]
    TRANSACTION_CHOICES = [
        ('sell', 'Sell'),
        ('rent', 'Rent'),
    ]
    RENTAL_PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
        ]
    PROPERTY_MORTGAGE_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    LISTER_TYPE_CHOICES = [
        ('agent', 'Agent'),
        ('landlord', 'Landlord'),
    ]
    PROPERTY_CHOICES = [
        ('complete', 'Complete'),
        ('under_construction', 'Under Construction'),
            ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='Cafe'
    )
    property_title = models.CharField(max_length=255, verbose_name="Property Title")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    created_at = models.DateTimeField(default=timezone.now)
    nearby_location = models.ManyToManyField(NearbyLocation) 
    main_amenities = models.ManyToManyField(MainAmenities)
    additional_amenities = models.ManyToManyField(AdditionalAmenities)  
    REGION_CHOICES = [
        ('MS', 'Muscat'),
        ('DH', 'Dhofar'),
        ('BT', 'Al Batinah'),
        ('DA', 'Al Dakhiliya'),
        ('SH', 'Al Sharqiya'),
        ('BR', 'Al Buraimi'),
        ('ZU', 'Al Dhahirah'),
        ('MW', 'Musandam'),
        ('WR', 'Al Wusta'),
    ]

    regions = models.CharField(
        max_length=250,
        choices=REGION_CHOICES,
        default='MS'  
    )
    cities=models.TextField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    plot_area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Surface Area")
   
    description = models.TextField(verbose_name="Property Description")
    
    
    listing_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_CHOICES,
        default='sell',
        verbose_name="Listing Type"
    )
  
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    property_mortgage = models.CharField(
        max_length=3, 
        choices=PROPERTY_MORTGAGE_CHOICES, 
        default='no', 
        verbose_name="Property Mortgage"
    )
    rental_period = models.CharField(
        max_length=10,
        choices=RENTAL_PERIOD_CHOICES,
        null=True,
        blank=True,
        verbose_name="Rental Period"
        )
    images = models.ManyToManyField(
        'CafeImage', 
        blank=True, 
        related_name='Cafe', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'CafeVideo',
        blank=True,
        related_name='Cafe',
        verbose_name="Videos"
    )
    lister_type = models.CharField(
        max_length=10,
        choices=LISTER_TYPE_CHOICES,
        verbose_name="Lister Type"
    )
    property = models.CharField(
        max_length=20,
        choices=PROPERTY_CHOICES,
         default='under_construction', 
        verbose_name="Property Status"
    )

    def __str__(self):
        return self.property_title
    
    def get_region_display(self):
        return dict(self.REGION_CHOICES).get(self.regions, self.regions)

class CafeImage(models.Model):
    image = models.ImageField(upload_to='Cafe/images/', verbose_name="Image")

    def __str__(self):
        return f"Image {self.id}"

class CafeVideo(models.Model):
    video = models.FileField(upload_to='Cafe/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"
    


class Staff(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout','Soldout')
    ]
    TRANSACTION_CHOICES = [
        ('sell', 'Sell'),
        ('rent', 'Rent'),
    ]
    RENTAL_PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
        ]
    PROPERTY_MORTGAGE_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    LISTER_TYPE_CHOICES = [
        ('agent', 'Agent'),
        ('landlord', 'Landlord'),
    ]
    PROPERTY_CHOICES = [
        ('complete', 'Complete'),
        ('under_construction', 'Under Construction'),
            ]
    FURNISHED_CHOICES = [
        ('furnished', 'Furnished'),
        ('semi_furnished', 'Semi-Furnished'),
        ('unfurnished', 'Unfurnished'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='Staff'
    )
    nearby_location = models.ManyToManyField(NearbyLocation) 
    main_amenities = models.ManyToManyField(MainAmenities)
    additional_amenities = models.ManyToManyField(AdditionalAmenities)  
    property_title = models.CharField(max_length=255, verbose_name="Property Title")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    created_at = models.DateTimeField(default=timezone.now)
    bedrooms = models.CharField(
        max_length=10,
        choices=[
            ('studio', 'Studio'),
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4'),
            ('5', '5'),
            ('6+', '6+'),
        ],
        verbose_name="Number of Bedrooms"
    )
    REGION_CHOICES = [
        ('MS', 'Muscat'),
        ('DH', 'Dhofar'),
        ('BT', 'Al Batinah'),
        ('DA', 'Al Dakhiliya'),
        ('SH', 'Al Sharqiya'),
        ('BR', 'Al Buraimi'),
        ('ZU', 'Al Dhahirah'),
        ('MW', 'Musandam'),
        ('WR', 'Al Wusta'),
    ]

    regions = models.CharField(
        max_length=250,
        choices=REGION_CHOICES,
        default='MS'  
    )
    cities=models.TextField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    plot_area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Plot Area")
   
    description = models.TextField(verbose_name="Property Description")
    FLOOR_CHOICES = [
    ('1_floor', '1 Floor'),
    ('2_floor', '2 Floors'),  # Fixed
    ('3_floor', '3 Floors'),  # Fixed
    ('4_floor', '4 Floors'),  # Fixed
    ('5_floor', '5+ Floors'),  # Fixed
    ]

    floors = models.CharField(
       max_length=250,
       choices=FLOOR_CHOICES,
       default='1_floor'  # Fixed
    )
    listing_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_CHOICES,
        default='sell',
        verbose_name="Listing Type"
    )
    furnished = models.CharField(
        max_length=20, 
        choices=FURNISHED_CHOICES, 
        default='unfurnished', 
        verbose_name="Furnished"
    )

  
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    property_mortgage = models.CharField(
        max_length=3, 
        choices=PROPERTY_MORTGAGE_CHOICES, 
        default='no', 
        verbose_name="Property Mortgage"
    )
    rental_period = models.CharField(
        max_length=10,
        choices=RENTAL_PERIOD_CHOICES,
        null=True,
        blank=True,
        verbose_name="Rental Period"
        )
    images = models.ManyToManyField(
        'StaffImage', 
        blank=True, 
        related_name='Staff', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'StaffVideo',
        blank=True,
        related_name='Staff',
        verbose_name="Videos"
    )
    lister_type = models.CharField(
        max_length=10,
        choices=LISTER_TYPE_CHOICES,
        verbose_name="Lister Type"
    )
    property = models.CharField(
        max_length=20,
        choices=PROPERTY_CHOICES,
         default='under_construction', 
        verbose_name="Property Status"
    )

    def __str__(self):
        return self.property_title
    
    def get_region_display(self):
        return dict(self.REGION_CHOICES).get(self.regions, self.regions)

class StaffImage(models.Model):
    image = models.ImageField(upload_to='Staff/images/', verbose_name="Image")

    def __str__(self):
        return f"Image {self.id}"

class StaffVideo(models.Model):
    video = models.FileField(upload_to='Staff/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"
    


class Warehouse(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout','Soldout')
    ]
    TRANSACTION_CHOICES = [
        ('sell', 'Sell'),
        ('rent', 'Rent'),
    ]
    RENTAL_PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
        ]
    PROPERTY_MORTGAGE_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    LISTER_TYPE_CHOICES = [
        ('agent', 'Agent'),
        ('landlord', 'Landlord'),
    ]
    PROPERTY_CHOICES = [
        ('complete', 'Complete'),
        ('under_construction', 'Under Construction'),
            ]
    

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='Warehouse'
    )
    property_title = models.CharField(max_length=255, verbose_name="Property Title")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    created_at = models.DateTimeField(default=timezone.now)
    nearby_location = models.ManyToManyField(NearbyLocation) 
    main_amenities = models.ManyToManyField(MainAmenities)
    additional_amenities = models.ManyToManyField(AdditionalAmenities)  
    REGION_CHOICES = [
        ('MS', 'Muscat'),
        ('DH', 'Dhofar'),
        ('BT', 'Al Batinah'),
        ('DA', 'Al Dakhiliya'),
        ('SH', 'Al Sharqiya'),
        ('BR', 'Al Buraimi'),
        ('ZU', 'Al Dhahirah'),
        ('MW', 'Musandam'),
        ('WR', 'Al Wusta'),
    ]

    regions = models.CharField(
        max_length=250,
        choices=REGION_CHOICES,
        default='MS'  
    )
    cities=models.TextField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    plot_area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Surface Area")
    description = models.TextField(verbose_name="Property Description")
    
    listing_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_CHOICES,
        default='sell',
        verbose_name="Listing Type"
    )
    
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    rental_period = models.CharField(
        max_length=10,
        choices=RENTAL_PERIOD_CHOICES,
        null=True,
        blank=True,
        verbose_name="Rental Period"
        )
    property_mortgage = models.CharField(
        max_length=3, 
        choices=PROPERTY_MORTGAGE_CHOICES, 
        default='no', 
        verbose_name="Property Mortgage"
    )
    images = models.ManyToManyField(
        'WarehouseImage', 
        blank=True, 
        related_name='Warehouse', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'WarehouseVideo',
        blank=True,
        related_name='Warehouse',
        verbose_name="Videos"
    )
    lister_type = models.CharField(
        max_length=10,
        choices=LISTER_TYPE_CHOICES,
        verbose_name="Lister Type"
    )
    property = models.CharField(
        max_length=20,
        choices=PROPERTY_CHOICES,
         default='under_construction', 
        verbose_name="Property Status"
    )

    def __str__(self):
        return self.property_title
    
    def get_region_display(self):
        return dict(self.REGION_CHOICES).get(self.regions, self.regions)

class WarehouseImage(models.Model):
    image = models.ImageField(upload_to='Warehouse/images/', verbose_name="Image")

    def __str__(self):
        return f"Image {self.id}"

class WarehouseVideo(models.Model):
    video = models.FileField(upload_to='Warehouse/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"

class Townhouse(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout','Soldout')
    ]
    TRANSACTION_CHOICES = [
        ('sell', 'Sell'),
        ('rent', 'Rent'),
    ]
    RENTAL_PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
        ]
    
    FURNISHED_CHOICES = [
        ('furnished', 'Furnished'),
        ('semi_furnished', 'Semi-Furnished'),
        ('unfurnished', 'Unfurnished'),
    ]
    BUILDING_AGE_CHOICES = [
        ('under_construction', 'Under Construction'),
        ('0-11_months', '0-11 Months'),
        ('1-5_years', '1-5 Years'),
        ('6-9_years', '6-9 Years'),
        ('10-19_years', '10-19 Years'),
        ('20+_years', '20+ Years'),
    ]
    
    LISTER_TYPE_CHOICES = [
        ('agent', 'Agent'),
        ('landlord', 'Landlord'),
    ]
    PROPERTY_MORTGAGE_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    FACADE_CHOICES = [
        ('northern', 'Northern'),
        ('southern', 'Southern'),
        ('eastern', 'Eastern'),
        ('western', 'Western'),
        ('northeast', 'Northeast'),
        ('southeast', 'Southeast'),
        ('northwest', 'Northwest'),
        ('southwest', 'Southwest'),

    ]
    nearby_location = models.ManyToManyField(NearbyLocation) 
    main_amenities = models.ManyToManyField(MainAmenities)
    additional_amenities = models.ManyToManyField(AdditionalAmenities)  
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='Townhouse'
    )
    property_title = models.CharField(max_length=255, verbose_name="Property Title")
    
    created_at = models.DateTimeField(default=timezone.now)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    REGION_CHOICES = [
        ('MS', 'Muscat'),
        ('DH', 'Dhofar'),
        ('BT', 'Al Batinah'),
        ('DA', 'Al Dakhiliya'),
        ('SH', 'Al Sharqiya'),
        ('BR', 'Al Buraimi'),
        ('ZU', 'Al Dhahirah'),
        ('MW', 'Musandam'),
        ('WR', 'Al Wusta'),
    ]

    regions = models.CharField(
        max_length=250,
        choices=REGION_CHOICES,
        default='MS'  
    )
    rental_period = models.CharField(
        max_length=10,
        choices=RENTAL_PERIOD_CHOICES,
        null=True,
        blank=True,
        verbose_name="Rental Period"
        )
    cities=models.TextField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    plot_area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Land Area")
    surface_area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Surface Area")
    FLOOR_CHOICES = [
    ('1_floor', '1 Floor'),
    ('2_floor', '2 Floors'),  # Fixed
    ('3_floor', '3 Floors'),  # Fixed
    ('4_floor', '4 Floors'),  # Fixed
    ('5_floor', '5+ Floors'),  # Fixed
    ]

    floors = models.CharField(
       max_length=250,
       choices=FLOOR_CHOICES,
       default='1_floor'  # Fixed
    )
    bedrooms = models.CharField(
        max_length=10,
        choices=[
            ('studio', 'Studio'),
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4'),
            ('5', '5'),
            ('6+', '6+'),
        ],
        verbose_name="Number of Bedrooms"
    )
    bathrooms = models.CharField(
        max_length=10,
        choices=[
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4'),
            ('5', '5'),
            ('6+', '6+'),
        ],
        verbose_name="Number of Bathrooms"
    )
    description = models.TextField(verbose_name="Property Description")
    
    
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    furnished = models.CharField(
        max_length=20, 
        choices=FURNISHED_CHOICES, 
        default='unfurnished', 
        verbose_name="Furnished"
    )
    building = models.CharField(max_length=20, choices=BUILDING_AGE_CHOICES,default='under_construction',  verbose_name="Building Age")
    
    listing_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_CHOICES,
        default='sell',
        verbose_name="Listing Type"
    )
    
    lister_type = models.CharField(
        max_length=10,
        choices=LISTER_TYPE_CHOICES,
        verbose_name="Lister Type"
    )
    
    
    property_mortgage = models.CharField(
        max_length=3, 
        choices=PROPERTY_MORTGAGE_CHOICES, 
        default='no', 
        verbose_name="Property Mortgage"
    )
    facade = models.CharField(
        max_length=10, 
        choices=FACADE_CHOICES, 
        verbose_name="Facade"
    )

    images = models.ManyToManyField(
        'TownhouseImage', 
        blank=True, 
        related_name='Townhouse', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'TownhouseVideo', 
        blank=True, 
        related_name='Townhouse', 
        verbose_name="Videos"
    )

    def get_region_display(self):
        return dict(self.REGION_CHOICES).get(self.regions, self.regions)
    
class TownhouseImage(models.Model):
    image = models.ImageField(upload_to='Townhouse/images/', verbose_name="Image")

    def __str__(self):
        return f"Image {self.id}"
class TownhouseVideo(models.Model):
    video = models.FileField(upload_to='Townhouse/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"



class Fullfloors(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout','Soldout')
    ]
    TRANSACTION_CHOICES = [
        ('sell', 'Sell'),
        ('rent', 'Rent'),
    ]
    RENTAL_PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
        ]
    
    LISTER_TYPE_CHOICES = [
        ('agent', 'Agent'),
        ('landlord', 'Landlord'),
    ]
    PROPERTY_MORTGAGE_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    PROPERTY_CHOICES = [
        ('complete', 'Complete'),
        ('under_construction', 'Under Construction'),
            ]
   

    nearby_location = models.ManyToManyField(NearbyLocation) 
    main_amenities = models.ManyToManyField(MainAmenities)
    additional_amenities = models.ManyToManyField(AdditionalAmenities)  
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='Fullfloors'
    )
    property_title = models.CharField(max_length=255, verbose_name="Property Title")
    
    created_at = models.DateTimeField(default=timezone.now)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    REGION_CHOICES = [
        ('MS', 'Muscat'),
        ('DH', 'Dhofar'),
        ('BT', 'Al Batinah'),
        ('DA', 'Al Dakhiliya'),
        ('SH', 'Al Sharqiya'),
        ('BR', 'Al Buraimi'),
        ('ZU', 'Al Dhahirah'),
        ('MW', 'Musandam'),
        ('WR', 'Al Wusta'),
    ]

    regions = models.CharField(
        max_length=250,
        choices=REGION_CHOICES,
        default='MS'  
    )
    cities=models.TextField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    plot_area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Surface Area")
    FLOOR_CHOICES = [
    ('basement_floor', 'Basement Floor'),
    ('semiground_floor', 'Semi Ground Floor'),
    ('ground_floor', 'Ground Floor'),
    ('1_floor', '1 Floor'),
    ('2_floor', '2 Floors'),
    ('3_floor', '3 Floors'),
    ('4_floor', '4 Floors'),
    ('5_floor', '5 Floors'),
    ('6_floor', '6 Floors'),
    ('7_floor', '7 Floors'),
    ('8_floor', '8 Floors'),
    ('lastfloorwith_roof', 'Last Floor with Roof'),
    ]
    floors = models.CharField(
       max_length=250,
       choices=FLOOR_CHOICES,
       default='1_floor'  # Fixed
    )
    rental_period = models.CharField(
        max_length=10,
        choices=RENTAL_PERIOD_CHOICES,
        null=True,
        blank=True,
        verbose_name="Rental Period"
        )
    description = models.TextField(verbose_name="Property Description")
    
    
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    
    listing_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_CHOICES,
        default='sell',
        verbose_name="Listing Type"
    )
    
    lister_type = models.CharField(
        max_length=10,
        choices=LISTER_TYPE_CHOICES,
        verbose_name="Lister Type"
    )
    property = models.CharField(
        max_length=20,
        choices=PROPERTY_CHOICES,
         default='under_construction', 
        verbose_name="Property Status"
    )
    
    
    property_mortgage = models.CharField(
        max_length=3, 
        choices=PROPERTY_MORTGAGE_CHOICES, 
        default='no', 
        verbose_name="Property Mortgage"
    )
   
    images = models.ManyToManyField(
        'FullfloorsImage', 
        blank=True, 
        related_name='Fullfloors', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'FullfloorsVideo', 
        blank=True, 
        related_name='Fullfloors', 
        verbose_name="Videos"
    )

    def get_region_display(self):
        return dict(self.REGION_CHOICES).get(self.regions, self.regions)
    
class FullfloorsImage(models.Model):
    image = models.ImageField(upload_to='Fullfloors/images/', verbose_name="Image")

    def __str__(self):
        return f"Image {self.id}"
class FullfloorsVideo(models.Model):
    video = models.FileField(upload_to='Fullfloors/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"
    



class Showrooms(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout','Soldout')
    ]
    TRANSACTION_CHOICES = [
        ('sell', 'Sell'),
        ('rent', 'Rent'),
    ]
    RENTAL_PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
        ]
    
    LISTER_TYPE_CHOICES = [
        ('agent', 'Agent'),
        ('landlord', 'Landlord'),
    ]
    PROPERTY_MORTGAGE_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    PROPERTY_CHOICES = [
        ('complete', 'Complete'),
        ('under_construction', 'Under Construction'),
            ]
   
    nearby_location = models.ManyToManyField(NearbyLocation) 
    main_amenities = models.ManyToManyField(MainAmenities)
    additional_amenities = models.ManyToManyField(AdditionalAmenities)  
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='Showrooms'
    )
    property_title = models.CharField(max_length=255, verbose_name="Property Title")
    
    created_at = models.DateTimeField(default=timezone.now)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    REGION_CHOICES = [
        ('MS', 'Muscat'),
        ('DH', 'Dhofar'),
        ('BT', 'Al Batinah'),
        ('DA', 'Al Dakhiliya'),
        ('SH', 'Al Sharqiya'),
        ('BR', 'Al Buraimi'),
        ('ZU', 'Al Dhahirah'),
        ('MW', 'Musandam'),
        ('WR', 'Al Wusta'),
    ]

    regions = models.CharField(
        max_length=250,
        choices=REGION_CHOICES,
        default='MS'  
    )
    cities=models.TextField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    plot_area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Surface Area")
    
    
   
    description = models.TextField(verbose_name="Property Description")
    
    
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    
    listing_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_CHOICES,
        default='sell',
        verbose_name="Listing Type"
    )
    rental_period = models.CharField(
        max_length=10,
        choices=RENTAL_PERIOD_CHOICES,
        null=True,
        blank=True,
        verbose_name="Rental Period"
        )
    
    lister_type = models.CharField(
        max_length=10,
        choices=LISTER_TYPE_CHOICES,
        verbose_name="Lister Type"
    )
    property = models.CharField(
        max_length=20,
        choices=PROPERTY_CHOICES,
         default='under_construction', 
        verbose_name="Property Status"
    )
    
    
    property_mortgage = models.CharField(
        max_length=3, 
        choices=PROPERTY_MORTGAGE_CHOICES, 
        default='no', 
        verbose_name="Property Mortgage"
    )
   
    images = models.ManyToManyField(
        'ShowroomsImage', 
        blank=True, 
        related_name='Showrooms', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'ShowroomsVideo', 
        blank=True, 
        related_name='Showrooms', 
        verbose_name="Videos"
    )

    def get_region_display(self):
        return dict(self.REGION_CHOICES).get(self.regions, self.regions)
    
class ShowroomsImage(models.Model):
    image = models.ImageField(upload_to='Showrooms/images/', verbose_name="Image")

    def __str__(self):
        return f"Image {self.id}"
class ShowroomsVideo(models.Model):
    video = models.FileField(upload_to='Showrooms/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"
    
class Wholebuilding(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout','Soldout')
    ]
    TRANSACTION_CHOICES = [
        ('sell', 'Sell'),
        ('rent', 'Rent'),
    ]
    RENTAL_PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
        ]
    
    LISTER_TYPE_CHOICES = [
        ('agent', 'Agent'),
        ('landlord', 'Landlord'),
    ]
    PROPERTY_MORTGAGE_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    PROPERTY_CHOICES = [
        ('complete', 'Complete'),
        ('under_construction', 'Under Construction'),
            ]
    BUILDING_AGE_CHOICES = [
        ('under_construction', 'Under Construction'),
        ('0-11_months', '0-11 Months'),
        ('1-5_years', '1-5 Years'),
        ('6-9_years', '6-9 Years'),
        ('10-19_years', '10-19 Years'),
        ('20+_years', '20+ Years'),
    ]
    FACADE_CHOICES = [
        ('northern', 'Northern'),
        ('southern', 'Southern'),
        ('eastern', 'Eastern'),
        ('western', 'Western'),
        ('northeast', 'Northeast'),
        ('southeast', 'Southeast'),
        ('northwest', 'Northwest'),
        ('southwest', 'Southwest'),

    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='Wholebuilding'
    )
    property_title = models.CharField(max_length=255, verbose_name="Property Title")
    created_at = models.DateTimeField(default=timezone.now)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    nearby_location = models.ManyToManyField(NearbyLocation) 
    REGION_CHOICES = [
        ('MS', 'Muscat'),
        ('DH', 'Dhofar'),
        ('BT', 'Al Batinah'),
        ('DA', 'Al Dakhiliya'),
        ('SH', 'Al Sharqiya'),
        ('BR', 'Al Buraimi'),
        ('ZU', 'Al Dhahirah'),
        ('MW', 'Musandam'),
        ('WR', 'Al Wusta'),
    ]

    regions = models.CharField(
        max_length=250,
        choices=REGION_CHOICES,
        default='MS'  
    )
    cities=models.TextField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    plot_area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Land Area")
    surface_area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Surface Area")
    FLOOR_CHOICES = [
    ('1_floor', '1 Floor'),
    ('2_floor', '2 Floors'),  # Fixed
    ('3_floor', '3 Floors'),  # Fixed
    ('4_floor', '4 Floors'),  # Fixed
    ('5_floor', '5+ Floors'),  # Fixed
    ]

    floors = models.CharField(
       max_length=250,
       choices=FLOOR_CHOICES,
       default='1_floor'  # Fixed
    )  
    rental_period = models.CharField(
        max_length=10,
        choices=RENTAL_PERIOD_CHOICES,
        null=True,
        blank=True,
        verbose_name="Rental Period"
        ) 
    description = models.TextField(verbose_name="Property Description")
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    
    listing_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_CHOICES,
        default='sell',
        verbose_name="Listing Type"
    )
    
    lister_type = models.CharField(
        max_length=10,
        choices=LISTER_TYPE_CHOICES,
        verbose_name="Lister Type"
    )
    property = models.CharField(
        max_length=20,
        choices=PROPERTY_CHOICES,
         default='under_construction', 
        verbose_name="Property Status"
    )
    building = models.CharField(max_length=20, choices=BUILDING_AGE_CHOICES,default='under_construction',  verbose_name="Building Age")
    property_mortgage = models.CharField(
        max_length=3, 
        choices=PROPERTY_MORTGAGE_CHOICES, 
        default='no', 
        verbose_name="Property Mortgage"
    )
    facade = models.CharField(
        max_length=10, 
        choices=FACADE_CHOICES, 
        verbose_name="Facade"
    )
   
    images = models.ManyToManyField(
        'WholebuildingImage', 
        blank=True, 
        related_name='Wholebuilding', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'WholebuildingVideo', 
        blank=True, 
        related_name='Wholebuilding', 
        verbose_name="Videos"
    )

    def get_region_display(self):
        return dict(self.REGION_CHOICES).get(self.regions, self.regions)
    
class WholebuildingImage(models.Model):
    image = models.ImageField(upload_to='Wholebuilding/images/', verbose_name="Image")

    def _str_(self):
        return f"Image {self.id}"
class WholebuildingVideo(models.Model):
    video = models.FileField(upload_to='Wholebuilding/videos/', verbose_name="Video")

    def _str_(self):
        return f"Video {self.id}"
    
class Supermarket(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout','Soldout')
    ]
    TRANSACTION_CHOICES = [
        ('sell', 'Sell'),
        ('rent', 'Rent'),
    ]
    RENTAL_PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
        ]
    
    LISTER_TYPE_CHOICES = [
        ('agent', 'Agent'),
        ('landlord', 'Landlord'),
    ]
    PROPERTY_MORTGAGE_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    PROPERTY_CHOICES = [
        ('complete', 'Complete'),
        ('under_construction', 'Under Construction'),
            ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='Supermarket'
    )
    property_title = models.CharField(max_length=255, verbose_name="Property Title")
    nearby_location = models.ManyToManyField(NearbyLocation) 
    main_amenities = models.ManyToManyField(MainAmenities)
    additional_amenities = models.ManyToManyField(AdditionalAmenities) 
    created_at = models.DateTimeField(default=timezone.now)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    REGION_CHOICES = [
        ('MS', 'Muscat'),
        ('DH', 'Dhofar'),
        ('BT', 'Al Batinah'),
        ('DA', 'Al Dakhiliya'),
        ('SH', 'Al Sharqiya'),
        ('BR', 'Al Buraimi'),
        ('ZU', 'Al Dhahirah'),
        ('MW', 'Musandam'),
        ('WR', 'Al Wusta'),
    ]

    regions = models.CharField(
        max_length=250,
        choices=REGION_CHOICES,
        default='MS'  
    )
    cities=models.TextField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    plot_area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Surface Area")
    description = models.TextField(verbose_name="Property Description")
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    
    listing_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_CHOICES,
        default='sell',
        verbose_name="Listing Type"
    )
    
    lister_type = models.CharField(
        max_length=10,
        choices=LISTER_TYPE_CHOICES,
        verbose_name="Lister Type"
    )
    property = models.CharField(
        max_length=20,
        choices=PROPERTY_CHOICES,
         default='under_construction', 
        verbose_name="Property Status"
    )
    rental_period = models.CharField(
        max_length=10,
        choices=RENTAL_PERIOD_CHOICES,
        null=True,
        blank=True,
        verbose_name="Rental Period"
        )
    property_mortgage = models.CharField(
        max_length=3, 
        choices=PROPERTY_MORTGAGE_CHOICES, 
        default='no', 
        verbose_name="Property Mortgage"
    )
    images = models.ManyToManyField(
        'SupermarketImage', 
        blank=True, 
        related_name='Supermarket', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'SupermarketVideo', 
        blank=True, 
        related_name='Supermarket', 
        verbose_name="Videos"
    )

    def get_region_display(self):
        return dict(self.REGION_CHOICES).get(self.regions, self.regions)
    
class SupermarketImage(models.Model):
    image = models.ImageField(upload_to='Supermarket/images/', verbose_name="Image")

    def _str_(self):
        return f"Image {self.id}"
class SupermarketVideo(models.Model):
    video = models.FileField(upload_to='Supermarket/videos/', verbose_name="Video")

    def _str_(self):
        return f"Video {self.id}"
    
class Foreign(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout','Soldout')
    ]
    TRANSACTION_CHOICES = [
        ('sell', 'Sell'),
        ('rent', 'Rent'),
    ]
    RENTAL_PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
        ]
    
    LISTER_TYPE_CHOICES = [
        ('agent', 'Agent'),
        ('landlord', 'Landlord'),
    ]
    PROPERTY_MORTGAGE_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    ESTATE_TYPE_CHOICES = [
        ('apartment', 'Apartment'),
        ('chalets', 'Chalets - Summer Houses'),
        ('commercial', 'Commercial'),
        ('farm', 'Farm'),
        ('land', 'Land'),
        ('villa', 'Villa House'),
    ]
    nearby_location = models.ManyToManyField(NearbyLocation) 
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='Foreign'
    )
    property_title = models.CharField(max_length=255, verbose_name="Property Title")
    created_at = models.DateTimeField(default=timezone.now)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    REGION_CHOICES = [
        ('MS', 'Muscat'),
        ('DH', 'Dhofar'),
        ('BT', 'Al Batinah'),
        ('DA', 'Al Dakhiliya'),
        ('SH', 'Al Sharqiya'),
        ('BR', 'Al Buraimi'),
        ('ZU', 'Al Dhahirah'),
        ('MW', 'Musandam'),
        ('WR', 'Al Wusta'),
    ]

    regions = models.CharField(
        max_length=250,
        choices=REGION_CHOICES,
        default='MS'  
    )
    cities=models.TextField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    country = CountryField(blank_label="Select Country")
    description = models.TextField(verbose_name="Property Description")
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    listing_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_CHOICES,
        default='sell',
        verbose_name="Listing Type"
    )
    lister_type = models.CharField(
        max_length=10,
        choices=LISTER_TYPE_CHOICES,
        verbose_name="Lister Type"
    )
    estate_type = models.CharField(
        max_length=20,
        choices=ESTATE_TYPE_CHOICES,
         default='apartment', 
        verbose_name="Estate Type"
    )
    rental_period = models.CharField(
        max_length=10,
        choices=RENTAL_PERIOD_CHOICES,
        null=True,
        blank=True,
        verbose_name="Rental Period"
        )
    property_mortgage = models.CharField(
        max_length=3, 
        choices=PROPERTY_MORTGAGE_CHOICES, 
        default='no', 
        verbose_name="Property Mortgage"
    )
    images = models.ManyToManyField(
        'ForeignImage', 
        blank=True, 
        related_name='Foreign', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'ForeignVideo', 
        blank=True, 
        related_name='Foreign', 
        verbose_name="Videos"
    )

    def get_region_display(self):
        return dict(self.REGION_CHOICES).get(self.regions, self.regions)
    
class ForeignImage(models.Model):
    image = models.ImageField(upload_to='Foreign/images/', verbose_name="Image")

    def _str_(self):
        return f"Image {self.id}"
class ForeignVideo(models.Model):
    video = models.FileField(upload_to='Foreign/videos/', verbose_name="Video")

    def _str_(self):
        return f"Video {self.id}"
    
class Shared(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout', 'Soldout')
    ]
    
    TRANSACTION_CHOICES = [
        ('rent', 'Rent'),
    ]
    
    RENTAL_PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]
    
    FURNISHED_CHOICES = [
        ('furnished', 'Furnished'),
        ('semi_furnished', 'Semi-Furnished'),
        ('unfurnished', 'Unfurnished'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='shared'
    )
    
    property_title = models.CharField(max_length=255, verbose_name="Property Title")
    created_at = models.DateTimeField(default=timezone.now)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    
    REGION_CHOICES = [
        ('MS', 'Muscat'),
        ('DH', 'Dhofar'),
        ('BT', 'Al Batinah'),
        ('DA', 'Al Dakhiliya'),
        ('SH', 'Al Sharqiya'),
        ('BR', 'Al Buraimi'),
        ('ZU', 'Al Dhahirah'),
        ('MW', 'Musandam'),
        ('WR', 'Al Wusta'),
    ]

    regions = models.CharField(
        max_length=250,
        choices=REGION_CHOICES,
        default='MS'  
    )
    
    cities = models.TextField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    description = models.TextField(verbose_name="Property Description")
    
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    
    listing_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_CHOICES,
        default='rent',
        verbose_name="Listing Type"
    )
    
    rental_period = models.CharField(
        max_length=10,
        choices=RENTAL_PERIOD_CHOICES,
        null=True,
        blank=True,
        verbose_name="Rental Period"
    )
    
    images = models.ManyToManyField(
        'SharedImage', 
        blank=True, 
        related_name='Shared', 
        verbose_name="Images"
    )
    
    videos = models.ManyToManyField(
        'SharedVideo', 
        blank=True, 
        related_name='Shared', 
        verbose_name="Videos"
    )
    
    furnished = models.CharField(
        max_length=20, 
        choices=FURNISHED_CHOICES, 
        default='unfurnished', 
        verbose_name="Furnished"
    )

    def get_region_display(self):
        return dict(self.REGION_CHOICES).get(self.regions, self.regions)
    
class SharedImage(models.Model):
    image = models.ImageField(upload_to='Shared/images/', verbose_name="Image")

    def __str__(self):
        return f"Image {self.id}"
    
class SharedVideo(models.Model):
    video = models.FileField(upload_to='Shared/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"



    
class Suits(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout', 'Soldout')
    ]
    
    TRANSACTION_CHOICES = [
        ('rent', 'Rent'),
    ]
    
    RENTAL_PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]
    
    FURNISHED_CHOICES = [
        ('furnished', 'Furnished'),
        ('semi_furnished', 'Semi-Furnished'),
        ('unfurnished', 'Unfurnished'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='Suits'
    )
    
    property_title = models.CharField(max_length=255, verbose_name="Property Title")
    created_at = models.DateTimeField(default=timezone.now)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    
    REGION_CHOICES = [
        ('MS', 'Muscat'),
        ('DH', 'Dhofar'),
        ('BT', 'Al Batinah'),
        ('DA', 'Al Dakhiliya'),
        ('SH', 'Al Sharqiya'),
        ('BR', 'Al Buraimi'),
        ('ZU', 'Al Dhahirah'),
        ('MW', 'Musandam'),
        ('WR', 'Al Wusta'),
    ]

    regions = models.CharField(
        max_length=250,
        choices=REGION_CHOICES,
        default='MS'  
    )
    
    cities = models.TextField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    description = models.TextField(verbose_name="Property Description")
    
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    
    listing_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_CHOICES,
        default='rent',
        verbose_name="Listing Type"
    )
    
    rental_period = models.CharField(
        max_length=10,
        choices=RENTAL_PERIOD_CHOICES,
        null=True,
        blank=True,
        verbose_name="Rental Period"
    )
    
    images = models.ManyToManyField(
        'SuitsImage', 
        blank=True, 
        related_name='Suits', 
        verbose_name="Images"
    )
    
    videos = models.ManyToManyField(
        'SuitsVideo', 
        blank=True, 
        related_name='Suits', 
        verbose_name="Videos"
    )
    
    furnished = models.CharField(
        max_length=20, 
        choices=FURNISHED_CHOICES, 
        default='unfurnished', 
        verbose_name="Furnished"
    )

    def get_region_display(self):
        return dict(self.REGION_CHOICES).get(self.regions, self.regions)
    
class SuitsImage(models.Model):
    image = models.ImageField(upload_to='Suits/images/', verbose_name="Image")

    def __str__(self):
        return f"Image {self.id}"
    
class SuitsVideo(models.Model):
    video = models.FileField(upload_to='Suits/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"
# ----------------------------------------------------------------------Motors---------------------------------------------------  


    

    
    

    

   
class Part(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout', 'Soldout')
    ]
    TYPES_CHOICES = [
        ('batteries', 'Batteries'),
        ('bodyparts', 'Body Parts'),
        ('mechanical', 'Mechanical Parts'),
        ('spareparts', 'Spare Parts'),
        ('other', 'Other'),
    ]
    SUBTYPE_CHOICES = {
        'batteries': [('batteries', 'Batteries'), ('hybrid', 'Hybrid')],
        'bodyparts': [('exterior', 'Exterior Parts'), ('interior', 'Interior Parts'), ('light', 'Light'), ('other', 'Other')],
        'mechanical': [
            ('brakes', 'Brakes'), ('chips', 'Computer Chips'), ('engines', 'Engines'),
            ('filters', 'Filters'), ('mechanical', 'Mechanical Parts'), ('oil', 'Oil'),
            ('suspensions', 'Suspensions'), ('transmission', 'Transmission'), ('other', 'Other')
        ],
        'spareparts': [
            ('coolers', 'Coolers'), ('headers', 'Headers'), ('sport_filters', 'Sport Filters'),
            ('steering_wheel', 'Steering Wheel'), ('turbo', 'Turbo Supercharge'), ('other', 'Other')
        ]
    }
    PROVIDE_DELIVERY_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    condition = models.CharField(
        max_length=10, 
        choices=[('used', 'Used'), ('like_new', 'Like New')], 
        verbose_name="Condition"
    )

    
   
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='Part'
    )
    
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    types = models.CharField(max_length=20, choices=TYPES_CHOICES, default='other')
    subtype = models.CharField(max_length=20)
    
    REGION_CHOICES = [
        ('MS', 'Muscat'),
        ('DH', 'Dhofar'),
        ('BT', 'Al Batinah'),
        ('DA', 'Al Dakhiliya'),
        ('SH', 'Al Sharqiya'),
        ('BR', 'Al Buraimi'),
        ('ZU', 'Al Dhahirah'),
        ('MW', 'Musandam'),
        ('WR', 'Al Wusta'),
    ]

    regions = models.CharField(
        max_length=250,
        choices=REGION_CHOICES,
        default='MS'  
    )
    
    cities = models.TextField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    description = models.TextField(verbose_name="Description")
    
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    provide = models.CharField(
        max_length=3, 
        choices=PROVIDE_DELIVERY_CHOICES, 
        default='no', 
        verbose_name="Delivery"
    )
    
   
    
    images = models.ManyToManyField(
        'PartImage', 
        blank=True, 
        related_name='Part', 
        verbose_name="Images"
    )
    
    videos = models.ManyToManyField(
        'PartVideo', 
        blank=True, 
        related_name='Part', 
        verbose_name="Videos"
    )
    
   

    def get_region_display(self):
        return dict(self.REGION_CHOICES).get(self.regions, self.regions)
    
class PartImage(models.Model):
    image = models.ImageField(upload_to='Carpart/images/', verbose_name="Image")

    def __str__(self):
        return f"Image {self.id}"
    
class PartVideo(models.Model):
    video = models.FileField(upload_to='Carpart/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"
    


    
class SportsCar(models.Model):
    # Status choices
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout', 'Soldout')
    ]
    
    # Rental period choices
    RENTAL_PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]
    
    # Vehicle specific body types
    BODYTYPE_CHOICES = [
        ('coupe', 'Coupe'),
        ('convertible', 'Convertible'),
        ('targa', 'Targa'),
        ('roadster', 'Roadster'),
        ('supercar', 'Supercar'),
        ('hypercar', 'Hypercar'),
        ('track', 'Track Car'),
        ('gt', 'Grand Tourer'),
    ]
    
    # Performance measurement units
    TOP_SPEED_UNITS = [
        ('kmh', 'km/h'),
        ('mph', 'mph'),
    ]
    
    make = models.CharField(max_length=100, verbose_name="Manufacturer")
    year = models.PositiveIntegerField(verbose_name="Year")
    description = models.TextField(verbose_name="Description")
    
    # Region choices for Oman
    REGION_CHOICES = [
        ('MS', 'Muscat'),
        ('DH', 'Dhofar'),
        ('BT', 'Al Batinah'),
        ('DA', 'Al Dakhiliya'),
        ('SH', 'Al Sharqiya'),
        ('BR', 'Al Buraimi'),
        ('ZU', 'Al Dhahirah'),
        ('MW', 'Musandam'),
        ('WR', 'Al Wusta'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='SportsCar'
    )

    # Body type field with specific choices
    bodytype = models.CharField(
        max_length=100, 
        choices=BODYTYPE_CHOICES,
        verbose_name="Vehicle Body Type"
    )
    
    # Performance fields
    top_speed = models.PositiveIntegerField(
        verbose_name="Top Speed",
        null=True,
        blank=True
    )
    
    top_speed_unit = models.CharField(
        max_length=5,
        choices=TOP_SPEED_UNITS,
        default='kmh',
        verbose_name="Top Speed Unit"
    )
    
    acceleration = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Acceleration Time",
        null=True,
        blank=True
    )
    
    
    
    drivetrain = models.CharField(
        max_length=20,
        choices=[
            ('rwd', 'Rear-Wheel Drive'),
            ('fwd', 'Front-Wheel Drive'),
            ('awd', 'All-Wheel Drive'),
            ('4wd', 'Four-Wheel Drive'),
        ],
        default='rwd',
        verbose_name="Drivetrain"
    )
    
    # Location fields
    regions = models.CharField(
        max_length=250,
        choices=REGION_CHOICES,
        default='MS'
    )
    
    cities = models.CharField(
        max_length=250,
        verbose_name="City"
    )
    
    latitude = models.FloatField(
        null=True,
        blank=True
    )
    
    longitude = models.FloatField(
        null=True,
        blank=True
    )
    
    # Rental details
    rental_period = models.CharField(
        max_length=10,
        choices=RENTAL_PERIOD_CHOICES,
        verbose_name="Rental Period"
    )
    
    rental_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Rental Price"
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Approval Status"
    )
    
    # Engine specifications
    horsepower = models.PositiveIntegerField(
        verbose_name="Horsepower",
        null=True,
        blank=True
    )
    
    torque = models.PositiveIntegerField(
        verbose_name="Torque (Nm)",
        null=True,
        blank=True
    )
    

    
    # Media fields
    images = models.ManyToManyField(
        'SportsCarImage', 
        blank=True, 
        related_name='sports_car', 
        verbose_name="Images"
    )
    
    videos = models.ManyToManyField(
        'SportsCarVideo', 
        blank=True, 
        related_name='sports_car', 
        verbose_name="Videos"
    )

    def get_region_display(self):
        return dict(self.REGION_CHOICES).get(self.regions, self.regions)

class SportsCarImage(models.Model):
    image = models.ImageField(upload_to='sports_cars/images/', verbose_name="Image")

    def __str__(self):
        return f"Image {self.id}"

class SportsCarVideo(models.Model):
    video = models.FileField(upload_to='sports_cars/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"
