from django.shortcuts import render
from .models import *
from django.urls import reverse
from django.utils.safestring import mark_safe
import json
from django.db.models import Q
from django_countries import countries


# Region code to name mapping
REGION_NAMES = {
    'MS': 'Muscat',
    'DH': 'Dhofar',
    'BT': 'Batinah',
    'DA': 'Ad Dakhiliyah',
    'SH': 'Ash Sharqiyah',
    'BZ': 'Al Buraimi',
    'BR': 'Buraimi',
    'DZ': 'Masandam',
    'WT': 'Al Wusta',
    'ZU': 'Zufar'
}

def index(request):
    advertisement=Advertisement.objects.all()
    # Get the filter parameters from the request
    selected_region_code = request.GET.get('region')  # Get region code
    selected_city = request.GET.get('city')
    selected_category = request.GET.get('category')
    selected_listing_type = request.GET.get('listing_type')
    name_query = request.GET.get('name', '')  # Get the search query (default is empty string)

    # Convert the selected region code to a full name
    selected_region = REGION_NAMES.get(selected_region_code, selected_region_code) if selected_region_code else None

    # Define the categories and their respective models
    categories = {
        'Electronics': Mobile,
        'Properties': Villa,
        'Motors': Automobile,  
    }

    # Initialize an empty list for ads
    all_ads = []

    # Filter based on selected region and city first (first filter type)
    for category_name, model in categories.items():
        if selected_category and category_name.lower() != selected_category.lower():
            continue  # Skip if the category does not match

        # Start building the query
        query = model.objects.filter(status='approved')

        # Filter by region if selected
        if selected_region_code:  # Keep filtering based on region **code** in the DB
            query = query.filter(regions__icontains=selected_region_code)

        # Filter by city if selected and not "All Cities"
        if selected_city and selected_city != "All Cities":
            query = query.filter(cities__icontains=selected_city)

        # Filter by name/search query if present (second filter type)
        if name_query:
            if model == Mobile:
                query = query.filter(Q(product_name__icontains=name_query) | Q(brand__icontains=name_query))
            elif model == Villa:
                query = query.filter(Q(property_title__icontains=name_query) | Q(description__icontains=name_query))
            elif model == Automobile:
                query = query.filter(Q(regions__icontains=name_query) | Q(cities__icontains=name_query) | Q(name__icontains=name_query) | Q(make__icontains=name_query))

        # Limit the number of items fetched
        items = query.order_by('-id')  # Adjust the limit as needed

        for item in items:
            product_type = category_name.lower()  # Dynamically create the product type
            images = [{"image": image.image.url} for image in item.images.all()]
            main_image_url = images[0]["image"] if images else "/static/assets/images/resource/default.jpg"
            images_json = mark_safe(json.dumps(images))

            all_ads.append({
                'category': category_name,
                'data': item,
                'product_type': product_type,
                'url': reverse('browseads11', kwargs={'category': product_type, 'id': item.id}),
                'main_image_url': main_image_url,
                'images_json': images_json,
                'total_images': len(images),
            })

    # Prepare category data for rendering
    category_data = {
        'Electronics': {'count': Mobile.objects.filter(status='approved').count(), 'icon': 'fa-plug', 'link': 'index3'},
        'Properties': {'count': Villa.objects.filter(status='approved').count(), 'icon': 'fa-building', 'link': 'index5'},
        'Motors': {'count': Automobile.objects.filter(status='approved').count(), 'icon': 'fa-car', 'link': 'index3'},
    }
   
    return render(request, 'index.html', {
        'advertisement':advertisement,
        'category_data': category_data,
        'all_ads': all_ads,
        'selected_region': selected_region,  # Now passing full region name
        'selected_city': selected_city,  # Pass the selected city to the template
        'selected_category': selected_category,
        'selected_listing_type': selected_listing_type,
        'name_query': name_query  # Pass the search query back to the template
        
    })

from django.shortcuts import render
from django.urls import reverse
from django.utils.safestring import mark_safe
import json
from .models import Region, City, Automobile, Motorcycle, HeavyVehicle, Boat  # Ensure you import your models


def index2(request):
    # Get the filter parameters from the request
    selected_region_code = request.GET.get('region')  # Get region code
    selected_city = request.GET.get('city')  # Get the selected city from the request
    selected_category = request.GET.get('category')
    selected_listing_type = request.GET.get('listing_type')
    name_query = request.GET.get('name', '')

    # Convert the selected region code to a full name
    selected_region = REGION_NAMES.get(selected_region_code, selected_region_code) if selected_region_code else None

    # Define categories and their respective models
    categories = {
        'automobiles': Automobile,
        'motorcycles': Motorcycle,
        'heavy_vehicles': HeavyVehicle,
        'boats': Boat,
        'accessoriesparts': AutoAccessoryPart,
        'number_plate': NumberPlate  # Include NumberPlate in categories
    }

    # Initialize an empty list for ads
    all_ads = []

    # Initialize category counts dictionary
    category_counts = {
        'automobiles_sell': 0,
        'automobiles_rent': 0,
        'number_plate': 0  # Initialize count for NumberPlate
    }

    # Process each category
    for category_name, model in categories.items():
        # Start building the query
        query = model.objects.filter(status='approved')

        # Apply filters
        if selected_region_code:  # Keep filtering based on region **code** in the DB
            query = query.filter(regions__icontains=selected_region_code)

        if selected_city and selected_city != "All Cities":
            query = query.filter(cities__icontains=selected_city)

        if selected_listing_type:
            query = query.filter(listing_type=selected_listing_type)

        if name_query:
            if model == Motorcycle:
                query = query.filter(
                    Q(make__icontains=name_query) | 
                    Q(name__icontains=name_query) | 
                    Q(model__icontains=name_query) | 
                    Q(year__icontains=name_query) | 
                    Q(regions__icontains=name_query) | 
                    Q(cities__icontains=name_query)
                )
            elif model == Boat:
                query = query.filter(
                    Q(name__icontains=name_query) | 
                    Q(manufacturer__icontains=name_query) | 
                    Q(year__icontains=name_query) | 
                    Q(regions__icontains=name_query) | 
                    Q(cities__icontains=name_query)
                )
            elif model == NumberPlate:
                query = query.filter(
                    Q(number__icontains=name_query) | 
                    Q(regions__icontains=name_query) | 
                    Q(cities__icontains=name_query)
                )
            elif model == AutoAccessoryPart:
                query = query.filter(
                    Q(name__icontains=name_query) | 
                    Q(regions__icontains=name_query) | 
                    Q(cities__icontains=name_query)
                )
            elif model == HeavyVehicle:
                query = query.filter(
                    Q(name__icontains=name_query) | 
                    Q(manufacturer__icontains=name_query) | 
                    Q(regions__icontains=name_query) | 
                    Q(cities__icontains=name_query)
                )
            elif model == Automobile:
                query = query.filter(
                    Q(regions__icontains=name_query) | 
                    Q(cities__icontains=name_query) | 
                    Q(name__icontains=name_query) | 
                    Q(make__icontains=name_query) | 
                    Q(year__icontains=name_query)
                )

        # Specific handling for automobiles
        if category_name == 'automobiles':
            category_counts['automobiles_sell'] = query.filter(listing_type='sell').count()
            category_counts['automobiles_rent'] = query.filter(listing_type='rent').count()

        # Count the total items for the category
        category_counts[category_name] = query.count()

        # Skip adding NumberPlate products to all_ads
        if category_name == 'number_plate':
            continue  # Skip the rest of the loop for NumberPlate

        # Fetch the latest items (limit to 5)
        items = query.order_by('-id')[:5]

        # Process each item in the category
        for item in items:
            # Fetch images and construct data-images JSON
            images = [{"image": image.image.url} for image in item.images.all()]
            main_image_url = images[0]["image"] if images else "/static/assets/images/resource/default.jpg"
            images_json = mark_safe(json.dumps(images))

            # Append ad data
            all_ads.append({
                'category': category_name[:-1].capitalize(),  # Singularized category name
                'data': item,
                'product_type': category_name[:-1].lower(),
                'url': reverse('browseads11', kwargs={'category': category_name, 'id': item.id}),
                'main_image_url': main_image_url,
                'images_json': images_json,
                'total_images': len(images),
            })

    # Prepare the context for rendering the template
    context = {
        'all_ads': all_ads,
        'selected_region': selected_region,  # Pass the full region name
        'selected_city': selected_city,  # Pass the selected city to the template
        'selected_category': selected_category,
        'selected_listing_type': selected_listing_type,
        'name_query': name_query,
        'category_counts': category_counts,
    }

    return render(request, 'index-2.html', context)
def indexarabic(request):
    return render(request, 'indexarabic.html') 

def login1(request):
    return render(request, 'login.html') 

def sign(request):
    return render(request, 'signup.html') 

# def map_view(request):
#     return render(request, 'map/map.html')

import json
import logging
from django.shortcuts import render
from django.db.models import Q
from .models import Mobile, Computer, Sound
def index6(request):
    # Define a mapping of region codes to full names (you can expand this as needed)
    region_mapping = {
        'MS': 'Muscat',
        'DH': 'Dhofar',
        'BT': 'Batinah',
        'DA': 'Dakhiliyah',
        'SH': 'Sharqiyah',
        'BR': 'Buraimi',
        'ZU': 'Zufar',
        'DZ': 'Masandam',
        'WR': 'Wusta',
    }

    # Define categories and their respective models
    categories = {
        'mobiles': Mobile,
        'computers': Computer,
        'sounds': Sound,
    }

    # Initialize the ads list
    all_ads = []

    # Get filter parameters from the request
    selected_region_code = request.GET.get('region')  # Get selected region code
    selected_city = request.GET.get('city')  # Get selected city
    selected_category = request.GET.get('category')
    name_query = request.GET.get('name', '')  # Search query

    # Convert the selected region code to a full name
    selected_region = region_mapping.get(selected_region_code, selected_region_code) if selected_region_code else None

    # Loop through each category (mobile, computer, sound)
    for category_name, model in categories.items():
        if selected_category and category_name.lower() != selected_category.lower():
            continue  # Skip if the category doesn't match

        # Start filtering the model
        query = model.objects.filter(status='approved')

        # Filter by region
        if selected_region_code:  # Keep filtering based on region **code** in the DB
            query = query.filter(regions__icontains=selected_region_code)

        # Filter by city if selected and not "All Cities"
        if selected_city and selected_city != "All Cities":
            query = query.filter(cities__icontains=selected_city)

        # Filter by search query
        if name_query:
            query = query.filter(
                Q(brand__icontains=name_query) | 
                Q(model_number__icontains=name_query) |
                Q(regions__icontains=name_query) |
                Q(cities__icontains=name_query)
            )

        # Fetch the latest items (You can adjust the limit as needed)
        items = query.order_by('-id')[:5]

        for item in items:
            images = [{"image": image.image.url} for image in item.images.all()]
            main_image_url = images[0]["image"] if images else "/static/assets/images/resource/default.jpg"
            images_json = json.dumps(images) if images else "[]"

            all_ads.append({
                'category': category_name[:-1],  # Singularize category name (e.g., 'mobiles' -> 'mobile')
                'data': item,
                'name': item.brand + (" " + item.model_number if hasattr(item, 'model_number') else ""),
                'main_image_url': main_image_url,
                'images_json': images_json,
                'product_type': category_name.lower(),
                'region_name': region_mapping.get(item.regions, item.regions),
            })

    # Count items in each category (you can also add filters for this)
    category_counts = {
        'mobiles': Mobile.objects.filter(status='approved').count(),
        'computers': Computer.objects.filter(status='approved').count(),
        'sounds': Sound.objects.filter(status='approved').count(),
    }

    # Log to check if all_ads has data
    logging.debug(f"All Ads: {all_ads}")

    # Prepare context for template
    context = {
        'all_ads': all_ads,
        'category_counts': category_counts,
        'selected_region': selected_region,  # Pass the full region name
        'selected_city': selected_city,  # Pass the selected city to the template
        'selected_category': selected_category,
        'name_query': name_query,
    }

    return render(request, 'index-6.html', context)

import json
import re
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.db.models import Q
from django.urls import reverse
from PIL import Image as PILImage, ImageFilter
import pytesseract
from pyproj import Proj, Transformer
from .models import Land, Villa, Commercial, Farm, Chalet, UploadedImage
from .forms import ImageUploadForm

def index3(request):
    # Mapping region codes to full names
    region_mapping = {
        'MS': 'Muscat', 'DH': 'Dhofar', 'BT': 'Batinah',
        'DA': 'Dakhiliyah', 'SH': 'Sharqiyah', 'BR': 'Buraimi',
        'ZU': 'Zufar', 'DZ': 'Masandam', 'WR': 'Wusta',
    }

    # Count approved ads in each category
    category_counts = {
        'villa': Villa.objects.filter(status='approved').count(),
        'land': Land.objects.filter(status='approved').count(),
        'apartment': Apartment.objects.filter(status='approved').count(),
        'Office': Office.objects.filter(status='approved').count(),
        'shop': Shop.objects.filter(status='approved').count(),
        'cafe': Cafe.objects.filter(status='approved').count(),
        'wholebuilding': Wholebuilding.objects.filter(status='approved').count(),
    }

    # Fetch filter parameters from request
    advertisement=Advertisement.objects.all()
    selected_region_code = request.GET.get('region')
    selected_city = request.GET.get('city')
    selected_category = request.GET.get('category')
    selected_listing_type = request.GET.get('listing_type')
    name_query = request.GET.get('name', '')

    # Convert region code to full name
    selected_region = region_mapping.get(selected_region_code, selected_region_code) if selected_region_code else None

    # Define models for each category
    categories = {
        'apartments': {'model': Apartment, 'filters': ['rent', 'sell']},
        'villas': {'model': Villa, 'filters': ['rent', 'sell']},
        'shops': {'model': Shop, 'filters': ['rent', 'sell']},
        'lands': {'model': Land, 'filters': ['sell','rent']},
        'cafes': {'model': Cafe, 'filters': ['sell','rent']},
        'offices': {'model': Office, 'filters': ['rent']},
        'wholebuilding': {'model': Wholebuilding, 'filters': ['rent']}
    }

    # Gather all ads with applied filters
    all_ads = []

    for category_name, details in categories.items():
        model = details['model']

        for listing_type in details['filters']:
            query = model.objects.filter(status='approved', listing_type=listing_type)

            # Apply region and city filters
            if selected_region_code:
                query = query.filter(regions__icontains=selected_region_code)
            if selected_city and selected_city != "All Cities":
                query = query.filter(cities__icontains=selected_city)

            # Apply name search
            if name_query:
                query = query.filter(
                    Q(property_title__icontains=name_query) | 
                    Q(regions__icontains=name_query) | 
                    Q(cities__icontains=name_query) |
                    Q(listing_type__icontains=name_query)
                )

            # Debugging: Print the query to check if it's working as expected
            print(query.query)

            # Limit results to 5 per category and listing type
            items = query.order_by('-id')[:5]

            for item in items:
                images = [{"image": img.image.url} for img in item.images.all()]
                main_image_url = images[0]["image"] if images else "/static/assets/images/resource/default.jpg"
                images_json = mark_safe(json.dumps(images)) if images else "[]"

                all_ads.append({
                    'category': category_name.capitalize(),
                    'listing_type': listing_type.capitalize(),
                    'data': item,
                    'main_image_url': main_image_url,
                    'images_json': images_json,
                    'product_type': category_name.lower(),
                    'region_name': region_mapping.get(item.regions, item.regions),
                })

    # OCR & Coordinate Extraction Section
    extracted_text = ""
    table_data = []
    converted_coords = []

    if request.method == 'POST' and 'image' in request.FILES:
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.save()
            image_path = uploaded_image.image.path

            # Preprocess image for OCR
            image = PILImage.open(image_path).convert('L').filter(ImageFilter.MedianFilter(size=3))
            image = image.point(lambda x: 0 if x < 128 else 255, '1')

            # Extract text with OCR
            extracted_text = pytesseract.image_to_string(image)

            # Parse Easting & Northing from extracted text
            lines = extracted_text.split("\n")
            for line in lines:
                numbers = re.findall(r"\d+\.\d+|\d+", line)
                if len(numbers) >= 2:
                    table_data.append((numbers[0], numbers[1]))

            # Convert UTM to Lat/Lon
            utm_proj = Proj(proj="utm", zone=40, ellps="WGS84", south=False)
            wgs_proj = Proj(proj="latlong", datum="WGS84")
            transformer = Transformer.from_proj(utm_proj, wgs_proj)

            for easting, northing in table_data:
                try:
                    lon, lat = transformer.transform(float(easting), float(northing))
                    converted_coords.append((lat, lon))
                except Exception as e:
                    print(f"⚠ Coordinate conversion error: {e}")
    else:
        form = ImageUploadForm()

    # Prepare context for rendering
    context = {
        'all_ads': all_ads,
        'category_counts': category_counts,
        'selected_region': selected_region,
        'selected_city': selected_city,
        'selected_category': selected_category,
        'selected_listing_type': selected_listing_type,
        'name_query': name_query,  'advertisement':advertisement,
        'property_locations': json.dumps([{
            'title': ad['data'].property_title,
            'lat': ad['data'].latitude,
            'lng': ad['data'].longitude,
            'category': ad['product_type'].capitalize(),
            'url': reverse('browseads1', kwargs={'category': ad['product_type'].capitalize(), 'id': ad['data'].id})
        } for ad in all_ads if ad['data'].latitude and ad['data'].longitude]),
        # OCR-related context
        'form': form,
        'extracted_text': extracted_text,
        'table_data': table_data,
        'converted_coords': converted_coords,
    }

    return render(request, 'index-3.html', context)

def villa(request):
    region_mapping = {
        'MS': 'Muscat', 'DH': 'Dhofar', 'BT': 'Batinah', 'DA': 'Dakhiliyah',
        'SH': 'Sharqiyah', 'BR': 'Buraimi', 'ZU': 'Zufar', 'DZ': 'Masandam', 'WR': 'Wusta',
    }

    # Fetch query parameters
    selected_region_code = request.GET.get('region', None)
    advertisement=Advertisement.objects.all()

    selected_listing_type = request.GET.get('listing_type', None)
    selected_city = request.GET.getlist('city')
    name_query = request.GET.get('name', '')
    price_from = request.GET.get('price_from')
    price_to = request.GET.get('price_to')
    selected_property_type = request.GET.get('property_type', None)
    bedrooms = request.GET.get('bedrooms')
    bathrooms = request.GET.get('bathrooms')
    furnished = request.GET.get('furnished')
    rental_period = request.GET.get('rental_period')
    lister_type = request.GET.get('lister_type')
    property_mortgage = request.GET.get('property_mortgage')
    facade = request.GET.get('facade')  
    floors = request.GET.get('floors')
    building = request.GET.get('building')
    main_amenity = request.GET.get('main_amenity')
    additional_amenity = request.GET.get('additional_amenity')
    nearby = request.GET.get('nearby')

    # Additional Filters
    surface_area_from = request.GET.get('surface_area_from')
    surface_area_to = request.GET.get('surface_area_to')
    land_area_from = request.GET.get('land_area_from')
    land_area_to = request.GET.get('land_area_to')

    # Start with all approved villas
    villas = Villa.objects.filter(status='approved')

    # Apply Filters
    if selected_region_code and selected_region_code != "all":
        villas = villas.filter(regions=selected_region_code)
   
    if selected_city:
        # Create a Q object to filter for any of the selected cities
        city_filter = Q()
        for city in selected_city:
            city_filter |= Q(cities__icontains=city)
        villas = villas.filter(city_filter)
    if selected_listing_type and selected_listing_type != "all":
        villas = villas.filter(listing_type=selected_listing_type)
    if selected_property_type and selected_property_type != "all":
        villas = villas.filter(property_type=selected_property_type)
    if name_query:
        villas = villas.filter(
            Q(property_title__icontains=name_query) |
            Q(regions__icontains=name_query) |
            Q(cities__icontains=name_query) |
            Q(listing_type__icontains=name_query) |
            Q(property_type__icontains=name_query)
        )
    if price_from:
        villas = villas.filter(price__gte=price_from)
    if price_to:
        villas = villas.filter(price__lte=price_to)
    if bedrooms:
        bedroom_list = bedrooms.split(',')
        villas = villas.filter(bedrooms__in=bedroom_list)
    if bathrooms:
        bathroom_list = bathrooms.split(',')
        villas = villas.filter(bathrooms__in=bathroom_list)
    if furnished and furnished != "all":
        villas = villas.filter(furnished=furnished)
    if floors:
        floor_list = floors.split(',')
        villas = villas.filter(floors__in=floor_list)
    if building:
        building_list = building.split(',')
        villas = villas.filter(building__in=building_list)
    if rental_period and rental_period != "all":
        villas = villas.filter(rental_period=rental_period)
    if lister_type and lister_type != "all":
        villas = villas.filter(lister_type=lister_type)
    if property_mortgage and property_mortgage != "all":
        villas = villas.filter(property_mortgage=property_mortgage)
    if facade:
        facade_list = facade.split(',')
        villas = villas.filter(facade__in=facade_list)

    # Apply surface area filter if provided
    if land_area_from and land_area_to:
       villas = villas.filter(plot_area__gte=land_area_from, plot_area__lte=land_area_to)
    elif land_area_from:
       villas = villas.filter(plot_area__gte=land_area_from)
    elif land_area_to:
       villas = villas.filter(plot_area__lte=land_area_to)
    if surface_area_from and surface_area_to:
       villas = villas.filter(surface_area__gte=surface_area_from, surface_area__lte=surface_area_to)
    elif surface_area_from:
       villas = villas.filter(surface_area__gte=surface_area_from)
    elif surface_area_to:
       villas = villas.filter(surface_area__lte=surface_area_to)
   
    # Main Amenities filter
    if main_amenity:
        main_amenity_list = main_amenity.split(',')
        villas = villas.filter(main_amenities__name__in=main_amenity_list).distinct()
    if additional_amenity:
        additional_amenity_list = additional_amenity.split(',')
        villas = villas.filter(additional_amenities__name__in=additional_amenity_list).distinct()
    if nearby:
        nearby_list = nearby.split(',')
        villas = villas.filter(nearby_location__name__in=nearby_list).distinct()

    # Add images JSON
    for villa in villas:
        villa.images_json = json.dumps([image.image.url for image in villa.images.all()])

    # Pagination
    paginator = Paginator(villas, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Fetch filter options
    regions = [("all", "All")] + list(Villa.REGION_CHOICES)
    listing_types = [("all", "All")] + list(Villa.TRANSACTION_CHOICES)
    furnished_options = [("all", "All")] + list(Villa.FURNISHED_CHOICES)
    building_options = [("all", "All")] + list(Villa.BUILDING_AGE_CHOICES)
    rental_period_options = [("all", "All")] + list(Villa.RENTAL_PERIOD_CHOICES)
    lister_type_options = [("all", "All")] + list(Villa.LISTER_TYPE_CHOICES)
    property_mortgage_options = [("all", "All")] + list(Villa.PROPERTY_MORTGAGE_CHOICES)
    facade_options = [("all", "All")] + list(Villa.FACADE_CHOICES)
    floors_options = [("all", "All")] + list(Villa.FLOOR_CHOICES)

    # Context
    context = {
        'page_obj': page_obj,
        'regions': regions,
        'listing_types': listing_types,
        'furnished_options': furnished_options,
        'rental_period_options': rental_period_options,
        'lister_type_options': lister_type_options,
        'property_mortgage_options': property_mortgage_options,
        'facade_options': facade_options,
        'floors_options': floors_options,
        'selected_region': region_mapping.get(selected_region_code, selected_region_code) if selected_region_code else None,
        'selected_listing_type': selected_listing_type,
        'selected_city': selected_city,
        'selected_property_type': selected_property_type,
        'name_query': name_query,
        'price_from': price_from,
        'price_to': price_to,
        'bedrooms': bedrooms,
        'bathrooms': bathrooms,
        'selected_furnished': furnished,
        'building_options': building_options,
        'selected_building': building,
        'selected_rental_period': rental_period,
        'selected_lister_type': lister_type,
        'selected_property_mortgage': property_mortgage,
        'selected_facade': facade,
        'selected_floors': floors,
        'main_amenity': main_amenity,
        'additional_amenity': additional_amenity,
        'nearby': nearby,
        'advertisement':advertisement,
        'formatted_url_name': request.resolver_match.url_name.replace("_", " ").title(),
    }

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'estate/villa_list_partial.html', {'page_obj': page_obj,'formatted_url_name': request.resolver_match.url_name.replace("_", " ").title()})
    
    return render(request, 'estate/villa.html', context)

def villa_details(request, id):
    villa = get_object_or_404(Villa.objects.prefetch_related('nearby_location', 'main_amenities', 'additional_amenities'), id=id)
    return render(request, 'estate/villa_details.html', {'villa': villa})

from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Q
from .models import Villa, Land, Commercial, Chalet, Farm  # Ensure you import your models
import json
def land(request):
    # Region mapping
    region_mapping = {
        'MS': 'Muscat', 'DH': 'Dhofar', 'BT': 'Batinah', 'DA': 'Dakhiliyah',
        'SH': 'Sharqiyah', 'BR': 'Buraimi', 'ZU': 'Zufar', 'DZ': 'Masandam', 'WR': 'Wusta'
    }

    # Fetch query parameters
    advertisement=Advertisement.objects.all()
    selected_region_code = request.GET.get('region', None)
    selected_listing_type = request.GET.get('listing_type', None)
    selected_city = request.GET.getlist('city')
    name_query = request.GET.get('name', '')
    price_from = request.GET.get('price_from')
    price_to = request.GET.get('price_to')
    selected_property_type = request.GET.get('property_type')
    filters = request.GET.get('filters', '')
   # Additional Filters
    land_area_from = request.GET.get('land_area_from')
    land_area_to = request.GET.get('land_area_to')
    rental_period = request.GET.get('rental_period')
    lister_type = request.GET.get('lister_type')
    selected_property_mortgage = request.GET.get('property_mortgage', None)
    facade = request.GET.get('facade')  
    zoned_for = request.GET.get('zoned_for')
    nearby = request.GET.get('nearby')
    
    # Fetch approved lands
    lands = Land.objects.filter(status='approved')
    
    # Convert region code to full name
    selected_region = region_mapping.get(selected_region_code, selected_region_code) if selected_region_code else None

    if selected_city:
        # Create a Q object to filter for any of the selected cities
        city_filter = Q()
        for city in selected_city:
            city_filter |= Q(cities__icontains=city)
        lands = lands.filter(city_filter)
    if selected_listing_type and selected_listing_type != "all":
        lands = lands.filter(listing_type=selected_listing_type)
    if selected_property_type and selected_property_type != "all":
        lands = lands.filter(property_type=selected_property_type)
    if name_query:
        lands = lands.filter(
            Q(property_title__icontains=name_query) |
            Q(regions__icontains=name_query) |
            Q(cities__icontains=name_query)
        )
    if price_from:
        lands = lands.filter(price__gte=price_from)
    if price_to:
        lands = lands.filter(price__lte=price_to)
    if filters:
        lands = lands.filter(property_title__icontains=filters)
    if rental_period and rental_period != "all":
        lands = lands.filter(rental_period=rental_period)
    if lister_type and lister_type != "all":
        lands = lands.filter(lister_type=lister_type)
    if selected_property_mortgage and selected_property_mortgage != "all":
        mortgage_values = selected_property_mortgage.split(',')
        lands = lands.filter(property_mortgage__in=mortgage_values)
    if facade:
        facade_list = facade.split(',')
        lands = lands.filter(facade__in=facade_list)
    if zoned_for:
        zoned_for_list = zoned_for.split(',')
        lands = lands.filter(zoned_for__in=zoned_for_list)

    if nearby:
        nearby_list = nearby.split(',')
        lands = lands.filter(nearby_location__name__in=nearby_list).distinct()

    if land_area_from and land_area_to:
        lands = lands.filter(plot_area__range=(land_area_from, land_area_to))
    elif land_area_from:
        lands = lands.filter(plot_area__gte=land_area_from)
    elif land_area_to:
        lands = lands.filter(plot_area__lte=land_area_to)
    
    # Add images JSON to each land
    for land in lands:
        land.images_json = json.dumps([img.image.url for img in land.images.all()])

    # Pagination
    paginator = Paginator(lands, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Fetch category counts
    category_counts = {
        'villa': Villa.objects.filter(status='approved').count(),
        'land': Land.objects.filter(status='approved').count(),
        'commercial': Commercial.objects.filter(status='approved').count(),
        'chalet': Chalet.objects.filter(status='approved').count(),
        'farm': Farm.objects.filter(status='approved').count(),
    }

    # OCR & Coordinate Extraction
    extracted_text, table_data, converted_coords = "", [], []
    if request.method == 'POST' and 'image' in request.FILES:
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.save()
            image_path = uploaded_image.image.path
            image = PILImage.open(image_path).convert('L').filter(ImageFilter.MedianFilter(size=3))
            extracted_text = pytesseract.image_to_string(image)
            
            for line in extracted_text.split("\n"):
                numbers = re.findall(r"\d+\.\d+|\d+", line)
                if len(numbers) >= 2:
                    table_data.append((numbers[0], numbers[1]))
            
            utm_proj = Proj(proj="utm", zone=40, ellps="WGS84", south=False)
            wgs_proj = Proj(proj="latlong", datum="WGS84")
            transformer = Transformer.from_proj(utm_proj, wgs_proj)

            for easting, northing in table_data:
                try:
                    lon, lat = transformer.transform(float(easting), float(northing))
                    converted_coords.append((lat, lon))
                except Exception as e:
                    print(f"⚠ Coordinate conversion error: {e}")
    else:
        form = ImageUploadForm()

    # Prepare context
    context = {
        'page_obj': page_obj,
        'category_counts': category_counts,
        'regions': [("all", "All")] + list(Land.REGION_CHOICES),
        'listing_types': [("all", "All")] + list(Land.LISTING_TYPE_CHOICES),
        'rental_periods': [("all", "All")] + list(Land.RENTAL_PERIOD_CHOICES),
        'lister_types': [("all", "All")] + list(Land.LISTER_TYPE_CHOICES),
        'property_mortgages': [("all", "All")] + list(Land.PROPERTY_MORTGAGE_CHOICES),
        'facades': [("all", "All")] + list(Land.FACADE_CHOICES),
        'zoned_fors': [("all", "All")] + list(Land.ZONED_FOR_CHOICES),
        'selected_region': selected_region,
        'selected_city': selected_city,'advertisement':advertisement,
        'selected_property_mortgage': selected_property_mortgage,
        'formatted_url_name': request.resolver_match.url_name.replace("_", " ").title(),
        'property_locations': json.dumps([
            {
                'title': land.property_title,
                'lat': land.latitude,
                'lng': land.longitude,
                'category': 'Land',
                'url': reverse('browseads1', kwargs={'category': 'Land', 'id': land.id})
            } for land in lands if land.latitude and land.longitude
        ]),
        'form': form,
        'extracted_text': extracted_text,
        'table_data': table_data,
        'converted_coords': converted_coords,
    }
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # AJAX request - return only the product HTML
        return render(request, 'estate/land_list_partial.html', {
            'page_obj': page_obj,
            'formatted_url_name': request.resolver_match.url_name.replace("_", " ").title()
        })
    return render(request, 'estate/land.html', context)
def land_details(request, id):
    land = get_object_or_404(Land.objects.prefetch_related('nearby_location'), id=id)
    return render(request, 'estate/land_details.html', {'land': land})

from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Q
from .models import Villa, Land, Commercial, Chalet, Farm, NearbyLocation, MainAmenities, AdditionalAmenities
import json

def commercial(request):
    region_mapping = {
        'MS': 'Muscat', 'DH': 'Dhofar', 'BT': 'Batinah', 'DA': 'Dakhiliyah',
        'SH': 'Sharqiyah', 'BR': 'Buraimi', 'ZU': 'Zufar', 'DZ': 'Masandam', 'WR': 'Wusta',
    }

    # Fetch query parameters
    advertisement=Advertisement.objects.all()
    selected_region_code = request.GET.get('region', None)
    selected_listing_type = request.GET.get('listing_type', None)
    selected_city = request.GET.getlist('city')
    name_query = request.GET.get('name', '')
    price_from = request.GET.get('price_from')
    price_to = request.GET.get('price_to')
    selected_property_type = request.GET.get('property_type', None)
    bedrooms = request.GET.get('bedrooms')
    bathrooms = request.GET.get('bathrooms')
    furnished = request.GET.get('furnished')
    rental_period = request.GET.get('rental_period')
    lister_type = request.GET.get('lister_type')
    property_mortgage = request.GET.get('property_mortgage')
    facade = request.GET.get('facade')  
    floors = request.GET.get('floors')
    building = request.GET.get('building')
    main_amenity = request.GET.get('main_amenity')
    additional_amenity = request.GET.get('additional_amenity')
    nearby = request.GET.get('nearby')

    # Additional Filters
    surface_area_from = request.GET.get('surface_area_from')
    surface_area_to = request.GET.get('surface_area_to')
    
    # Start with all approved staff
    staff = Commercial.objects.filter(status='approved')

    # Apply Filters
    if selected_region_code and selected_region_code != "all":
        staff = staff.filter(regions=selected_region_code)
   
    if selected_city:
        # Create a Q object to filter for any of the selected cities
        city_filter = Q()
        for city in selected_city:
            city_filter |= Q(cities__icontains=city)
        staff = staff.filter(city_filter)
    if selected_listing_type and selected_listing_type != "all":
        staff = staff.filter(listing_type=selected_listing_type)
    if selected_property_type and selected_property_type != "all":
        staff = staff.filter(property_type=selected_property_type)
    if name_query:
        staff = staff.filter(
            Q(property_title__icontains=name_query) |
            Q(regions__icontains=name_query) |
            Q(cities__icontains=name_query) |
            Q(listing_type__icontains=name_query) |
            Q(property_type__icontains=name_query)
        )
    if price_from:
        staff = staff.filter(price__gte=price_from)
    if price_to:
        staff = staff.filter(price__lte=price_to)
    if bedrooms:
        bedroom_list = bedrooms.split(',')
        staff = staff.filter(bedrooms__in=bedroom_list)
    if bathrooms:
        bathroom_list = bathrooms.split(',')
        staff = staff.filter(bathrooms__in=bathroom_list)
    if furnished and furnished != "all":
        staff = staff.filter(furnished=furnished)
    if floors:
        floor_list = floors.split(',')
        staff = staff.filter(floors__in=floor_list)
    if building:
        building_list = building.split(',')
        staff = staff.filter(building__in=building_list)
    if rental_period and rental_period != "all":
        staff = staff.filter(rental_period=rental_period)
    if lister_type and lister_type != "all":
        staff = staff.filter(lister_type=lister_type)
    if property_mortgage and property_mortgage != "all":
        staff = staff.filter(property_mortgage=property_mortgage)
    if facade:
        facade_list = facade.split(',')
        staff = staff.filter(facade__in=facade_list)

    # Apply surface area filter if provided
    if surface_area_from and surface_area_to:
       staff = staff.filter(plot_area__gte=surface_area_from, plot_area__lte=surface_area_to)
    elif surface_area_from:
       staff = staff.filter(plot_area__gte=surface_area_from)
    elif surface_area_to:
       staff = staff.filter(plot_area__lte=surface_area_to)
   
    # Main Amenities filter
    if main_amenity:
        main_amenity_list = main_amenity.split(',')
        staff = staff.filter(main_amenities__name__in=main_amenity_list).distinct()
    if additional_amenity:
        additional_amenity_list = additional_amenity.split(',')
        staff = staff.filter(additional_amenities__name__in=additional_amenity_list).distinct()
    if nearby:
        nearby_list = nearby.split(',')
        staff = staff.filter(nearby_location__name__in=nearby_list).distinct()

    # Add images JSON
    for villa in staff:
        villa.images_json = json.dumps([image.image.url for image in villa.images.all()])

    # Pagination
    paginator = Paginator(staff, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Fetch filter options
    regions = [("all", "All")] + list(Commercial.REGION_CHOICES)
    listing_types = [("all", "All")] + list(Commercial.TRANSACTION_CHOICES)
    furnished_options = [("all", "All")] + list(Commercial.FURNISHED_CHOICES)
    rental_period_options = [("all", "All")] + list(Commercial.RENTAL_PERIOD_CHOICES)
    lister_type_options = [("all", "All")] + list(Commercial.LISTER_TYPE_CHOICES)
    property_mortgage_options = [("all", "All")] + list(Commercial.PROPERTY_MORTGAGE_CHOICES)
    floors_options = [("all", "All")] + list(Commercial.FLOOR_CHOICES)

    # Context
    context = {
        'page_obj': page_obj,
        'regions': regions,
        'listing_types': listing_types,
        'furnished_options': furnished_options,
        'rental_period_options': rental_period_options,
        'lister_type_options': lister_type_options,
        'property_mortgage_options': property_mortgage_options,
        'floors_options': floors_options,
        'selected_region': region_mapping.get(selected_region_code, selected_region_code) if selected_region_code else None,
        'selected_listing_type': selected_listing_type,
        'selected_city': selected_city,
        'selected_property_type': selected_property_type,
        'name_query': name_query,
        'price_from': price_from,
        'price_to': price_to,
        'bedrooms': bedrooms,
        'bathrooms': bathrooms,
        'selected_furnished': furnished,
        'selected_building': building,
        'selected_rental_period': rental_period,
        'selected_lister_type': lister_type,
        'selected_property_mortgage': property_mortgage,
        'selected_facade': facade,
        'selected_floors': floors,
        'main_amenity': main_amenity,
        'advertisement':advertisement,
        'additional_amenity': additional_amenity,
        'nearby': nearby,
        'formatted_url_name': request.resolver_match.url_name.replace("_", " ").title(),
    }

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'estate/commercial-list-partial.html', {'page_obj': page_obj,'formatted_url_name': request.resolver_match.url_name.replace("_", " ").title()})
    
    return render(request, 'estate/commercials.html', context)

def commercial_details(request, id):
    commercial = get_object_or_404(Commercial.objects.prefetch_related('nearby_location', 'main_amenities', 'additional_amenities'), id=id)
    return render(request, 'estate/commercial_details.html', {'commercial': commercial})

from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Q
from .models import Villa, Land, Commercial, Chalet, Farm, MainAmenities, AdditionalAmenities, NearbyLocation
import json
def farm(request):
    region_mapping = {
        'MS': 'Muscat', 'DH': 'Dhofar', 'BT': 'Batinah', 'DA': 'Dakhiliyah',
        'SH': 'Sharqiyah', 'BR': 'Buraimi', 'ZU': 'Zufar', 'DZ': 'Masandam', 'WR': 'Wusta',
    }

    # Fetch query parameters
    advertisement=Advertisement.objects.all()
    selected_region_code = request.GET.get('region', None)
    selected_listing_type = request.GET.get('listing_type', None)
    selected_city = request.GET.getlist('city')
    name_query = request.GET.get('name', '')
    price_from = request.GET.get('price_from')
    price_to = request.GET.get('price_to')
    selected_property_type = request.GET.get('property_type', None)
    bedrooms = request.GET.get('bedrooms')
    bathrooms = request.GET.get('bathrooms')
    furnished = request.GET.get('furnished')
    rental_period = request.GET.get('rental_period')
    lister_type = request.GET.get('lister_type')
    property_mortgage = request.GET.get('property_mortgage')
    facade = request.GET.get('facade')  
    building = request.GET.get('building')
    main_amenity = request.GET.get('main_amenity')
    additional_amenity = request.GET.get('additional_amenity')
    nearby = request.GET.get('nearby')

    # Additional Filters
    surface_area_from = request.GET.get('surface_area_from')
    surface_area_to = request.GET.get('surface_area_to')
    land_area_from = request.GET.get('land_area_from')
    land_area_to = request.GET.get('land_area_to')

    # Start with all approved farms
    farms = Farm.objects.filter(status='approved')

    # Apply Filters
    if selected_region_code and selected_region_code != "all":
        farms = farms.filter(regions=selected_region_code)
   
    if selected_city:
        # Create a Q object to filter for any of the selected cities
        city_filter = Q()
        for city in selected_city:
            city_filter |= Q(cities__icontains=city)
        farms = farms.filter(city_filter)
    if selected_listing_type and selected_listing_type != "all":
        farms = farms.filter(listing_type=selected_listing_type)
    if selected_property_type and selected_property_type != "all":
        farms = farms.filter(property_type=selected_property_type)
    if name_query:
        farms = farms.filter(
            Q(property_title__icontains=name_query) |
            Q(regions__icontains=name_query) |
            Q(cities__icontains=name_query) |
            Q(listing_type__icontains=name_query) |
            Q(property_type__icontains=name_query)
        )
    if price_from:
        farms = farms.filter(price__gte=price_from)
    if price_to:
        farms = farms.filter(price__lte=price_to)
    if bedrooms:
        bedroom_list = bedrooms.split(',')
        farms = farms.filter(bedrooms__in=bedroom_list)
    if bathrooms:
        bathroom_list = bathrooms.split(',')
        farms = farms.filter(bathrooms__in=bathroom_list)
    if furnished and furnished != "all":
        farms = farms.filter(furnished=furnished)

    if building:
        building_list = building.split(',')
        farms = farms.filter(building__in=building_list)
    if rental_period and rental_period != "all":
        farms = farms.filter(rental_period=rental_period)
    if lister_type and lister_type != "all":
        farms = farms.filter(lister_type=lister_type)
    if property_mortgage and property_mortgage != "all":
        farms = farms.filter(property_mortgage=property_mortgage)
    if facade:
        facade_list = facade.split(',')
        farms = farms.filter(facade__in=facade_list)

    # Apply surface area filter if provided
    if land_area_from and land_area_to:
       farms = farms.filter(plot_area__gte=land_area_from, plot_area__lte=land_area_to)
    elif land_area_from:
       farms = farms.filter(plot_area__gte=land_area_from)
    elif land_area_to:
       farms = farms.filter(plot_area__lte=land_area_to)
    if surface_area_from and surface_area_to:
       farms = farms.filter(surface_area__gte=surface_area_from, surface_area__lte=surface_area_to)
    elif surface_area_from:
       farms = farms.filter(surface_area__gte=surface_area_from)
    elif surface_area_to:
       farms = farms.filter(surface_area__lte=surface_area_to)
   
    # Main Amenities filter
    if main_amenity:
        main_amenity_list = main_amenity.split(',')
        farms = farms.filter(main_amenities__name__in=main_amenity_list).distinct()
    if additional_amenity:
        additional_amenity_list = additional_amenity.split(',')
        farms = farms.filter(additional_amenities__name__in=additional_amenity_list).distinct()
    if nearby:
        nearby_list = nearby.split(',')
        farms = farms.filter(nearby_location__name__in=nearby_list).distinct()

    # Add images JSON
    for farm in farms:
        farm.images_json = json.dumps([image.image.url for image in farm.images.all()])

    # Pagination
    paginator = Paginator(farms, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Fetch filter options
    regions = [("all", "All")] + list(Villa.REGION_CHOICES)
    listing_types = [("all", "All")] + list(Villa.TRANSACTION_CHOICES)
    furnished_options = [("all", "All")] + list(Villa.FURNISHED_CHOICES)
    building_options = [("all", "All")] + list(Villa.BUILDING_AGE_CHOICES)
    rental_period_options = [("all", "All")] + list(Villa.RENTAL_PERIOD_CHOICES)
    lister_type_options = [("all", "All")] + list(Villa.LISTER_TYPE_CHOICES)
    property_mortgage_options = [("all", "All")] + list(Villa.PROPERTY_MORTGAGE_CHOICES)
    facade_options = [("all", "All")] + list(Villa.FACADE_CHOICES)
   
    # Context
    context = {
        'page_obj': page_obj,
        'regions': regions,
        'listing_types': listing_types,
        'furnished_options': furnished_options,
        'building_options': building_options,
        'rental_period_options': rental_period_options,
        'lister_type_options': lister_type_options,
        'property_mortgage_options': property_mortgage_options,
        'facade_options': facade_options,
        'selected_region': region_mapping.get(selected_region_code, selected_region_code) if selected_region_code else None,
        'selected_listing_type': selected_listing_type,
        'selected_city': selected_city,
        'selected_property_type': selected_property_type,
        'name_query': name_query,
        'price_from': price_from,
        'price_to': price_to,
        'bedrooms': bedrooms,
        'bathrooms': bathrooms,
        'selected_furnished': furnished,
        'selected_building': building,
        'selected_rental_period': rental_period,
        'selected_lister_type': lister_type,'advertisement':advertisement,
        'selected_property_mortgage': property_mortgage,
        'selected_facade': facade,
        'main_amenity': main_amenity,
        'additional_amenity': additional_amenity,
        'nearby': nearby,
        'formatted_url_name': request.resolver_match.url_name.replace("_", " ").title(),
    }

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'estate/farm-list-partial.html', {'page_obj': page_obj,'formatted_url_name': request.resolver_match.url_name.replace("_", " ").title()})
    
    return render(request, 'estate/farm.html', context)

def farm_details(request, id):
    farm = get_object_or_404(Farm.objects.prefetch_related('nearby_location', 'main_amenities', 'additional_amenities'), id=id)
    return render(request, 'estate/farm_details.html', {'farm': farm})

from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Q
from .models import Chalet, Villa, Land, Commercial, Farm  # Ensure you import your models
import json

def chalet(request):
    # Define a mapping of region codes to full names
    region_mapping = {
        'MS': 'Muscat',
        'DH': 'Dhofar',
        'BT': 'Batinah',
        'DA': 'Dakhiliyah',
        'SH': 'Sharqiyah',
        'BR': 'Buraimi',
        'ZU': 'Zufar',
        'DZ': 'Masandam',
        'WR': 'Wusta',
    }

    # Fetch query parameters
    selected_region_code = request.GET.get('region', None)  # If no region is selected, use None
    selected_listing_type = request.GET.get('listing_type', None)  # If no listing type is selected, use None
    selected_city = request.GET.get('city')  # Get selected city
    name_query = request.GET.get('name', '')  # Search query
    price_from = request.GET.get('price_from')  # Price range: from
    price_to = request.GET.get('price_to')      # Price range: to
    selected_amenities = request.GET.get('amenities', None)  # Amenities filter
    filters = request.GET.get('filters', '')  # Additional filters
    bedrooms = request.GET.get('bedrooms')  # Bedrooms filter
    bathrooms = request.GET.get('bathrooms')  # Bathrooms filter
    tenancy_information = request.GET.get('tenancy_information')  # Tenancy information filter

    # Start with all approved chalets
    chalet_queryset = Chalet.objects.filter(status='approved')

    # Apply region filter if selected
    if selected_region_code and selected_region_code != "all":
        chalet_queryset = chalet_queryset.filter(regions=selected_region_code)

    # Apply listing type filter if selected
    if selected_listing_type and selected_listing_type != "all":
        chalet_queryset = chalet_queryset.filter(listing_type=selected_listing_type)

    # Filter by city if selected and not "All Cities"
    if selected_city and selected_city != "All Cities":
        chalet_queryset = chalet_queryset.filter(cities__icontains=selected_city)

    # Apply amenities filter if selected
    if selected_amenities and selected_amenities != "all":
        chalet_queryset = chalet_queryset.filter(amenities__icontains=selected_amenities)

    # Apply search query filter
    if name_query:
        chalet_queryset = chalet_queryset.filter(
            Q(property_title__icontains=name_query) |
            Q(regions__icontains=name_query) |
            Q(cities__icontains=name_query) |
            Q(listing_type__icontains=name_query) 
        )

    # Price Range Filtering
    if price_from and price_to:
        chalet_queryset = chalet_queryset.filter(price__gte=price_from, price__lte=price_to)
    elif price_from:
        chalet_queryset = chalet_queryset.filter(price__gte=price_from)
    elif price_to:
        chalet_queryset = chalet_queryset.filter(price__lte=price_to)

    # Bedrooms Filtering
    if bedrooms:
        chalet_queryset = chalet_queryset.filter(bedrooms=bedrooms)

    # Bathrooms Filtering
    if bathrooms:
        chalet_queryset = chalet_queryset.filter(bathrooms=bathrooms)

    # Tenancy Information Filtering
    if tenancy_information and tenancy_information != "all":
        chalet_queryset = chalet_queryset.filter(tenancy_information=tenancy_information)

    # Additional filters
    if filters:
        chalet_queryset = chalet_queryset.filter(property_title__icontains=filters)

    # Process images for each chalet
    for chalet in chalet_queryset:
        chalet.images_json = json.dumps([image.image.url for image in chalet.images.all()])

    # Calculate category counts
    category_counts = {
        'villa': Villa.objects.filter(status='approved').count(),
        'land': Land.objects.filter(status='approved').count(),
        'commercial': Commercial.objects.filter(status='approved').count(),
        'chalet': Chalet.objects.filter(status='approved').count(),
        'farm': Farm.objects.filter(status='approved').count(),
    }

    # Set up pagination
    paginator = Paginator(chalet_queryset, 6)  # Show 6 chalets per page
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)  

    # Get the available regions and property types for the filter dropdowns
    regions = [("all", "All")] + list(Chalet.REGION_CHOICES)  # Assuming REGION_CHOICES is a class variable in the Chalet model
    listing_types = [("all", "All")] + list(Chalet.TRANSACTION_CHOICES)  # Assuming TRANSACTION_CHOICES is a class variable in the Chalet model
    tenancy_options = [("all", "All")] + list(Chalet.tenancy_information.field.choices)  # Tenancy information choices

    # Render the template with the context
    return render(request, 'estate/chalet.html', {
        'page_obj': page_obj,
        'regions': regions,
        'listing_types': listing_types,
        'tenancy_options': tenancy_options,
        'selected_region': region_mapping.get(selected_region_code, selected_region_code) if selected_region_code else None,  # Pass the full region name
        'selected_listing_type': selected_listing_type,  # Pass the selected listing type to the template
        'selected_amenities': selected_amenities,  # Pass the selected property type to the template
        'selected_city':selected_city,
        'category_counts': category_counts,
        'name_query': name_query,
        'price_from': price_from,
        'price_to': price_to,
        'filters': filters,
        'bedrooms': bedrooms,
        'bathrooms': bathrooms,
        'tenancy_information': tenancy_information,
    })

def chalet_details(request, id):
    chalet = get_object_or_404(Chalet, id=id)
    return render(request, 'estate/chalet_details.html', {'chalet': chalet})


import random
import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model

def is_valid_email(email):
    api_key = "5638ffa2eb8b40869e15ca6edd10b116"  # Replace with your Abstract API Key
    url = f"https://emailvalidation.abstractapi.com/v1/?api_key={api_key}&email={email}"

    response = requests.get(url)
    data = response.json()

    # Check if email is valid & exists
    if data.get("is_valid_format", {}).get("value") and data.get("deliverability") == "DELIVERABLE":
        return True
    return False

from django.contrib.auth import get_user_model
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import random

def signup_view1(request):
    CustomUser = get_user_model()
    
    if request.method == "POST":
        if "verify_otp" in request.POST:  # OTP Verification Step
            entered_otp = request.POST.get("otp")
            session_otp = request.session.get("otp")
            email = request.session.get("email")

            if not session_otp or not email:
                messages.error(request, "Session expired. Please try again.")
                return redirect("signup")

            if entered_otp == str(session_otp):
                request.session["otp_verified"] = True
                messages.success(request, "OTP Verified! Please complete your registration.")
                return render(request, "signup.html", {"show_password_form": True, "email": email})
            else:
                messages.error(request, "Invalid OTP. Try again.")
                return render(request, "signup.html", {"show_otp": True, "email": email})

        elif "final_register" in request.POST:  # Final Registration Step
            if not request.session.get("otp_verified"):
                messages.error(request, "Unauthorized action. Please verify OTP first.")
                return redirect("signup")

            username = request.POST.get("username")
            email = request.POST.get("email")
            password1 = request.POST.get("password1")
            password2 = request.POST.get("password2")

            if password1 != password2:
                messages.error(request, "Passwords do not match.")
                return render(request, "signup.html", {"show_password_form": True, "email": email})

            if CustomUser.objects.filter(username=username).exists():
                messages.error(request, "Username already exists.")
                return render(request, "signup.html", {"show_password_form": True, "email": email})

            user = CustomUser.objects.create_user(username=username, email=email, password=password1)
            user.save()

            request.session.flush()  # Clear session data after successful signup
            messages.success(request, "Registration successful! You can now log in.")
            return redirect("login")

        else:  # Initial Email Submission
            email = request.POST.get("email")

            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, "Email is already registered.")
                return redirect("signup")

            # Verify email before sending OTP
            if not is_valid_email(email):
                messages.error(request, "Invalid email address. Please enter a valid email.")
                return redirect("signup")

            otp = random.randint(100000, 999999)  # Generate OTP
            request.session["otp"] = otp
            request.session["email"] = email

            # Send OTP Email
            send_mail(
                "Your OTP Code",
                f"Your OTP code is {otp}. Do not share it with anyone.",
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )

            messages.success(request, "OTP sent to your email. Please verify.")
            return render(request, "signup.html", {"show_otp": True, "email": email})

    return render(request, "signup.html")







def custom_logout_view(request):
    logout(request)
    request.session.flush()  # Clears session data
    return redirect('login1')

    
from django.db.models import Q
from django.core.paginator import Paginator
import json
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render
import json
from .models import Fashion, Toys, Food, Fitness, Pet, Book, Appliance  # Ensure you import your models

def fashion(request):
    # Define a mapping of region codes to full names
    region_mapping = {
        'MS': 'Muscat',
        'DH': 'Dhofar',
        'BT': 'Batinah',
        'DA': 'Dakhiliyah',
        'SH': 'Sharqiyah',
        'BR': 'Buraimi',
        'ZU': 'Zufar',
        'DZ': 'Masandam',
        'WR': 'Wusta',
    }

    fashion_queryset = Fashion.objects.filter(status='approved')

    # Retrieve query parameters
    selected_region_code = request.GET.get('region')  # Get selected region code
    selected_city = request.GET.get('city')  # Get selected city
    name_query = request.GET.get('name', '')  
    cities = request.GET.get('cities')  
    brand = request.GET.get('brand')  
    category = request.GET.get('category')  
    size = request.GET.getlist('size')  # Use getlist to retrieve multiple values
    gender = request.GET.get('gender')  
    condition = request.GET.get('condition')  
    price_from = request.GET.get('price_from')  
    price_to = request.GET.get('price_to')  
    color = request.GET.get('color')  # New color filter
    filters = request.GET.get('filters')  

    # Apply filters
    if selected_region_code:
        fashion_queryset = fashion_queryset.filter(regions__iexact=selected_region_code)

    if name_query:
        fashion_queryset = fashion_queryset.filter(
            Q(regions__icontains=name_query) |
            Q(cities__icontains=name_query) |
            Q(name__icontains=name_query) |
            Q(brand__icontains=name_query) |
            Q(category__icontains=name_query)
        )

    if cities:
        fashion_queryset = fashion_queryset.filter(cities__icontains=cities)

         # Filter by city if selected and not "All Cities"
    if selected_city and selected_city != "All Cities":
        fashion_queryset = fashion_queryset.filter(cities__icontains=selected_city)

    if brand:
        fashion_queryset = fashion_queryset.filter(brand__icontains=brand)

    if category:
        fashion_queryset = fashion_queryset.filter(category__iexact=category)

    if size:
        fashion_queryset = fashion_queryset.filter(size__in=size)  # Use __in for multiple sizes

    if gender:
        fashion_queryset = fashion_queryset.filter(gender__iexact=gender)

    if condition:
        fashion_queryset = fashion_queryset.filter(condition__iexact=condition)

    # Price filtering
    if price_from and price_to:
        fashion_queryset = fashion_queryset.filter(price__gte=float(price_from), price__lte=float(price_to))
    elif price_from:
        fashion_queryset = fashion_queryset.filter(price__gte=float(price_from))
    elif price_to:
        fashion_queryset = fashion_queryset.filter(price__lte=float(price_to))

    if color:
        fashion_queryset = fashion_queryset.filter(color__icontains=color)  # Apply color filter

    if filters:
        fashion_queryset = fashion_queryset.filter(name__icontains=filters)

    # Pagination
    paginator = Paginator(fashion_queryset, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Convert images to JSON format
    for fashion in page_obj:
        fashion.images_json = json.dumps([image.image.url for image in fashion.images.all()])

    # Count items in each category
    category_counts = {
        'fashion': Fashion.objects.filter(status='approved').count(),
        'toys': Toys.objects.filter(status='approved').count(),
        'food': Food.objects.filter(status='approved').count(),
        'fitness': Fitness.objects.filter(status='approved').count(),
        'pet': Pet.objects.filter(status='approved').count(),
        'book': Book.objects.filter(status='approved').count(),
        'appliances': Appliance.objects.filter(status='approved').count(),
    }

    # Prepare context for rendering the template
    context = {
        'fashion': fashion_queryset,
        'page_obj': page_obj,
        'category_counts': category_counts,
        'selected_region': region_mapping.get(selected_region_code, selected_region_code) if selected_region_code else None,  # Pass the full region name
        'name_query': name_query,
        'selected_city':selected_city,
        'cities': cities,
        'brand': brand,
        'category': category,
        'size': size,
        'gender': gender,
        'condition': condition,
        'price_from': price_from,
        'price_to': price_to,
        'color': color,  # Include color in context
        'filters': filters,
    }

    return render(request, 'fashion.html', context)

def fashion_details(request, id):
    fashion = get_object_or_404(Fashion, id=id)
    return render(request, 'fashion_details.html', {'fashion': fashion})



from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render
import json
from .models import Fashion, Toys, Food, Fitness, Pet, Book, Appliance  # Ensure you import your models

def toys(request):
    # Define a mapping of region codes to full names
    region_mapping = {
        'MS': 'Muscat',
        'DH': 'Dhofar',
        'BT': 'Batinah',
        'DA': 'Dakhiliyah',
        'SH': 'Sharqiyah',
        'BR': 'Buraimi',
        'ZU': 'Zufar',
        'DZ': 'Masandam',
        'WR': 'Wusta',
    }

    toy_queryset = Toys.objects.filter(status='approved')

    # Retrieve query parameters
    selected_region_code = request.GET.get('region')  # Get selected region code
    name_query = request.GET.get('name', '')  
    cities = request.GET.get('cities')  
    selected_city = request.GET.get('city')  # Get selected city
    brand = request.GET.get('brand')  
    category = request.GET.get('category')  
    age_group = request.GET.get('age_group')  
    platform = request.GET.getlist('platform')  # Use getlist to retrieve multiple values
    condition = request.GET.get('condition')  
    price_from = request.GET.get('price_from')  
    price_to = request.GET.get('price_to')  
    filters = request.GET.get('filters')  

    # Apply filters
    if selected_region_code:
        toy_queryset = toy_queryset.filter(regions__iexact=selected_region_code)

    if name_query:
        toy_queryset = toy_queryset.filter(
            Q(regions__icontains=name_query) |
            Q(cities__icontains=name_query) |
            Q(product_name__icontains=name_query) |  # Assuming product_name is the field for toy name
            Q(brand__icontains=name_query) |
            Q(category__icontains=name_query)
        )
    
     # Filter by city if selected and not "All Cities"
    if selected_city and selected_city != "All Cities":
        toy_queryset = toy_queryset.filter(cities__icontains=selected_city)

    if cities:
        toy_queryset = toy_queryset.filter(cities__icontains=cities)

    if brand:
        toy_queryset = toy_queryset.filter(brand__icontains=brand)

    if category:
        toy_queryset = toy_queryset.filter(category__iexact=category)

    if age_group:
        toy_queryset = toy_queryset.filter(age_group__iexact=age_group)

    if platform:
        toy_queryset = toy_queryset.filter(platform__in=platform)  # Use __in for multiple platforms

    if condition:
        toy_queryset = toy_queryset.filter(condition__iexact=condition)

    # Price filtering
    if price_from and price_to:
        toy_queryset = toy_queryset.filter(price__gte=float(price_from), price__lte=float(price_to))
    elif price_from:
        toy_queryset = toy_queryset.filter(price__gte=float(price_from))
    elif price_to:
        toy_queryset = toy_queryset.filter(price__lte=float(price_to))

    if filters:
        toy_queryset = toy_queryset.filter(product_name__icontains=filters)  # Assuming product_name is the field for toy name

    # Pagination
    paginator = Paginator(toy_queryset, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Convert images to JSON format for each toy item
    for toy in page_obj:
        toy.images_json = json.dumps([image.image.url for image in toy.images.all()])

    # Count items in each category
    category_counts = {
        'fashion': Fashion.objects.filter(status='approved').count(),
        'toys': Toys.objects.filter(status='approved').count(),
        'food': Food.objects.filter(status='approved').count(),
        'fitness': Fitness.objects.filter(status='approved').count(),
        'pet': Pet.objects.filter(status='approved').count(),
        'book': Book.objects.filter(status='approved').count(),
        'appliances': Appliance.objects.filter(status='approved').count(),
    }

    # Prepare context for rendering the template
    context = {
        'toys': toy_queryset,
        'page_obj': page_obj,
        'category_counts': category_counts,
        'selected_region': region_mapping.get(selected_region_code, selected_region_code) if selected_region_code else None,  # Pass the full region name
        'name_query': name_query,
        'selected_city':selected_city,
        'cities': cities,
        'brand': brand,
        'category': category,
        'age_group': age_group,
        'platform': platform,  # Include platform in context
        'condition': condition,
        'price_from': price_from,
        'price_to': price_to,
        'filters': filters,
    }

    return render(request, 'toys.html', context)

def toy_details(request, id):
    toy = get_object_or_404(Toys, id=id)
    return render(request, 'toy_details.html', {'toy': toy})

from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render
import json
from .models import Fashion, Toys, Food, Fitness, Pet, Book, Appliance  # Ensure you import your models

def foods(request):
    # Define a mapping of region codes to full names
    region_mapping = {
        'MS': 'Muscat',
        'DH': 'Dhofar',
        'BT': 'Batinah',
        'DA': 'Dakhiliyah',
        'SH': 'Sharqiyah',
        'BR': 'Buraimi',
        'ZU': 'Zufar',
        'DZ': 'Masandam',
        'WR': 'Wusta',
    }

    food_queryset = Food.objects.filter(status='approved')

    # Retrieve query parameters
    selected_region_code = request.GET.get('region')  # Get selected region code
    name_query = request.GET.get('name', '')  
    cities = request.GET.get('cities')  
    brand = request.GET.get('brand')  
    selected_city = request.GET.get('city')  # Get selected city
    product_type = request.GET.get('product_type')  
    expiration_date = request.GET.get('expiration_date')  
    dietary_info = request.GET.get('dietary_info')  
    condition = request.GET.get('condition')  
    price_from = request.GET.get('price_from')  
    price_to = request.GET.get('price_to')  

    # Apply filters
    if selected_region_code:
        food_queryset = food_queryset.filter(regions__iexact=selected_region_code)

    if name_query:
        food_queryset = food_queryset.filter(
            Q(regions__icontains=name_query) |
            Q(cities__icontains=name_query) |
            Q(product_name__icontains=name_query) |
            Q(brand__icontains=name_query) |
            Q(product_type__icontains=name_query)
        )

    if cities:
        food_queryset = food_queryset.filter(cities__icontains=cities)

    if brand:
        food_queryset = food_queryset.filter(brand__icontains=brand)
         # Filter by city if selected and not "All Cities"
    if selected_city and selected_city != "All Cities":
        food_queryset = food_queryset.filter(cities__icontains=selected_city)

    if product_type:
        food_queryset = food_queryset.filter(product_type__iexact=product_type)

    if expiration_date:
        food_queryset = food_queryset.filter(expiration_date__gte=expiration_date)  # Filter for expiration date

    if dietary_info:
        food_queryset = food_queryset.filter(dietary_info__icontains=dietary_info)  # Filter for dietary information

    if condition:
        food_queryset = food_queryset.filter(condition__iexact=condition)

    # Price filtering
    if price_from and price_to:
        food_queryset = food_queryset.filter(price__gte=float(price_from), price__lte=float(price_to))
    elif price_from:
        food_queryset = food_queryset.filter(price__gte=float(price_from))
    elif price_to:
        food_queryset = food_queryset.filter(price__lte=float(price_to))

    # Pagination
    paginator = Paginator(food_queryset, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Convert images to JSON format for each food item
    for food in page_obj:
        food.images_json = json.dumps([image.image.url for image in food.images.all()])

    # Count items in each category
    category_counts = {
        'fashion': Fashion.objects.filter(status='approved').count(),
        'toys': Toys.objects.filter(status='approved').count(),
        'food': Food.objects.filter(status='approved').count(),
        'fitness': Fitness.objects.filter(status='approved').count(),
        'pet': Pet.objects.filter(status='approved').count(),
        'book': Book.objects.filter(status='approved').count(),
        'appliances': Appliance.objects.filter(status='approved').count(),
    }

    # Prepare context for rendering the template
    context = {
        'food': food_queryset,
        'page_obj': page_obj,
        'category_counts': category_counts,
        'selected_region': region_mapping.get(selected_region_code, selected_region_code) if selected_region_code else None,  # Pass the full region name
        'name_query': name_query,
        'selected_city':selected_city,
        'cities': cities,
        'brand': brand,
        'product_type': product_type,
        'expiration_date': expiration_date,
        'dietary_info': dietary_info,
        'condition': condition,
        'price_from': price_from,
        'price_to': price_to,
    }

    return render(request, 'foods.html', context)

def food_details(request, id):
    food = get_object_or_404(Food, id=id)
    return render(request, 'food_details.html', {'food': food})


from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Q
from .models import Fashion, Toys, Food, Fitness, Pet, Book, Appliance  # Ensure you import your models
import json

def fitness(request):
    # Define a mapping of region codes to full names
    region_mapping = {
        'MS': 'Muscat',
        'DH': 'Dhofar',
        'BT': 'Batinah',
        'DA': 'Dakhiliyah',
        'SH': 'Sharqiyah',
        'BR': 'Buraimi',
        'ZU': 'Zufar',
        'DZ': 'Masandam',
        'WR': 'Wusta',
    }

    fitness_queryset = Fitness.objects.filter(status='approved')

    # Retrieve query parameters
    selected_region_code = request.GET.get('region')  # Get selected region code
    name_query = request.GET.get('name', '')  
    cities = request.GET.get('cities')  
    selected_city = request.GET.get('city')  # Get selected city
    brand = request.GET.get('brand')  
    category = request.GET.get('category')
    condition = request.GET.get('condition')   
    warranty_status = request.GET.get('warranty_status')  # New filter
    price_from = request.GET.get('price_from')  
    price_to = request.GET.get('price_to')  
    filters = request.GET.get('filters')  

    # Apply filters
    if selected_region_code:
        fitness_queryset = fitness_queryset.filter(regions__iexact=selected_region_code)

    if name_query:
        fitness_queryset = fitness_queryset.filter(
            Q(regions__icontains=name_query) |
            Q(cities__icontains=name_query) |
            Q(product_name__icontains=name_query) |  # Assuming product_name is the field for fitness item name
            Q(brand__icontains=name_query) |
            Q(category__icontains=name_query)
        )

    if cities:
        fitness_queryset = fitness_queryset.filter(cities__icontains=cities)

         # Filter by city if selected and not "All Cities"
    if selected_city and selected_city != "All Cities":
        fitness_queryset = fitness_queryset.filter(cities__icontains=selected_city)

    if brand:
        fitness_queryset = fitness_queryset.filter(brand__icontains=brand)

    if category:
        fitness_queryset = fitness_queryset.filter(category__iexact=category)

    if condition:
        fitness_queryset = fitness_queryset.filter(condition__iexact=condition)

    if warranty_status:
        fitness_queryset = fitness_queryset.filter(warranty_status__iexact=warranty_status)  # Filter for warranty status

    # Price filtering
    if price_from and price_to:
        fitness_queryset = fitness_queryset.filter(price__gte=float(price_from), price__lte=float(price_to))
    elif price_from:
        fitness_queryset = fitness_queryset.filter(price__gte=float(price_from))
    elif price_to:
        fitness_queryset = fitness_queryset.filter(price__lte=float(price_to))

    if filters:
        fitness_queryset = fitness_queryset.filter(product_name__icontains=filters)

    # Pagination
    paginator = Paginator(fitness_queryset, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Convert images to JSON format for each fitness item
    for fitness in page_obj:
        fitness.images_json = json.dumps([image.image.url for image in fitness.images.all()])

    # Count items in each category
    category_counts = {
        'fashion': Fashion.objects.filter(status='approved').count(),
        'toys': Toys.objects.filter(status='approved').count(),
        'food': Food.objects.filter(status='approved').count(),
        'fitness': Fitness.objects.filter(status='approved').count(),
        'pet': Pet.objects.filter(status='approved').count(),
        'book': Book.objects.filter(status='approved').count(),
        'appliances': Appliance.objects.filter(status='approved').count(),
    }

    # Prepare context for rendering the template
    context = {
        'fitness': fitness_queryset,
        'page_obj': page_obj,
        'category_counts': category_counts,
        'selected_region': region_mapping.get(selected_region_code, selected_region_code) if selected_region_code else None,  # Pass the full region name
        'name_query': name_query,
        'cities': cities,
        'brand': brand,
        'selected_city':selected_city,
        'category': category,
        'condition': condition,
        'warranty_status': warranty_status,  # Include warranty status in context
        'price_from': price_from,
        'price_to': price_to,
        'filters': filters,
    }

    return render(request, 'fitness.html', context)


def fitness_details(request, id):
    fitness = get_object_or_404(Fitness, id=id)
    return render(request, 'fitness_details.html', {'fitness': fitness})

from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Q
from .models import Fashion, Toys, Food, Fitness, Pet, Book, Appliance  # Ensure you import your models
import json

def pets(request):
    # Define a mapping of region codes to full names
    region_mapping = {
        'MS': 'Muscat',
        'DH': 'Dhofar',
        'BT': 'Batinah',
        'DA': 'Dakhiliyah',
        'SH': 'Sharqiyah',
        'BR': 'Buraimi',
        'ZU': 'Zufar',
        'DZ': 'Masandam',
        'WR': 'Wusta',
    }

    pet_queryset = Pet.objects.filter(status='approved')

    # Retrieve query parameters
    selected_region_code = request.GET.get('region')  # Get selected region code
    name_query = request.GET.get('name', '')  
    cities = request.GET.get('cities')  
    breed = request.GET.get('breed')  
    selected_city = request.GET.get('city')  # Get selected city
    pet_type = request.GET.get('pet_type')
    vaccinated = request.GET.get('vaccinated')   
    price_from = request.GET.get('price_from')  
    price_to = request.GET.get('price_to')  
    age = request.GET.get('age')  # New filter for age

    # Apply filters
    if selected_region_code:
        pet_queryset = pet_queryset.filter(regions__iexact=selected_region_code)

    if name_query:
        pet_queryset = pet_queryset.filter(
            Q(regions__icontains=name_query) |
            Q(cities__icontains=name_query) |
            Q(pet_name__icontains=name_query) |
            Q(breed__icontains=name_query)
        )

    if cities:
        pet_queryset = pet_queryset.filter(cities__icontains=cities)

         # Filter by city if selected and not "All Cities"
    if selected_city and selected_city != "All Cities":
        pet_queryset = pet_queryset.filter(cities__icontains=selected_city)

    if breed:
        pet_queryset = pet_queryset.filter(breed__icontains=breed)

    if pet_type:
        pet_queryset = pet_queryset.filter(pet_type__iexact=pet_type)

    if vaccinated:
        pet_queryset = pet_queryset.filter(vaccinated__iexact=vaccinated)

    # Age filtering
    if age:
        age_range = age.split('-')
        if len(age_range) == 2:
            min_age = int(age_range[0])
            max_age = int(age_range[1]) if age_range[1] != '+' else float('inf')
            pet_queryset = pet_queryset.filter(age__gte=min_age, age__lte=max_age)

    # Price filtering
    if price_from and price_to:
        pet_queryset = pet_queryset.filter(price__gte=float(price_from), price__lte=float(price_to))
    elif price_from:
        pet_queryset = pet_queryset.filter(price__gte=float(price_from))
    elif price_to:
        pet_queryset = pet_queryset.filter(price__lte=float(price_to))

    # Pagination
    paginator = Paginator(pet_queryset, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Convert images to JSON format for each pet item
    for pet in page_obj:
        pet.images_json = json.dumps([image.image.url for image in pet.images.all()])

    # Count items in each category
    category_counts = {
        'fashion': Fashion.objects.filter(status='approved').count(),
        'toys': Toys.objects.filter(status='approved').count(),
        'food': Food.objects.filter(status='approved').count(),
        'fitness': Fitness.objects.filter(status='approved').count(),
        'pet': Pet.objects.filter(status='approved').count(),
        'book': Book.objects.filter(status='approved').count(),
        'appliances': Appliance.objects.filter(status='approved').count(),
    }

    # Prepare context for rendering the template
    context = {
        'pet': pet_queryset,
        'page_obj': page_obj,
        'category_counts': category_counts,
        'selected_region': region_mapping.get(selected_region_code, selected_region_code) if selected_region_code else None,  # Pass the full region name
        'name_query': name_query,
        'cities': cities,
        'selected_city':selected_city,
        'breed': breed,
        'pet_type': pet_type,
        'vaccinated': vaccinated,
        'price_from': price_from,
        'price_to': price_to,
        'age': age,  # Include age in context
    }

    return render(request, 'pets.html', context)

def pet_details(request, id):
    pet = get_object_or_404(Pet, id=id)
    return render(request, 'pet_details.html', {'pet': pet})

from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Q
from .models import Fashion, Toys, Food, Fitness, Pet, Appliance, Book  # Ensure you import your models
import json

def books(request):
    # Define a mapping of region codes to full names
    region_mapping = {
        'MS': 'Muscat',
        'DH': 'Dhofar',
        'BT': 'Batinah',
        'DA': 'Dakhiliyah',
        'SH': 'Sharqiyah',
        'BR': 'Buraimi',
        'ZU': 'Zufar',
        'DZ': 'Masandam',
        'WR': 'Wusta',
    }

    book_queryset = Book.objects.filter(status='approved')

    # Retrieve query parameters
    selected_region_code = request.GET.get('region')  # Get selected region code
    name_query = request.GET.get('name', '')  
    cities = request.GET.get('cities')  
    selected_city = request.GET.get('city')  # Get selected city
    brand = request.GET.get('brand')  
    category = request.GET.get('category')
    condition = request.GET.get('condition')   
    price_from = request.GET.get('price_from')  
    price_to = request.GET.get('price_to')  
    filters = request.GET.get('filters')  
    book_name = request.GET.get('book_name', '')  # New filter for book_name
    genre = request.GET.get('genre')  # New filter for genre

    # Apply filters
    if selected_region_code:
        book_queryset = book_queryset.filter(regions__iexact=selected_region_code)

    if name_query:
        book_queryset = book_queryset.filter(
            Q(regions__icontains=name_query) |
            Q(cities__icontains=name_query) |
            Q(book_name__icontains=name_query) |  # Updated to use book_name
            Q(brand__icontains=name_query) |
            Q(category__icontains=name_query)
        )

    if cities:
        book_queryset = book_queryset.filter(cities__icontains=cities)

    if brand:
        book_queryset = book_queryset.filter(brand__icontains=brand)

        # Filter by city if selected and not "All Cities"
    if selected_city and selected_city != "All Cities":
        book_queryset = book_queryset.filter(cities__icontains=selected_city)

    if category:
        book_queryset = book_queryset.filter(category__iexact=category)

    if condition:
        book_queryset = book_queryset.filter(condition__iexact=condition)

    # New filters for book_name and genre
    if book_name:
        book_queryset = book_queryset.filter(book_name__icontains=book_name)

    if genre:
        book_queryset = book_queryset.filter(genre__iexact=genre)

    # Price filtering
    if price_from and price_to:
        book_queryset = book_queryset.filter(price__gte=float(price_from), price__lte=float(price_to))
    elif price_from:
        book_queryset = book_queryset.filter(price__gte=float(price_from))
    elif price_to:
        book_queryset = book_queryset.filter(price__lte=float(price_to))

    if filters:
        book_queryset = book_queryset.filter(product_name__icontains=filters)  # Corrected from 'name' to 'product_name'

    # Pagination
    paginator = Paginator(book_queryset, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Convert images to JSON format for each book item
    for book in page_obj:
        book.images_json = json.dumps([image.image.url for image in book.images.all()])

    # Count items in each category
    category_counts = {
        'fashion': Fashion.objects.filter(status='approved').count(),
        'toys': Toys.objects.filter(status='approved').count(),
        'food': Food.objects.filter(status='approved').count(),
        'fitness': Fitness.objects.filter(status='approved').count(),
        'pet': Pet.objects.filter(status='approved').count(),
        'book': Book.objects.filter(status='approved').count(),
        'appliances': Appliance.objects.filter(status='approved').count(),
    }

    # Prepare context for rendering the template
    context = {
        'book': book_queryset,
        'page_obj': page_obj,
        'category_counts': category_counts,
        'selected_region': region_mapping.get(selected_region_code, selected_region_code) if selected_region_code else None,  # Pass the full region name
        'name_query': name_query,
        'cities': cities,
        'brand': brand,
        'category': category,
        'selected_city':selected_city,
        'condition': condition,
        'price_from': price_from,
        'price_to': price_to,
        'filters': filters,
        'book_name': book_name,  # Pass book_name to the context
        'genre': genre,  # Pass genre to the context
    }

    return render(request, 'books.html', context)


def book_details(request, id):
    book = get_object_or_404(Book, id=id)
    return render(request, 'book_details.html', {'book': book})


from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Q
from .models import Appliance, Fashion, Toys, Food, Fitness, Pet, Book  # Ensure you import your models
import json

def appliances(request):
    # Define a mapping of region codes to full names
    region_mapping = {
        'MS': 'Muscat',
        'DH': 'Dhofar',
        'BT': 'Batinah',
        'DA': 'Dakhiliyah',
        'SH': 'Sharqiyah',
        'BR': 'Buraimi',
        'ZU': 'Zufar',
        'DZ': 'Masandam',
        'WR': 'Wusta',
    }

    appliance_queryset = Appliance.objects.filter(status='approved')

    # Retrieve query parameters
    selected_region_code = request.GET.get('region')  # Get selected region code
    name_query = request.GET.get('name', '')  
    cities = request.GET.get('cities')  
    brand = request.GET.get('brand')  
    selected_city = request.GET.get('city')  # Get selected city
    warranty_status = request.GET.get('warranty_status')  # New filter
    appliance_type = request.GET.get('appliance_type')
    condition = request.GET.get('condition')   
    price_from = request.GET.get('price_from')  
    price_to = request.GET.get('price_to')  
    filters = request.GET.get('filters')  

    # Apply filters
    if selected_region_code:
        appliance_queryset = appliance_queryset.filter(regions__iexact=selected_region_code)

    if name_query:
        appliance_queryset = appliance_queryset.filter(
            Q(regions__icontains=name_query) |
            Q(cities__icontains=name_query) |
            Q(product_name__icontains=name_query) |
            Q(brand__icontains=name_query) |
            Q(appliance_type__icontains=name_query)
        )

    if cities:
        appliance_queryset = appliance_queryset.filter(cities__icontains=cities)

        
    # Filter by city if selected and not "All Cities"
    if selected_city and selected_city != "All Cities":
        appliance_queryset = appliance_queryset.filter(cities__icontains=selected_city)


    if brand:
        appliance_queryset = appliance_queryset.filter(brand__icontains=brand)

    if warranty_status:  # New filter
        appliance_queryset = appliance_queryset.filter(warranty_status=warranty_status)

    if appliance_type:
        appliance_queryset = appliance_queryset.filter(appliance_type__iexact=appliance_type)

    if condition:
        appliance_queryset = appliance_queryset.filter(condition__iexact=condition)

    # Price filtering
    if price_from and price_to:
        appliance_queryset = appliance_queryset.filter(price__gte=float(price_from), price__lte=float(price_to))
    elif price_from:
        appliance_queryset = appliance_queryset.filter(price__gte=float(price_from))
    elif price_to:
        appliance_queryset = appliance_queryset.filter(price__lte=float(price_to))

    if filters:
        appliance_queryset = appliance_queryset.filter(product_name__icontains=filters)

    # Pagination
    paginator = Paginator(appliance_queryset, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Convert images to JSON format for each appliance item
    for appliance in page_obj:
        appliance.images_json = json.dumps([image.image.url for image in appliance.images.all()])

    # Count items in each category
    category_counts = {
        'fashion': Fashion.objects.filter(status='approved').count(),
        'toys': Toys.objects.filter(status='approved').count(),
        'food': Food.objects.filter(status='approved').count(),
        'fitness': Fitness.objects.filter(status='approved').count(),
        'pet': Pet.objects.filter(status='approved').count(),
        'book': Book.objects.filter(status='approved').count(),
        'appliances': Appliance.objects.filter(status='approved').count(),
    }

    # Prepare context for rendering the template
    context = {
        'appliance': appliance_queryset,
        'page_obj': page_obj,
        'category_counts': category_counts,
        'selected_region': region_mapping.get(selected_region_code, selected_region_code) if selected_region_code else None,  # Pass the full region name
        'name_query': name_query,
        'cities': cities,
        'brand': brand,
        'selected_city':selected_city,
        'warranty_status': warranty_status,  # Add to context
        'appliance_type': appliance_type,
        'condition': condition,
        'price_from': price_from,
        'price_to': price_to,
        'filters': filters,
    }

    return render(request, 'appliances.html', context)


def appliance_details(request, id):
    appliance = get_object_or_404(Appliance, id=id)
    return render(request, 'appliances_details.html', {'appliance': appliance})

#Electronics

from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator
import json
from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Q
from .models import Mobile, Computer, Sound  # Ensure you import your models
import json

def mobiles(request):
    # Define a mapping of region codes to full names
    region_mapping = {
        'MS': 'Muscat',
        'DH': 'Dhofar',
        'BT': 'Batinah',
        'DA': 'Dakhiliyah',
        'SH': 'Sharqiyah',
        'BR': 'Buraimi',
        'ZU': 'Zufar',
        'DZ': 'Masandam',
        'WR': 'Wusta',
    }

    mobile_queryset = Mobile.objects.filter(status='approved')

    # Retrieve query parameters
    selected_region_code = request.GET.get('region')  # Get selected region code
    name_query = request.GET.get('name', '')  
    cities = request.GET.get('cities')  
    brand = request.GET.get('brand')  
    selected_city = request.GET.get('city')  # Get selected city
    operating_system = request.GET.get('operating_system')
    condition = request.GET.get('condition')   
    price_from = request.GET.get('price_from')  
    price_to = request.GET.get('price_to')  
    filters = request.GET.get('filters')  
    battery_capacity = request.GET.get('battery_capacity')  # New filter
    storage_capacity = request.GET.get('storage_capacity')  # New filter

    # Apply filters
    if selected_region_code:
        mobile_queryset = mobile_queryset.filter(regions__iexact=selected_region_code)

    if name_query:
        mobile_queryset = mobile_queryset.filter(
            Q(regions__icontains=name_query) |
            Q(cities__icontains=name_query) |
            Q(name__icontains=name_query) |
            Q(brand__icontains=name_query)
        )

    if cities:
        mobile_queryset = mobile_queryset.filter(cities__icontains=cities)

    # Filter by city if selected and not "All Cities"
    if selected_city and selected_city != "All Cities":
        mobile_queryset = mobile_queryset.filter(cities__icontains=selected_city)    

    if brand:
        mobile_queryset = mobile_queryset.filter(brand__icontains=brand)

    if operating_system:
        mobile_queryset = mobile_queryset.filter(operating_system__iexact=operating_system)

    if condition:
        mobile_queryset = mobile_queryset.filter(condition__iexact=condition)

    # Price filtering
    if price_from and price_to:
        mobile_queryset = mobile_queryset.filter(price__gte=float(price_from), price__lte=float(price_to))
    elif price_from:
        mobile_queryset = mobile_queryset.filter(price__gte=float(price_from))
    elif price_to:
        mobile_queryset = mobile_queryset.filter(price__lte=float(price_to))

    if filters:
        mobile_queryset = mobile_queryset.filter(name__icontains=filters)

    # Battery capacity filtering
    if battery_capacity:
        mobile_queryset = mobile_queryset.filter(battery_capacity=battery_capacity)

    # Storage capacity filtering
    if storage_capacity:
        mobile_queryset = mobile_queryset.filter(storage_capacity=storage_capacity)

    # Pagination
    paginator = Paginator(mobile_queryset, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Convert images to JSON format for each mobile item
    for mobile in page_obj:
        mobile.images_json = json.dumps([image.image.url for image in mobile.images.all()])

    # Count items in each category
    category_counts = {
        'mobiles': Mobile.objects.filter(status='approved').count(),
        'computer': Computer.objects.filter(status='approved').count(),
        'sounds': Sound.objects.filter(status='approved').count(),
    }

    # Prepare context for rendering the template
    context = {
        'mobile': mobile_queryset,
        'page_obj': page_obj,
        'category_counts': category_counts,
        'selected_region': region_mapping.get(selected_region_code, selected_region_code) if selected_region_code else None,  # Pass the full region name
        'name_query': name_query,
        'selected_city':selected_city,
        'cities': cities,
        'brand': brand,
        'operating_system': operating_system,
        'condition': condition,
        'price_from': price_from,
        'price_to': price_to,
        'filters': filters,
        'battery_capacity': battery_capacity,  # Include in context
        'storage_capacity': storage_capacity,  # Include in context
    }

    return render(request, 'mobiles.html', context)


def mobiles_details(request, id):
    mobile = get_object_or_404(Mobile, id=id)
    return render(request, 'mobiles_details.html', {'mobile': mobile})

from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Q
from .models import Mobile, Computer, Sound  # Ensure you import your models
import json

def computer(request):
    # Define a mapping of region codes to full names
    region_mapping = {
        'MS': 'Muscat',
        'DH': 'Dhofar',
        'BT': 'Batinah',
        'DA': 'Dakhiliyah',
        'SH': 'Sharqiyah',
        'BR': 'Buraimi',
        'ZU': 'Zufar',
        'DZ': 'Masandam',
        'WR': 'Wusta',
    }

    computer_queryset = Computer.objects.filter(status='approved')

    # Retrieve query parameters
    selected_region_code = request.GET.get('region')  # Get selected region code
    name_query = request.GET.get('name', '')  
    cities = request.GET.get('cities')  
    selected_city = request.GET.get('city')  # Get selected city
    brand = request.GET.get('brand')  
    operating_system = request.GET.get('operating_system')
    condition = request.GET.get('condition')   
    price_from = request.GET.get('price_from')  
    price_to = request.GET.get('price_to')  
    battery_life = request.GET.get('battery_life')  
    processor = request.GET.get('processor')  
    graphics_card = request.GET.get('graphics_card')  

    # Apply filters
    if selected_region_code:
        computer_queryset = computer_queryset.filter(regions__iexact=selected_region_code)

    if name_query:
        computer_queryset = computer_queryset.filter(
            Q(regions__icontains=name_query) |
            Q(cities__icontains=name_query) |
            Q(name__icontains=name_query) |
            Q(brand__icontains=name_query)
        )

    if cities:
        computer_queryset = computer_queryset.filter(cities__icontains=cities)

    
 # Filter by city if selected and not "All Cities"
    if selected_city and selected_city != "All Cities":
        computer_queryset =  computer_queryset.filter(cities__icontains=selected_city)

    if brand:
        computer_queryset = computer_queryset.filter(brand__icontains=brand)

    if operating_system:
        computer_queryset = computer_queryset.filter(operating_system__iexact=operating_system)

    if condition:
        computer_queryset = computer_queryset.filter(condition__iexact=condition)

    if battery_life:
        computer_queryset = computer_queryset.filter(battery_life__icontains=battery_life)

    if processor:
        computer_queryset = computer_queryset.filter(processor__iexact=processor)

    if graphics_card:
        graphics_cards = graphics_card.split(',')  # Split the comma-separated values
        computer_queryset = computer_queryset.filter(graphics_card__in=graphics_cards)

    # Price filtering
    if price_from and price_to:
        computer_queryset = computer_queryset.filter(price__gte=float(price_from), price__lte=float(price_to))
    elif price_from:
        computer_queryset = computer_queryset.filter(price__gte=float(price_from))
    elif price_to:
        computer_queryset = computer_queryset.filter(price__lte=float(price_to))

    # Pagination
    paginator = Paginator(computer_queryset, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Convert images to JSON format for each computer item
    for computer in page_obj:
        computer.images_json = json.dumps([image.image.url for image in computer.images.all()])

    # Count items in each category
    category_counts = {
        'mobiles': Mobile.objects.filter(status='approved').count(),
        'computer': Computer.objects.filter(status='approved').count(),
        'sounds': Sound.objects.filter(status='approved').count(),
    }

    # Prepare context for rendering the template
    context = {
        'computer': computer_queryset,
        'page_obj': page_obj,
        'category_counts': category_counts,
        'selected_region': region_mapping.get(selected_region_code, selected_region_code) if selected_region_code else None,  # Pass the full region name
        'name_query': name_query,
        'cities': cities,
        'brand': brand,
        'selected_city':selected_city,
        'operating_system': operating_system,
        'condition': condition,
        'price_from': price_from,
        'price_to': price_to,
        'battery_life': battery_life,
        'processor': processor,
        'graphics_card': graphics_card,
    }

    return render(request, 'computer.html', context)


def computer_details(request, id):
    computer = get_object_or_404(Computer, id=id)
    return render(request, 'computer_details.html', {'computer': computer})

from django.shortcuts import render
from django.db.models import Q
from .models import Sound, Mobile, Computer
from django.core.paginator import Paginator
import json
from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Q
from .models import Mobile, Computer, Sound  # Ensure you import your models
import json

def sounds(request):
    # Define a mapping of region codes to full names
    region_mapping = {
        'MS': 'Muscat',
        'DH': 'Dhofar',
        'BT': 'Batinah',
        'DA': 'Dakhiliyah',
        'SH': 'Sharqiyah',
        'BR': 'Buraimi',
        'ZU': 'Zufar',
        'DZ': 'Masandam',
        'WR': 'Wusta',
    }

    sound_queryset = Sound.objects.filter(status='approved')

    # Retrieve query parameters
    selected_region_code = request.GET.get('region')  # Get selected region code
    name_query = request.GET.get('name', '')  
    cities = request.GET.get('cities')  
    selected_city = request.GET.get('city')  # Get selected city
    brand = request.GET.get('brand')  
    output_power = request.GET.get('output_power')  # New filter
    has_smart_assistant = request.GET.get('has_smart_assistant')  # New filter
    connectivity = request.GET.get('connectivity')  
    condition = request.GET.get('condition')   
    price_from = request.GET.get('price_from')  
    price_to = request.GET.get('price_to')  
    filters = request.GET.get('filters')  

    # Apply filters
    if selected_region_code:
        sound_queryset = sound_queryset.filter(regions__iexact=selected_region_code)

    if name_query:
        sound_queryset = sound_queryset.filter(
            Q(regions__icontains=name_query) |
            Q(cities__icontains=name_query) |
            Q(name__icontains=name_query) |
            Q(brand__icontains=name_query)
        )

    if cities:
        sound_queryset = sound_queryset.filter(cities__icontains=cities)
    # Filter by city if selected and not "All Cities"
    if selected_city and selected_city != "All Cities":
        sound_queryset = sound_queryset.filter(cities__icontains=selected_city)

    if brand:
        sound_queryset = sound_queryset.filter(brand__iexact=brand)  # Use exact match for radio button

    if output_power:
        sound_queryset = sound_queryset.filter(output_power__icontains=output_power)  # Filter by output power

    if has_smart_assistant is not None:  # Check if the value is not None
        sound_queryset = sound_queryset.filter(has_smart_assistant=(has_smart_assistant == 'true'))  # Boolean filter

    if connectivity:
        sound_queryset = sound_queryset.filter(connectivity__iexact=connectivity)

    if condition:
        sound_queryset = sound_queryset.filter(condition__iexact=condition)

    # Price filtering
    if price_from and price_to:
        sound_queryset = sound_queryset.filter(price__gte=float(price_from), price__lte=float(price_to))
    elif price_from:
        sound_queryset = sound_queryset.filter(price__gte=float(price_from))
    elif price_to:
        sound_queryset = sound_queryset.filter(price__lte=float(price_to))

    if filters:
        sound_queryset = sound_queryset.filter(name__icontains=filters)

    # Pagination
    paginator = Paginator(sound_queryset, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Convert images to JSON format for each sound item
    for sound in page_obj:
        sound.images_json = json.dumps([image.image.url for image in sound.images.all()])

    # Count items in each category
    category_counts = {
        'mobiles': Mobile.objects.filter(status='approved').count(),
        'computer': Computer.objects.filter(status='approved').count(),
        'sounds': Sound.objects.filter(status='approved').count(),
    }

    # Prepare context for rendering the template
    context = {
        'sound': sound_queryset,
        'page_obj': page_obj,
        'category_counts': category_counts,
        'selected_region': region_mapping.get(selected_region_code, selected_region_code) if selected_region_code else None,  # Pass the full region name
        'name_query': name_query,
        'selected_city':selected_city,
        'cities': cities,
        'brand': brand,
        'output_power': output_power,  # Add to context
        'has_smart_assistant': has_smart_assistant,  # Add to context
        'connectivity': connectivity,
        'condition': condition,
        'price_from': price_from,
        'price_to': price_to,
        'filters': filters,
    }

    return render(request, 'sound.html', context)


def sounds_details(request, id):
    sound = get_object_or_404(Sound, id=id)
    return render(request, 'sound_details.html', {'sound': sound})

#Community
from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Q
from .models import Business, Education, Service  # Ensure you import your models
import json

def business(request):
    # Define a mapping of region codes to full names
    region_mapping = {
        'MS': 'Muscat',
        'DH': 'Dhofar',
        'BT': 'Batinah',
        'DA': 'Dakhiliyah',
        'SH': 'Sharqiyah',
        'BR': 'Buraimi',
        'ZU': 'Zufar',
        'DZ': 'Masandam',
        'WR': 'Wusta',
    }

    business_query = Business.objects.filter(status='approved')

    # Retrieve query parameters
    selected_region_code = request.GET.get('region')  # Get selected region code
    selected_city = request.GET.get('city')  # Get selected city
    name_query = request.GET.get('name', '')  
    category = request.GET.get('category')  
    condition = request.GET.get('condition')  
    warranty_status = request.GET.get('warranty_status')  
    price_from = request.GET.get('price_from') 
    price_to = request.GET.get('price_to')      
    cities = request.GET.get('cities')  
    filters = request.GET.get('filters')  

    # Apply filters
    if selected_region_code:
        business_query = business_query.filter(regions=selected_region_code)

    if name_query:
        business_query = business_query.filter(
            Q(product_name__icontains=name_query) |
            Q(brand__icontains=name_query) |
            Q(description__icontains=name_query)
        )

    if category:
        business_query = business_query.filter(category=category)

    # Filter by city if selected and not "All Cities"
    if selected_city and selected_city != "All Cities":
        business_query = business_query.filter(cities__icontains=selected_city)


    if condition:
        business_query = business_query.filter(condition=condition)

    if warranty_status:
        business_query = business_query.filter(warranty_status=warranty_status)

    if cities:
        business_query = business_query.filter(cities__icontains=cities)

    if price_from and price_to:
        business_query = business_query.filter(price__gte=price_from, price__lte=price_to)
    elif price_from:
        business_query = business_query.filter(price__gte=price_from)
    elif price_to:
        business_query = business_query.filter(price__lte=price_to)

    if filters:
        business_query = business_query.filter(
            Q(product_name__icontains=filters) |
            Q(brand__icontains=filters) |
            Q(description__icontains=filters)
        )

    # Process images for each business
    for business in business_query:
        business.images_json = json.dumps([image.image.url for image in business.images.all()])

    # Calculate category counts
    category_counts = {
        'business': Business.objects.filter(status='approved').count(),
        'education': Education.objects.filter(status='approved').count(),
        'service': Service.objects.filter(status='approved').count(),
    }

    # Set up pagination
    paginator = Paginator(business_query, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Prepare context for rendering the template
    context = {
        'business': business_query,
        'page_obj': page_obj,
        'category_counts': category_counts,
        'selected_region': region_mapping.get(selected_region_code, selected_region_code) if selected_region_code else None,  # Pass the full region name
        'name_query': name_query,
        'selected_city':selected_city,
        'category': category,
        'condition': condition,
        'warranty_status': warranty_status,
        'price_from': price_from,
        'price_to': price_to,
        'cities': cities,
        'filters': filters,
    }

    return render(request, 'business.html', context)

def business_details(request, id):
    business = get_object_or_404(Business, id=id)
    return render(request, 'business_details.html', {'business': business})

from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Q
from .models import Business, Education, Service  # Ensure you import your models
import json

def education(request):
    # Define a mapping of region codes to full names
    region_mapping = {
        'MS': 'Muscat',
        'DH': 'Dhofar',
        'BT': 'Batinah',
        'DA': 'Dakhiliyah',
        'SH': 'Sharqiyah',
        'BR': 'Buraimi',
        'ZU': 'Zufar',
        'DZ': 'Masandam',
        'WR': 'Wusta',
    }

    # Start with the base query for approved education entries
    education_query = Education.objects.filter(status='approved')

    # Retrieve query parameters
    selected_region_code = request.GET.get('region')  # Get selected region code
    name_query = request.GET.get('name', '')  # Get the search query (default is empty string)
    course_type = request.GET.get('course_type')  # Filter by course type
    selected_city = request.GET.get('city')  # Get selected city
    subject = request.GET.get('subject')  # Filter by course subject
    price_from = request.GET.get('price_from')  # Get the price from input
    price_to = request.GET.get('price_to')      # Get the price to input
    cities = request.GET.get('cities')  # Filter by cities
    filters = request.GET.get('filters')  # General filter for description or instructor name
    duration = request.GET.getlist('duration')  # Get list of selected durations
    qualification = request.GET.get('qualification')

    # Apply filters
    if duration:
        education_query = education_query.filter(duration__in=duration)

    if qualification:
        education_query = education_query.filter(qualification__iexact=qualification)

    # Apply filters based on request parameters
    if selected_region_code:
        education_query = education_query.filter(regions=selected_region_code)

        
 # Filter by city if selected and not "All Cities"
    if selected_city and selected_city != "All Cities":
        education_query = education_query.filter(cities__icontains=selected_city)

    if name_query:
        education_query = education_query.filter(
            Q(subject__icontains=name_query) |
            Q(description__icontains=name_query) |
            Q(instructor_name__icontains=name_query)
        )

    if course_type:
        education_query = education_query.filter(course_type=course_type)

    if subject:
        education_query = education_query.filter(subject__icontains=subject)

    if cities:
        education_query = education_query.filter(cities__icontains=cities)

    # Price Range Filtering
    if price_from and price_to:
        education_query = education_query.filter(price__gte=price_from, price__lte=price_to)
    elif price_from:
        education_query = education_query.filter(price__gte=price_from)
    elif price_to:
        education_query = education_query.filter(price__lte=price_to)

    if filters:
        education_query = education_query.filter(
            Q(description__icontains=filters) |
            Q(instructor_name__icontains=filters) |
            Q(qualification__icontains=filters)
        )

    # Prepare images JSON for each education entry
    for education in education_query:
        education.images_json = json.dumps([image.image.url for image in education.images.all()])

    # Calculate category counts
    category_counts = {
        'business': Business.objects.filter(status='approved').count(),
        'education': Education.objects.filter(status='approved').count(),
        'service': Service.objects.filter(status='approved').count(),
    }

    # Pagination
    paginator = Paginator(education_query, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Prepare context for rendering the template
    context = {
        'education': education_query,
        'page_obj': page_obj,
        'category_counts': category_counts,
        'selected_region': region_mapping.get(selected_region_code, selected_region_code) if selected_region_code else None,  # Pass the full region name
        'name_query': name_query,
        'selected_city':selected_city,
        'course_type': course_type,
        'subject': subject,
        'price_from': price_from,
        'price_to': price_to,
        'cities': cities,
        'filters': filters,
        'duration': duration,  # Include duration in context
        'qualification': qualification,  # Include qualification in context
    }

    return render(request, 'education.html', context)

def education_details(request, id):
    education = get_object_or_404(Education, id=id)
    return render(request, 'education_details.html', {'education': education})

from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Q
from .models import Business, Education, Service  # Ensure you import your models
import json

def service(request):
    # Define a mapping of region codes to full names
    region_mapping = {
        'MS': 'Muscat',
        'DH': 'Dhofar',
        'BT': 'Batinah',
        'DA': 'Dakhiliyah',
        'SH': 'Sharqiyah',
        'BR': 'Buraimi',
        'ZU': 'Zufar',
        'DZ': 'Masandam',
        'WR': 'Wusta',
    }

    # Start with the base query for approved services
    service_queryset = Service.objects.filter(status='approved')

    # Retrieve query parameters
    selected_region_code = request.GET.get('region')  # Get selected region code
    name_query = request.GET.get('name', '')  # Get the search query (default is empty string)
    service_type = request.GET.get('service_type')  # Filter by service type
    selected_city = request.GET.get('city')  # Get selected city
    cities = request.GET.get('cities')  # Filter by cities
    price_from = request.GET.get('price_from')  # Get the price from input
    price_to = request.GET.get('price_to')      # Get the price to input
    filters = request.GET.get('filters')  # General filter for description or provider name

    # Apply filters based on request parameters
    if selected_region_code:
        service_queryset = service_queryset.filter(regions=selected_region_code)
     # Filter by city if selected and not "All Cities"
    if selected_city and selected_city != "All Cities":
        service_queryset = service_queryset.filter(cities__icontains=selected_city)

    if name_query:
        service_queryset = service_queryset.filter(
            Q(provider_name__icontains=name_query) |
            Q(description__icontains=name_query) |
            Q(contact_info__icontains=name_query)
        )

    if service_type:
        service_queryset = service_queryset.filter(service_type=service_type)

    if cities:
        service_queryset = service_queryset.filter(cities__icontains=cities)

    # Price Range Filtering
    if price_from and price_to:
        service_queryset = service_queryset.filter(price_range__gte=price_from, price_range__lte=price_to)
    elif price_from:
        service_queryset = service_queryset.filter(price_range__gte=price_from)
    elif price_to:
        service_queryset = service_queryset.filter(price_range__lte=price_to)

    if filters:
        service_queryset = service_queryset.filter(
            Q(description__icontains=filters) |
            Q(provider_name__icontains=filters)
        )

    # Prepare images JSON for each service entry
    for service in service_queryset:
        service.images_json = json.dumps([image.image.url for image in service.images.all()])

    # Calculate category counts
    category_counts = {
        'business': Business.objects.filter(status='approved').count(),
        'education': Education.objects.filter(status='approved').count(),
        'service': Service.objects.filter(status='approved').count(),
    }

    # Pagination
    paginator = Paginator(service_queryset, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Prepare context for rendering the template
    context = {
        'service': service_queryset,
        'page_obj': page_obj,
        'category_counts': category_counts,
        'selected_region': region_mapping.get(selected_region_code, selected_region_code) if selected_region_code else None,  # Pass the full region name
        'name_query': name_query,
        'selected_city':selected_city,
        'service_type': service_type,
        'cities': cities,
        'price_from': price_from,
        'price_to': price_to,
        'filters': filters,
    }

    return render(request, 'service.html', context)

def service_details(request, id):
    service = get_object_or_404(Service, id=id)
    return render(request, 'service_details.html', {'service': service})


def job(request):
    # Fetch all job categories
    categories = JobCategory.objects.all()
    
    # Fetch approved job posts grouped by category
    jobs_by_category = {
        category.name: JobPost.objects.filter(
            job_category=category,application_deadline__gte=timezone.now()
        ).order_by('-posted_on')[:2]  # Limit to 2 per category
        for category in categories
    }
    
    # Flatten jobs into a single list with additional details
    all_jobs = []
    for category_name, jobs in jobs_by_category.items():
        for job in jobs:
            all_jobs.append({
                'category': category_name,
                'data': job,
                'job_type': job.job_type,
            })

    context = {
        'all_jobs': all_jobs,
    }

    return render(request, 'job.html', context)


def full_time_jobs(request):
    # Fetch all job categories
    categories = JobCategory.objects.all()

    # Fetch approved full-time job posts grouped by category
    jobs_by_category = {
        category.name: JobPost.objects.filter(
            job_category=category,
            job_type='full-time' ,application_deadline__gte=timezone.now() # Filter for full-time jobs based on the job_type choice
        ).order_by('-posted_on')  # Limit to 2 per category
        for category in categories
    }

    # Flatten jobs into a single list with additional details
    full_time_jobs = []
    for category_name, jobs in jobs_by_category.items():
        for job in jobs:
            # Ensure jobs are not repeated
            full_time_jobs.append({
                'category': category_name,
                'data': job,
                'job_type': job.job_type,
            })

    context = {
        'full_time_jobs': full_time_jobs,
    }

    return render(request, 'full_time.html', context)


def part_time_jobs(request):
    # Fetch all job categories
    categories = JobCategory.objects.all()

    # Fetch part-time job posts filtered by job_type 'part-time', grouped by category
    jobs_by_category = {
        category.name: JobPost.objects.filter(
            job_category=category,  # Ensure the jobs belong to the correct category
            job_type='part-time' ,application_deadline__gte=timezone.now() # Filter for part-time jobs based on the job_type choice
        ).order_by('-posted_on')  # Order by most recent post
        for category in categories
    }

    # Flatten jobs into a single list with additional details
    part_time_jobs = []
    for category_name, jobs in jobs_by_category.items():
        for job in jobs:
            part_time_jobs.append({
                'category': category_name,
                'data': job,
                'job_type': job.job_type,
            })

    context = {
        'part_time_jobs': part_time_jobs,
    }

    return render(request, 'part_time.html', context)


def job_details_index(request, job_id):
    job = get_object_or_404(JobPost, id=job_id)
    
    return render(request, 'job_details_index.html', {'job': job})
    




from django.shortcuts import render
from django.db.models import Q
import json
from django.utils.safestring import mark_safe
from .models import Fashion, Food, Fitness, Pet, Book, Appliance  # Ensure models are imported

from django.shortcuts import render
from django.db.models import Q
import json
from django.utils.safestring import mark_safe
from .models import Fashion, Food, Fitness, Pet, Book, Appliance, Toys
def index5(request):
    # Get filter parameters from the request
    selected_region_code = request.GET.get('region')  # Get selected region code
    selected_city = request.GET.get('city')  # Get selected city
    selected_category = request.GET.get('category')
    name_query = request.GET.get('name', '')  # Search query

    # Define a mapping of region codes to full names (if needed)
    region_mapping = {
        'MS': 'Muscat',
        'DH': 'Dhofar',
        'BT': 'Batinah',
        'DA': 'Dakhiliyah',
        'SH': 'Sharqiyah',
        'BR': 'Buraimi',
        'ZU': 'Zufar',
        'DZ': 'Masandam',
        'WR': 'Wusta',
    }

    # Define category model mappings
    category_mappings = {
        'fashion': Fashion.objects.filter(status='approved'),
        'toys': Toys.objects.filter(status='approved'),
        'food': Food.objects.filter(status='approved'),
        'fitness': Fitness.objects.filter(status='approved'),
        'pets': Pet.objects.filter(status='approved'),
        'books': Book.objects.filter(status='approved'),
        'appliances': Appliance.objects.filter(status='approved'),
    }

    # Correct singularization of category names
    category_singular_mapping = {
        'fashion': 'fashion',
        'toys': 'toy',
        'food': 'food',
        'fitness': 'fitness',
        'pets': 'pet',
        'books': 'book',
        'appliances': 'appliance',
    }

    # Compute category counts
    category_counts = {key: queryset.count() for key, queryset in category_mappings.items()}

    all_ads = []

    for category, queryset in category_mappings.items():
        if selected_category and category != selected_category:
            continue  # Skip non-matching categories

        # Filter by region if selected
        if selected_region_code:
            queryset = queryset.filter(regions__icontains=selected_region_code)

        # Filter by city if selected and not "All Cities"
        if selected_city and selected_city != "All Cities":
            queryset = queryset.filter(cities__icontains=selected_city)

        # Filter by search query
        if name_query:
            queryset = queryset.filter(
                Q(name__icontains=name_query) | Q(regions__icontains=name_query)
            )

        queryset = queryset.order_by('-id')[:5]

        for item in queryset:
            display_name = getattr(
                item,
                {'pets': 'breed', 'books': 'genre'}.get(category, 'brand'),
                'Unnamed Product'
            )

            images = [{"image": image.image.url} for image in item.images.all()]
            main_image_url = images[0]["image"] if images else "/static/assets/images/resource/default.jpg"
            images_json = mark_safe(json.dumps(images))

            all_ads.append({
                'category': category_singular_mapping.get(category, category),  # Fixed singular category
                'data': item,
                'name': display_name,
                'product_type': category,
                'main_image_url': main_image_url,
                'images_json': images_json,
                'total_images': len(images),
            })

    context = {
        'all_ads': all_ads,
        'selected_region': region_mapping.get(selected_region_code, selected_region_code) if selected_region_code else None,  # Pass the full region name
        'selected_city': selected_city,  # Pass the selected city to the template
        'selected_category': selected_category,
        'name_query': name_query,
        'category_counts': category_counts,
    }

    return render(request, 'index-5.html', context)



from django.shortcuts import render


import logging

def mobilelist(request):
    categories = {
        'mobiles': Mobile.objects.filter(status='approved').order_by('-id')[:2],
        'computers': Computer.objects.filter(status='approved').order_by('-id')[:2],
        'sounds': Sound.objects.filter(status='approved').order_by('-id')[:2],
    }

    all_ads = []
    for category, items in categories.items():
        for item in items:
            display_name = item.brand
            if hasattr(item, 'model_number'):
                display_name += f" {item.model_number}"

            all_ads.append({
                'category': category[:-1],  # Singularize category name (e.g., 'mobiles' -> 'mobile')
                'data': item,
                'name': display_name,
            })

    # Log to check if all_ads has data
    logging.debug(f"All Ads: {all_ads}")

    context = {
        'all_ads': all_ads,
    }
    return render(request, 'mobilelist.html', context)




from django.shortcuts import render
from .models import Business, Education, Service

import json
from django.shortcuts import render
from .models import Business, Education, Service
def community(request):
    # Define a mapping of region codes to full names (expand as necessary)
    region_mapping = {
        'MS': 'Muscat',
        'DH': 'Dhofar',
        'BT': 'Batinah',
        'DA': 'Dakhiliyah',
        'SH': 'Sharqiyah',
        'BR': 'Buraimi',
        'ZU': 'Zufar',
        'DZ': 'Masandam',
        'WR': 'Wusta',
    }

    # Categories and models
    categories = {
        'business': Business,
        'education': Education,
        'service': Service,
    }

    all_ads = []
    category_counts = {}  # Dictionary to store the count for each category

    # Get filter parameters from the request
    selected_region_code = request.GET.get('region')  # Get selected region code
    selected_city = request.GET.get('city')  # Get selected city
    name_query = request.GET.get('name', '')  # Search query

    # Loop through categories and apply filters
    for category_name, model in categories.items():
        # Filter query by status
        query = model.objects.filter(status='approved')

        # Apply region filter if selected
        if selected_region_code:
            query = query.filter(regions__icontains=selected_region_code)

        # Apply city filter if selected
        if selected_city and selected_city != "All Cities":
            query = query.filter(cities__icontains=selected_city)

        # Apply search query if available
        if name_query:
            query = query.filter(
                Q(brand__icontains=name_query) | 
                Q(subject__icontains=name_query) |
                Q(provider_name__icontains=name_query) |
                Q(regions__icontains=name_query) |
                Q(cities__icontains=name_query)
            )

        # Fetch items (limit as per original query, you can adjust the limit)
        items = query.order_by('-id')[:5]

        # Count items per category
        category_counts[category_name] = len(items)

        # Loop through the filtered items
        for item in items:
            # Handle image URLs (similar to previous examples)
            images = [{"image": image.image.url} for image in item.images.all()]
            main_image_url = images[0]["image"] if images else "/static/assets/images/resource/default.jpg"
            images_json = json.dumps(images) if images else "[]"

            # Define display name for each category
            if category_name == 'business':
                name = item.brand
            elif category_name == 'education':
                name = item.subject
            elif category_name == 'service':
                name = item.provider_name

            # Add the item to the ads list with additional info
            all_ads.append({
                'category': category_name,
                'data': item,
                'name': name,
                'main_image_url': main_image_url,
                'images_json': images_json,
                'product_type': category_name,
                'region_name': region_mapping.get(item.regions, item.regions),
            })

    context = {
        'all_ads': all_ads,
        'category_counts': category_counts,  # Add category counts to the context
        'selected_region': region_mapping.get(selected_region_code, selected_region_code) if selected_region_code else None,  # Pass the full region name
        'selected_city': selected_city,  # Pass the selected city to the template
        'name_query': name_query,  # Pass the search query back to the template
    }

    return render(request, 'community.html', context)




def browseads2(request, category, id):
    
    print(f"Category: {category}, ID: {id}")  
    
    ad_model_mapping = {
        'Lands': Land,
        'Villas': Villa,
        'Commercials': Commercial,
        'Farms': Farm,
        'Chalets': Chalet,
        'Automobiles': Automobile,
        'Motorcycle': Motorcycle,
        'Heavyvehicle': HeavyVehicle,
        'Boat': Boat,
        'Accessoriesparts': AutoAccessoryPart,
        'Numberplate': NumberPlate,
        'Education': Education,
        'Business': Business,
        'Services': Service,
        'Mobile': Mobile,
        'Computer': Computer,
        'Sound': Sound,
        'Fashion': Fashion,
        'Toys': Toys,
        'Foods': Food,
        'Fitness': Fitness,
        'Pets': Pet,
        'Books': Book,
        'Appliances': Appliance,
    }
    
    if category == 'Properties':
        categories = ['Lands', 'Villas', 'Commercials', 'Farms', 'Chalets']
    else:
        categories = [category]
    
    ad = None
    for cat in categories:
        ad_model = ad_model_mapping.get(cat)
        if ad_model:
            print(f"Checking {cat} model for ID {id}")  # Debugging
            ad = ad_model.objects.filter(id=id).first()
            if ad:
                print(f"Found ad in {cat} model: {ad}")  # Debugging
                break
    
    if not ad:
        raise Http404("No matching ad found")
    
    features = []
    if ad:
        features.append(('Price', f"OMR {ad.price}"))
        features.append(('Location', ad.location))
        
        if isinstance(ad, Land):
            features += [
                ('Plot Area', f"{ad.plot_area} sqm"),
                ('Ownership', ad.ownership_details),
                ('Additional Info', ad.additional_information),
                ('Property', ad.property_type),
            ]
        elif isinstance(ad, Villa):
            features += [
                ('Bedrooms', ad.bedrooms),
                ('Bathrooms', ad.bathrooms),
                ('Plot Area', f"{ad.plot_area} sqm"),
                ('Ownership', ad.ownership_details),
                ('Additional Info', ad.additional_information),
            ]
        elif isinstance(ad, Commercial):
            features += [
                ('Property Type', ad.property_type),
                ('Plot Area', f"{ad.plot_area} sqm"),
                ('Ownership', ad.ownership_details),
                ('Additional Info', ad.additional_information),
            ]
        elif isinstance(ad, Farm):
            features += [
                ('Water Source', ad.irrigation_water_source),
                ('Soil Type', ad.soil_type),
                ('Tenancy Information', ad.tenancy_information),
                ('Plot Area', f"{ad.plot_area} sqm"),
            ]
        elif isinstance(ad, Chalet):
            features += [
                ('Amenities', ad.amenities),
                ('Plot Area', f"{ad.plot_area} sqm"),
                ('Additional Info', ad.additional_information),
            ]
        elif isinstance(ad, Automobile):
            features += [
                ('Make', ad.make),
             
                ('Year', ad.year),
                ('Mileage', f"{ad.mileage} km"),
                ('Transmission', ad.transmission),
            ]
        elif isinstance(ad, Motorcycle):
            features += [
                ('Make', ad.make),
                ('Model', ad.model),
                ('Year', ad.year),
                ('Mileage', f"{ad.mileage} km"),
                ('Engine Size', f"{ad.engine_size} cc"),
            ]
        elif isinstance(ad, HeavyVehicle):
            features += [
              
                ('Year', ad.year),
                ('Mileage', f"{ad.mileage} km"),
            ]
        elif isinstance(ad, Boat):
            features += [
                
                ('Year', ad.year),
                ('Length', f"{ad.length} m"),
            ]
        elif isinstance(ad, AutoAccessoryPart):
            features += [
                ('Type', ad.name),
            ]
        elif isinstance(ad, NumberPlate):
            features += [
                ('Number', ad.number),
                ('Region', ad.regions),
            ]
        elif isinstance(ad, Education):
            features += [
                
                
                ('Duration', ad.duration),
            ]
        elif isinstance(ad, Business):
            features += [
                
                ('Location', ad.location),
                ('Turnover', f"OMR {ad.turnover}"),
            ]
        elif isinstance(ad, Service):
            features += [
                ('Service Type', ad.service_type),
                ('Location', ad.location),
               
            ]
        elif isinstance(ad, Mobile):
            features += [
                ('Brand', ad.brand),
              
                ('Condition', ad.condition),
                ('Storage', f"{ad.storage} GB"),
            ]
        elif isinstance(ad, Computer):
            features += [
                ('Brand', ad.brand),
               
                ('Condition', ad.condition),
               
            ]
        elif isinstance(ad, Sound):
            features += [
               
                ('Brand', ad.brand),
               
                ('Condition', ad.condition),
            ]
        elif isinstance(ad, Fashion):
            features += [
               
                ('Brand', ad.brand),
                ('Size', ad.size),
                ('Condition', ad.condition),
            ]
        elif isinstance(ad, Toys):
            features += [
             
                ('Brand', ad.brand),
                ('Condition', ad.condition),
            ]
        elif isinstance(ad, Food):
            features += [
               
                ('Brand', ad.brand),
                ('Expiry Date', ad.expiration_date),
            ]
        elif isinstance(ad, Fitness):
            features += [
               
                ('Brand', ad.brand),
                ('Condition', ad.condition),
            ]
        elif isinstance(ad, Pet):
            features += [
                ('Type', ad.pet_type),
                ('Breed', ad.breed),
                ('Age', ad.age),
            ]
        elif isinstance(ad, Book):
            features += [
                ('Title', ad.book_name),
                ('Genre', ad.genre),
                ('Condition', ad.condition),
            ]
        elif isinstance(ad, Appliance):
            features += [
                ('Type', ad.appliance_type),
                ('Brand', ad.brand),
                ('Condition', ad.condition),
            ]
    
    return render(request, 'browse-ads-2.html', {'ad': ad, 'features': features})

def browseads3(request):
    return render(request, 'browse-ads-3.html')

def joblist(request):
    return render(request, 'joblist.html') 

def classifiedlist(request):
    return render(request, 'classifiedlist.html')

def communitylist(request):
    return render(request, 'communitylist.html')

def browseadsdetails(request):
    return render(request, 'browse-ads-details.html')

from django.http import Http404
def browseads1(request, category, id):
    print(f"Category: {category}, ID: {id}")  # Debugging
    
    ad_model_mapping = {
        'Lands': Land,
        'Villas': Villa,
        'Apartments': Apartment,
        'Shops': Shop,
        'Cafes': Cafe,
        'Offices' : Office,
        'Wholebuilding' : Wholebuilding,
    }
    
    if category == 'Properties':
        categories = ['Lands', 'Villas', 'Apartments', 'Shops', 'Cafes' , 'Offices', 'Wholebuilding']
    else:
        categories = [category]
    
    ad = None
    for cat in categories:
        ad_model = ad_model_mapping.get(cat)
        if ad_model:
            print(f"Checking {cat} model for ID {id}")  # Debugging
            ad = ad_model.objects.filter(id=id).first()
            if ad:
                print(f"Found ad in {cat} model: {ad}")  # Debugging
                break
    
    if not ad:
        raise Http404("No matching ad found")
    
    features = []
    if ad:
        # features.append(('Price', f"OMR {ad.price}"))
        
        
        if isinstance(ad, Land):
            features += [
        ('Plot Area', f"{ad.plot_area} sqm"),
        ('Zoned For', f"{ad.get_zoned_for_display()}"),  # Using get_display
        ('Lister Type', f"{ad.get_lister_type_display()}"),
        ('Property Mortgage', f"{ad.get_property_mortgage_display()}"),
        ('Facade', f"{ad.get_facade_display()}"),
    ]

        elif isinstance(ad, Villa):
            features += [
                ('Bedrooms', ad.bedrooms),
                ('Bathrooms', ad.bathrooms),
                ('Plot Area', f"{ad.plot_area} sqm"),
                ('Surface Area', f"{ad.surface_area} sqm"),
                ('Floors', ad.floors),
                ('Lister Type', ad.lister_type),
                ('Building age', ad.building),
                ('Property Mortgage', ad.property_mortgage),
                ('Facade', ad.facade),
                
            ]
        elif isinstance(ad, Apartment):
            features += [
                
                ('Plot Area', f"{ad.plot_area} sqm"),
                ('Bedrooms', ad.bedrooms),
                ('Bathrooms', ad.bathrooms),
                ('Floors', ad.floors),
                ('Furnished', ad.furnished),
                ('Building Age', ad.building),
                ('Lister Type', ad.lister_type),
                ('Property Mortgage', ad.property_mortgage),
                ('Facade', ad.facade),
                
            ]
        elif isinstance(ad, Shop):
            features += [
               
                ('Plot Area', f"{ad.plot_area} sqm"),
                ('Property Mortgage', ad.property_mortgage),
                ('Lister Type', ad.lister_type),
            
            ]
        elif isinstance(ad, Cafe):
            features += [
                
                ('Plot Area', f"{ad.plot_area} sqm"),
                ('Lister Type', ad.lister_type),
                ('Property', ad.property),
                ('Property Mortgage', ad.property_mortgage),
            ]
        elif isinstance(ad, Wholebuilding):
            features += [
                
                ('Plot Area', f"{ad.plot_area} sqm"),
               
                
                ('Property', ad.property),
                ('Lister Type', ad.lister_type),
                ('Property Mortgage', ad.property_mortgage),
                
                
            ]
        elif isinstance(ad, Office):
            features += [
                
              ('Plot Area', f"{ad.plot_area} sqm"),
                
                ('Furnished', ad.furnished),
                ('Property', ad.property),
                ('Lister Type', ad.lister_type),
                ('Property Mortgage', ad.property_mortgage),
                ('Floors', ad.floors),
                
                
            ]
    
    return render(request, 'browse-ads-1.html', {'ad': ad, 'features': features})


def jobdetails(request, user_id, job_id):
    # Fetch the user by user_id
    user = get_object_or_404(CustomUser, id=user_id)
    
    # Get the job post based on the provided job_id
    job = get_object_or_404(JobPost, id=job_id)
    
    # Check if the user has already applied for this job
    has_applied = JobApplication.objects.filter(user=user, job=job).exists()

    if request.method == 'POST':
        if has_applied:
            # If the user has already applied, handle accordingly, e.g., show a message
            # Redirect or return a response indicating that the user has already applied
            return redirect('jobdetails')  # Replace with your actual redirect or message
        else:
            form = JobApplicationForm(request.POST, request.FILES)
            if form.is_valid():
                job_application = form.save(commit=False)
                job_application.user = user  # Associate the application with the provided user
                job_application.status = 'pending'  # Associate the application with the provided user
                job_application.job = job  # Associate the application with the specific job
                
                # Fetch the Company instance based on the company name from the JobPost
                company_instance = job.company  # This references the Company instance associated with the job
                
                # Ensure company is assigned with the correct Company instance
                job_application.company = company_instance
                job_application.save()
                
                
                # Redirect to a success page or a detail page for the job application
                return redirect(jobapplication, user_id=user.id)  
    else:
        form = JobApplicationForm()

    # Pass the 'has_applied' flag to the template to conditionally render the button
    return render(request, 'jobdetails.html', {
        'job': job,
        'form': form,
        'has_applied': has_applied
    })



def job_details_non_authenticated(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, 'jobnon.html', {'job': job})


def job_post_detail(request, pk):
    # Fetch the job post object by its primary key (pk)
    job_post = get_object_or_404(JobPost, pk=pk)
    
    # Render a template and pass the job post object as context
    return render(request, 'job_post_detail.html', {'job_post': job_post})

from django.shortcuts import render, get_object_or_404
from .models import Fashion, Toys, Food, Fitness, Pet, Book, Appliance


def classified_details(request, ad_type, ad_id):
    # Mapping between ad_type and the corresponding model
    ad_model_mapping = {
        'fashion': Fashion,
        'toy': Toys,
        'food': Food,
        'fitness': Fitness,
        'pet': Pet,
        'book': Book,
        'appliance': Appliance,
    }

    # Debugging: Check incoming URL parameters
    print(f"Ad Type: {ad_type}, Ad ID: {ad_id}")

    # Get the model class for the ad_type
    ad_model = ad_model_mapping.get(ad_type)
    
    if ad_model:
        ad = get_object_or_404(ad_model, id=ad_id)
        print(f"Ad Found: {ad}")  # Debugging: Ensure ad is fetched
    else:
        ad = None

    features = []
    if ad:
        features.append(('Price', f"OMR {ad.price}"))
        features.append(('Location', ad.location))

        if ad_type == 'fashion':
            features += [
                ('Brand', ad.brand),
                ('Size', ad.size),
                ('Gender', ad.gender),
                ('Color', ad.color),
                ('Material', ad.material),
                ('Condition', ad.condition),
                ('Contact Details', ad.contact_details),
            ]
        elif ad_type == 'toy':
            features += [
                ('Brand', ad.brand),
                ('Platform', ad.platform),
                ('Age Group', ad.age_group),
                ('Condition', ad.condition),
            ]
        elif ad_type == 'food':
            features += [
                ('Product Type', ad.product_type),
                ('Brand', ad.brand),
                ('Quantity', f"{ad.quantity} grams"),
                ('Expiration Date', ad.expiration_date),
                ('Dietary Info', ad.dietary_info),
            ]
        elif ad_type == 'fitness':
            features += [
                ('Category', ad.category),
                ('Brand', ad.brand),
                ('Condition', ad.condition),
                ('Warranty Status', ad.warranty_status),
            ]
        elif ad_type == 'pet':
            features += [
                ('Pet Type', ad.pet_type),
                ('Breed', ad.breed),
                ('Age', f"{ad.age} years"),
                ('Vaccinated', ad.vaccinated),
            ]
        elif ad_type == 'book':
            features += [
                ('Category', ad.category),
                ('Genre', ad.genre),
                ('Condition', ad.condition),
            ]
        elif ad_type == 'appliance':
            features += [
                ('Appliance Type', ad.appliance_type),
                ('Brand', ad.brand),
                ('Model Number', ad.model_number),
                ('Condition', ad.condition),
                ('Warranty Status', ad.warranty_status),
            ]

    # Debugging: Ensure features are correctly set
    print(f"Features: {features}")

    return render(request, 'classifieddetails.html', {'ad': ad, 'features': features})


def mobiledetails(request, category, id):
    # Mapping between category and the corresponding model
    category_model_mapping = {
        'electronics' : Mobile,
        'mobile': Mobile,
        'computer': Computer,
        'sound': Sound,
    }

    # Get the model class for the category
    model_class = category_model_mapping.get(category)

    if model_class:
        # Fetch the ad by ID (404 if not found or not approved)
        ad = get_object_or_404(model_class, id=id, status='approved')
    else:
        ad = None

    features = []
    if ad:
        # Common features
        features.append(('Price', f"OMR {ad.price}"))
        features.append(('Location', ad.location))
        features.append(('Condition', ad.condition))

        # Category-specific features
        if category == 'mobile':
            features += [
                ('Brand', ad.brand),
                ('Model Number', ad.model_number),
                ('Operating System', ad.operating_system),
                ('Screen Size', f"{ad.screen_size} inches"),
                ('Storage Capacity', f"{ad.storage_capacity} GB"),
                ('RAM Size', f"{ad.ram_size} GB"),
                ('Battery Capacity', f"{ad.battery_capacity} mAh"),
                  ]
        elif category == 'electronics':
            features += [
                ('Brand', ad.brand),
                ('Model Number', ad.model_number),
                ('Operating System', ad.operating_system),
                ('Screen Size', f"{ad.screen_size} inches"),
                ('Storage Capacity', f"{ad.storage_capacity} GB"),
                ('RAM Size', f"{ad.ram_size} GB"),
                ('Battery Capacity', f"{ad.battery_capacity} mAh"),
            ]
        elif category == 'computer':
            features += [
                ('Brand', ad.brand),
                ('Model Number', ad.model_number),
                ('Operating System', ad.operating_system),
                ('Screen Size', f"{ad.screen_size} inches"),
                ('Storage Capacity', f"{ad.storage_capacity} GB"),
                ('RAM Size', f"{ad.ram_size} GB"),
                ('Processor', ad.processor),
                ('Graphics Card', ad.graphics_card),
                ('Battery Life', ad.battery_life),
            ]
        elif category == 'sound':
            features += [
                ('Brand', ad.brand),
                ('Model Number', ad.model_number),
                ('Connectivity', ad.connectivity),
                ('Output Power', ad.output_power),
                ('Audio Channels', ad.channels),
                ('Smart Assistant Support', "Yes" if ad.has_smart_assistant else "No"),
            ]

    # Render the template and pass the ad object and features list
    return render(request, 'mobiledetails.html', {'ad': ad, 'features': features})

   

from django.shortcuts import get_object_or_404, render

def communitydetails(request, ad_type, ad_id):
    # Mapping between ad_type and the corresponding model
    ad_model_mapping = {
        'business': Business,
        'education': Education,
        'service': Service,
    }

    # Get the model class for the ad_type
    ad_model = ad_model_mapping.get(ad_type)
    
    if ad_model:
        # Fetch the ad by ID (404 if not found or not approved)
        ad = get_object_or_404(ad_model, id=ad_id)
    else:
        ad = None

    features = []
    if ad:
        # Common features
        
        features.append(('Location', ad.location))
        

        # Category-specific features
        if ad_type == 'business':
            features += [
               
                ('Category', ad.category),
                ('Category', ad.category),
                ('Brand', ad.brand),
                ('Condition', ad.condition),
                ('Price', f"OMR {ad.price}"),
                ('Warranty Status', ad.warranty_status),
               
                
            ]
        elif ad_type == 'education':
            features += [
                
                ('Course Type', ad.course_type),
                ('Subject', ad.subject),
                ('Duration', f"{ad.duration} weeks/months"),
                ('Price', f"OMR {ad.price}"),
                ('Instructor Name', ad.instructor_name),
                ('Instructor Qualification', ad.qualification),
                ('Instructor Experience', ad.experience),
                
                
            
               
            ]
        elif ad_type == 'service':
            features += [
                 ('Service Type', ad.service_type),
                ('Provider Name', ad.provider_name),
                ('Price Range', f"OMR {ad.price_range}"),
                ('Contact Info', ad.contact_info),
                
               
            ]

    # Render the template and pass the ad object and features list
    return render(request, 'communitydetails.html', {'ad': ad, 'features': features})


#user
from django.utils.timezone import now
from django.shortcuts import render, get_object_or_404
from .models import JobApplication, CustomUser


@login_required
def jobapplication(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    # Fetch all applications for the user, including other companies
    applications = JobApplication.objects.filter(user=user).select_related('job', 'company')

    # Filter applications by status
    rejected_applications = applications.filter(status='rejected')
    approved_applications = applications.filter(status='approved')  # Example, based on your status choices.
    pending_applications = applications.filter(status='pending')  # Adjust as needed.

    # Categorize applications by deadline
    active_applications = applications.filter(job__application_deadline__gte=now())
    expired_applications = applications.filter(job__application_deadline__lt=now())

    return render(
        request,
        'jobapplications.html',
        {
            'user': user,
            'active_applications': active_applications,
            'expired_applications': expired_applications,
            'rejected_applications': rejected_applications,
            'approved_applications': approved_applications,
            'pending_applications': pending_applications,
            'rejected_count': rejected_applications.count(),  # Count of rejected applications
        }
    )
from django_countries import countries
@login_required
def userprofile(request, user_id):
    if request.user.id != user_id:
        messages.error(request, "You are not authorized to view this profile.")
        return redirect('index')

    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        form = CustomUserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('index')
        else:
            # Log form errors to the terminal
            print("Form Errors:")
            for field, error_list in form.errors.items():
                for error in error_list:
                    print(f"{field}: {error}")
            messages.error(request, "Please correct the errors in the form.")
    else:
        form = CustomUserProfileForm(instance=user)

    return render(request, 'userprofile.html', {'form': form, 'user': user, 'countries': countries})

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Land, Villa, CustomUser  # Import your models

from django.db.models import Q
from django.apps import apps
@login_required
def adss(request, user_id):
    user = request.user  # Assuming you are using the logged-in user

    # Define the model-to-context mapping
    models = [
        'Land', 'Villa', 'Automobile', 'Commercial', 'Farm', 'Chalet',
        'Fashion', 'Toys', 'Food', 'Pet', 'Book', 'Appliance',
        'Fitness', 'Business', 'Education', 'Service', 
        'Mobile', 'Computer', 'Sound','Motorcycle','Boat',
        'HeavyVehicle','AutoAccessoryPart','NumberPlate',
        'DrivingTraining','Apartment','Factory','Complex',
        'Clinic','Hostel','Office','Shop','Cafe','Staff',
        'Warehouse','Townhouse','Fullfloors','Showrooms',
        'Wholebuilding','Supermarket','Foreign'
    ]

    # Get filter criteria from the request (default to 'pending' if not specified)
    status_filter = request.GET.get('status', 'pending')  # e.g., 'pending', 'approved', 'rejected', 'soldout'

    # Initialize context
    context = {'user': user, 'status_filter': status_filter, 'counts': {}, 'aggregated_counts': {}}

    # Initialize aggregated counts
    aggregated_counts = {
        'pending': 0,
        'approved': 0,
        'rejected': 0,
        'soldout': 0,
    }

    # Iterate over the models
    for model_name in models:
        model = apps.get_model(app_label='oman_app', model_name=model_name)
        queryset = model.objects.filter(user=user)

        # Filter the queryset by status if applicable
        if status_filter in ['pending', 'approved', 'rejected', 'soldout']:
            filtered_queryset = queryset.filter(status=status_filter)
        else:
            filtered_queryset = queryset

        # Add the filtered queryset to the context
        context[f'{model_name.lower()}_list'] = filtered_queryset

        # Count products for each status
        counts = {
            'pending': queryset.filter(status='pending').count(),
            'approved': queryset.filter(status='approved').count(),
            'rejected': queryset.filter(status='rejected').count(),
            'soldout': queryset.filter(status='soldout').count(),
        }

        # Add counts to the context under 'counts'
        context['counts'][model_name] = counts

        # Update aggregated counts
        aggregated_counts['pending'] += counts['pending']
        aggregated_counts['approved'] += counts['approved']
        aggregated_counts['rejected'] += counts['rejected']
        aggregated_counts['soldout'] += counts['soldout']

    # Add aggregated counts to the context
    context['aggregated_counts'] = aggregated_counts

    return render(request, 'listingadss1.html', context)

@login_required
def listingadss(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    return render(request, 'listingads.html', {'user': user})
    
from django.contrib.auth import authenticate, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import CustomUser

@login_required
def account_settings(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    # Handle password change request
    if request.method == 'POST':
        # Check if the password change form is submitted
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # Check if the current password is correct
        if user.check_password(current_password):
            if new_password == confirm_password:
                # Set the new password
                user.set_password(new_password)
                user.save()
                # Re-authenticate the user
                update_session_auth_hash(request, user)  # Important to keep the user logged in
                return redirect('account_settings', user_id=user.id)  # Redirect to the same page to show success
            else:
                error_message = "New passwords do not match."
        else:
            error_message = "Current password is incorrect."

        # Show error message if the password change failed
        return render(request, 'account_settings.html', {
            'user': user,
            'error_message': error_message
        })

    return render(request, 'account_settings.html', {'user': user})


def listingads(request):
    return render(request, 'listingads.html') 

# def listingsub(request):
#     return render(request, 'subcategory.html') 

def favorites(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    return render(request, 'favorites.html',{'user': user}) 

#Job
def jobcategories(request):
    jobcat=JobCategory.objects.all()
    return render(request, 'jobcategory.html',{'jobcat':jobcat}) 

def jobcategorylist(request,category_id):
    # Retrieve filter values from GET request
    location = request.GET.get('location', '')
    category = request.GET.get('category', '')
    experience = request.GET.get('experience', '')
    job_type = request.GET.get('job_type', '')
    qualification = request.GET.get('qualification', '')
    gender = request.GET.get('gender', '')
    
    category = get_object_or_404(JobCategory, id=category_id)
    job_posts = JobPost.objects.filter(job_category=category,application_deadline__gte=timezone.now())
    return render(request, 'jobcategorylist.html', {'category': category, 'job_posts': job_posts})
    # Apply filters based on the user input
    jobs = Job.objects.all()

    if location:
        jobs = jobs.filter(location__icontains=location)
    if category:
        jobs = jobs.filter(category__icontains=category)
    if experience:
        jobs = jobs.filter(experience__icontains=experience)
    if job_type:
        jobs = jobs.filter(job_type__icontains=job_type)
    if qualification:
        jobs = jobs.filter(qualification__icontains=qualification)
    if gender:
        jobs = jobs.filter(gender__icontains=gender)
    

    return render(request, 'jobcategorylist.html', {'category': category, 'job_posts': job_posts})

from django.http import JsonResponse
from .models import Company, JobPost

def view_company_posts_ajax(request, company_id):
    # Get the company object
    company = get_object_or_404(Company, id=company_id)
    
    # Retrieve all job posts related to this company
    job_posts = JobPost.objects.filter(company_name=company)
    
    # Prepare a list of job posts to send as JSON
    job_posts_data = []
    for post in job_posts:
        job_posts_data.append({
            'title': post.title,
            'description': post.description,
            'posted_on': post.posted_on.strftime('%d/%m/%Y'),
        })
    
    # Return the data as JSON
    return JsonResponse({'job_posts': job_posts_data})
 

# ADMIN 

from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate,login, logout
from .forms import *
from django.contrib import messages


def admin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_superuser:
                login(request, user)
                return redirect('admin_dashboard')  # Replace with your admin dashboard URL
            else:
                messages.error(request, "Only administrators can log in here.")
                return redirect('admin')  # Reload the admin login page
        else:
            messages.error(request, "Invalid username or password.")  # Incorrect credentials

    return render(request, 'admin1/adminlogin.html')  # Custom admin login template

from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache

from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache


@never_cache
def admin_dashboard(request):
    if request.user.is_authenticated:
        # Fetching the count of pending status for each product category
        land_products_pending_count = Land.objects.filter(status='pending').count()
        villa_products_pending_count = Villa.objects.filter(status='pending').count()
        automobile_products_pending_count = Automobile.objects.filter(status='pending').count()
        commercial_products_pending_count = Commercial.objects.filter(status='pending').count()
        farm_products_pending_count = Farm.objects.filter(status='pending').count()
        apartment_products_pending_count = Apartment.objects.filter(status='pending').count()
        
        factory_products_pending_count = Factory.objects.filter(status='pending').count()
        complexes_products_pending_count = Complex.objects.filter(status='pending').count()
        clinic_products_pending_count = Clinic.objects.filter(status='pending').count()
        hostel_products_pending_count = Hostel.objects.filter(status='pending').count()
        office_products_pending_count = Office.objects.filter(status='pending').count()
        shop_products_pending_count = Shop.objects.filter(status='pending').count()

        cafe_products_pending_count = Cafe.objects.filter(status='pending').count()
        staff_products_pending_count = Staff.objects.filter(status='pending').count()
        warehouse_products_pending_count = Warehouse.objects.filter(status='pending').count()
        townhouse_products_pending_count = Townhouse.objects.filter(status='pending').count()
        fullfloors_products_pending_count = Fullfloors.objects.filter(status='pending').count()
        showrooms_products_pending_count = Showrooms.objects.filter(status='pending').count()
        wholebuilding_products_pending_count = Wholebuilding.objects.filter(status='pending').count()
        supermarket_products_pending_count = Supermarket.objects.filter(status='pending').count()
        foreign_products_pending_count = Foreign.objects.filter(status='pending').count()
        shared_products_pending_count = Shared.objects.filter(status='pending').count()
        suits_products_pending_count = Suits.objects.filter(status='pending').count()



        automobile_products_pending_count = Automobile.objects.filter(status='pending').count()
        motorcycle_products_pending_count = Motorcycle.objects.filter(status='pending').count()
        heavy_vehicle_products_pending_count = HeavyVehicle.objects.filter(status='pending').count()
        boat_products_pending_count = Boat.objects.filter(status='pending').count()
        autoaccessorypart_products_pending_count = AutoAccessoryPart.objects.filter(status='pending').count()
        numberplate_products_pending_count = NumberPlate.objects.filter(status='pending').count()


        fashion_products_pending_count = Fashion.objects.filter(status='pending').count()
        toys_products_pending_count = Toys.objects.filter(status='pending').count()
        food_products_pending_count = Food.objects.filter(status='pending').count()
        fitness_products_pending_count = Fitness.objects.filter(status='pending').count()
        pet_products_pending_count = Pet.objects.filter(status='pending').count()
        book_products_pending_count = Book.objects.filter(status='pending').count()
        appliance_products_pending_count = Appliance.objects.filter(status='pending').count()
        business_products_pending_count = Business.objects.filter(status='pending').count()
        education_products_pending_count = Education.objects.filter(status='pending').count()
        service_products_pending_count = Service.objects.filter(status='pending').count()
        mobile_products_pending_count = Mobile.objects.filter(status='pending').count()
        computer_products_pending_count = Computer.objects.filter(status='pending').count()
        sound_products_pending_count = Sound.objects.filter(status='pending').count()
        job_posts_pending_count = JobPost.objects.filter(status='pending').count()

        # Fetching the product data for each category
        land_products = Land.objects.select_related('user').all()
        villa_products = Villa.objects.select_related('user').all()
        automobile_products = Automobile.objects.select_related('user').all()
        motorcycle_products = Motorcycle.objects.select_related('user').all()
        boat_products = Boat.objects.select_related('user').all()
        heavy_vehicle_products = HeavyVehicle.objects.select_related('user').all()
        accessoriesparts_products = AutoAccessoryPart.objects.select_related('user').all()
        numberplate_products = NumberPlate.objects.select_related('user').all()

        commercial_products = Commercial.objects.select_related('user').all()
        farm_products = Farm.objects.select_related('user').all()
        apartment_products = Apartment.objects.select_related('user').all()

        factory_products = Factory.objects.select_related('user').all()
        complexes_products = Complex.objects.select_related('user').all()
        clinic_products = Clinic.objects.select_related('user').all()
        hostel_products = Hostel.objects.select_related('user').all()
        office_products = Office.objects.select_related('user').all()
        shop_products = Shop.objects.select_related('user').all()

        cafe_products = Cafe.objects.select_related('user').all()
        staff_products = Staff.objects.select_related('user').all()
        warehouse_products = Warehouse.objects.select_related('user').all()
        townhouse_products = Townhouse.objects.select_related('user').all()
        fullfloors_products = Fullfloors.objects.select_related('user').all()
        showrooms_products = Showrooms.objects.select_related('user').all()
        wholebuilding_products = Wholebuilding.objects.select_related('user').all()
        supermarket_products = Supermarket.objects.select_related('user').all()
        foreign_products = Foreign.objects.select_related('user').all()
        shared_products = Shared.objects.select_related('user').all()
        suits_products = Suits.objects.select_related('user').all()

        fashion_products = Fashion.objects.select_related('user').all()
        toys_products = Toys.objects.select_related('user').all()
        food_products = Food.objects.select_related('user').all()
        fitness_products = Fitness.objects.select_related('user').all()
        pet_products = Pet.objects.select_related('user').all()
        book_products = Book.objects.select_related('user').all()
        appliance_products = Appliance.objects.select_related('user').all()
        business_products = Business.objects.select_related('user').all()
        education_products = Education.objects.select_related('user').all()
        service_products = Service.objects.select_related('user').all()
        mobile_products = Mobile.objects.select_related('user').all()
        computer_products = Computer.objects.select_related('user').all()
        sound_products = Sound.objects.select_related('user').all()
        job_posts = JobPost.objects.select_related('user').all()

        # Rendering the template with product data and pending counts
        return render(request, 'admin1/dashboard.html', {
            'land_products': land_products,
            'villa_products': villa_products,
            'automobile_products': automobile_products,
            'motorcycle_products': motorcycle_products,
            'heavy_vehicle_products': heavy_vehicle_products,
            'boat_products': boat_products,
            'accessoriesparts_products':accessoriesparts_products,
            'numberplate_products':numberplate_products,
            'commercial_products': commercial_products,
            'farm_products': farm_products,
            'apartment_products': apartment_products,
            'factory_products':factory_products,
            'complexes_products':complexes_products,
            'clinic_products':clinic_products,
            'hostel_products':hostel_products,
            'office_products':office_products,
            'foreign_products':foreign_products,
            'shared_products':shared_products,
            'suits_products':suits_products,


            'cafe_products':cafe_products,
            'staff_products':staff_products,
            'warehouse_products':warehouse_products,
            'townhouse_products':townhouse_products,
            'fullfloors_products':fullfloors_products,
            'showrooms_products':showrooms_products,
            'wholebuilding_products':wholebuilding_products,
            'supermarket_products':supermarket_products,
            'shop_products':shop_products,



            'fashion_products': fashion_products,
            'toys_products': toys_products,
            'food_products': food_products,
            'fitness_products': fitness_products,
            'pet_products': pet_products,
            'book_products': book_products,
            'appliance_products': appliance_products,
            'business_products': business_products,
            'education_products': education_products,
            'service_products': service_products,
            'mobile_products': mobile_products,
            'computer_products': computer_products,
            'sound_products': sound_products,
            'job_posts': job_posts,

            # Passing the pending counts to the template
            'land_products_pending_count': land_products_pending_count,
            'villa_products_pending_count': villa_products_pending_count,
            'automobile_products_pending_count': automobile_products_pending_count,
            'motorcycle_products_pending_count': motorcycle_products_pending_count,
            'heavy_vehicle_products_pending_count': heavy_vehicle_products_pending_count,
            'boat_products_pending_count': boat_products_pending_count,
            'autoaccessorypart_products_pending_count':autoaccessorypart_products_pending_count,
            'numberplate_products_pending_count':numberplate_products_pending_count,
            'commercial_products_pending_count': commercial_products_pending_count,
            'farm_products_pending_count': farm_products_pending_count,
            'apartment_products_pending_count': apartment_products_pending_count,

            'factory_products_pending_count': factory_products_pending_count,
            'complexes_products_pending_count': complexes_products_pending_count,
            'clinic_products_pending_count': clinic_products_pending_count,
            'hostel_products_pending_count': hostel_products_pending_count,
            'office_products_pending_count': office_products_pending_count,
            'shop_products_pending_count': shop_products_pending_count,

            'cafe_products_pending_count':cafe_products_pending_count,
            'staff_products_pending_count':staff_products_pending_count,
            'warehouse_products_pending_count':warehouse_products_pending_count,
            'townhouse_products_pending_count':townhouse_products_pending_count,
            'fullfloors_products_pending_count':fullfloors_products_pending_count,
            'showrooms_products_pending_count':showrooms_products_pending_count,
            'wholebuilding_products_pending_count':wholebuilding_products_pending_count,
            'supermarket_products_pending_count':supermarket_products_pending_count,
            'foreign_products_pending_count':foreign_products_pending_count,
            'shared_products_pending_count':shared_products_pending_count,
            'suits_products_pending_count':suits_products_pending_count,


            'fashion_products_pending_count': fashion_products_pending_count,
            'toys_products_pending_count': toys_products_pending_count,
            'food_products_pending_count': food_products_pending_count,
            'fitness_products_pending_count': fitness_products_pending_count,
            'pet_products_pending_count': pet_products_pending_count,
            'book_products_pending_count': book_products_pending_count,
            'appliance_products_pending_count': appliance_products_pending_count,
            'business_products_pending_count': business_products_pending_count,
            'education_products_pending_count': education_products_pending_count,
            'service_products_pending_count': service_products_pending_count,
            'mobile_products_pending_count': mobile_products_pending_count,
            'computer_products_pending_count': computer_products_pending_count,
            'sound_products_pending_count': sound_products_pending_count,
            'job_posts_pending_count': job_posts_pending_count,
        })
    return redirect('admin')




@never_cache
def logoutadmin(request):
    if request.user.is_authenticated:
        logout(request)
    # Redirect to a page that ensures users cannot navigate back
    return redirect('admin')

@never_cache
def category(request):
    if request.user.is_authenticated:
        return render(request, 'admin1/category.html')
    return redirect('admin')

@never_cache
def subcategory(request):
    if request.user.is_authenticated:
        return render(request, 'admin1/subcategory.html')
    return redirect('admin')






def custom_login_view1(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if not user.is_staff:  # Ensure only non-admin users log in here
                    login(request, user)
                    return redirect('index')  # Redirect to user dashboard
                else:
                    messages.error(request, "Admins cannot log in from the user login page.")
                    return redirect('login1')  # Redirect to user login page
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = CustomAuthenticationForm()

    return render(request, 'login.html', {'form': form})





# password reset

from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

from django.contrib.auth.forms import PasswordResetForm
from django.shortcuts import render
from django.http import HttpResponse

def password_reset_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        
        # Validate the email and username (you can add more specific checks as needed)
        try:
            user = CustomUser.objects.get(email=email, username=username)
            form = PasswordResetForm(request.POST)
            if form.is_valid():
                form.save(request=request)
                return render(request, 'password_reset_form.html', {'success_message': 'Reset email has been sent.check it'})
        except CustomUser.DoesNotExist:
            return render(request, 'password_reset_form.html', {'error_message': 'Invalid email or username.'})
    
    return render(request, 'password_reset_form.html')

from django.contrib.auth.views import PasswordResetConfirmView
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'
    
    def form_valid(self, form):
        # Check if the passwords match
        new_password = form.cleaned_data.get('new_password1')
        confirm_password = form.cleaned_data.get('new_password2')

        if new_password != confirm_password:
            messages.error(self.request, "Passwords do not match. Please try again.")
            return self.render_to_response(self.get_context_data(form=form))

        # If passwords match, proceed to save the new password
        response = super().form_valid(form)

        # Create the success message with a login link
        login_url = reverse('login')  # Make sure 'login' is the name of your login URL
        messages.success(self.request, f"Your password has been successfully reset. You can now <a href='{login_url}'><strong>login</strong></a>.")

        # Return the response with the success message
        return self.render_to_response(self.get_context_data(form=form))
    
    def form_invalid(self, form):
        # Handle form invalid cases
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)
        
@login_required
def listingsub(request):
    user = request.user
    nearby_locations=NearbyLocation.objects.all()
    main_amenities=MainAmenities.objects.all()
    additional_amenities=AdditionalAmenities.objects.all()
    if request.method == 'POST':
        product_type = request.POST.get('product_type')

        if product_type == 'land':
            form = LandForm(request.POST, request.FILES)
            if form.is_valid():
                land = form.save(commit=False)
                land.user = user
                land.status = 'pending'
                land.save()

                form.save_m2m()

                # Handle image uploads
                for img in request.FILES.getlist('images'):
                    land_image = LandImage(image=img)
                    land_image.save()
                    land.images.add(land_image)

                # Handle video uploads
                videos = request.FILES.getlist('videos')
                for video in videos:
                    land_video = LandVideo(video=video)
                    land_video.save()
                    land.videos.add(land_video)

                messages.success(request, "Land registered successfully!")
                return redirect(adss, user_id=user.id)

        elif product_type == 'villa':
            form = Villaform(request.POST, request.FILES)
            if form.is_valid():
                villa = form.save(commit=False)
                villa.user = user
                villa.status = 'pending'
                villa.save()

                form.save_m2m()

                for img in request.FILES.getlist('images'):
                    villa_image = VillaImage(image=img)
                    villa_image.save()
                    villa.images.add(villa_image)
                
                # Handle video uploads
                for video in request.FILES.getlist('videos'):
                  villa_video = VillaVideo(video=video)
                  villa_video.save()
                  villa.videos.add(villa_video)
                messages.success(request, "Villa registered successfully!")
                return redirect(adss, user_id=user.id)

        elif product_type == 'commercial':
            form = CommercialForm(request.POST, request.FILES)
            if form.is_valid():
                commercial = form.save(commit=False)
                commercial.user = user
                commercial.status = 'pending'
                commercial.save()

                form.save_m2m()

                for img in request.FILES.getlist('images'):
                    commercial_image = ComImage(image=img)
                    commercial_image.save()
                    commercial.images.add(commercial_image)
                for video in request.FILES.getlist('videos'):
                    commercial_video = ComVideo(video=video)
                    commercial_video.save()
                    commercial.videos.add(commercial_video)
                messages.success(request, "Commercial property registered successfully!")
                return redirect(adss, user_id=user.id)

        elif product_type == 'chalet':
            form = ChaletForm(request.POST, request.FILES)
            if form.is_valid():
                chalet = form.save(commit=False)
                chalet.user = user
                chalet.status = 'pending'
                chalet.save()

                form.save_m2m()

                for img in request.FILES.getlist('images'):
                    chalet_image = ChaletImage(image=img)
                    chalet_image.save()
                    chalet.images.add(chalet_image)

                messages.success(request, "Chalet registered successfully!")
                return redirect(adss, user_id=user.id)

        elif product_type == 'farm':
            form = FarmForm(request.POST, request.FILES)
            if form.is_valid():
                farm = form.save(commit=False)
                farm.user = user
                farm.status = 'pending'
                farm.save()

                form.save_m2m()

                for img in request.FILES.getlist('images'):
                    farm_image = FarmImage(image=img)
                    farm_image.save()
                    farm.images.add(farm_image)

                # Handle video uploads
                for video in request.FILES.getlist('videos'):
                   farm_video = FarmVideo(video=video)
                   farm_video.save()
                   farm.videos.add(farm_video)

                messages.success(request, "Farm registered successfully!")
                return redirect(adss, user_id=user.id)
            


        elif product_type == 'apartment':
            form = ApartmentForm(request.POST, request.FILES)
            if form.is_valid():
                apartment = form.save(commit=False)
                apartment.user = user
                apartment.status = 'pending'
                apartment.save()

                form.save_m2m()

                for img in request.FILES.getlist('images'):
                    apartment_image = ApartmentImage(image=img)
                    apartment_image.save()
                    apartment.images.add(apartment_image)

                # Handle video uploads
                for video in request.FILES.getlist('videos'):
                   apartment_video = ApartmentVideo(video=video)
                   apartment_video.save()
                   apartment.videos.add(apartment_video)

                messages.success(request, "apartment registered successfully!")
                return redirect(adss, user_id=user.id)
            
        elif product_type == 'factory':
            form = FactoryForm(request.POST, request.FILES)
            if form.is_valid():
                factory = form.save(commit=False)
                factory.user = user
                factory.status = 'pending'
                factory.save()

                form.save_m2m()

                for img in request.FILES.getlist('images'):
                    factory_image = FactoryImage(image=img)
                    factory_image.save()
                    factory.images.add(factory_image)

                # Handle video uploads
                for video in request.FILES.getlist('videos'):
                   factory_video = FactoryVideo(video=video)
                   factory_video.save()
                   factory.videos.add(factory_video)

                messages.success(request, "factory registered successfully!")
                return redirect(adss, user_id=user.id)
            
        elif product_type == 'complex':
            form = ComplexForm(request.POST, request.FILES)
            if form.is_valid():
                complex = form.save(commit=False)
                complex.user = user
                complex.status = 'pending'
                complex.save()

                form.save_m2m()

                for img in request.FILES.getlist('images'):
                    complex_image = ComplexImage(image=img)
                    complex_image.save()
                    complex.images.add(complex_image)

                # Handle video uploads
                for video in request.FILES.getlist('videos'):
                   complex_video = ComplexVideo(video=video)
                   complex_video.save()
                   complex.videos.add(complex_video)

                messages.success(request, "complex registered successfully!")
                return redirect(adss, user_id=user.id)
            
        elif product_type == 'clinic':
            form = ClinicForm(request.POST, request.FILES)
            if form.is_valid():
                clinic = form.save(commit=False)
                clinic.user = user
                clinic.status = 'pending'
                clinic.save()

                form.save_m2m()

                for img in request.FILES.getlist('images'):
                    clinic_image = ClinicImage(image=img)
                    clinic_image.save()
                    clinic.images.add(clinic_image)

                # Handle video uploads
                for video in request.FILES.getlist('videos'):
                   clinic_video = ClinicVideo(video=video)
                   clinic_video.save()
                   clinic.videos.add(clinic_video)

                messages.success(request, "clinic registered successfully!")
                return redirect(adss, user_id=user.id)
            
        elif product_type == 'hostel':
            form = HostelForm(request.POST, request.FILES)
            if form.is_valid():
                hostel = form.save(commit=False)
                hostel.user = user
                hostel.status = 'pending'
                hostel.save()

                form.save_m2m()

                for img in request.FILES.getlist('images'):
                    hostel_image = HostelImage(image=img)
                    hostel_image.save()
                    hostel.images.add(hostel_image)

                # Handle video uploads
                for video in request.FILES.getlist('videos'):
                   hostel_video = HostelVideo(video=video)
                   hostel_video.save()
                   hostel.videos.add(hostel_video)

                messages.success(request, "hostel registered successfully!")
                return redirect(adss, user_id=user.id)
            
        elif product_type == 'office':
            form = OfficeForm(request.POST, request.FILES)
            if form.is_valid():
                office = form.save(commit=False)
                office.user = user
                office.status = 'pending'
                office.save()

                form.save_m2m()

                for img in request.FILES.getlist('images'):
                    office_image = OfficeImage(image=img)
                    office_image.save()
                    office.images.add(office_image)

                # Handle video uploads
                for video in request.FILES.getlist('videos'):
                   office_video = OfficeVideo(video=video)
                   office_video.save()
                   office.videos.add(office_video)

                messages.success(request, "office registered successfully!")
                return redirect(adss, user_id=user.id)
        
        elif product_type == 'shop':
            form = ShopForm(request.POST, request.FILES)
            if form.is_valid():
                shop = form.save(commit=False)
                shop.user = user
                shop.status = 'pending'
                shop.save()

                form.save_m2m()

                for img in request.FILES.getlist('images'):
                    shop_image = ShopImage(image=img)
                    shop_image.save()
                    shop.images.add(shop_image)

                # Handle video uploads
                for video in request.FILES.getlist('videos'):
                   shop_video = ShopVideo(video=video)
                   shop_video.save()
                   shop.videos.add(shop_video)

                messages.success(request, "shop registered successfully!")
                return redirect(adss, user_id=user.id)
            
        elif product_type == 'cafe':
            form = CafeForm(request.POST, request.FILES)
            if form.is_valid():
                cafe = form.save(commit=False)
                cafe.user = user
                cafe.status = 'pending'
                cafe.save()
                form.save_m2m()


                for img in request.FILES.getlist('images'):
                    cafe_image = CafeImage(image=img)
                    cafe_image.save()
                    cafe.images.add(cafe_image)

                # Handle video uploads
                for video in request.FILES.getlist('videos'):
                   cafe_video = CafeVideo(video=video)
                   cafe_video.save()
                   cafe.videos.add(cafe_video)

                messages.success(request, "cafe registered successfully!")
                return redirect(adss, user_id=user.id)
            
        elif product_type == 'staff':
            form = StaffForm(request.POST, request.FILES)
            if form.is_valid():
                staff = form.save(commit=False)
                staff.user = user
                staff.status = 'pending'
                staff.save()

                form.save_m2m()

                for img in request.FILES.getlist('images'):
                    staff_image = StaffImage(image=img)
                    staff_image.save()
                    staff.images.add(staff_image)

                # Handle video uploads
                for video in request.FILES.getlist('videos'):
                   staff_video = StaffVideo(video=video)
                   staff_video.save()
                   staff.videos.add(staff_video)

                messages.success(request, "staff registered successfully!")
                return redirect(adss, user_id=user.id)
        
        elif product_type == 'warehouse':
            form = WarehouseForm(request.POST, request.FILES)
            if form.is_valid():
                warehouse = form.save(commit=False)
                warehouse.user = user
                warehouse.status = 'pending'
                warehouse.save()

                form.save_m2m()

                for img in request.FILES.getlist('images'):
                    warehouse_image = WarehouseImage(image=img)
                    warehouse_image.save()
                    warehouse.images.add(warehouse_image)

                # Handle video uploads
                for video in request.FILES.getlist('videos'):
                   warehouse_video = WarehouseVideo(video=video)
                   warehouse_video.save()
                   warehouse.videos.add(warehouse_video)

                messages.success(request, "warehouse registered successfully!")
                return redirect(adss, user_id=user.id)
            
        elif product_type == 'townhouse':
            form = Townhouseform(request.POST, request.FILES)
            if form.is_valid():
                townhouse = form.save(commit=False)
                townhouse.user = user
                townhouse.status = 'pending'
                townhouse.save()

                form.save_m2m()

                for img in request.FILES.getlist('images'):
                    townhouse_image = TownhouseImage(image=img)
                    townhouse_image.save()
                    townhouse.images.add(townhouse_image)

                # Handle video uploads
                for video in request.FILES.getlist('videos'):
                   townhouse_video = TownhouseVideo(video=video)
                   townhouse_video.save()
                   townhouse.videos.add(townhouse_video)

                messages.success(request, "townhouse registered successfully!")
                return redirect(adss, user_id=user.id)
            
        elif product_type == 'fullfloors':
            form = Fullfloorsform(request.POST, request.FILES)
            if form.is_valid():
                fullfloors = form.save(commit=False)
                fullfloors.user = user
                fullfloors.status = 'pending'
                fullfloors.save()

                form.save_m2m()

                for img in request.FILES.getlist('images'):
                    fullfloors_image = FullfloorsImage(image=img)
                    fullfloors_image.save()
                    fullfloors.images.add(fullfloors_image)

                # Handle video uploads
                for video in request.FILES.getlist('videos'):
                   fullfloors_video = FullfloorsVideo(video=video)
                   fullfloors_video.save()
                   fullfloors.videos.add(fullfloors_video)

                messages.success(request, "fullfloors registered successfully!")
                return redirect(adss, user_id=user.id)
            
        elif product_type == 'showrooms':
            form = Showroomsform(request.POST, request.FILES)
            if form.is_valid():
                showrooms = form.save(commit=False)
                showrooms.user = user
                showrooms.status = 'pending'
                showrooms.save()

                form.save_m2m()

                for img in request.FILES.getlist('images'):
                    showrooms_image = ShowroomsImage(image=img)
                    showrooms_image.save()
                    showrooms.images.add(showrooms_image)

                # Handle video uploads
                for video in request.FILES.getlist('videos'):
                   showrooms_video = ShowroomsVideo(video=video)
                   showrooms_video.save()
                   showrooms.videos.add(showrooms_video)

                messages.success(request, "showrooms registered successfully!")
                return redirect(adss, user_id=user.id)
            
        elif product_type == 'wholebuilding':
            form = Wholebuildingform(request.POST, request.FILES)
            if form.is_valid():
                wholebuilding = form.save(commit=False)
                wholebuilding.user = user
                wholebuilding.status = 'pending'
                wholebuilding.save()

                form.save_m2m()

                for img in request.FILES.getlist('images'):
                    wholebuilding_image = WholebuildingImage(image=img)
                    wholebuilding_image.save()
                    wholebuilding.images.add(wholebuilding_image)

                # Handle video uploads
                for video in request.FILES.getlist('videos'):
                   wholebuilding_video = WholebuildingVideo(video=video)
                   wholebuilding_video.save()
                   wholebuilding.videos.add(wholebuilding_video)

                messages.success(request, "wholebuilding registered successfully!")
                return redirect(adss, user_id=user.id)
            
        elif product_type == 'supermarket':
            form = Supermarketform(request.POST, request.FILES)
            if form.is_valid():
                supermarket = form.save(commit=False)
                supermarket.user = user
                supermarket.status = 'pending'
                supermarket.save()

                form.save_m2m()

                for img in request.FILES.getlist('images'):
                    supermarket_image = SupermarketImage(image=img)
                    supermarket_image.save()
                    supermarket.images.add(supermarket_image)

                # Handle video uploads
                for video in request.FILES.getlist('videos'):
                   supermarket_video = SupermarketVideo(video=video)
                   supermarket_video.save()
                   supermarket.videos.add(supermarket_video)

                messages.success(request, "supermarket registered successfully!")
                return redirect(adss, user_id=user.id)
        elif product_type == 'foreign':
            form = Foreignform(request.POST, request.FILES)
            if form.is_valid():
                foreign = form.save(commit=False)
                foreign.user = user
                foreign.status = 'pending'
                foreign.save()

                form.save_m2m()

                for img in request.FILES.getlist('images'):
                    foreign_image = ForeignImage(image=img)
                    foreign_image.save()
                    foreign.images.add(foreign_image)

                # Handle video uploads
                for video in request.FILES.getlist('videos'):
                   foreign_video = ForeignVideo(video=video)
                   foreign_video.save()
                   foreign.videos.add(foreign_video)

                messages.success(request, "foreign registered successfully!")
                return redirect(adss, user_id=user.id)
            
        elif product_type == 'shared':
            form = Sharedform(request.POST, request.FILES)
            if form.is_valid():
                shared = form.save(commit=False)
                shared.user = user
                shared.status = 'pending'
                shared.save()

                form.save_m2m()

                for img in request.FILES.getlist('images'):
                    shared_image = SharedImage(image=img)
                    shared_image.save()
                    shared.images.add(shared_image)

                # Handle video uploads
                for video in request.FILES.getlist('videos'):
                   shared_video = SharedVideo(video=video)
                   shared_video.save()
                   shared.videos.add(shared_video)

                messages.success(request, "shared registered successfully!")
                return redirect(adss, user_id=user.id)
                
        elif product_type == 'suits':
            form = Suitsform(request.POST, request.FILES)
            if form.is_valid():
                suits = form.save(commit=False)
                suits.user = user
                suits.status = 'pending'
                suits.save()

                form.save_m2m()

                for img in request.FILES.getlist('images'):
                    suits_image = SuitsImage(image=img)
                    suits_image.save()
                    suits.images.add(suits_image)

                # Handle video uploads
                for video in request.FILES.getlist('videos'):
                   suits_video = SuitsVideo(video=video)
                   suits_video.save()
                   suits.videos.add(suits_video)

                messages.success(request, "suits registered successfully!")
                return redirect(adss, user_id=user.id)
    
    land_form = LandForm()
    villa_form = Villaform()
    commercial_form = CommercialForm()
    chalet_form = ChaletForm()
    farm_form = FarmForm()
    factory_form = FactoryForm()
    apartment_form = ApartmentForm()
    complex_form = ComplexForm()
    clinic_form = ClinicForm()
    hostel_form = HostelForm()
    office_form = OfficeForm()
    shop_form = ShopForm()
    cafe_form = CafeForm()
    staff_form = StaffForm()
    warehouse_form = WarehouseForm()
    townhouse_form = Townhouseform()
    fullfloors_form = Fullfloorsform()
    showrooms_form = Showroomsform()
    wholebuilding_form = Wholebuilding()
    supermarket_form = Supermarket()
    foreign_form= Foreignform()
    shared_form = Sharedform()
    suits_form = Suitsform()

    return render(request, 'subcategory.html', {
        'land_form': land_form,
        'villa_form': villa_form,
        'commercial_form': commercial_form,
        'chalet_form': chalet_form,
        'farm_form': farm_form,
        'apartment_form' : apartment_form,
        'factory_form': factory_form,
        'complex_form': complex_form,
        'clinic_form': clinic_form,
        'hostel_form' : hostel_form,
        'office_form': office_form,
        'shop_form': shop_form,
        'cafe_form': cafe_form,
        'staff_form': staff_form,
        'warehouse_form': warehouse_form,
        'townhouse_form': townhouse_form,
        'fullfloors_form' : fullfloors_form,
        'showrooms_form': showrooms_form,
        'wholebuilding_form' : wholebuilding_form,
        'supermarket_form' : supermarket_form,
        'foreign_form' : foreign_form,
        'additional_amenities':additional_amenities,
        'main_amenities':main_amenities,
        'nearby_locations':nearby_locations,
       'countries': list(countries),
       'shared_form': shared_form,
       'suits_form': suits_form,

    })

@login_required
def listingsub1(request):
    user = request.user
    regions=Region.objects.all()
    if request.method == 'POST':
        product_type = request.POST.get('product_type')

        if product_type == 'automobile':
            form = CarForm(request.POST, request.FILES)
            if form.is_valid():
                automobile = form.save(commit=False)
                automobile.user = user
                automobile.status = 'pending'
                automobile.save()

                # Handle image uploads
                for img in request.FILES.getlist('images'):
                    automobile_image = AutomobileImage(image=img)
                    automobile_image.save()
                    automobile.images.add(automobile_image)

                # Handle video uploads
                videos = request.FILES.getlist('videos')
                for video in videos:
                    automobile_video = AutomobileVideo(video=video)
                    automobile_video.save()
                    automobile.videos.add(automobile_video)


                messages.success(request, "Automobile registered successfully!")
                return redirect(adss, user_id=user.id)

        elif product_type == 'motorcycle':
            form = BikeForm(request.POST, request.FILES)
            if form.is_valid():
                motorcycle = form.save(commit=False)
                motorcycle.user = user
                motorcycle.status = 'pending'
                motorcycle.save()

                # Handle image uploads
                for img in request.FILES.getlist('images'):
                    motorcycle_image = MotorcycleImage(image=img)
                    motorcycle_image.save()
                    motorcycle.images.add(motorcycle_image)

                # Handle video uploads
                videos = request.FILES.getlist('videos')
                for video in videos:
                    motorcycle_video = MotorcycleVideo(video=video)
                    motorcycle_video.save()
                    motorcycle.videos.add(motorcycle_video)

                motorcycle.save()  # Save motorcycle after adding media

                messages.success(request, "Motorcycle registered successfully!")
                return redirect(adss, user_id=user.id)

        elif product_type == 'accessory':
            form = AccessoryForm(request.POST, request.FILES)
            if form.is_valid():
                accessory = form.save(commit=False)
                accessory.user = user
                accessory.status = 'pending'
                accessory.save()

                # Handle image uploads
                for img in request.FILES.getlist('images'):
                    accessory_image = AutoAccessoryPartImage(image=img)
                    accessory_image.save()
                    accessory.images.add(accessory_image)

                # Handle video uploads
                videos = request.FILES.getlist('videos')
                for video in videos:
                    accessory_video = AutoAccessoryPartVideo(video=video)
                    accessory_video.save()
                    accessory.videos.add(accessory_video)

                accessory.save()  # Save motorcycle after adding media


                messages.success(request, "Accessory registered successfully!")
                return redirect(adss, user_id=user.id)

        elif product_type == 'heavy_vehicle':
            form = HeavyVehicleForm(request.POST, request.FILES)
            if form.is_valid():
                heavy_vehicle = form.save(commit=False)
                heavy_vehicle.user = user
                heavy_vehicle.status = 'pending'
                heavy_vehicle.save()

                # Handle image uploads
                for img in request.FILES.getlist('images'):
                    heavy_vehicle_image = HeavyVehicleImage(image=img)
                    heavy_vehicle_image.save()
                    heavy_vehicle.images.add(heavy_vehicle_image)

                # Handle video uploads
                videos = request.FILES.getlist('videos')
                for video in videos:
                    heavy_vehicle_video = HeavyVehicleVideo(video=video)
                    heavy_vehicle_video.save()
                    heavy_vehicle.videos.add(heavy_vehicle_video)

                heavy_vehicle.save()  # Save heavy vehicle after adding media

                messages.success(request, "Heavy Vehicle registered successfully!")
                return redirect(adss, user_id=user.id)

        elif product_type == 'boat':
            form = BoatForm(request.POST, request.FILES)
            if form.is_valid():
                boat = form.save(commit=False)
                boat.user = user
                boat.status = 'pending'
                boat.save()

                # Handle image uploads
                for img in request.FILES.getlist('images'):
                    boat_image = BoatImage(image=img)
                    boat_image.save()
                    boat.images.add(boat_image)

                # Handle video uploads
                videos = request.FILES.getlist('videos')
                for video in videos:
                    boat_video = BoatVideo(video=video)
                    boat_video.save()
                    boat.videos.add(boat_video)


                boat.save()  # Save boat after adding media

                messages.success(request, "Boat registered successfully!")
                return redirect(adss, user_id=user.id)
            
        elif product_type == 'heavy_vehicle':
            form = HeavyVehicleForm(request.POST, request.FILES)
            if form.is_valid():
                part = form.save(commit=False)
                part.user = user
                part.status = 'pending'
                part.save()

                # Handle image uploads
                for img in request.FILES.getlist('images'):
                    part_image = PartImage(image=img)
                    part_image.save()
                    part.images.add(part_image)

                # Handle video uploads
                videos = request.FILES.getlist('videos')
                for video in videos:
                    part_video = PartVideo(video=video)
                    part_video.save()
                    part.videos.add(part_video)

                part.save()  # Save heavy vehicle after adding media

                messages.success(request, "Heavy Vehicle registered successfully!")
                return redirect(adss, user_id=user.id)
            

        elif product_type == 'sports_car':
            form = SportsCarForm(request.POST, request.FILES)
            if form.is_valid():
                sportscar = form.save(commit=False)
                sportscar.user = request.user
                sportscar.status = 'pending'
                sportscar.save()

                for img in request.FILES.getlist('images'):
                    car_image = SportsCarImage(image=img)
                    car_image.save()
                    sportscar.images.add(car_image)

                for video in request.FILES.getlist('videos'):
                    car_video = SportsCarVideo(video=video)
                    car_video.save()
                    sportscar.videos.add(car_video)

                    messages.success(request, "Sports car registered successfully!")
                    return redirect(adss, user_id=request.user.id)

        elif product_type == 'number_plate':
            form = NumberPlateForm(request.POST, request.FILES)
            if form.is_valid():
                number_plate = form.save(commit=False)
                number_plate.user = user
                number_plate.status = 'pending'
                number_plate.save()

                number_plate.save()  # Save boat after adding media

                messages.success(request, "Number Plate registered successfully!")
                return redirect(adss, user_id=user.id)
            
        

    automobile_form = CarForm()
    motorcycle_form = BikeForm()
    accessory_form = AccessoryForm()
    heavy_vehicle_form = HeavyVehicleForm()
    boat_form = BoatForm()
    number_plate_form = NumberPlateForm()
    part_form = PartForm()
    sportscar_form = SportsCarForm()
   

    return render(request, 'motors.html', {
        'automobile_form': automobile_form,
        'motorcycle_form': motorcycle_form,
        'accessory_form': accessory_form,
        'heavy_vehicle_form': heavy_vehicle_form,
        'boat_form': boat_form,
        'number_plate_form': number_plate_form,
        'regions':regions,
        'part_form': part_form,
        'sportscar_form': sportscar_form,
        
    })


  
from django.shortcuts import get_object_or_404, render
from .models import (Land, Villa, Automobile, Commercial, Farm, Chalet, Fitness, Pet, 
                     Book, Appliance, Fashion, Toys, Food, Business, Education, Service, 
                     Mobile, Computer, Sound, NumberPlate, Motorcycle, Boat, HeavyVehicle, AutoAccessoryPart)

def product_detail(request, product_type, product_id):
    model_map = {
        'land': Land,
        'villa': Villa,
        'automobile': Automobile,
        'motorcycle': Motorcycle,
        'boat': Boat,
        'heavyvehicle': HeavyVehicle,
        'autoaccessorypart': AutoAccessoryPart,
        'numberplate': NumberPlate,
        'commercial': Commercial,
        'farm': Farm,
        'apartment': Apartment,
        'factory': Factory,
        'complexes': Complex,
        'clinic': Clinic,
        'hostel': Hostel,
        'office': Office,
        'shop': Shop,

         'cafe': Cafe,
            'warehouse': Warehouse,
            'staff': Staff,
            'townhouse': Townhouse,
            'fullfloors': Fullfloors,
            'showrooms': Showrooms,
            'wholebuilding': Wholebuilding,
            'supermarket': Supermarket,
            'foreign': Foreign,
            'shared' : Shared,
            'suits' : Suits,

        'fitness': Fitness,
        'pet': Pet,
        'book': Book,
        'appliance': Appliance,
        'fashion': Fashion,
        'toy': Toys,
        'food': Food,
        'business': Business,
        'education': Education,
        'service': Service,
        'mobile': Mobile,
        'computer': Computer,
        'sound': Sound,
    }

    model = model_map.get(product_type)
    
    if not model:
        return render(request, '404.html', status=404)

    product = get_object_or_404(model, id=product_id)

    # Check if the product has an 'images' field before accessing it
    images = product.images.all() if hasattr(product, 'images') else None

    context = {
        'product_type': product_type,
        'product': product,
        'images': images  # Only include images if they exist
    }
    
    return render(request, 'product_detail.html', context)

def delete_product(request, product_type, product_id):
    if request.method == 'POST':  # Only allow POST requests for deletion
        model_map = {
            'land': Land,
            'villa': Villa,
            'automobile': Automobile,
            'motorcycle':Motorcycle,
            'autoaccessorypart':AutoAccessoryPart,
            'boat':Boat,
            'numberplate':NumberPlate,
            'heavyvehicle':HeavyVehicle,
            'commercial': Commercial,
            'farm': Farm,
           'apartment': Apartment,
        'factory': Factory,
        'complexes': Complex,
        'clinic': Clinic,
        'hostel': Hostel,
        'office': Office,
        'shop': Shop,
         'cafe': Cafe,
            'warehouse': Warehouse,
            'staff': Staff,
            'townhouse': Townhouse,
            'fullfloors': Fullfloors,
            'showrooms': Showrooms,
            'wholebuilding': Wholebuilding,
            'supermarket': Supermarket,
            'foreign': Foreign,
            'fitness':Fitness,
            'pet':Pet,
            'book':Book,
            'appliance':Appliance,
            'fashion':Fashion,
            'toy':Toys,
            'food':Food,
            'business':Business,
            'education':Education,
            'service':Service,
            'mobile':Mobile,
            'computer':Computer,
            'sound':Sound,
            'training':DrivingTraining
        }

        model = model_map.get(product_type)
        if not model:
            return render(request, '404.html', status=404)

        product = get_object_or_404(model, id=product_id)
        product.delete()
        messages.success(request, f'{product_type.capitalize()} with ID {product_id} has been deleted successfully.')
        return redirect(adss, user_id=request.user.id)  # Redirect to the list view

    return render(request, '404.html', status=404)

def property_detail_view(request, property_type, pk):
    # Determine the model based on property_type
    if property_type == 'land':
        product = get_object_or_404(Land, id=pk)
    elif property_type == 'villa':
        product = get_object_or_404(Villa, id=pk)
    elif property_type == 'commercial':
        product = get_object_or_404(Commercial, id=pk)
    elif property_type == 'farm':
        product = get_object_or_404(Farm, id=pk)
    elif property_type == 'apartment':
        product = get_object_or_404(Apartment, id=pk)

    elif property_type == 'factory':
        product = get_object_or_404(Factory, id=pk)
    elif property_type == 'complexes':
        product = get_object_or_404(Complex, id=pk)
    elif property_type == 'clinic':
        product = get_object_or_404(Clinic, id=pk)
    elif property_type == 'hostel':
        product = get_object_or_404(Hostel, id=pk)
    elif property_type == 'office':
        product = get_object_or_404(Office, id=pk)
    elif property_type == 'shop':
        product = get_object_or_404(Shop, id=pk)

    elif property_type == 'cafe':
        product = get_object_or_404(Cafe, id=pk)

    elif property_type == 'staff':
        product = get_object_or_404(Staff, id=pk)
    elif property_type == 'warehouse':
        product = get_object_or_404(Warehouse, id=pk)
    elif property_type == 'townhouse':
        product = get_object_or_404(Townhouse, id=pk)
    elif property_type == 'fullfloors':
        product = get_object_or_404(Fullfloors, id=pk)
    elif property_type == 'showrooms':
        product = get_object_or_404(Showrooms, id=pk)
    elif property_type == 'wholebuilding':
        product = get_object_or_404(Wholebuilding, id=pk)
    elif property_type == 'supermarket':
        product = get_object_or_404(Supermarket, id=pk)
    elif property_type == 'foreign':
        product = get_object_or_404(Foreign, id=pk)
    elif property_type == 'shared':
        product = get_object_or_404(Shared, id=pk)
    elif property_type == 'suits':
        product = get_object_or_404(Suits, id=pk)

    elif property_type == 'automobile':
        product = get_object_or_404(Automobile, id=pk)
    elif property_type == 'motorcycle':
        product = get_object_or_404(Motorcycle, id=pk)
    elif property_type == 'heavyvehicle':
        product = get_object_or_404(HeavyVehicle, id=pk)
    elif property_type == 'accessoriesparts':
        product = get_object_or_404(AutoAccessoryPart, id=pk)
    elif property_type == 'numberplate':
        product = get_object_or_404(NumberPlate, id=pk)
    elif property_type == 'boat':
        product = get_object_or_404(Boat, id=pk)
    elif property_type == 'fashion':
        product = get_object_or_404(Fashion, id=pk)
    elif property_type == 'toys':
        product = get_object_or_404(Toys, id=pk)
    elif property_type == 'food':
        product = get_object_or_404(Food, id=pk)
    elif property_type == 'fitness':
        product = get_object_or_404(Fitness, id=pk)

    elif property_type == 'pet':
        product = get_object_or_404(Pet, id=pk)
    elif property_type == 'book':
        product = get_object_or_404(Book, id=pk)
    elif property_type == 'appliance':
        product = get_object_or_404(Appliance, id=pk)
    elif property_type == 'business':
        product = get_object_or_404(Business, id=pk)
    elif property_type == 'education':
        product = get_object_or_404(Education, id=pk)
    elif property_type == 'service':
        product = get_object_or_404(Service, id=pk)

    elif property_type == 'mobile':
        product = get_object_or_404(Mobile, id=pk)
    elif property_type == 'computer':
        product = get_object_or_404(Computer, id=pk)
    elif property_type == 'sound':
        product = get_object_or_404(Sound, id=pk)
    elif property_type == 'training':
        product = get_object_or_404(DrivingTraining, id=pk)
    
    else:
        messages.error(request, "Invalid property type.")
        return redirect('product_dashboard')  # Adjust redirect as needed

    if request.method == 'POST':
        # Get the status from the POST data
        status = request.POST.get('status')

        # If status is valid (either 'approved' or 'rejected'), update the product status
        if status in ['approved', 'rejected']:
            product.status = status
            product.save()
            messages.success(request, f"The {property_type} status has been updated to {status}.")
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Invalid status selected.")

    # Render the appropriate template based on property_type
    template_name = f'admin1/property_detail.html'
    return render(request, template_name, {'product': product,'product_type':property_type})
    

def automobile_detail_view(request, pk):
    product = get_object_or_404(Automobile, id=pk)

    if request.method == 'POST':
        # Get the status from the POST data
        status = request.POST.get('status')
        
        # If status is valid (either 'approved' or 'rejected'), update the product status
        if status in ['approved', 'rejected']:
            product.status = status
            product.save()
            messages.success(request, f"The automobile status has been updated to {status}.")
        else:
            messages.error(request, "Invalid status selected.")

    return render(request, 'admin1/property_detail.html', {'product': product})

def product_dashboard(request):
    # Fetch the query parameter for status
    status = request.GET.get('status', None)

    # Define filters for status, or fetch all if no status provided
    if status == 'approved_or_rejected_or_soldout':
        filter_args = {'status__in': ['approved', 'rejected', 'soldout']}
    elif status:
        filter_args = {'status': status}
    else:
        filter_args = {}

    # List of models to fetch data from
    models = [
        ('lands', Land),
        ('villas', Villa),
        ('automobiles', Automobile), 
         ('boat', Boat),
          ('heavy_vehicle', HeavyVehicle),
           ('motorcycle', Motorcycle),
            ('accessories', AutoAccessoryPart),
             ('numberplate', NumberPlate),
             # Automobiles is handled separately
        ('commercials', Commercial),
        ('farms', Farm),
        ('apartment', Apartment),
        ('factory', Factory),
        ('complexes', Complex),
        ('clinic', Clinic),
        ('hostel', Hostel),
        ('office', Office),
        ('shop', Shop),

        ('cafe', Cafe),
        ('staff', Staff),
        ('warehouse', Warehouse),
        ('townhouse', Townhouse),
        ('fullfloors', Fullfloors),
        ('showrooms', Showrooms),
        ('wholebuilding', Wholebuilding),
        ('supermarket', Supermarket),
        ('foreign', Foreign),
        ('shared' , Shared),
        ('suits' , Suits),


        ('fashions', Fashion),
        ('toys', Toys),
        ('foods', Food),
        ('fitness', Fitness),
        ('pets', Pet),
        ('books', Book),
        ('appliances', Appliance),
        ('businesses', Business),
        ('education', Education),
        ('services', Service),
        ('mobile', Mobile),
        ('computer', Computer),
        ('sound', Sound)
    ]

    # Dynamically build context
    context = {'status': status}

    # Initialize counters for each status group
    approved_count = 0
    rejected_count = 0
    soldout_count = 0
    
    # Initialize category counters
    properties_count = 0
    classified_count = 0
    electronics_count = 0
    services_count = 0
    automobiles_count = 0 
    
     # Add a separate count for automobiles
    
    for key, model in models:
        # Get the queryset based on the filter args
        queryset = model.objects.filter(**filter_args)
        context[key] = queryset
        
        # Count the number of approved, rejected, and soldout items for each model
        approved = queryset.filter(status='approved').count()
        rejected = queryset.filter(status='rejected').count()
        soldout = queryset.filter(status='soldout').count()

        # Store individual counts in context
        context[f'{key}_approved'] = approved
        context[f'{key}_rejected'] = rejected
        context[f'{key}_soldout'] = soldout

        # Add to the totals
        approved_count += approved
        rejected_count += rejected
        soldout_count += soldout

        # Update category counts
        if key in ['lands', 'villas', 'commercials', 'farms', 'apartment','complexes','factory','complexes','suits','clinic','hostel','office','shop','cafe','staff','warehouse','shared','townhouse','fullfloors','showrooms','wholebuilding','supermarket','foreign']:
            properties_count += queryset.count()
        elif key in ['fashions', 'toys', 'foods', 'fitness', 'pets', 'books', 'appliances']:
            classified_count += queryset.count()  # Appliances are classified
        elif key in ['automobiles', 'boat', 'heavy_vehicle', 'motorcycle','accessories','numberplate']:  # Automobiles and related subcategories
            automobiles_count += queryset.count()
            
        elif key in ['mobile', 'computer', 'sound']:
            electronics_count += queryset.count()
        elif key in ['businesses', 'education', 'services']:
            services_count += queryset.count()

    
    # Add total counts to context
    context['approved_count'] = approved_count
    context['rejected_count'] = rejected_count
    context['soldout_count'] = soldout_count
    context['properties_count'] = properties_count
    context['classified_count'] = classified_count
    context['electronics_count'] = electronics_count
    context['services_count'] = services_count
    context['automobiles_count'] = automobiles_count
    


    # Render the template with the context
    return render(request, 'admin1/product_dashboard.html', context)

from django.http import JsonResponse
from .models import Land, Villa, Automobile, Commercial, Farm, Chalet  # Ensure correct models are imported

from django.http import JsonResponse
from .models import Land, Villa, Automobile, Commercial, Farm, Chalet  # Ensure correct models are imported

from django.http import JsonResponse
from .models import Land, Villa, Automobile, Commercial, Farm, Chalet  # Ensure correct models are imported

def get_product_details(request, product_type, product_id):
    if product_type == 'land':
        land = Land.objects.get(id=product_id)
        images = [{'url': image.image.url} for image in land.images.all()]
        videos = [{'url': video.video.url} for video in land.videos.all()]
        
        data = {
            'property_title': land.property_title,
            'price': land.price,
            'plot_area': land.plot_area,
            'description': land.description,
            'regions': land.get_region_display(),  # Use get_region_display for readability
            'cities': land.cities,
            'latitude': land.latitude,
            'longitude': land.longitude,
            'status': land.get_status_display(),
            'listing_type': land.get_listing_type_display(),
            'rental_period': land.get_rental_period_display() if land.rental_period else None,  # Handle rental period
            'lister_type': land.get_lister_type_display(),
            'property_mortgage': land.get_property_mortgage_display(),
            'facade': land.get_facade_display(),
            'zoned_for': land.get_zoned_for_display(),
            'nearby_locations': [location.name for location in land.nearby_location.all()],  # Assuming `NearbyLocation` has a `name` field
            'images': images,
            'videos': videos,
        }

        return JsonResponse(data)  # Assuming you want to return this as a JSON response
    
    elif product_type == 'villa':
        villa = Villa.objects.get(id=product_id)
        images = [{'url': image.image.url} for image in villa.images.all()]
        videos = [{'url': video.video.url} for video in villa.videos.all()]
        
        data = {
            'property_title': villa.property_title,
            'price': villa.price,
            'plot_area': villa.plot_area,
            'surface_area': villa.surface_area,  # Added surface area
            'bedrooms': villa.get_bedrooms_display(),  # Use get_FOO_display() for choice fields
            'bathrooms': villa.get_bathrooms_display(),
            'description': villa.description,
            'regions': villa.get_region_display(),  # Ensuring the display value is used
            'cities': villa.cities,
            'latitude': villa.latitude,
            'longitude': villa.longitude,
            'listing_type': villa.get_listing_type_display(),
            'rental_period': villa.get_rental_period_display() if villa.rental_period else None,  
            'status': villa.get_status_display(),
            'furnished': villa.get_furnished_display(),
            'building': villa.get_building_display(),
            'floors': villa.get_floors_display(),
            'lister_type': villa.get_lister_type_display(),
            'property_mortgage': villa.get_property_mortgage_display(),
            'facade': villa.get_facade_display(),
            'created_at': villa.created_at.strftime('%Y-%m-%d %H:%M:%S'),  # Formatting datetime
            'main_amenities': [amenity.name for amenity in villa.main_amenities.all()],  # Fetching amenities
            'additional_amenities': [amenity.name for amenity in villa.additional_amenities.all()],
            'nearby_locations': [location.name for location in villa.nearby_location.all()],
            'images': images,
            'videos': videos,
        }

    elif product_type == 'automobile':
        automobile = Automobile.objects.get(id=product_id)
        images = [{'url': image.image.url} for image in automobile.images.all()]
        videos = [{'url': video.video.url} for video in automobile.videos.all()]
        data = {
           'name':automobile.name,
           'make': automobile.make,
           'price': automobile.price,
           'year': automobile.year,
           'body_type': automobile.body_type,
           'description': automobile.description,
           'fuel_type': automobile.get_fuel_type_display(),
           'engine_capacity': automobile.engine_capacity,
           'transmission': automobile.get_transmission_display(),
           'exterior_color': automobile.exterior_color,
           'warranty_status': automobile.get_warranty_status_display(),
           'condition': automobile.get_condition_display(),
           'status': automobile.get_status_display(),
           'regions': automobile.regions,
           'cities': automobile.cities,
           'latitude': automobile.latitude,
           'longitude': automobile.longitude,
           'location': automobile.location,
           'listing_type': automobile.get_listing_type_display(),  # Add the new field here
            'images': images,
            'videos': videos,
        }

    elif product_type == 'motorcycle':
        motorcycle = Motorcycle.objects.get(id=product_id)
        images = [{'url': image.image.url} for image in motorcycle.images.all()]
        videos = [{'url': video.video.url} for video in motorcycle.videos.all()]
        data = {
          'make': motorcycle.make,
          'name': motorcycle.name,
          'model': motorcycle.model,
          'year': motorcycle.year,
          'description': motorcycle.description,
          'price': motorcycle.price,
          'engine_capacity': motorcycle.engine_capacity,
          'body_type': motorcycle.body_type,
          'condition': motorcycle.get_condition_display(),
          'status': motorcycle.get_status_display(),
          'regions': motorcycle.regions,
          'cities': motorcycle.cities,
          'latitude': motorcycle.latitude,
          'longitude': motorcycle.longitude,
          'location': motorcycle.location,
           'listing_type': motorcycle.get_listing_type_display(),  # Add the new field here
          'images': images,
            'videos': videos,
        }

    elif product_type == 'accessory':
        accessory = AutoAccessoryPart.objects.get(id=product_id)
        images = [{'url': image.image.url} for image in accessory.images.all()]
        videos = [{'url': video.video.url} for video in accessory.videos.all()]
        data = {
          'name': accessory.name,
          'description': accessory.description,
          'price': accessory.price,
          'regions': accessory.regions,
          'cities': accessory.cities,
          'latitude': accessory.latitude,
          'longitude': accessory.longitude,
          'location': accessory.location,
          'status': accessory.get_status_display(),
          'listing_type': accessory.get_listing_type_display(),  # Add the new field here
          'images': images,
            'videos': videos,
        }

    elif product_type == 'heavy_vehicle':
        heavy_vehicle = HeavyVehicle.objects.get(id=product_id)
        images = [{'url': image.image.url} for image in heavy_vehicle.images.all()]
        videos = [{'url': video.video.url} for video in heavy_vehicle.videos.all()]
        data = {
          'name': heavy_vehicle.name,
          'description': heavy_vehicle.description,
          'manufacturer': heavy_vehicle.manufacturer,
          'year': heavy_vehicle.year,
          'fuel_type': heavy_vehicle.get_fuel_type_display(),
          'engine_capacity': heavy_vehicle.engine_capacity,
          'transmission': heavy_vehicle.get_transmission_display(),
          'price': heavy_vehicle.price,
          'mileage': heavy_vehicle.mileage,
          'load_capacity': heavy_vehicle.load_capacity,
          'condition': heavy_vehicle.get_condition_display(),
          'status': heavy_vehicle.get_status_display(),
          'regions': heavy_vehicle.regions,
          'cities': heavy_vehicle.cities,
          'latitude': heavy_vehicle.latitude,
          'longitude': heavy_vehicle.longitude,
          'location': heavy_vehicle.location,
          'listing_type': heavy_vehicle.get_listing_type_display(),  # Add the new field here
            'images': images,
            'videos': videos,
        }

    elif product_type == 'boat':
        boat = Boat.objects.get(id=product_id)
        images = [{'url': image.image.url} for image in boat.images.all()]
        videos = [{'url': video.video.url} for video in boat.videos.all()]
        data = {
          'name': boat.name,
          'description': boat.description,
          'manufacturer': boat.manufacturer,
          'year': boat.year,
          'length': boat.length,
          'engine_type': boat.get_engine_type_display(),
          'engine_power': boat.engine_power,
          'fuel_type': boat.get_fuel_type_display(),
          'price': boat.price,
          'condition': boat.get_condition_display(),
          'status': boat.get_status_display(),
          'regions': boat.regions,
          'cities': boat.cities,
          'latitude': boat.latitude,
          'longitude': boat.longitude,
          'location': boat.location,
          'listing_type': boat.get_listing_type_display(),  # Add the new field here
           'images': images,
           'videos': videos,
        }

    elif product_type == 'number_plate':
      number_plate = NumberPlate.objects.get(id=product_id)
      images = [{'url': image.image.url} for image in number_plate.images.all()]
      videos = [{'url': video.video.url} for video in number_plate.videos.all()]

      data = {
        'number': number_plate.number,
        'price': number_plate.price,
        'description': number_plate.description,
        'regions': number_plate.regions,
        'cities': number_plate.cities,
        'latitude': number_plate.latitude,
        'longitude': number_plate.longitude,
        'location': number_plate.location,
        'status': number_plate.get_status_display(),
        'listing_type': number_plate.get_listing_type_display(),  # Add the new field here
        'images': images,
        'videos': videos,
    }
    elif product_type == 'commercial':
        commercial = Commercial.objects.get(id=product_id)
        images = [{'url': image.image.url} for image in commercial.images.all()]
        videos = [{'url': video.video.url} for video in commercial.videos.all()]
        
        data = {
            'property_title': commercial.property_title,
            'price': commercial.price,
            'plot_area': commercial.plot_area,
            'status': commercial.get_status_display(),
            'listing_type': commercial.get_listing_type_display(),
            'description': commercial.description,
            'regions': commercial.get_region_display(),  # Using display method
            'cities': commercial.cities,
            'latitude': commercial.latitude,
            'longitude': commercial.longitude,
            'floors': commercial.get_floors_display(),
            'furnished': commercial.get_furnished_display(),
            'property_mortgage': commercial.get_property_mortgage_display(),
            'lister_type': commercial.get_lister_type_display(),
            'property_status': commercial.get_property_display(),
            'main_amenities': [amenity.name for amenity in commercial.main_amenities.all()],
            'additional_amenities': [amenity.name for amenity in commercial.additional_amenities.all()],
            'nearby_location': [location.name for location in commercial.nearby_location.all()],
            'images': images,
            'videos': videos,
        }


    elif product_type == 'farm':
        farm = Farm.objects.get(id=product_id)
        images = [{'url': image.image.url} for image in farm.images.all()]
        videos = [{'url': video.video.url} for video in farm.videos.all()]

        data = {
            'property_title': farm.property_title,
            'price': farm.price,
            'surface_area': farm.surface_area,
            'bedrooms': farm.get_bedrooms_display(),
            'bathrooms': farm.get_bathrooms_display(),
            'plot_area': farm.plot_area,
            'regions': farm.get_region_display(),
            'cities': farm.cities,
            'latitude': farm.latitude,
            'longitude': farm.longitude,
            'listing_type': farm.get_listing_type_display(),
            'status': farm.get_status_display(),
            'furnished': farm.get_furnished_display(),
            'building_age': farm.get_building_display(),
            'lister_type': farm.get_lister_type_display(),
            'property_mortgage': farm.get_property_mortgage_display(),
            'facade': farm.get_facade_display(),
            'description': farm.description,
            'created_at': farm.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'images': images,
            'videos': videos,
        }

    elif product_type == 'apartment':
        apartment = Apartment.objects.get(id=product_id)
        images = [{'url': image.image.url} for image in apartment.images.all()]
        videos = [{'url': video.video.url} for video in apartment.videos.all()]
        
        data = {
            'property_title': apartment.property_title,
            'price': apartment.price,
            'plot_area': apartment.plot_area,
            'bedrooms': apartment.get_bedrooms_display(),
            'bathrooms': apartment.get_bathrooms_display(),
            'description': apartment.description,
            'regions': apartment.get_region_display(),
            'cities': apartment.cities,
            'latitude': apartment.latitude,
            'longitude': apartment.longitude,
            'listing_type': apartment.get_listing_type_display(),
            'status': apartment.get_status_display(),
            'furnished': apartment.get_furnished_display(),
            'building': apartment.get_building_display(),
            'lister_type': apartment.get_lister_type_display(),
            'property_mortgage': apartment.get_property_mortgage_display(),
            'facade': apartment.get_facade_display(),
            'floors': apartment.get_floors_display(),
            'main_amenities': [amenity.name for amenity in apartment.main_amenities.all()],
            'additional_amenities': [amenity.name for amenity in apartment.additional_amenities.all()],
            'nearby_location': [location.name for location in apartment.nearby_location.all()],
            'images': images,
            'videos': videos,
        }
    elif product_type == 'factory':
        factory = Factory.objects.get(id=product_id)
        images = [{'url': image.image.url} for image in factory.images.all()]
        videos = [{'url': video.video.url} for video in factory.videos.all()]

        data = {
            'property_title': factory.property_title,
            'price': factory.price,
            'plot_area': factory.plot_area,
            'description': factory.description,
            'regions': factory.get_region_display(),
            'cities': factory.cities,
            'latitude': factory.latitude,
            'longitude': factory.longitude,
            'listing_type': factory.get_listing_type_display(),
            'status': factory.get_status_display(),
            'lister_type': factory.get_lister_type_display(),
            'property_mortgage': factory.get_property_mortgage_display(),
            'main_amenities': [amenity.name for amenity in factory.main_amenities.all()],
            'additional_amenities': [amenity.name for amenity in factory.additional_amenities.all()],
            'nearby_location': [location.name for location in factory.nearby_location.all()],
            'images': images,
            'videos': videos,
        }

    elif product_type == 'complexes':
        complex = Complex.objects.get(id=product_id)
        images = [{'url': image.image.url} for image in complex.images.all()]
        videos = [{'url': video.video.url} for video in complex.videos.all()]
        
        data = {
            'property_title': complex.property_title,
            'price': complex.price,
            'plot_area': complex.plot_area,
            'description': complex.description,
            'regions': complex.get_region_display(),
            'cities': complex.cities,
            'latitude': complex.latitude,
            'longitude': complex.longitude,
            'floors': complex.get_floors_display(),
            'listing_type': complex.get_listing_type_display(),
            'status': complex.get_status_display(),
            'property_mortgage': complex.get_property_mortgage_display(),
            'property': complex.get_property_display(),
            'lister_type': complex.get_lister_type_display(),
            'main_amenities': [amenity.name for amenity in complex.main_amenities.all()],
            'additional_amenities': [amenity.name for amenity in complex.additional_amenities.all()],
            'nearby_location': [location.name for location in complex.nearby_location.all()],
            'images': images,
            'videos': videos,
        }
    elif product_type == 'clinic':
        clinic = Clinic.objects.get(id=product_id)
        images = [{'url': image.image.url} for image in clinic.images.all()]
        videos = [{'url': video.video.url} for video in clinic.videos.all()]
        
        data = {
            'property_title': clinic.property_title,
            'price': clinic.price,
            'plot_area': clinic.plot_area,
            'description': clinic.description,
            'regions': clinic.get_region_display(),
            'cities': clinic.cities,
            'latitude': clinic.latitude,
            'longitude': clinic.longitude,
            'floors': dict(Clinic.FLOOR_CHOICES).get(clinic.floors, clinic.floors),
            'listing_type': dict(Clinic.TRANSACTION_CHOICES).get(clinic.listing_type, clinic.listing_type),
            'status': dict(Clinic.STATUS_CHOICES).get(clinic.status, clinic.status),
            'property_mortgage': dict(Clinic.PROPERTY_MORTGAGE_CHOICES).get(clinic.property_mortgage, clinic.property_mortgage),
            'property': dict(Clinic.PROPERTY_CHOICES).get(clinic.property, clinic.property),
            'lister_type': dict(Clinic.LISTER_TYPE_CHOICES).get(clinic.lister_type, clinic.lister_type),
            'main_amenities': [amenity.name for amenity in clinic.main_amenities.all()],
            'additional_amenities': [amenity.name for amenity in clinic.additional_amenities.all()],
            'nearby_location': [location.name for location in clinic.nearby_location.all()],
            'images': images,
            'videos': videos,
        }
    elif product_type == 'hostel':
        hostel = Hostel.objects.get(id=product_id)
        images = [{'url': image.image.url} for image in hostel.images.all()]
        videos = [{'url': video.video.url} for video in hostel.videos.all()]
        
        data = {
            'property_title': hostel.property_title,
            'price': hostel.price,
            'plot_area': hostel.plot_area,
            'description': hostel.description,
            'regions': hostel.get_region_display(),
            'cities': hostel.cities,
            'latitude': hostel.latitude,
            'longitude': hostel.longitude,
            'floors': dict(Hostel.FLOOR_CHOICES).get(hostel.floors, hostel.floors),
            'listing_type': dict(Hostel.TRANSACTION_CHOICES).get(hostel.listing_type, hostel.listing_type),
            'status': dict(Hostel.STATUS_CHOICES).get(hostel.status, hostel.status),
            'property_mortgage': dict(Hostel.PROPERTY_MORTGAGE_CHOICES).get(hostel.property_mortgage, hostel.property_mortgage),
            'property': dict(Hostel.PROPERTY_CHOICES).get(hostel.property, hostel.property),
            'lister_type': dict(Hostel.LISTER_TYPE_CHOICES).get(hostel.lister_type, hostel.lister_type),
            'main_amenities': [amenity.name for amenity in hostel.main_amenities.all()],
            'additional_amenities': [amenity.name for amenity in hostel.additional_amenities.all()],
            'nearby_location': [location.name for location in hostel.nearby_location.all()],
            'images': images,
            'videos': videos,
        }

    elif product_type == 'office':
        office = Office.objects.get(id=product_id)
        images = [{'url': image.image.url} for image in office.images.all()]
        videos = [{'url': video.video.url} for video in office.videos.all()]

        data = {
            'property_title': office.property_title,
            'price': str(office.price),  # Convert Decimal to string
            'plot_area': str(office.plot_area),  # Convert Decimal to string
            'description': office.description,
            'regions': office.get_region_display(),
            'cities': office.cities,
            'latitude': office.latitude,
            'longitude': office.longitude,
            'floors': dict(Office.FLOOR_CHOICES).get(office.floors, office.floors),
            'listing_type': dict(Office.TRANSACTION_CHOICES).get(office.listing_type, office.listing_type),
            'status': dict(Office.STATUS_CHOICES).get(office.status, office.status),
            'property_mortgage': dict(Office.PROPERTY_MORTGAGE_CHOICES).get(office.property_mortgage, office.property_mortgage),
            'property': dict(Office.PROPERTY_CHOICES).get(office.property, office.property),
            'lister_type': dict(Office.LISTER_TYPE_CHOICES).get(office.lister_type, office.lister_type),
            'furnished': dict(Office.FURNISHED_CHOICES).get(office.furnished, office.furnished),
            'main_amenities': [amenity.name for amenity in office.main_amenities.all()],
            'additional_amenities': [amenity.name for amenity in office.additional_amenities.all()],
            'nearby_location': [location.name for location in office.nearby_location.all()],
            'images': images,
            'videos': videos,
        }
        
    elif product_type == 'shop':
        shop = Shop.objects.get(id=product_id)
        images = [{'url': image.image.url} for image in shop.images.all()]
        videos = [{'url': video.video.url} for video in shop.videos.all()]
        
        data = {
            'property_title': shop.property_title,
            'price': shop.price,
            'plot_area': shop.plot_area,
            'description': shop.description,
            'regions': shop.get_region_display(),
            'cities': shop.cities,
            'latitude': shop.latitude,
            'longitude': shop.longitude,
            'listing_type': dict(Shop.TRANSACTION_CHOICES).get(shop.listing_type, shop.listing_type),
            'status': dict(Shop.STATUS_CHOICES).get(shop.status, shop.status),
            'property_mortgage': dict(Shop.PROPERTY_MORTGAGE_CHOICES).get(shop.property_mortgage, shop.property_mortgage),
            'lister_type': dict(Shop.LISTER_TYPE_CHOICES).get(shop.lister_type, shop.lister_type),
            'main_amenities': [amenity.name for amenity in shop.main_amenities.all()],
            'additional_amenities': [amenity.name for amenity in shop.additional_amenities.all()],
            'nearby_location': [location.name for location in shop.nearby_location.all()],
            'images': images,
            'videos': videos,
        }
    elif product_type == 'cafe':
        cafe = Cafe.objects.get(id=product_id)
        images = [{'url': image.image.url} for image in cafe.images.all()]
        videos = [{'url': video.video.url} for video in cafe.videos.all()]
        
        data = {
            'property_title': cafe.property_title,
            'price': cafe.price,
            'plot_area': cafe.plot_area,
            'description': cafe.description,
            'regions': cafe.get_region_display(),
            'cities': cafe.cities,
            'latitude': cafe.latitude,
            'longitude': cafe.longitude,
            'listing_type': dict(Cafe.TRANSACTION_CHOICES).get(cafe.listing_type, cafe.listing_type),
            'status': dict(Cafe.STATUS_CHOICES).get(cafe.status, cafe.status),
            'property_mortgage': dict(Cafe.PROPERTY_MORTGAGE_CHOICES).get(cafe.property_mortgage, cafe.property_mortgage),
            'lister_type': dict(Cafe.LISTER_TYPE_CHOICES).get(cafe.lister_type, cafe.lister_type),
            'main_amenities': [amenity.name for amenity in cafe.main_amenities.all()],
            'additional_amenities': [amenity.name for amenity in cafe.additional_amenities.all()],
            'nearby_location': [location.name for location in cafe.nearby_location.all()],
            'images': images,
            'videos': videos,
        }
    elif product_type == 'staff':
        staff = Staff.objects.get(id=product_id)
        images = [{'url': image.image.url} for image in staff.images.all()]
        videos = [{'url': video.video.url} for video in staff.videos.all()]
        
        data = {
            'property_title': staff.property_title,
            'price': staff.price,
            'plot_area': staff.plot_area,
            'description': staff.description,
            'regions': staff.get_region_display(),
            'cities': staff.cities,
            'latitude': staff.latitude,
            'longitude': staff.longitude,
            'listing_type': dict(Staff.TRANSACTION_CHOICES).get(staff.listing_type, staff.listing_type),
            'status': dict(Staff.STATUS_CHOICES).get(staff.status, staff.status),
            'property_mortgage': dict(Staff.PROPERTY_MORTGAGE_CHOICES).get(staff.property_mortgage, staff.property_mortgage),
            'lister_type': dict(Staff.LISTER_TYPE_CHOICES).get(staff.lister_type, staff.lister_type),
            'main_amenities': [amenity.name for amenity in staff.main_amenities.all()],
            'additional_amenities': [amenity.name for amenity in staff.additional_amenities.all()],
            'nearby_location': [location.name for location in staff.nearby_location.all()],
            'images': images,
            'videos': videos,
        }
    elif product_type == 'warehouse':
        warehouse = Warehouse.objects.get(id=product_id)
        images = [{'url': image.image.url} for image in warehouse.images.all()]
        videos = [{'url': video.video.url} for video in warehouse.videos.all()]
        
        data = {
            'property_title': warehouse.property_title,
            'price': warehouse.price,
            'plot_area': warehouse.plot_area,
            'description': warehouse.description,
            'regions': warehouse.get_region_display(),
            'cities': warehouse.cities,
            'latitude': warehouse.latitude,
            'longitude': warehouse.longitude,
            'listing_type': dict(Warehouse.TRANSACTION_CHOICES).get(warehouse.listing_type, warehouse.listing_type),
            'status': dict(Warehouse.STATUS_CHOICES).get(warehouse.status, warehouse.status),
            'property_mortgage': dict(Warehouse.PROPERTY_MORTGAGE_CHOICES).get(warehouse.property_mortgage, warehouse.property_mortgage),
            'lister_type': dict(Warehouse.LISTER_TYPE_CHOICES).get(warehouse.lister_type, warehouse.lister_type),
            'main_amenities': [amenity.name for amenity in warehouse.main_amenities.all()],
            'additional_amenities': [amenity.name for amenity in warehouse.additional_amenities.all()],
            'nearby_location': [location.name for location in warehouse.nearby_location.all()],
            'images': images,
            'videos': videos,
        }
    elif product_type == 'townhouse':
        townhouse = Townhouse.objects.get(id=product_id)
        images = [{'url': image.image.url} for image in townhouse.images.all()]
        videos = [{'url': video.video.url} for video in townhouse.videos.all()]
        
        data = {
            'property_title': townhouse.property_title,
            'price': townhouse.price,
            'plot_area': townhouse.plot_area,
            'description': townhouse.description,
            'regions': townhouse.get_region_display(),
            'cities': townhouse.cities,
            'latitude': townhouse.latitude,
            'longitude': townhouse.longitude,
            'listing_type': dict(Townhouse.TRANSACTION_CHOICES).get(townhouse.listing_type, townhouse.listing_type),
            'status': dict(Townhouse.STATUS_CHOICES).get(townhouse.status, townhouse.status),
            'property_mortgage': dict(Townhouse.PROPERTY_MORTGAGE_CHOICES).get(townhouse.property_mortgage, townhouse.property_mortgage),
            'lister_type': dict(Townhouse.LISTER_TYPE_CHOICES).get(townhouse.lister_type, townhouse.lister_type),
            'main_amenities': [amenity.name for amenity in townhouse.main_amenities.all()],
            'additional_amenities': [amenity.name for amenity in townhouse.additional_amenities.all()],
            'nearby_location': [location.name for location in townhouse.nearby_location.all()],
            'images': images,
            'videos': videos,
        }

    elif product_type == 'fullfloors':
        fullfloors = Fullfloors.objects.get(id=product_id)
        images = [{'url': image.image.url} for image in fullfloors.images.all()]
        videos = [{'url': video.video.url} for video in fullfloors.videos.all()]
        
        data = {
            'property_title': fullfloors.property_title,
            'price': fullfloors.price,
            'plot_area': fullfloors.plot_area,
            'description': fullfloors.description,
            'regions': fullfloors.get_region_display(),
            'cities': fullfloors.cities,
            'latitude': fullfloors.latitude,
            'longitude': fullfloors.longitude,
            'listing_type': dict(Fullfloors.TRANSACTION_CHOICES).get(fullfloors.listing_type, fullfloors.listing_type),
            'status': dict(Fullfloors.STATUS_CHOICES).get(fullfloors.status, fullfloors.status),
            'property_mortgage': dict(Fullfloors.PROPERTY_MORTGAGE_CHOICES).get(fullfloors.property_mortgage, fullfloors.property_mortgage),
            'lister_type': dict(Fullfloors.LISTER_TYPE_CHOICES).get(fullfloors.lister_type, fullfloors.lister_type),
            'main_amenities': [amenity.name for amenity in fullfloors.main_amenities.all()],
            'additional_amenities': [amenity.name for amenity in fullfloors.additional_amenities.all()],
            'nearby_location': [location.name for location in fullfloors.nearby_location.all()],
            'images': images,
            'videos': videos,
        }

    elif product_type == 'showrooms':
        showrooms = Showrooms.objects.get(id=product_id)
        images = [{'url': image.image.url} for image in showrooms.images.all()]
        videos = [{'url': video.video.url} for video in showrooms.videos.all()]
        
        data = {
            'property_title': showrooms.property_title,
            'price': showrooms.price,
            'plot_area': showrooms.plot_area,
            'description': showrooms.description,
            'regions': showrooms.get_region_display(),
            'cities': showrooms.cities,
            'latitude': showrooms.latitude,
            'longitude': showrooms.longitude,
            'listing_type': dict(Showrooms.TRANSACTION_CHOICES).get(showrooms.listing_type, showrooms.listing_type),
            'status': dict(Showrooms.STATUS_CHOICES).get(showrooms.status, showrooms.status),
            'property_mortgage': dict(Showrooms.PROPERTY_MORTGAGE_CHOICES).get(showrooms.property_mortgage, showrooms.property_mortgage),
            'lister_type': dict(Showrooms.LISTER_TYPE_CHOICES).get(showrooms.lister_type, showrooms.lister_type),
            'main_amenities': [amenity.name for amenity in showrooms.main_amenities.all()],
            'additional_amenities': [amenity.name for amenity in showrooms.additional_amenities.all()],
            'nearby_location': [location.name for location in showrooms.nearby_location.all()],
            'images': images,
            'videos': videos,
        }
    elif product_type == 'wholebuilding':
        wholebuilding = Wholebuilding.objects.get(id=product_id)
        images = [{'url': image.image.url} for image in wholebuilding.images.all()]
        videos = [{'url': video.video.url} for video in wholebuilding.videos.all()]
        
        data = {
            'property_title': wholebuilding.property_title,
            'price': wholebuilding.price,
            'plot_area': wholebuilding.plot_area,
            'description': wholebuilding.description,
            'regions': wholebuilding.get_region_display(),
            'cities': wholebuilding.cities,
            'latitude': wholebuilding.latitude,
            'longitude': wholebuilding.longitude,
            'listing_type': dict(Wholebuilding.TRANSACTION_CHOICES).get(wholebuilding.listing_type, wholebuilding.listing_type),
            'status': dict(Wholebuilding.STATUS_CHOICES).get(wholebuilding.status, wholebuilding.status),
            'property_mortgage': dict(Wholebuilding.PROPERTY_MORTGAGE_CHOICES).get(wholebuilding.property_mortgage, wholebuilding.property_mortgage),
            'lister_type': dict(Wholebuilding.LISTER_TYPE_CHOICES).get(wholebuilding.lister_type, wholebuilding.lister_type),
            # 'main_amenities': [amenity.name for amenity in wholebuilding.main_amenities.all()],
            # 'additional_amenities': [amenity.name for amenity in wholebuilding.additional_amenities.all()],
            'nearby_location': [location.name for location in wholebuilding.nearby_location.all()],
            'images': images,
            'videos': videos,
        }
    elif product_type == 'supermarket':
        supermarket = Supermarket.objects.get(id=product_id)
        images = [{'url': image.image.url} for image in supermarket.images.all()]
        videos = [{'url': video.video.url} for video in supermarket.videos.all()]
        
        data = {
            'property_title': supermarket.property_title,
            'price': supermarket.price,
            'plot_area': supermarket.plot_area,
            'description': supermarket.description,
            'regions': supermarket.get_region_display(),
            'cities': supermarket.cities,
            'latitude': supermarket.latitude,
            'longitude': supermarket.longitude,
            'listing_type': dict(Supermarket.TRANSACTION_CHOICES).get(supermarket.listing_type, supermarket.listing_type),
            'status': dict(Supermarket.STATUS_CHOICES).get(supermarket.status, supermarket.status),
            'property_mortgage': dict(Supermarket.PROPERTY_MORTGAGE_CHOICES).get(supermarket.property_mortgage, supermarket.property_mortgage),
            'lister_type': dict(Supermarket.LISTER_TYPE_CHOICES).get(supermarket.lister_type, supermarket.lister_type),
            'main_amenities': [amenity.name for amenity in supermarket.main_amenities.all()],
            'additional_amenities': [amenity.name for amenity in supermarket.additional_amenities.all()],
            'nearby_location': [location.name for location in supermarket.nearby_location.all()],
            'images': images,
            'videos': videos,
        }
    elif product_type == 'foreign':
        foreign = Foreign.objects.get(id=product_id)
        images = [{'url': image.image.url} for image in foreign.images.all()]
        videos = [{'url': video.video.url} for video in foreign.videos.all()]
        
        data = {
            'property_title': foreign.property_title,
            'price': foreign.price,
            'description': foreign.description,
            'regions': foreign.get_region_display(),
            'cities': foreign.cities,
            'country': foreign.country,
            'latitude': foreign.latitude,
            'longitude': foreign.longitude,
            'estate_type': dict(Foreign.ESTATE_TYPE_CHOICES).get(foreign.estate_type, foreign.estate_type),
            'listing_type': dict(Foreign.TRANSACTION_CHOICES).get(foreign.listing_type, foreign.listing_type),
            'status': dict(Foreign.STATUS_CHOICES).get(foreign.status, foreign.status),
            'property_mortgage': dict(Foreign.PROPERTY_MORTGAGE_CHOICES).get(foreign.property_mortgage, foreign.property_mortgage),
            'lister_type': dict(Foreign.LISTER_TYPE_CHOICES).get(foreign.lister_type, foreign.lister_type),
            'nearby_location': [location.name for location in foreign.nearby_location.all()],
            'images': images,
            'videos': videos,
        }


    elif product_type == 'fashion':
        fashion_item = Fashion.objects.get(id=product_id)
        images = [{'url': image.image.url} for image in fashion_item.images.all()]
        videos = [{'url': video.video.url} for video in fashion_item.videos.all()]

        data = {
            'brand': fashion_item.brand,
            'category': fashion_item.category,
            'size': fashion_item.size,
            'gender': fashion_item.gender,
            'color': fashion_item.color,
            'material': fashion_item.material,
            'condition': fashion_item.condition,
            'price': fashion_item.price,
            'description': fashion_item.description,
            'regions': fashion_item.regions,
            'cities': fashion_item.cities,
            'latitude': fashion_item.latitude,
            'longitude': fashion_item.longitude,
            'product_name':fashion_item.price,
            'location': fashion_item.location,
            'contact_details': fashion_item.contact_details,
            'status': fashion_item.get_status_display(),
            'images': images,
            'videos':videos
        }
    elif product_type == 'toys':
        toy = Toys.objects.get(id=product_id)
        images = [{'url': image.image.url} for image in toy.images.all()]
        videos = [{'url': video.video.url} for video in toy.videos.all()]

        data = {
            'brand': toy.brand,
            'category': toy.category,
            'platform': toy.platform,
            'age_group': toy.age_group,
            'condition': toy.condition,
            'price': toy.price,
            'location': toy.location,
            'description': toy.description,
            'regions': toy.regions,
            'cities': toy.cities,
            'longitude': toy.longitude,
            'latitude': toy.latitude,
            'product_name':toy.product_name,
            'status': toy.get_status_display(),
            'images': images,
            'videos':videos
        }
    elif product_type == 'food':
        food_item = Food.objects.get(id=product_id)
        images = [{'url': image.image.url} for image in food_item.images.all()]
        videos = [{'url': video.video.url} for video in food_item.videos.all()]

        data = {
            'brand': food_item.brand,
            'product_type': food_item.product_type,
            'quantity': food_item.quantity,
            'expiration_date': food_item.expiration_date,
            'price': food_item.price,
            'location': food_item.location,
            'dietary_info': food_item.dietary_info,
            'description': food_item.description,
            'regions': food_item.regions,
            'cities': food_item.cities,
            'longitude': food_item.longitude,
            'latitude': food_item.latitude,
            'product_name':food_item.product_name,
            'status': food_item.get_status_display(),
            'images': images,
            'videos':videos
        }
    elif product_type == 'fitness':
        fitness_item = Fitness.objects.get(id=product_id)
        images = [{'url': image.image.url} for image in fitness_item.images.all()]
        videos = [{'url': video.video.url} for video in fitness_item.videos.all()]

        data = {
            'brand': fitness_item.brand,
            'category': fitness_item.category,
            'condition': fitness_item.condition,
            'price': fitness_item.price,
            'location': fitness_item.location,
            'description': fitness_item.description,
            'regions': fitness_item.regions,
            'cities': fitness_item.cities,
            'longitude': fitness_item.longitude,
            'latitude': fitness_item.latitude,
            'product_name':fitness_item.product_name,
            'status': fitness_item.get_status_display(),
            'images': images,
            'videos':videos
        }
    elif product_type == 'pet':
        pet_item = Pet.objects.get(id=product_id)
        images = [{'url': image.image.url} for image in pet_item.images.all()]
        videos = [{'url': video.video.url} for video in pet_item.videos.all()]
        data = {
            'pet_type': pet_item.pet_type,
            'pet_name': pet_item.pet_name,
            'breed': pet_item.breed,
            'description': pet_item.description,
            'regions': pet_item.regions,
            'cities': pet_item.cities,
            'longitude': pet_item.longitude,
            'latitude': pet_item.latitude,
            'age': pet_item.age,
            'price': pet_item.price,
            'vaccinated': pet_item.vaccinated,
            'location': pet_item.location,
            'status': pet_item.get_status_display(),
            'images': images,
            'videos':videos
        }

    elif product_type == 'book':
        book_item = Book.objects.get(id=product_id)
        images = [{'url': image.image.url} for image in book_item.images.all()]
        videos = [{'url': video.video.url} for video in book_item.videos.all()]

        data = {
            'category': book_item.category,
            'genre': book_item.genre,
            'condition': book_item.condition,
            'price': book_item.price,
            'location': book_item.location,
            'description': book_item.description,
            'regions': book_item.regions,
            'cities': book_item.cities,
            'longitude': book_item.longitude,
            'latitude': book_item.latitude,
            'book_name':book_item.book_name,
            'status': book_item.get_status_display(),
            'images': images,
            'videos': videos,

        }


    elif product_type == 'appliance':
        appliance_item = Appliance.objects.get(id=product_id)
        images = [{'url': image.image.url} for image in appliance_item.images.all()]
        videos = [{'url': video.video.url} for video in appliance_item.videos.all()]

        data = {
            'appliance_type': appliance_item.appliance_type,
            'brand': appliance_item.brand,
            'model_number': appliance_item.model_number,
            'condition': appliance_item.condition,
            'warranty_status': appliance_item.warranty_status,
            'price': appliance_item.price,
            'location': appliance_item.location,
            'description': appliance_item.description,
            'regions': appliance_item.regions,
            'cities': appliance_item.cities,
            'longitude': appliance_item.longitude,
            'latitude': appliance_item.latitude,
            'product_name':appliance_item.product_name,
            'status': appliance_item.get_status_display(),
            'images': images,
            'videos':videos
        }
    elif product_type == 'business':
        business_item = Business.objects.get(id=product_id)
        images = [{'url': image.image.url} for image in business_item.images.all()]
        videos = [{'url': video.video.url} for video in business_item.videos.all()]

        data = {
            'category': business_item.get_category_display(),
            'brand': business_item.brand,
            'condition': business_item.get_condition_display(),
            'price': f"{business_item.price} OMR",
            'warranty_status': business_item.get_warranty_status_display(),
            'location': business_item.location,
            'description': business_item.description,
            'regions':business_item.regions,
            'cities': business_item.cities,
            'latitude': business_item.latitude,
            'longitude': business_item.longitude,
            'status': business_item.get_status_display(),
            'images': images,
            'videos':videos
        }

    elif product_type == 'education':
        education_item = Education.objects.get(id=product_id)
        images = [{'url': image.image.url} for image in education_item.images.all()]
        videos = [{'url': video.video.url} for video in education_item.videos.all()]

        data = {
            'course_type': education_item.get_course_type_display(),
            'subject': education_item.subject,
            'duration': f"{education_item.duration} weeks/months",
            'price': f"{education_item.price} OMR",
            'location': education_item.location,
             'description': education_item.description,
            'regions':education_item.regions,
            'cities': education_item.cities,
            'latitude': education_item.latitude,
            'longitude': education_item.longitude,
            'instructor_name': education_item.instructor_name,
            'qualification': education_item.qualification,
            'experience': education_item.experience,
            'status': education_item.get_status_display(),
            'images': images,
            'videos':videos
        }

    elif product_type == 'service':
        service_item = Service.objects.get(id=product_id)
        images = [{'url': image.image.url} for image in service_item.images.all()]
        videos = [{'url': video.video.url} for video in service_item.videos.all()]

        data = {
            'service_type': service_item.get_service_type_display(),
            'provider_name': service_item.provider_name,
            'price_range': f"{service_item.price_range} OMR",
            'contact_info': service_item.contact_info,
            'location': service_item.location,
             'description': service_item.description,
            'regions':service_item.regions,
            'cities': service_item.cities,
            'latitude': service_item.latitude,
            'longitude': service_item.longitude,
            'status': service_item.get_status_display(),
            'images': images,
            'videos':videos
        }
    elif product_type == 'mobile':
        mobile_item = Mobile.objects.get(id=product_id)
        images = [{'url': image.image.url} for image in mobile_item.images.all()]
        videos = [{'url': video.video.url} for video in mobile_item.videos.all()]

        data = {
            'brand': mobile_item.brand,
            'model_number': mobile_item.model_number,
            'operating_system': mobile_item.get_operating_system_display(),
            'screen_size': mobile_item.screen_size,
            'storage_capacity': mobile_item.storage_capacity,
            'ram_size': mobile_item.ram_size,
            'battery_capacity': mobile_item.battery_capacity,
            'price': f"{mobile_item.price} OMR",
            'condition': mobile_item.get_condition_display(),
            'location': mobile_item.location,
            'description': mobile_item.description,
            'regions':mobile_item.regions,
            'cities': mobile_item.cities,
            'latitude': mobile_item.latitude,
            'longitude': mobile_item.longitude,
            'product_name': mobile_item.product_name,
            'status': mobile_item.get_status_display(),
            'images': images,
            'videos':videos
        }
    elif product_type == 'computer':
        computer_item = Computer.objects.get(id=product_id)
        images = [{'url': image.image.url} for image in computer_item.images.all()]
        videos = [{'url': video.video.url} for video in computer_item.videos.all()]

        data = {
            'brand': computer_item.brand,
            'model_number': computer_item.model_number,
            'operating_system': computer_item.get_operating_system_display(),
            'screen_size': computer_item.screen_size,
            'storage_capacity': computer_item.storage_capacity,
            'ram_size': computer_item.ram_size,
            'processor': computer_item.processor,
            'graphics_card': computer_item.graphics_card,
            'battery_life': computer_item.battery_life,
            'price': f"{computer_item.price} OMR",
            'condition': computer_item.get_condition_display(),
            'location': computer_item.location,
            'description': computer_item.description,
            'regions':computer_item.regions,
            'cities': computer_item.cities,
            'latitude': computer_item.latitude,
            'longitude': computer_item.longitude,
            'product_name': computer_item.product_name,
            'status': computer_item.get_status_display(),
            'images': images,
            'videos':videos
        }

    elif product_type == 'sound':
        sound_item = Sound.objects.get(id=product_id)
        images = [{'url': image.image.url} for image in sound_item.images.all()]
        videos = [{'url': video.video.url} for video in sound_item.videos.all()]

        data = {
            'brand': sound_item.brand,
            'model_number': sound_item.model_number,
            'connectivity': sound_item.get_connectivity_display(),
            'output_power': sound_item.output_power,
            'channels': sound_item.channels,
            'has_smart_assistant': sound_item.has_smart_assistant,
            'price': f"{sound_item.price} OMR",
            'condition': sound_item.get_condition_display(),
            'location': sound_item.location,
            'description': sound_item.description,
            'regions':sound_item.regions,
            'cities': sound_item.cities,
            'latitude': sound_item.latitude,
            'longitude': sound_item.longitude,
            'product_name': sound_item.product_name,
            'status': sound_item.get_status_display(),
            'images': images,
            'videos':videos
        }

    else:
        data = {'error': 'Invalid product type'}

    return JsonResponse(data)



# category

@never_cache
def category(request):
    if request.user.is_authenticated:
        cat = Category.objects.all()
        return render(request, 'admin1/category/category.html', {'cat': cat})
    return redirect('admin')



@never_cache
def add_category(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = categoryForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('category')
        else:
            form = categoryForm()
        return render(request, 'admin1/category/addcategory.html', {'form': form})
    return redirect('admin')


@never_cache
def edit_category(request, cat_id):
    if request.user.is_authenticated:
        cat = get_object_or_404(Category, pk=cat_id)
        form = categoryForm(request.POST or None, request.FILES or None, instance=cat)
        if request.method == 'POST' and form.is_valid():
            form.save()
            return redirect('category')
        return render(request, 'admin1/category/editcategory.html', {'form': form, 'cat': cat})
    return redirect('admin')


@never_cache
def delete_category(request, cat_id):
    if request.user.is_authenticated:
        cat = get_object_or_404(Category, pk=cat_id)
        if request.method == 'POST':
            cat.delete()
            # Optionally, show a success message
            return redirect('category')
        return render(request, 'admin1/category/deletecategory.html', {'cat': cat})
    return redirect('admin')


@never_cache

def view_category(request, cat_id):
     if request.user.is_authenticated:

         cat = get_object_or_404(Category, pk=cat_id)
         return render(request, 'admin1/category/viewcategory.html', {'cat': cat})
     return redirect('admin')


# jobcategory

@never_cache
def jobcategory(request):
    if request.user.is_authenticated:
        jobcat = JobCategory.objects.all()
        return render(request, 'admin1/jobcategory/jobcategory.html', {'jobcat': jobcat})
    return redirect('admin')
@never_cache
def jobpost(request):
    if request.user.is_authenticated:
        job_posts = JobPost.objects.select_related('user').all()
        return render(request, 'admin1/jobcategory/jobpost.html', {'job_posts': job_posts})
    return redirect('admin')


@never_cache
def add_jobcategory(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = jobcategoryForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('jobcategory')
        else:
            form = jobcategoryForm()
        return render(request, 'admin1/jobcategory/addjobcategory.html', {'form': form})
    return redirect('admin')


@never_cache
def edit_jobcategory(request, jobcat_id):
    if request.user.is_authenticated:
        jobcat = get_object_or_404(JobCategory, pk=jobcat_id)
        form = jobcategoryForm(request.POST or None, request.FILES or None, instance=jobcat)
        if request.method == 'POST' and form.is_valid():
            form.save()
            return redirect('jobcategory')
        return render(request, 'admin1/jobcategory/editjobcategory.html', {'form': form, 'jobcat': jobcat})
    return redirect('admin')


@never_cache
def delete_jobcategory(request, jobcat_id):
    if request.user.is_authenticated:
        jobcat = get_object_or_404(JobCategory, pk=jobcat_id)
        if request.method == 'POST':
            jobcat.delete()
            # Optionally, show a success message
            return redirect('jobcategory')
        return render(request, 'admin1/jobcategory/deletejobcategory.html', {'jobcat': jobcat})
    return redirect('admin')


@never_cache

def view_jobcategory(request, jobcat_id):
     if request.user.is_authenticated:

         jobcat = get_object_or_404(JobCategory, pk=jobcat_id)
         return render(request, 'admin1/jobcategory/viewjobcategory.html', {'jobcat': jobcat})
     return redirect('admin')



@never_cache
def subcategory(request):
    if request.user.is_authenticated:
        return render(request, 'admin1/subcategory.html')
    return redirect('admin')

# Region

@never_cache
def region(request):
    if request.user.is_authenticated:
        region = Region.objects.all()
        return render(request, 'admin1/regions/regions.html', {'region': region})
    return redirect('admin')



@never_cache
def add_region(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = regionForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('region')
        else:
            form = regionForm()
        return render(request, 'admin1/region/regions.html', {'form': form})
    return redirect('admin')

@never_cache
def edit_region(request, region_id):
    if request.user.is_authenticated:
        region = get_object_or_404(Region, pk=region_id)
        form = regionForm(request.POST or None, request.FILES or None, instance=region)
        if request.method == 'POST' and form.is_valid():
            form.save()
            return redirect('region')
        return render(request, 'admin1/region/editregion.html', {'form': form, 'region': region})
    return redirect('admin')


@never_cache
def delete_region(request, region_id):
    if request.user.is_authenticated:
        region = get_object_or_404(Region, pk=region_id)
        if request.method == 'POST':
            region.delete()
            # Optionally, show a success message
            return redirect('region')
        return render(request, 'admin1/region/deleteregion.html', {'region': region})
    return redirect('admin')


@never_cache

def view_region(request, region_id):
     if request.user.is_authenticated:

         region = get_object_or_404(Region, pk=region_id)
         return render(request, 'admin1/region/viewregion.html', {'region': region})
     return redirect('admin')
#nearby_location
@never_cache
def nearbylocation(request):
    if request.user.is_authenticated:
        nearbylocation = NearbyLocation.objects.all()
        return render(request, 'admin1/nearbylocation/nearbylocations.html', {'nearbylocation': nearbylocation})
    return redirect('admin')

@never_cache
def add_nearbylocation(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = nearbylocationForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('nearbylocation')
        else:
            form = nearbylocationForm()
        return render(request, 'admin1/nearbylocation/nearbylocations.html', {'form': form})
    return redirect('admin')

@never_cache
def edit_nearbylocation(request, nearbylocation_id):
    if request.user.is_authenticated:
        nearbylocation = get_object_or_404(NearbyLocation, pk=nearbylocation_id)
        form = nearbylocationForm(request.POST or None, request.FILES or None, instance=nearbylocation)
        if request.method == 'POST' and form.is_valid():
            form.save()
            return redirect('nearbylocation')
        return render(request, 'admin1/nearbylocation/editnearbylocation.html', {'form': form, 'nearbylocation': nearbylocation})
    return redirect('admin')


@never_cache
def delete_nearbylocation(request, nearbylocation_id):
    if request.user.is_authenticated:
        nearbylocation = get_object_or_404(NearbyLocation, pk=nearbylocation_id)
        if request.method == 'POST':
            nearbylocation.delete()
            # Optionally, show a success message
            return redirect('nearbylocation')
        return render(request, 'admin1/nearbylocation/deletenearbylocation.html', {'nearbylocation': nearbylocation})
    return redirect('admin')


@never_cache

def view_nearbylocation(request, nearbylocation_id):
     if request.user.is_authenticated:

         nearbylocation = get_object_or_404(NearbyLocation, pk=nearbylocation_id)
         return render(request, 'admin1/nearbylocation/viewnearbylocation.html', {'nearbylocation': nearbylocation})
     return redirect('admin')


#main_amenities
@never_cache
def mainamenities(request):
    if request.user.is_authenticated:
        mainamenities = MainAmenities.objects.all()
        return render(request, 'admin1/mainamenities/mainamenities.html', {'mainamenities': mainamenities})
    return redirect('admin')

@never_cache
def add_mainamenities(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = mainamenitiesForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('mainamenities')
        else:
            form = mainamenitiesForm()
        return render(request, 'admin1/mainamenities/mainamenities.html', {'form': form})
    return redirect('admin')

@never_cache
def edit_mainamenities(request, mainamenities_id):
    if request.user.is_authenticated:
        mainamenities = get_object_or_404(MainAmenities, pk=mainamenities_id)
        form = mainamenitiesForm(request.POST or None, request.FILES or None, instance=mainamenities)
        if request.method == 'POST' and form.is_valid():
            form.save()
            return redirect('mainamenities')
        return render(request, 'admin1/mainamenities/editmainamenities.html', {'form': form, 'mainamenities': mainamenities})
    return redirect('admin')


@never_cache
def delete_mainamenities(request, mainamenities_id):
    if request.user.is_authenticated:
        mainamenities = get_object_or_404(MainAmenities, pk=mainamenities_id)
        if request.method == 'POST':
            mainamenities.delete()
            # Optionally, show a success message
            return redirect('mainamenities')
        return render(request, 'admin1/mainamenities/deletemainamenities.html', {'mainamenities': mainamenities})
    return redirect('admin')


@never_cache

def view_mainamenities(request, mainamenities_id):
     if request.user.is_authenticated:
         mainamenities = get_object_or_404(MainAmenities, pk=mainamenities_id)
         return render(request, 'admin1/mainamenities/viewmainamenities.html', {'mainamenities': mainamenities})
     return redirect('admin')

#aadditional_amenities
@never_cache
def additionalamenities(request):
    if request.user.is_authenticated:
        additionalamenities = AdditionalAmenities.objects.all()
        return render(request, 'admin1/additionalamenities/additionalamenities.html', {'additionalamenities': additionalamenities})
    return redirect('admin')

@never_cache
def add_additionalamenities(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = additionalamenitiesForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('additionalamenities')
        else:
            form = additionalamenitiesForm()
        return render(request, 'admin1/additionalamenities/additionalamenities.html', {'form': form})
    return redirect('admin')

@never_cache
def edit_additionalamenities(request, additionalamenities_id):
    if request.user.is_authenticated:
        additionalamenities = get_object_or_404(AdditionalAmenities, pk=additionalamenities_id)
        form = additionalamenitiesForm(request.POST or None, request.FILES or None, instance=additionalamenities)
        if request.method == 'POST' and form.is_valid():
            form.save()
            return redirect('additionalamenities')
        return render(request, 'admin1/additionalamenities/editadditionalamenities.html', {'form': form, 'additionalamenities': additionalamenities})
    return redirect('admin')


@never_cache
def delete_additionalamenities(request, additionalamenities_id):
    if request.user.is_authenticated:
        additionalamenities = get_object_or_404(AdditionalAmenities, pk=additionalamenities_id)
        if request.method == 'POST':
            additionalamenities.delete()
            # Optionally, show a success message
            return redirect('additionalamenities')
        return render(request, 'admin1/additionalamenities/deleteadditionalamenities.html', {'additionalamenities': additionalamenities})
    return redirect('admin')


@never_cache

def view_additionalamenities(request, additionalamenities_id):
     if request.user.is_authenticated:

         additionalamenities = get_object_or_404(AdditionalAmenities, pk=additionalamenities_id)
         return render(request, 'admin1/additionalamenities/viewadditionalamenities.html', {'additionalamenities': additionalamenities})
     return redirect('admin')

# Advertisements

@never_cache
def advertisement(request):
    if request.user.is_authenticated:
        advertisement = Advertisement.objects.all()
        return render(request, 'admin1/advertisements/advertisements.html', {'advertisement': advertisement})
    return redirect('admin')



@never_cache
def add_advertisements(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = advertisementForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('advertisement')
        else:
            form = advertisementForm()
        return render(request, 'admin1/advertisements/advertisements.html', {'form': form})
    return redirect('admin')

@never_cache
def edit_advertisements(request, advertisement_id):
    if request.user.is_authenticated:
        advertisement = get_object_or_404(Advertisement, pk=advertisement_id)
        form = advertisementForm(request.POST or None, request.FILES or None, instance=advertisement)
        if request.method == 'POST' and form.is_valid():
            form.save()
            return redirect('advertisement')
        return render(request, 'admin1/advertisements/editadvertisement.html', {'form': form, 'advertisement': advertisement})
    return redirect('admin')


@never_cache
def delete_advertisements(request, advertisement_id):
    if request.user.is_authenticated:
        advertisement = get_object_or_404(Advertisement, pk=advertisement_id)
        if request.method == 'POST':
            advertisement.delete()
            # Optionally, show a success message
            return redirect('advertisement')
        return render(request, 'admin1/advertisements/deleteadvertisement.html', {'advertisement': advertisement})
    return redirect('admin')


@never_cache

def view_advertisements(request, advertisement_id):
     if request.user.is_authenticated:

         advertisement = get_object_or_404(Advertisement, pk=advertisement_id)
         return render(request, 'admin1/advertisements/viewadvertisement.html', {'advertisement': advertisement})
     return redirect('admin')

# City

@never_cache
def city(request):
    if request.user.is_authenticated:
        region=Region.objects.all()
        cat = City.objects.all()
        return render(request, 'admin1/cities/cities.html', {'cat': cat,'region':region})
    return redirect('admin')



@never_cache
def add_city(request):
    if request.user.is_authenticated:
        region=Region.objects.all()
        if request.method == 'POST':
            form = cityForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('city')
        else:
            form = cityForm()
        return render(request, 'admin1/cityies/cities.html', {'form': form,'region':region})
    return redirect('admin')


@never_cache
def edit_city(request, city_id):
    if request.user.is_authenticated:
        cat = get_object_or_404(City, pk=city_id)
        form = cityForm(request.POST or None, request.FILES or None, instance=cat)
        if request.method == 'POST' and form.is_valid():
            form.save()
            return redirect('city')
        return render(request, 'admin1/city/editcity.html', {'form': form, 'cat': cat})
    return redirect('admin')


@never_cache
def delete_city(request, city_id):
    if request.user.is_authenticated:
        cat = get_object_or_404(City, pk=city_id)
        if request.method == 'POST':
            cat.delete()
            # Optionally, show a success message
            return redirect('city')
        return render(request, 'admin1/city/deletecity.html', {'cat': cat})
    return redirect('admin')


@never_cache

def view_city(request, city_id):
     if request.user.is_authenticated:

         cat = get_object_or_404(city, pk=city_id)
         return render(request, 'admin1/city/viewcity.html', {'cat': cat})
     return redirect('admin')


# User
@never_cache
def user(request):
    if request.user.is_authenticated:
        user = CustomUser.objects.all()
        return render(request, 'admin1/user/user.html', {'user': user})
    return redirect('admin')


@never_cache

@never_cache
def add_user(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = userForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('user')
        else:
            form = userForm()
        return render(request, 'admin1/user/adduser.html', {'form': form})
    return redirect('admin')


@never_cache
def edit_user(request, user_id):
    if request.user.is_authenticated:
        user = get_object_or_404(CustomUser, pk=user_id)
        form = userForm(request.POST or None, request.FILES or None, instance=user)
        if request.method == 'POST' and form.is_valid():
            form.save()
            return redirect('user')
        return render(request, 'admin1/user/edituser.html', {'form': form, 'user': user})
    return redirect('admin')


@never_cache
def delete_user(request, user_id):
    if request.user.is_authenticated:
        user = get_object_or_404(CustomUser, pk=user_id)
        if request.method == 'POST':
            user.delete()
            # Optionally, show a success message
            return redirect('user')
        return render(request, 'admin1/user/deleteuser.html', {'user': user})
    return redirect('admin')


@never_cache

def view_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    data = {
        'username': user.username,
        'email': user.email,
        'phone': user.phone,
        'address': user.address,
        'image': user.image.url if user.image else None,
    }
    return JsonResponse(data)

@login_required
def listingclassified(request):
    user = request.user

    if request.method == 'POST':
        product_type = request.POST.get('product_type')

        if product_type == 'fashion':
            form = FashionForm(request.POST, request.FILES)
            if form.is_valid():
                fashion = form.save(commit=False)
                fashion.user = user
                fashion.status = 'pending'
                fashion.save()

                for img in request.FILES.getlist('images'):
                    fashion_image = FashionImage(image=img)
                    fashion_image.save()
                    fashion.images.add(fashion_image)
                
                # Handle video uploads
                for video in request.FILES.getlist('videos'):
                   fashion_video = FashionVideo(video=video)
                   fashion_video.save()
                   fashion.videos.add(fashion_video)

                messages.success(request, "Fashion registered successfully!")
                return redirect(adss, user_id=user.id)

        elif product_type == 'toys':
            form = ToysForm(request.POST, request.FILES)
            if form.is_valid():
                toys = form.save(commit=False)
                toys.user = user
                toys.status = 'pending'
                toys.save()

                # Save images for Gaming Toys
                for img in request.FILES.getlist('images'):
                    toys_image = ToysImage(image=img)
                    toys_image.save()
                    toys.images.add(toys_image)

                # Handle video uploads
                for video in request.FILES.getlist('videos'):
                   toys_video = ToysVideo(video=video)
                   toys_video.save()
                   toys.videos.add(toys_video)

                messages.success(request, "Gaming Toys registered successfully!")
                return redirect(adss, user_id=user.id)
            
        elif product_type == 'food':
            form = FoodForm(request.POST, request.FILES)
            if form.is_valid():
                food = form.save(commit=False)
                food.user = user
                food.status = 'pending'
                food.save()

                # Save images for Food
                for img in request.FILES.getlist('images'):
                    food_image = FoodImage(image=img)
                    food_image.save()
                    food.images.add(food_image)

                # Handle video uploads
                for video in request.FILES.getlist('videos'):
                   food_video = FoodVideo(video=video)
                   food_video.save()
                   food.videos.add(food_video)

                messages.success(request, "Food registered successfully!")
                return redirect(adss, user_id=user.id)
            
        elif product_type == 'fitness':
            form = FitnessForm(request.POST, request.FILES)
            if form.is_valid():
                fitness = form.save(commit=False)
                fitness.user = user
                fitness.status = 'pending'
                fitness.save()

                # Save images for fitness
                for img in request.FILES.getlist('images'):
                    fitness_image = FitnessImage(image=img)
                    fitness_image.save()
                    fitness.images.add(fitness_image)

                # Handle video uploads
                for video in request.FILES.getlist('videos'):
                   fitness_video = FitnessVideo(video=video)
                   fitness_video.save()
                   fitness.videos.add(fitness_video)

                messages.success(request, "Fitness registered successfully!")
                return redirect(adss, user_id=user.id)
            
        elif product_type == 'pet':
            form = PetForm(request.POST, request.FILES)
            if form.is_valid():
                pet = form.save(commit=False)
                pet.user = user
                pet.status = 'pending'
                pet.save()

                # Save images for pet
                for img in request.FILES.getlist('images'):
                    pet_image = PetImage(image=img)
                    pet_image.save()
                    pet.images.add(pet_image)

                # Handle video uploads
                for video in request.FILES.getlist('videos'):
                   pet_video = PetVideo(video=video)
                   pet_video.save()
                   pet.videos.add(pet_video)

                messages.success(request, "Pet registered successfully!")
                return redirect(adss, user_id=user.id)
            
        elif product_type == 'book':
            form = BookForm(request.POST, request.FILES)
            if form.is_valid():
                book = form.save(commit=False)
                book.user = user
                book.status = 'pending'
                book.save()

                # Save images for book
                for img in request.FILES.getlist('images'):
                    book_image = BookImage(image=img)
                    book_image.save()
                    book.images.add(book_image)

                # Handle video uploads
                for video in request.FILES.getlist('videos'):
                   book_video = BookVideo(video=video)
                   book_video.save()
                   book.videos.add(book_video)

                messages.success(request, "Book registered successfully!")
                return redirect(adss, user_id=user.id)
        
        elif product_type == 'appliance':
            form = ApplianceForm(request.POST, request.FILES)
            if form.is_valid():
                appliance = form.save(commit=False)
                appliance.user = user
                appliance.status = 'pending'
                appliance.save()

                # Save images for Appliance
                for img in request.FILES.getlist('images'):
                    appliance_image = ApplianceImage(image=img)
                    appliance_image.save()
                    appliance.images.add(appliance_image)

                # Handle video uploads
                for video in request.FILES.getlist('videos'):
                   appliance_video = ApplianceVideo(video=video)
                   appliance_video.save()
                   appliance.videos.add(appliance_video)

                messages.success(request, "Appliance registered successfully!")
                return redirect(adss, user_id=user.id)
            else:
                messages.error(request, "Error in form submission. Please correct the errors below.")
                print(form.errors)  

    fashion_form = FashionForm()
    toys_form = ToysForm()
    food_form = FoodForm()
    fitness_form = FitnessForm()
    pet_form = PetForm()
    book_form = BookForm()
    appliance_form = ApplianceForm()

    return render(request, 'registrationclassified.html', {
        'fashion_form': fashion_form,
        'toys_form': toys_form,
        'food_form': food_form,
        'fitness_form': fitness_form,
        'pet_form': pet_form,
        'book_form': book_form,
        'appliance_form' : appliance_form

})

@login_required
def listingcommunity(request):
    user = request.user

    if request.method == 'POST':
        product_type = request.POST.get('product_type')

        if product_type == 'business':
            form = BusinessForm(request.POST, request.FILES)
            if form.is_valid():
                business = form.save(commit=False)
                business.user = user
                business.status = 'pending'
                business.save()

                for img in request.FILES.getlist('images'):
                    business_image = BusinessImage(image=img)
                    business_image.save()
                    business.images.add(business_image)

                # Handle video uploads
                for video in request.FILES.getlist('videos'):
                   business_video = BusinessVideo(video=video)
                   business_video.save()
                   business.videos.add(business_video)


                messages.success(request, "Business registered successfully!")
                return redirect(adss, user_id=user.id)

        elif product_type == 'education':
            form = EducationForm(request.POST, request.FILES)
            if form.is_valid():
                education = form.save(commit=False)
                education.user = user
                education.status = 'pending'
                education.save()

                # Save images for Education
                for img in request.FILES.getlist('images'):
                    education_image = EducationImage(image=img)
                    education_image.save()
                    education.images.add(education_image)

                for video in request.FILES.getlist('videos'):
                   education_video = EducationVideo(video=video)
                   education_video.save()
                   education.videos.add(education_video)

                messages.success(request, "Education registered successfully!")
                return redirect(adss, user_id=user.id)
            
        elif product_type == 'service':
            form = ServiceForm(request.POST, request.FILES)
            if form.is_valid():
                service = form.save(commit=False)
                service.user = user
                service.status = 'pending'
                service.save()

                # Save images for Service
                for img in request.FILES.getlist('images'):
                    service_image = ServiceImage(image=img)
                    service_image.save()
                    service.images.add(service_image)

                for video in request.FILES.getlist('videos'):
                   service_video = ServiceVideo(video=video)
                   service_video.save()
                   service.videos.add(service_video)

                messages.success(request, "Service registered successfully!")
                return redirect(adss, user_id=user.id)
            else:
                messages.error(request, "Error in form submission. Please correct the errors below.")
                print(form.errors)  

    education_form = EducationForm()
    service_form = ServiceForm()
    business_form = BusinessForm()
    

    return render(request, 'registrationcommunity.html', {
        
        'education_form': education_form,
        'service_form': service_form,
        'business_form': business_form,

    })

@login_required
def listingmobile(request):
    user = request.user

    # Handle POST request
    if request.method == 'POST':
        product_type = request.POST.get('product_type')

        # Handle Mobile form submission
        if product_type == 'mobile':
            form = MobileForm(request.POST, request.FILES)
            if form.is_valid():
                mobile = form.save(commit=False)
                mobile.user = user
                mobile.status = 'pending'
                mobile.save()

                # Handle uploaded images
                for img in request.FILES.getlist('images'):
                    mobile_image = MobileImage(image=img)
                    mobile_image.save()
                    mobile.images.add(mobile_image)

                # Handle video uploads
                for video in request.FILES.getlist('videos'):
                   mobile_video = MobileVideo(video=video)
                   mobile_video.save()
                   mobile.videos.add(mobile_video)

                messages.success(request, "Mobile registered successfully!")
                return redirect(adss, user_id=user.id)
           

        # Handle Laptop form submission
        elif product_type == 'computer':
            form = ComputerForm(request.POST, request.FILES)
            if form.is_valid():
                computer = form.save(commit=False)
                computer.user = user
                computer.status = 'pending'
                computer.save()

                # Handle uploaded images
                for img in request.FILES.getlist('images'):
                    computer_image = ComputerImage(image=img)
                    computer_image.save()
                    computer.images.add(computer_image)

                # Handle video uploads
                for video in request.FILES.getlist('videos'):
                   computer_video = ComputerVideo(video=video)
                   computer_video.save()
                   computer.videos.add(computer_video)

                messages.success(request, "Computer registered successfully!")
                return redirect(adss, user_id=user.id)
          
        # Handle Audio form submission
        elif product_type == 'sound':
            form = SoundForm(request.POST, request.FILES)
            if form.is_valid():
                sound = form.save(commit=False)
                sound.user = user
                sound.status = 'pending'
                sound.save()

                # Handle uploaded images
                for img in request.FILES.getlist('images'):
                    sound_image = DeviceImage(image=img)
                    sound_image.save()
                    sound.images.add(sound_image)

                # Handle video uploads
                for video in request.FILES.getlist('videos'):
                   sound_video = SoundVideo(video=video)
                   sound_video.save()
                   sound.videos.add(sound_video)

                messages.success(request, "Audio registered successfully!")
                return redirect(adss, user_id=user.id)
            else:
                print(form.errors)
                messages.error(request, "Error in audio form submission. Please correct the errors.")

    # Handle GET request
    mobile_form = MobileForm()
    computer_form = ComputerForm()
    sound_form = SoundForm()

    return render(request, 'registrationmobile.html', {
        'mobile_form': mobile_form,
        'computer_form': computer_form,
        'sound_form': sound_form,
    })




from django.contrib.contenttypes.models import ContentType

from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from .models import Land, Villa, Commercial, Farm, Chalet, Favorite

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from .models import Favorite, Land, Villa, Commercial, Chalet, Farm
def add_to_favorites(request, product_type, product_id, action):
    # Mapping product types to models
    print(f"Received product_type: {product_type}")
    print(f"Received product_id: {product_id}")
    print(f"Received action: {action}")

    product_models = {
        'land': Land,
        'villa': Villa,
        'commercial': Commercial,
        'chalet': Chalet,
        'farm': Farm,
        'food': Food,
        'toys': Toys,
        'pet': Pet,
        'book': Book,
        'fitness': Fitness,
        'appliance': Appliance,
        'fashion': Fashion,
        'sound': Sound,
        'mobile': Mobile,
        'computer': Computer,
        'business': Business,
        'education': Education,
        'service': Service,
        'jobpost':JobPost,
        'automobile':Automobile,
        'heavyvehicle':HeavyVehicle,
        'boat':Boat,
        'motorcycle':Motorcycle,
        'numberplate':NumberPlate,
        'autoaccessorypart':AutoAccessoryPart,
        'apartment':Apartment,
        'factory':Factory,
        'complex':Complex,
        'clinic':Clinic,
        'hostel':Hostel,
        'office':Office,
        'shop':Shop,
        'cafe':Cafe,
        'staff':Staff,
        'warehouse':Warehouse,
        'townhouse':Townhouse,
        'fullfloors':Fullfloors,
        'showrooms':Showrooms,
        'wholebuilding':Wholebuilding,
        'supermarket':Supermarket,
        'foreign':Foreign,
        'shared':Shared,
        'suits':Suits,
       
    }

    # Check if the product_type exists in the dictionary
    if product_type not in product_models:
        return JsonResponse({'status': 'error', 'message': 'Invalid product type'})

    # Get the corresponding product model
    product = get_object_or_404(product_models[product_type], id=product_id)
    
    # Get the ContentType for the product model
    content_type = ContentType.objects.get_for_model(product)
    
    # Handle the add or remove action
    if action == 'add':
        # Check if the product is already in the user's favorites
        if not Favorite.objects.filter(user=request.user, content_type=content_type, object_id=product.id).exists():
            # Add the product to the user's favorites
            Favorite.objects.create(user=request.user, content_type=content_type, object_id=product.id)
            return JsonResponse({'status': 'added', 'message': 'Product added to favorites'})
        else:
            return JsonResponse({'status': 'already', 'message': 'Product is already in favorites'})
    
    elif action == 'remove':
        # Remove the product from the user's favorites if it exists
        favorite = Favorite.objects.filter(user=request.user, content_type=content_type, object_id=product.id).first()
        if favorite:
            favorite.delete()
            return JsonResponse({'status': 'removed', 'message': 'Product removed from favorites'})
        else:
            return JsonResponse({'status': 'not_found', 'message': 'Product not found in favorites'})

    # Default case: Invalid action
    return JsonResponse({'status': 'error', 'message': 'Invalid action'})

@login_required
def favorites(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    print(f"User: {user.username}")  

    favorites = Favorite.objects.filter(user=user)
    print(f"Number of favorites: {favorites.count()}")  

    favorite_products = []

    for favorite in favorites:
        product = favorite.content_object  # This gives us the actual object (Chalet, Villa, etc.)
        
        if product is None:
            print(f"Warning: Favorite ID {favorite.id} has no associated product (deleted item)")
            continue  # Skip this entry

        print(f"Favorite Product: {product}")  
        product.model_name = product.__class__.__name__.lower()

        favorite_products.append(product)

    return render(request, 'favorites.html', {'user': user, 'favorite_products': favorite_products})

# jobs we are hiring
def we_are_hiring(request):
    user_id = request.user.id if request.user.is_authenticated else None
    return render(request, 'job_hiring.html', {'user_id': user_id})

def personal_registration(request):
    user_id = request.user.id if request.user.is_authenticated else None
    return render(request, 'personal_registration.html', {'user_id': user_id})

@login_required
def register_company(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)  # Fetch the user by user_id

    # Check if the user has already registered a company
    if Company.objects.filter(user=user).exists():
        messages.warning(request, "You can only register a single company.")
        return redirect('company_dashboard', user_id=user.id, company_id=Company.objects.filter(user=user).first().id)

    if request.method == 'POST':
        form = CompanyRegistrationForm(request.POST, request.FILES, user=user)
        if form.is_valid():
            company = form.save()  # Save the form and get the company instance
            return redirect('company_dashboard', user_id=user.id, company_id=company.id)
    else:
        form = CompanyRegistrationForm(user=user)

    return render(request, 'company_registration.html', {'form': form})
@login_required
def company_dashboard(request, user_id, company_id):
    user = get_object_or_404(CustomUser, id=user_id)
    company = get_object_or_404(Company, user=user, id=company_id)

    job_categories = JobCategory.objects.all()
    applications = JobApplication.objects.filter(company=company).exclude(status='rejected')  # Only show approved applications

    # Handle form submission for adding a job post
    if request.method == 'POST':
        form = JobPostForm(request.POST)
        if form.is_valid():
            job_post = form.save(commit=False)
            job_post.company = company
            job_post.user = request.user
            job_post.save()
            messages.success(request, "Job post created successfully.")
            return redirect('company_dashboard', user_id=request.user.id, company_id=company.id)
    else:
        form = JobPostForm()

    job_posts = JobPost.objects.filter(company=company)

    return render(request, 'company_dashboard.html', {
        'company': company,
        'form': form,
        'job_posts': job_posts,
        'applications': applications,
        'job_categories': job_categories,
    })

# View to approve a job application
@login_required
def approve_application(request, application_id):
    application = get_object_or_404(JobApplication, id=application_id)

    if application.status == 'pending':
        application.status = 'approved'
        application.save()
        messages.success(request, f"Application from {application.name} has been approved.")
    else:
        messages.warning(request, "Application has already been processed.")

    return redirect('company_dashboard', user_id=request.user.id, company_id=application.company.id)

# View to reject a job application
@login_required
def reject_application(request, application_id):
    application = get_object_or_404(JobApplication, id=application_id)

    if application.status == 'pending':
        application.status = 'rejected'
        application.save()
        messages.success(request, f"Application from {application.name} has been rejected.")
    else:
        messages.warning(request, "Application has already been processed.")

    return redirect('company_dashboard', user_id=request.user.id, company_id=application.company.id)



def mark_sold_out(request, product_type, product_id):
    if request.method == 'POST':  # Only allow POST requests for status change
        model_map = {
            'land': Land,
            'villa': Villa,
            'automobile': Automobile,
            'commercial': Commercial,
            'motorcycle':Motorcycle,
            'heavyvehicle':HeavyVehicle,
            'boat':Boat,
            'autoaccessorypart':AutoAccessoryPart,
            'numberplate':NumberPlate,
            'farm': Farm,
           'apartment': Apartment,
            'factory': Factory,
            'complexes': Complex,
            'clinic': Clinic,
            'hostel': Hostel,
            'office': Office,
            'shop': Shop,

            'cafe': Cafe,
            'warehouse': Warehouse,
            'staff': Staff,
            'townhouse': Townhouse,
            'fullfloors': Fullfloors,
            'showrooms': Showrooms,
            'wholebuilding': Wholebuilding,
            'supermarket': Supermarket,
            'foreign': Foreign,
            'fitness': Fitness,
            'pet': Pet,
            'book': Book,
            'appliance': Appliance,
            'fashion': Fashion,
            'toys': Toys,
            'food': Food,
            'business': Business,
            'education': Education,
            'service': Service,
            'mobile': Mobile,
            'computer': Computer,
            'sound': Sound,
        }

        model = model_map.get(product_type)
        if not model:
            return render(request, '404.html', status=404)

        product = get_object_or_404(model, id=product_id)

        # Check if the model has a status field
        if hasattr(product, 'status'):
            product.status = 'soldout'
            product.save()
            messages.success(request, f'{product_type.capitalize()} with ID {product_id} has been marked as Sold Out.')
            return redirect(adss, user_id=request.user.id)  # Redirect to the list view
        else:
            messages.error(request, f'{product_type.capitalize()} does not support marking as Sold Out.')
            return redirect(adss, user_id=request.user.id)

    return render(request, '404.html', status=404)

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from .models import ChatMessage
from django.utils import timezone
from datetime import datetime

User = get_user_model()

@login_required
def user_chat_view(request, receiver_id=None):
    """Handles user-to-admin and user-to-user chat"""
    
    # Fetch admin user for user-to-admin chat
    admin_user = User.objects.filter(is_superuser=True).first()
    
    # Determine the chat recipient (either admin or another user)
    if receiver_id:
        receiver = get_object_or_404(User, id=receiver_id)
    else:
        receiver = admin_user  # Default to admin if no receiver_id is provided

    if not receiver:
        return render(request, 'error.html', {'message': 'No recipient found'})

    # Handle sending a new message
    if request.method == 'POST':
        message = request.POST.get('message')
        if message.strip():
            ChatMessage.objects.create(
                sender=request.user,
                receiver=receiver,
                message=message,
                is_read=False  # Newly sent messages are unread by default
            )
            return JsonResponse({'message': message})

    # Fetch chat messages between the logged-in user and the receiver
    messages = ChatMessage.objects.filter(
        sender__in=[request.user, receiver],
        receiver__in=[request.user, receiver]
    ).order_by('timestamp')

    # Mark messages as read when viewed
    unread_messages = messages.filter(receiver=request.user, is_read=False)
    unread_messages.update(is_read=True)

    # Fetch all users for chat selection (excluding the current user)
    users = User.objects.exclude(id=request.user.id)

    # Calculate unread messages count and get the latest message time for sorting
    unread_counts = {}
    user_last_message_time = {}

    for user in users:
        # Count unread messages from each user
        unread_counts[user.id] = ChatMessage.objects.filter(
            receiver=request.user, sender=user, is_read=False
        ).count()

        # Get the latest message timestamp with each user
        latest_message = ChatMessage.objects.filter(
            sender__in=[request.user, user],
            receiver__in=[request.user, user]
        ).order_by('-timestamp').first()

        if latest_message:
            user_last_message_time[user.id] = latest_message.timestamp
        else:
            # Use a timezone-aware minimum datetime for comparison
            user_last_message_time[user.id] = timezone.make_aware(datetime.min)

    # Sort users by the latest message timestamp (newest first)
    sorted_users = sorted(users, key=lambda u: user_last_message_time.get(u.id), reverse=True)

    return render(request, 'chat.html', {
        'messages': messages,
        'receiver': receiver,
        'users': sorted_users,  # Pass sorted users to the template
        'admin_user': admin_user,
        'unread_counts': unread_counts
    })



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from oman_app.models import ChatMessage, CustomUser

def admin_chat_list_view(request):
    if not request.user.is_superuser:
        return redirect('login')  # Redirect non-admin users

    # Fetch users who have interacted with the admin (sent or received messages)
    users_with_messages = CustomUser.objects.filter(
        received_messages__sender=request.user
    ).distinct()

    # Include users who have sent messages to the admin, in case there were no received messages
    users_with_messages = users_with_messages.union(
        CustomUser.objects.filter(sent_messages__receiver=request.user).distinct()
    )

    # Prepare chat list with users and their last message
    chat_list = []
    for user in users_with_messages:
        # Get the last message either from user to admin or admin to user
        last_message = ChatMessage.objects.filter(
            sender=user, receiver=request.user
        ).order_by('-timestamp').first()

        # If no messages from user to admin, get the latest message from admin to user
        if not last_message:
            last_message = ChatMessage.objects.filter(
                sender=request.user, receiver=user
            ).order_by('-timestamp').first()

        chat_list.append({'user': user, 'last_message': last_message})

    return render(request, 'admin1/admin_chat_list.html', {'chat_list': chat_list})



from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import ChatMessage
from django.contrib.auth.decorators import login_required

@login_required
def admin_chat_view(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    
    if request.method == 'POST':
        message = request.POST.get('message')
        if message:
            # Save the new message from the admin to the user
            ChatMessage.objects.create(sender=request.user, receiver=user, message=message)

            # Return the new message as part of the response for the AJAX
            return JsonResponse({'message': message, 'sender': 'sent', 'timestamp': 'Just now'})

    # Fetch all messages between admin and the user
    messages = ChatMessage.objects.filter(
        sender__in=[request.user, user],
        receiver__in=[request.user, user]
    ).order_by('timestamp')

    return render(request, 'admin1/admin_chat.html', {'messages': messages, 'user': user})

# mobiles by brand
def mobiles_by_brand(request, brand):
    # Filter mobiles by the selected brand
    mobiles_queryset = Mobile.objects.filter(status='approved', brand__iexact=brand)
    
    # Apply pagination
    paginator = Paginator(mobiles_queryset, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Convert images to JSON format for each mobile item
    for mobile in page_obj:
        mobile.images_json = json.dumps([image.image.url for image in mobile.images.all()])

    # Count items in each category
    category_counts = {
        'mobiles': Mobile.objects.filter(status='approved').count(),
        'computer' : Computer.objects.filter(status='approved').count(),
        'sounds' : Sound.objects.filter(status='approved').count(),
    }

    return render(request, 'mobiles_brand.html', {
        'mobiles': mobiles_queryset,  # Pass filtered mobiles
        'page_obj': page_obj,
        'brand': brand,
        'category_counts': category_counts
    })

def computer_by_brand(request, brand):
    # Filter computers by the selected brand
    computers_queryset = Computer.objects.filter(status='approved', brand__iexact=brand)
    
    # Apply pagination
    paginator = Paginator(computers_queryset, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Convert images to JSON format for each computer item
    for computer in page_obj:
        computer.images_json = json.dumps([image.image.url for image in computer.images.all()])

    # Count items in each category
    category_counts = {
        'mobiles': Mobile.objects.filter(status='approved').count(),
        'computer' : Computer.objects.filter(status='approved').count(),
        'sounds' : Sound.objects.filter(status='approved').count(),
    }

    return render(request, 'computer_brand.html', {
        'computers': computers_queryset,  # Pass filtered computers
        'page_obj': page_obj,
        'brand': brand,
        'category_counts': category_counts
    })

def sound_by_brand(request, brand):
    # Filter sounds by the selected brand
    sounds_queryset = Sound.objects.filter(status='approved', brand__iexact=brand)
    
    # Apply pagination
    paginator = Paginator(sounds_queryset, 6)  # Adjust the number as needed
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Convert images to JSON format for each sound item
    for sound in page_obj:
        sound.images_json = json.dumps([image.image.url for image in sound.images.all()])

    # Count items in each category
    category_counts = {
       'mobiles': Mobile.objects.filter(status='approved').count(),
        'computer' : Computer.objects.filter(status='approved').count(),
        'sounds' : Sound.objects.filter(status='approved').count(),
    }

    return render(request, 'sound_brand.html', {
        'sounds': sounds_queryset,  # Pass filtered sounds
        'page_obj': page_obj,
        'brand': brand,
        'category_counts': category_counts
    })

from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator
import json

from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator
import json

from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator
import json

def car(request):
    # Start with the base query for approved cars
    car_query = Automobile.objects.filter(status='approved')

    # Define a mapping of region codes to full names
    region_mapping = {
        'MS': 'Muscat',
        'DH': 'Dhofar',
        'BT': 'Batinah',
        'DA': 'Dakhiliyah',
        'SH': 'Sharqiyah',
        'BR': 'Buraimi',
        'ZU': 'Zufar',
        'DZ': 'Masandam',
        'WR': 'Wusta',
    }

    # Retrieve query parameters
    advertisement=Advertisement.objects.all()
    selected_region_code = request.GET.get('region')  # Get selected region code
    selected_city = request.GET.get('city')  # Get selected city
    name_query = request.GET.get('name', '')  # Get the search query (default is empty string)
    cities = request.GET.get('cities')  # Ensure this matches the name in your form
    make = request.GET.get('make')
    condition = request.GET.get('condition')
    trim = request.GET.get('trim')
    price_from = request.GET.get('price_from')  # Get the price from input
    price_to = request.GET.get('price_to')      # Get the price to input
    year_from = request.GET.get('year_from')    # Get the year from input
    year_to = request.GET.get('year_to')        # Get the year to input
    filters = request.GET.get('filters')
    listing_type = request.GET.get('listing_type')  # New parameter for rental/sell filtering

    # Additional filters
    fuel_type = request.GET.get('fuel_type')  # New parameter for fuel type
    engine_capacity = request.GET.get('engine_capacity')  # New parameter for engine capacity
    transmission = request.GET.get('transmission')  # New parameter for transmission type
    exterior_color = request.GET.get('exterior_color')  # New parameter for exterior color

    # Apply filters based on request parameters
    if selected_region_code:
        car_query = car_query.filter(regions__icontains=selected_region_code)

    if cities:
        car_query = car_query.filter(cities__iexact=cities) 

    if name_query:
        car_query = car_query.filter(
            Q(regions__icontains=name_query) |
            Q(cities__icontains=name_query) |
            Q(name__icontains=name_query) |
            Q(make__icontains=name_query) |
            Q(year__icontains=name_query)
        )

    if selected_city and selected_city != "All Cities":
        car_query = car_query.filter(cities__iexact=selected_city)
    if make:
        car_query = car_query.filter(make__icontains=make)  # Allow partial matches

    if trim and trim != 'Search Trim':
        car_query = car_query.filter(trim__iexact=trim)

    # Filter by listing type (sell or rent)
    if listing_type:
        car_query = car_query.filter(listing_type=listing_type)

    if condition:
        car_query = car_query.filter(condition=condition)

    # Price Range Filtering
    if price_from and price_to:
        car_query = car_query.filter(price__gte=price_from, price__lte=price_to)
    elif price_from:
        car_query = car_query.filter(price__gte=price_from)
    elif price_to:
        car_query = car_query.filter(price__lte=price_to)

    # Year Range Filtering
    if year_from and year_to:
        car_query = car_query.filter(year__gte=year_from, year__lte=year_to)
    elif year_from:
        car_query = car_query.filter(year__gte=year_from)
    elif year_to:
        car_query = car_query.filter(year__lte=year_to)

    # Additional Filters
    if fuel_type:
        car_query = car_query.filter(fuel_type=fuel_type)
    if engine_capacity:
        car_query = car_query.filter(engine_capacity__gte=engine_capacity)  # Assuming you want to filter by minimum capacity
    if transmission:
        car_query = car_query.filter(transmission=transmission)
    if exterior_color:
        car_query = car_query.filter(exterior_color__icontains=exterior_color)

    if filters:
        car_query = car_query.filter(name__icontains=filters)

    for car in car_query:
        car.images_json = json.dumps([image.image.url for image in car.images.all()])

    # Calculate category counts
    category_counts = {
        'motorcycles': Motorcycle.objects.filter(status='approved').count(),
        'automobiles_sell': Automobile.objects.filter(status='approved', listing_type='sell').count(),
        'automobiles_rent': Automobile.objects.filter(status='approved', listing_type='rent').count(),
        'heavy_vehicles': HeavyVehicle.objects.filter(status='approved').count(),
        'boats': Boat.objects.filter(status='approved').count(),
        'accessoriesparts': AutoAccessoryPart.objects.filter(status='approved').count(),
        'number_plate': NumberPlate.objects.filter(status='approved').count(),
    }

    # Pagination
    paginator = Paginator(car_query, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Prepare context for rendering the template
    context = {
        'car': car_query,
        'page_obj': page_obj,
        'category_counts': category_counts,
        'selected_region': region_mapping.get(selected_region_code, selected_region_code) if selected_region_code else None,  # Pass the full region name
        'selected_city': selected_city,  # Pass the selected city to the template
        'name_query': name_query,
        'cities': cities,
        'make': make,
        'trim': trim,
        'condition':condition,
        'price_from': price_from,
        'price_to': price_to,
        'year_from': year_from,
        'year_to': year_to,
        'filters': filters,
        'listing_type': listing_type,
        'fuel_type': fuel_type,
        'engine_capacity': engine_capacity,
        'transmission': transmission,
        'exterior_color': exterior_color,
         'advertisement':advertisement,
    }

    return render(request, 'car.html', context)

def car_details(request, id):
    car = get_object_or_404(Automobile, id=id)
    return render(request, 'car_details.html', {'car': car})

from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator
import json

def motorcycle(request):
    # Start with the base query for approved motorcycles
    motorcycle_query = Motorcycle.objects.filter(status='approved')

    # Define a mapping of region codes to full names
    region_mapping = {
        'MS': 'Muscat',
        'DH': 'Dhofar',
        'BT': 'Batinah',
        'DA': 'Dakhiliyah',
        'SH': 'Sharqiyah',
        'BR': 'Buraimi',
        'ZU': 'Zufar',
        'DZ': 'Masandam',
        'WR': 'Wusta',
    }

    # Get filter parameters from the request
    selected_region_code = request.GET.get('region')  # Get selected region code
    selected_city = request.GET.get('city')  # Get selected city
    name_query = request.GET.get('name', '')  
    cities = request.GET.get('cities')  
    make = request.GET.get('make')
    price_from = request.GET.get('price_from')  
    price_to = request.GET.get('price_to')      
    year_from = request.GET.get('year_from')    
    year_to = request.GET.get('year_to')        
    filters = request.GET.get('filters')

    # New Filters
    condition = request.GET.get('condition')  # 'new' or 'used'
    listing_type = request.GET.get('listing_type')  # 'sell' or 'rent'
    body_type = request.GET.get('body_type')  
    engine_capacity_from = request.GET.get('engine_capacity_from')  
    engine_capacity_to = request.GET.get('engine_capacity_to')
    sort_by = request.GET.get('sort_by')  # Sorting option

    # Apply filters
    if selected_region_code:
        motorcycle_query = motorcycle_query.filter(regions__icontains=selected_region_code)

    if name_query:
        motorcycle_query = motorcycle_query.filter(
            Q(regions__icontains=name_query) | 
            Q(cities__icontains=name_query) | 
            Q(name__icontains=name_query) | 
            Q(make__icontains=name_query) | 
            Q(year__icontains=name_query)
        )

    if cities:
        motorcycle_query = motorcycle_query.filter(cities__iexact=cities)  

    if make:
        motorcycle_query = motorcycle_query.filter(make__icontains=make)

    if condition:
        motorcycle_query = motorcycle_query.filter(condition=condition)

    if listing_type:
        motorcycle_query = motorcycle_query.filter(listing_type=listing_type)

    if body_type:
        motorcycle_query = motorcycle_query.filter(body_type__icontains=body_type)

    # Engine Capacity Range
    if engine_capacity_from and engine_capacity_to:
        motorcycle_query = motorcycle_query.filter(engine_capacity__gte=engine_capacity_from, engine_capacity__lte=engine_capacity_to)
    elif engine_capacity_from:
        motorcycle_query = motorcycle_query.filter(engine_capacity__gte=engine_capacity_from)
    elif engine_capacity_to:
        motorcycle_query = motorcycle_query.filter(engine_capacity__lte=engine_capacity_to)

    # Price Range Filtering
    if price_from and price_to:
        motorcycle_query = motorcycle_query.filter(price__gte=price_from, price__lte=price_to)
    elif price_from:
        motorcycle_query = motorcycle_query.filter(price__gte=price_from)
    elif price_to:
        motorcycle_query = motorcycle_query.filter(price__lte=price_to)

    # Year Range Filtering
    if year_from and year_to:
        motorcycle_query = motorcycle_query.filter(year__gte=year_from, year__lte=year_to)
    elif year_from:
        motorcycle_query = motorcycle_query.filter(year__gte=year_from)
    elif year_to:
        motorcycle_query = motorcycle_query.filter(year__lte=year_to)

    if filters:
        motorcycle_query = motorcycle_query.filter(name__icontains=filters)

    # Sorting
    if sort_by == 'price_low_to_high':
        motorcycle_query = motorcycle_query.order_by('price')
    elif sort_by == 'price_high_to_low':
        motorcycle_query = motorcycle_query.order_by('-price')
    elif sort_by == 'newest':
        motorcycle_query = motorcycle_query.order_by('-created_at')
    elif sort_by == 'oldest':
        motorcycle_query = motorcycle_query.order_by('created_at')

    # Calculate category counts
    category_counts = {
        'motorcycles': Motorcycle.objects.filter(status='approved').count(),
        'automobiles_sell': Automobile.objects.filter(status='approved', listing_type='sell').count(),
        'automobiles_rent': Automobile.objects.filter(status='approved', listing_type='rent').count(),
        'heavy_vehicles': HeavyVehicle.objects.filter(status='approved').count(),
        'boats': Boat.objects.filter(status='approved').count(),
        'accessoriesparts': AutoAccessoryPart.objects.filter(status='approved').count(),
        'number_plate': NumberPlate.objects.filter(status='approved').count(),
    }

    for motorcycle in motorcycle_query:
        motorcycle.images_json = json.dumps([image.image.url for image in motorcycle.images.all()])

    # Pagination
    paginator = Paginator(motorcycle_query, 6)  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)  

    # Prepare context for rendering the template
    context = {
        'motorcycle': motorcycle_query,
        'page_obj': page_obj,
        'category_counts': category_counts,
        'selected_region': region_mapping.get(selected_region_code, selected_region_code) if selected_region_code else None,  # Pass the full region name
        'selected_city': selected_city,  # Pass the selected city to the template
        'name_query': name_query,
        'cities': cities,
        'make': make,
        'price_from': price_from,
        'price_to': price_to,
        'year_from': year_from,
        'year_to': year_to,
        'filters': filters,
        'condition': condition,
        'listing_type': listing_type,
        'body_type': body_type,
        'engine_capacity_from': engine_capacity_from,
        'engine_capacity_to': engine_capacity_to,
        'sort_by': sort_by,
    }

    return render(request, 'motorcycle.html', context)

def motorcycle_details(request, id):
    motorcycle = get_object_or_404(Motorcycle, id=id)
    return render(request, 'motorcycle_details.html', {'motorcycle': motorcycle})

from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Q
from .models import HeavyVehicle, Motorcycle, Automobile  # Ensure you import your models
import json

def heavyvehicle(request):
    # Start with the base query for approved heavy vehicles
    heavyvehicle_query = HeavyVehicle.objects.filter(status='approved')

    # Define a mapping of region codes to full names
    region_mapping = {
        'MS': 'Muscat',
        'DH': 'Dhofar',
        'BT': 'Batinah',
        'DA': 'Dakhiliyah',
        'SH': 'Sharqiyah',
        'BR': 'Buraimi',
        'ZU': 'Zufar',
        'DZ': 'Masandam',
        'WR': 'Wusta',
    }

    # Get filter parameters from the request
    selected_region_code = request.GET.get('region')  # Get selected region code
    selected_city = request.GET.get('city')  # Get selected city
    name_query = request.GET.get('name', '')  # Get the search query (default is empty string)
    cities = request.GET.get('cities')  # Ensure this matches the name in your form
    manufacturer = request.GET.get('manufacturer')
    trim = request.GET.get('trim')
    price_from = request.GET.get('price_from')  # Get the price from input
    price_to = request.GET.get('price_to')      # Get the price to input
    year_from = request.GET.get('year_from')    # Get the year from input
    year_to = request.GET.get('year_to')        # Get the year to input
    filters = request.GET.get('filters')

    # Additional filters
    listing_type = request.GET.get('listing_type')  # Sell or Rent
    fuel_type = request.GET.get('fuel_type')        # Petrol, Diesel, Electric, Hybrid
    transmission_types = request.GET.getlist('transmission')  # List of selected transmission types
    conditions = request.GET.getlist('condition')  # List of selected conditions

    # Apply filters based on request parameters
    if selected_region_code:
        heavyvehicle_query = heavyvehicle_query.filter(regions__icontains=selected_region_code)

    if name_query:
        heavyvehicle_query = heavyvehicle_query.filter(
            Q(name__icontains=name_query) | 
            Q(manufacturer__icontains=name_query) | 
            Q(regions__icontains=name_query) | 
            Q(cities__icontains=name_query)
        )
            
    if cities:
        heavyvehicle_query = heavyvehicle_query.filter(cities__iexact=cities)  # Use the cities field for filtering
    if manufacturer:
        heavyvehicle_query = heavyvehicle_query.filter(manufacturer__icontains=manufacturer)
    if trim and trim != 'Search Trim':
        heavyvehicle_query = heavyvehicle_query.filter(trim__iexact=trim)

    # Price Range Filtering
    if price_from and price_to:
        heavyvehicle_query = heavyvehicle_query.filter(price__gte=price_from, price__lte=price_to)
    elif price_from:
        heavyvehicle_query = heavyvehicle_query.filter(price__gte=price_from)
    elif price_to:
        heavyvehicle_query = heavyvehicle_query.filter(price__lte=price_to)

    # Year Range Filtering
    if year_from and year_to:
        heavyvehicle_query = heavyvehicle_query.filter(year__gte=year_from, year__lte=year_to)
    elif year_from:
        heavyvehicle_query = heavyvehicle_query.filter(year__gte=year_from)
    elif year_to:
        heavyvehicle_query = heavyvehicle_query.filter(year__lte=year_to)

    # Apply additional filters
    if listing_type:
        heavyvehicle_query = heavyvehicle_query.filter(listing_type=listing_type)

    if fuel_type:
        heavyvehicle_query = heavyvehicle_query.filter(fuel_type=fuel_type)

    if transmission_types:
        heavyvehicle_query = heavyvehicle_query.filter(transmission__in=transmission_types)

    if conditions:
        heavyvehicle_query = heavyvehicle_query.filter(condition__in=conditions)

    if filters:
        heavyvehicle_query = heavyvehicle_query.filter(name__icontains=filters)

    # Prepare images for JSON
    for heavyvehicle in heavyvehicle_query:
        heavyvehicle.images_json = json.dumps([image.image.url for image in heavyvehicle.images.all()])

    # Calculate category counts
    category_counts = {
        'motorcycles': Motorcycle.objects.filter(status='approved').count(),
        'automobiles_sell': Automobile.objects.filter(status='approved', listing_type='sell').count(),
        'automobiles_rent': Automobile.objects.filter(status='approved', listing_type='rent').count(),
        'heavy_vehicles': HeavyVehicle.objects.filter(status='approved').count(),
         'boats': Boat.objects.filter(status='approved').count(),
        'accessoriesparts': AutoAccessoryPart.objects.filter(status='approved').count(),
        'number_plate': NumberPlate.objects.filter(status='approved').count(),
        # Add other categories as needed
    }
    
    # Pagination
    paginator = Paginator(heavyvehicle_query, 6)  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)  

    # Prepare context for rendering the template
    context = {
        'heavyvehicle': heavyvehicle_query,
        'page_obj': page_obj,
        'category_counts': category_counts,
        'selected_region': region_mapping.get(selected_region_code, selected_region_code) if selected_region_code else None,  # Pass the full region name
        'selected_city': selected_city,  # Pass the selected city to the template
        'name_query': name_query,
        'cities': cities,
        'manufacturer': manufacturer,
        'trim': trim,
        'price_from': price_from,
        'price_to': price_to,
        'year_from': year_from,
        'year_to': year_to,
        'filters': filters,
        'listing_type': listing_type,
        'fuel_type': fuel_type,
        'transmission_types': transmission_types,
        'conditions': conditions,
    }

    return render(request, 'heavyvehicle.html', context)


def heavyvehicle_details(request, id):
    heavyvehicle = get_object_or_404(HeavyVehicle, id=id)
    return render(request, 'heavyvehicle_details.html', {'heavyvehicle': heavyvehicle})

from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Q
from .models import AutoAccessoryPart, Motorcycle, Automobile, HeavyVehicle, Boat  # Ensure you import your models
import json

def accessoriesparts(request):
    # Start with the base query for approved accessories parts
    accessoriesparts_query = AutoAccessoryPart.objects.filter(status='approved')

    # Define a mapping of region codes to full names
    region_mapping = {
        'MS': 'Muscat',
        'DH': 'Dhofar',
        'BT': 'Batinah',
        'DA': 'Dakhiliyah',
        'SH': 'Sharqiyah',
        'BR': 'Buraimi',
        'ZU': 'Zufar',
        'DZ': 'Masandam',
        'WR': 'Wusta',
    }

    # Get filter parameters from the request
    selected_region_code = request.GET.get('region')  # Get selected region code
    selected_city = request.GET.get('city')  # Get selected city
    name_query = request.GET.get('name', '')  # Get the search query (default is empty string)
    cities = request.GET.get('cities')  # Ensure this matches the name in your form
    price_from = request.GET.get('price_from')  # Get the price from input
    price_to = request.GET.get('price_to')      # Get the price to input
    year_from = request.GET.get('year_from')    # Get the year from input
    year_to = request.GET.get('year_to')        # Get the year to input
    filters = request.GET.get('filters')

    # Apply filters based on request parameters
    if selected_region_code:
        accessoriesparts_query = accessoriesparts_query.filter(regions__icontains=selected_region_code)

    if name_query:
        accessoriesparts_query = accessoriesparts_query.filter(
            Q(name__icontains=name_query) | 
            Q(regions__icontains=name_query) | 
            Q(cities__icontains=name_query)
        )
            
    if cities:
        accessoriesparts_query = accessoriesparts_query.filter(cities__iexact=cities)  # Use the cities field for filtering

    # Price Range Filtering
    if price_from and price_to:
        accessoriesparts_query = accessoriesparts_query.filter(price__gte=price_from, price__lte=price_to)
    elif price_from:
        accessoriesparts_query = accessoriesparts_query.filter(price__gte=price_from)
    elif price_to:
        accessoriesparts_query = accessoriesparts_query.filter(price__lte=price_to)

    # Year Range Filtering
    if year_from and year_to:
        accessoriesparts_query = accessoriesparts_query.filter(year__gte=year_from, year__lte=year_to)
    elif year_from:
        accessoriesparts_query = accessoriesparts_query.filter(year__gte=year_from)
    elif year_to:
        accessoriesparts_query = accessoriesparts_query.filter(year__lte=year_to)

    if filters:
        accessoriesparts_query = accessoriesparts_query.filter(name__icontains=filters)

    # Prepare images for JSON
    for accessoriespart in accessoriesparts_query:
        accessoriespart.images_json = json.dumps([image.image.url for image in accessoriespart.images.all()])

    # Calculate category counts
    category_counts = {
        'motorcycles': Motorcycle.objects.filter(status='approved').count(),
        'automobiles_sell': Automobile.objects.filter(status='approved', listing_type='sell').count(),
        'automobiles_rent': Automobile.objects.filter(status='approved', listing_type='rent').count(),
        'heavy_vehicles': HeavyVehicle.objects.filter(status='approved').count(),
        'boats': Boat.objects.filter(status='approved').count(),
        'accessoriesparts': AutoAccessoryPart.objects.filter(status='approved').count(),
        'number_plate': NumberPlate.objects.filter(status='approved').count(),
    }

    # Pagination
    paginator = Paginator(accessoriesparts_query, 6)  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)  

    # Prepare context for rendering the template
    context = {
        'accessoriesparts': accessoriesparts_query,
        'page_obj': page_obj,
        'category_counts': category_counts,
        'selected_region': region_mapping.get(selected_region_code, selected_region_code) if selected_region_code else None,  # Pass the full region name
        'selected_city': selected_city,  # Pass the selected city to the template
        'name_query': name_query,
        'cities': cities,
        'price_from': price_from,
        'price_to': price_to,
        'year_from': year_from,
        'year_to': year_to,
        'filters': filters,
    }

    return render(request, 'accessoriesparts.html', context)

def accessoriesparts_details(request, id):
    accessoriesparts = get_object_or_404(AutoAccessoryPart, id=id)
    return render(request, 'accessoriesparts_details.html', {'accessoriesparts': accessoriesparts})



from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Q
from .models import Boat, Motorcycle, Automobile, HeavyVehicle, AutoAccessoryPart, NumberPlate  # Ensure you import your models
import json

from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Q
from .models import AutoAccessoryPart, Motorcycle, Automobile, HeavyVehicle, Boat  # Ensure you import your models
import json

def boat(request):
    # Start with the base query for approved boats
    boat_query = Boat.objects.filter(status='approved')

    # Define a mapping of region codes to full names
    region_mapping = {
        'MS': 'Muscat',
        'DH': 'Dhofar',
        'BT': 'Al Batinah',
        'DA': 'Al Dakhiliya',
        'SH': 'Al Sharqiya',
        'BR': 'Al Buraimi',
        'ZU': 'Al Dhahirah',
        'DZ': 'Musandam',
        'WR': 'Al Wusta',
    } 
    # Get filter parameters from the request
    selected_region_code = request.GET.get('region')  # Get selected region code
    selected_city = request.GET.get('city')  # Get selected city
    name_query = request.GET.get('name', '')  # Get the search query (default is empty string)
    cities = request.GET.get('cities')  # Ensure this matches the name in your form
    manufacturer = request.GET.get('manufacturer')
    price_from = request.GET.get('price_from')  # Get the price from input
    price_to = request.GET.get('price_to')      # Get the price to input
    year_from = request.GET.get('year_from')    # Get the year from input
    year_to = request.GET.get('year_to')        # Get the year to input
    filters = request.GET.get('filters')

    # Additional filters
    listing_type = request.GET.get('listing_type')  # Sell or Rent
    engine_type = request.GET.get('engine_type')    # Inboard or Outboard
    fuel_type = request.GET.get('fuel_type')        # Diesel or Petrol
    condition = request.GET.get('condition')          # New or Used

    # Apply filters based on request parameters
    if selected_region_code:
        boat_query = boat_query.filter(regions__icontains=selected_region_code)

    if name_query:
        boat_query = boat_query.filter(
            Q(name__icontains=name_query) | 
            Q(manufacturer__icontains=name_query) | 
            Q(year__icontains=name_query) | 
            Q(regions__icontains=name_query) | 
            Q(cities__icontains=name_query)
        )
            
    if cities:
        boat_query = boat_query.filter(cities__iexact=cities)  # Use the cities field for filtering
    if manufacturer:
        boat_query = boat_query.filter(manufacturer__icontains=manufacturer)

    # Price Range Filtering
    if price_from and price_to:
        boat_query = boat_query.filter(price__gte=price_from, price__lte=price_to)
    elif price_from:
        boat_query = boat_query.filter(price__gte=price_from)
    elif price_to:
        boat_query = boat_query.filter(price__lte=price_to)

    # Year Range Filtering
    if year_from and year_to:
        boat_query = boat_query.filter(year__gte=year_from, year__lte=year_to)
    elif year_from:
        boat_query = boat_query.filter(year__gte=year_from)
    elif year_to:
        boat_query = boat_query.filter(year__lte=year_to)

    # Apply additional filters
    if listing_type:
        boat_query = boat_query.filter(listing_type=listing_type)

    if engine_type:
        boat_query = boat_query.filter(engine_type=engine_type)

    if fuel_type:
        boat_query = boat_query.filter(fuel_type=fuel_type)

    if condition:
        boat_query = boat_query.filter(condition=condition)

    if filters:
        boat_query = boat_query.filter(name__icontains=filters)

    # Prepare images for JSON
    for boat in boat_query:
        boat.images_json = json.dumps([image.image.url for image in boat.images.all()])

    # Calculate category counts
    category_counts = {
        'motorcycles': Motorcycle.objects.filter(status='approved').count(),
        'automobiles_sell': Automobile.objects.filter(status='approved', listing_type='sell').count(),
        'automobiles_rent': Automobile.objects.filter(status='approved', listing_type='rent').count(),
        'heavy_vehicles': HeavyVehicle.objects.filter(status='approved').count(),
        'boats': Boat.objects.filter(status='approved').count(),
        'accessoriesparts': AutoAccessoryPart.objects.filter(status='approved').count(),
        'number_plate': NumberPlate.objects.filter(status='approved').count(),
    }
    
    # Pagination
    paginator = Paginator(boat_query, 6)  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)  

    # Prepare context for rendering the template
    context = {
        'boat': boat_query,
        'page_obj': page_obj,
        'category_counts': category_counts,
        'selected_region': region_mapping.get(selected_region_code, selected_region_code) if selected_region_code else None,  # Pass the full region name
        'selected_city': selected_city,  # Pass the selected city to the template
        'name_query': name_query,
        'cities': cities,
        'manufacturer': manufacturer,
        'price_from': price_from,
        'price_to': price_to,
        'year_from': year_from,
        'year_to': year_to,
        'filters': filters,
        'listing_type': listing_type,
        'engine_type': engine_type,
        'fuel_type': fuel_type,
        'condition': condition,
    }

    return render(request, 'boat.html', context)

def boat_details(request, id):
    boat = get_object_or_404(Boat, id=id)
    return render(request, 'boat_details.html', {'boat': boat})

def numberplate(request):
    # Start with the base query for approved number plates
    numberplate_query = NumberPlate.objects.filter(status='approved')

    # Define a mapping of region codes to full names
    region_mapping = {
        'MS': 'Muscat',
        'DH': 'Dhofar',
        'BT': 'Al Batinah',
        'DA': 'Al Dakhiliya',
        'SH': 'Al Sharqiya',
        'BR': 'Al Buraimi',
        'ZU': 'Al Dhahirah',
        'DZ': 'Masandam',
        'WR': 'Al Wusta',
    }

    # Get filter parameters from the request
    selected_region_code = request.GET.get('region')  # Get selected region code
    selected_city = request.GET.get('city')  # Get selected city
    name_query = request.GET.get('name', '')  # Get the search query (default is empty string)
    number = request.GET.get('number')  # Filter by number
    digit_filter = request.GET.get('digit_filter') 
    selected_letters = request.GET.getlist('letter_english')  # Get list of selected letters
    letter_arabic = request.GET.get('letter_arabic')  # Filter by Arabic letter
    plate_type = request.GET.get('plate_type')  # Filter by plate type
    listing_type = request.GET.get('listing_type')  # Filter by listing type
    price_from = request.GET.get('price_from')  # Get the price from input
    price_to = request.GET.get('price_to')  # Get the price to input
    filters = request.GET.get('filters')  # General filter (not used in code, optional)

    # Apply filters based on request parameters
    if selected_region_code:
        numberplate_query = numberplate_query.filter(regions__icontains=selected_region_code)

    if selected_city:
        numberplate_query = numberplate_query.filter(cities__icontains=selected_city)

    if selected_letters:
        selected_letters = [letter.upper() for letter in selected_letters]  # Ensure case consistency
        numberplate_query = numberplate_query.filter(letter_english__in=selected_letters)

    if name_query:
        numberplate_query = numberplate_query.filter(
            Q(number__icontains=name_query) |
            Q(letter_english__icontains=name_query) |
            Q(letter_arabic__icontains=name_query) |
            Q(regions__icontains=name_query) |
            Q(cities__icontains=name_query)
        )

    if number:
        numberplate_query = numberplate_query.filter(number__iexact=number)

    # Handle digit filter
    if digit_filter:
        if digit_filter == 'single':
            numberplate_query = numberplate_query.filter(number__regex=r'^\d{1}$')
        elif digit_filter == 'double':
            numberplate_query = numberplate_query.filter(number__regex=r'^\d{2}$')
        elif digit_filter == 'triple':
            numberplate_query = numberplate_query.filter(number__regex=r'^\d{3}$')
        elif digit_filter == 'quadruple':
            numberplate_query = numberplate_query.filter(number__regex=r'^\d{4}$')
        elif digit_filter == 'quintuple':
            numberplate_query = numberplate_query.filter(number__regex=r'^\d{5}$')

    if letter_arabic:
        numberplate_query = numberplate_query.filter(letter_arabic__iexact=letter_arabic)

    if plate_type:
        numberplate_query = numberplate_query.filter(plate_type__iexact=plate_type)

    if listing_type:
        numberplate_query = numberplate_query.filter(listing_type__iexact=listing_type)

    # Price Range Filtering
    if price_from and price_to:
        numberplate_query = numberplate_query.filter(price__gte=price_from, price__lte=price_to)
    elif price_from:
        numberplate_query = numberplate_query.filter(price__gte=price_from)
    elif price_to:
        numberplate_query = numberplate_query.filter(price__lte=price_to)

    # Calculate category counts
    category_counts = {
        'motorcycles': Motorcycle.objects.filter(status='approved').count(),
        'automobiles_sell': Automobile.objects.filter(status='approved', listing_type='sell').count(),
        'automobiles_rent': Automobile.objects.filter(status='approved', listing_type='rent').count(),
        'heavy_vehicles': HeavyVehicle.objects.filter(status='approved').count(),
        'boats': Boat.objects.filter(status='approved').count(),
        'accessoriesparts': AutoAccessoryPart.objects.filter(status='approved').count(),
        'number_plate': NumberPlate.objects.filter(status='approved').count(),
    }

    # Pagination
    paginator = Paginator(numberplate_query, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Prepare context for rendering the template
    context = {
        'numberplate': numberplate_query,
        'page_obj': page_obj,
        'category_counts': category_counts,
        'selected_region': region_mapping.get(selected_region_code, selected_region_code) if selected_region_code else None,
        'selected_city': selected_city,
        'name_query': name_query,
        'number': number,
        'selected_letters': selected_letters,  # Pass selected letters to the template
        'letter_arabic': letter_arabic,
        'plate_type': plate_type,
        'listing_type': listing_type,
        'price_from': price_from,
        'price_to': price_to,
        'filters': filters,
    }

    return render(request, 'numberplate.html', context)


def numberplate_details(request, id):
    numberplate = get_object_or_404(NumberPlate, id=id)
    return render(request, 'numberplate_details.html', {'numberplate': numberplate})

def browseads11(request, category, id):
    # Update the mapping to include the specific categories
    ad_model_mapping = {
        'Automobile': Automobile,
        'Motorcycle': Motorcycle,
        'Heavy_vehicle': HeavyVehicle,
        'Boat': Boat,
        'Accessoriespart': AutoAccessoryPart,
     
        
     
        
    }
    print(Automobile.objects.filter(id=6).exists())
    print(Motorcycle.objects.filter(id=6).exists())
    print(HeavyVehicle.objects.filter(id=6).exists())
    # Adjust for 'Motors' category and map it to relevant categories
    if category == 'Motors':
        print(f"Category: {category}")

        categories = ['Automobile', 'Motorcycle', 'Heavy_vehicle', 'Boat' , 'Accessoriespart' ]  # Include both automobile and motorcycle
        print(f"Categories to check: {categories}")

    else:
        categories = [category]  # Use the given category directly

    # Initialize ad variable
    ad = None
    
    # Loop through the categories to find the corresponding ad
    for cat in categories:
        ad_model = ad_model_mapping.get(cat)
        if ad_model:
            try:
                ad = ad_model.objects.get(id=id)  # Fetch the ad
                break  # Exit the loop once the ad is found
            except ad_model.DoesNotExist:
                continue

    # Initialize the features list
    features = []

    if ad:
        # Add common features
        features.append(('Price', f"OMR {ad.price}"))
        features.append(('Location', ad.location))
        
        # Add product-type-specific features based on the actual category
        if isinstance(ad, Automobile):
            features += [
                ('Make', ad.make),
                ('Model', ad.name),
                ('Year', ad.year),
                ('Body Type', ad.body_type),
                ('Fuel Type', ad.fuel_type),
                ('Engine Capacity', f"{ad.engine_capacity} cc"),
                ('Transmission', ad.transmission),
                ('Exterior Color', ad.exterior_color),
                ('Warranty Status', ad.warranty_status),
                ('Condition', ad.condition),
                ('Listing', ad.listing_type)
            ]
        elif isinstance(ad, Motorcycle):
            features += [
                ('Make', ad.make),
                ('Model', ad.name),
                ('Year', ad.year),
                ('Body Type', ad.body_type),
                ('Engine Capacity', f"{ad.engine_capacity} cc"),
                ('Condition', ad.condition),
                ('Listing', ad.listing_type)
            ]
        elif isinstance(ad, HeavyVehicle):
            features += [
                ('Manufacturer', ad.manufacturer),
                ('Year', ad.year),
                ('Fuel Type', ad.fuel_type),
                ('Engine Capacity', f"{ad.engine_capacity} cc"),
                ('Transmission', ad.transmission),
                ('Load Capacity', f"{ad.load_capacity} tons"),
                ('Condition', ad.condition),
                ('Listing', ad.listing_type),
                ('Mileage', f"{ad.mileage} Km")
            ]
        elif isinstance(ad, Boat):
            features += [
                ('Manufacturer', ad.manufacturer),
                ('Year', ad.year),
                ('Length', f"{ad.length} meters"),
                ('Engine Type', ad.engine_type),
                ('Engine Power', f"{ad.engine_power} HP"),
                ('Fuel Type', ad.fuel_type),
                ('Condition', ad.condition),
                ('Listing', ad.listing_type),
            ]
        elif isinstance(ad, AutoAccessoryPart):
            features += [
                ('Part Type', ad.name),
                ('Listing', ad.listing_type),
            ]
        elif isinstance(ad, NumberPlate):
            features += [
                ('Number Plate Type', ad.number),
                ('Listing', ad.listing_type),
                
            ]
                

    return render(request, 'browse-ads-11.html', {'ad': ad, 'features': features})

from django.contrib.auth import get_user_model
@login_required
def edit_company(request, user_id, company_id):
    User = get_user_model()  # Resolve the AUTH_USER_MODEL to the actual user model
    user = get_object_or_404(User, id=user_id)
    company = get_object_or_404(Company, id=company_id, user=user)

    if request.method == 'POST':
        form = CompanyRegistrationForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            form.save()
            messages.success(request, "Company details updated successfully.")
            return redirect('company_dashboard', user_id=user.id, company_id=company.id)
    else:
        form = CompanyRegistrationForm(instance=company)

    return render(request, 'edit_company.html', {'form': form, 'company': company})


def delete_company(request, company_id):
    if request.method == 'DELETE':
        try:
            company = Company.objects.get(id=company_id)
            company.delete()
            # Redirect to the "We Are Hiring" page
            return redirect(we_are_hiring)  # Adjust 'we_are_hiring' with your URL name
        except Company.DoesNotExist:
            return JsonResponse({'error': 'Company not found.'}, status=404)
    return JsonResponse({'error': 'Invalid request method.'}, status=400)


def company_list_view(request):
    # Fetch all companies to display in the list
    companies = Company.objects.all()

    # Render the company list template
    return render(request, 'admin1/company/company.html', {'companies': companies})




from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Automobile

def car_make(request, make):
    # Start with the base query for approved cars of the specified make
    automobiles = Automobile.objects.filter(status='approved', make__iexact=make)

    # Retrieve query parameters
    selected_region = request.GET.get('region')
    name_query = request.GET.get('name', '')  # Get the search query (default is empty string)
    cities = request.GET.get('cities')  # Ensure this matches the name in your form
    trim = request.GET.get('trim')
    price_from = request.GET.get('price_from')  # Get the price from input
    price_to = request.GET.get('price_to')      # Get the price to input
    year_from = request.GET.get('year_from')    # Get the year from input
    year_to = request.GET.get('year_to')        # Get the year to input
    filters = request.GET.get('filters')
    listing_type = request.GET.get('listing_type')  # New parameter for rental/sell filtering

    # Apply filters based on request parameters
    if selected_region:
        automobiles = automobiles.filter(regions__icontains=selected_region)

    if name_query:
        automobiles = automobiles.filter(
            Q(regions__icontains=name_query) |
            Q(cities__icontains=name_query) |
            Q(name__icontains=name_query) |
            Q(make__icontains=name_query) |
            Q(year__icontains=name_query)
        )

    if cities:
        automobiles = automobiles.filter(cities__iexact=cities)
    if trim and trim != 'Search Trim':
        automobiles = automobiles.filter(trim__iexact=trim)

    # Filter by listing type (sell or rent)
    if listing_type:
        automobiles = automobiles.filter(listing_type=listing_type)

    # Price Range Filtering
    if price_from and price_to:
        automobiles = automobiles.filter(price__gte=price_from, price__lte=price_to)
    elif price_from:
        automobiles = automobiles.filter(price__gte=price_from)
    elif price_to:
        automobiles = automobiles.filter(price__lte=price_to)

    # Year Range Filtering
    if year_from and year_to:
        automobiles = automobiles.filter(year__gte=year_from, year__lte=year_to)
    elif year_from:
        automobiles = automobiles.filter(year__gte=year_from)
    elif year_to:
        automobiles = automobiles.filter(year__lte=year_to)

    if filters:
        automobiles = automobiles.filter(name__icontains=filters)

    for car in automobiles:  # Use 'automobiles' instead of 'car_query'
        car.images_json = json.dumps([image.image.url for image in car.images.all()])

    # Calculate category counts
    category_counts = {
        'motorcycles': Motorcycle.objects.filter(status='approved').count(),
        'automobiles_sell': Automobile.objects.filter(status='approved', listing_type='sell').count(),
        'automobiles_rent': Automobile.objects.filter(status='approved', listing_type='rent').count(),
        'heavy_vehicles': HeavyVehicle.objects.filter(status='approved').count(),
        'boats': Boat.objects.filter(status='approved').count(),
        'accessoriesparts': AutoAccessoryPart.objects.filter(status='approved').count(),
        'number_plate': NumberPlate.objects.filter(status='approved').count(),
    }

    # Apply pagination
    paginator = Paginator(automobiles, 6)  # Adjust the number of items per page as needed
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Prepare context for rendering the template
    context = {
        'automobiles': automobiles,  # Pass the non-paginated queryset if needed
        'page_obj': page_obj,  # Pass the paginated queryset
        'make': make,  # The make being filtered
        'category_counts': category_counts,
        'selected_region': selected_region,
        'name_query': name_query,
        'cities': cities,
        'trim': trim,
        'price_from': price_from,
        'price_to': price_to,
        'year_from': year_from,
        'year_to': year_to,
        'filters': filters,
        'listing_type': listing_type,
    }

    return render(request, 'car_make.html', context)

from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from oman_app.models import Motorcycle  # Adjust the import path to match your project

def motorcycle_make(request, make):
    # Start with the base query for approved motorcycles of the specified make
    motorcycles = Motorcycle.objects.filter(status='approved', make__iexact=make)

    # Retrieve query parameters
    selected_region = request.GET.get('region')
    name_query = request.GET.get('name', '')  # Get the search query (default is empty string)
    cities = request.GET.get('cities')  # Ensure this matches the name in your form
    trim = request.GET.get('trim')
    price_from = request.GET.get('price_from')  # Get the price from input
    price_to = request.GET.get('price_to')      # Get the price to input
    year_from = request.GET.get('year_from')    # Get the year from input
    year_to = request.GET.get('year_to')        # Get the year to input
    filters = request.GET.get('filters')
    listing_type = request.GET.get('listing_type')  # New parameter for rental/sell filtering

    # Apply filters based on request parameters
    if selected_region:
        motorcycles = motorcycles.filter(regions__icontains=selected_region)

    if name_query:
        motorcycles = motorcycles.filter(
            Q(name__icontains=name_query) |
            Q(make__icontains=name_query) |
            Q(year__icontains=name_query)
        )

    if cities:
        motorcycles = motorcycles.filter(cities__iexact=cities)
    if trim and trim != 'Search Trim':
        motorcycles = motorcycles.filter(trim__iexact=trim)

    # Filter by listing type (sell or rent)
    if listing_type:
        motorcycles = motorcycles.filter(listing_type=listing_type)

    # Price Range Filtering
    if price_from and price_to:
        motorcycles = motorcycles.filter(price__gte=price_from, price__lte=price_to)
    elif price_from:
        motorcycles = motorcycles.filter(price__gte=price_from)
    elif price_to:
        motorcycles = motorcycles.filter(price__lte=price_to)

    # Year Range Filtering
    if year_from and year_to:
        motorcycles = motorcycles.filter(year__gte=year_from, year__lte=year_to)
    elif year_from:
        motorcycles = motorcycles.filter(year__gte=year_from)
    elif year_to:
        motorcycles = motorcycles.filter(year__lte=year_to)

    if filters:
        motorcycles = motorcycles.filter(name__icontains=filters)

    for motorcycle in motorcycles:  # Use 'motorcycles' instead of 'car_query'
        motorcycle.images_json = json.dumps([image.image.url for image in motorcycle.images.all()])

    # Calculate category counts
    category_counts = {
        'motorcycles': Motorcycle.objects.filter(status='approved').count(),
        'automobiles_sell': Automobile.objects.filter(status='approved', listing_type='sell').count(),
        'automobiles_rent': Automobile.objects.filter(status='approved', listing_type='rent').count(),
        'heavy_vehicles': HeavyVehicle.objects.filter(status='approved').count(),
        'boats': Boat.objects.filter(status='approved').count(),
        'accessoriesparts': AutoAccessoryPart.objects.filter(status='approved').count(),
        'number_plate': NumberPlate.objects.filter(status='approved').count(),
    }

    # Apply pagination
    paginator = Paginator(motorcycles, 10)  # Show 10 motorcycles per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # Prepare context for rendering the template
    context = {
        'page_obj': page_obj,
        'make': make,  # The make being filtered
        'category_counts': category_counts,
        'selected_region': selected_region,
        'name_query': name_query,
        'cities': cities,
        'trim': trim,
        'price_from': price_from,
        'price_to': price_to,
        'year_from': year_from,
        'year_to': year_to,
        'filters': filters,
        'listing_type': listing_type,
    }

    return render(request, 'bike_make.html', context)


from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Q
from .models import HeavyVehicle, Motorcycle, Automobile  # Ensure you import your models

def heavy_vehicle_manufacturer(request, manufacturer):
    # Start with the base query for approved heavy vehicles of the specified manufacturer
    heavy_vehicles = HeavyVehicle.objects.filter(status='approved', manufacturer__iexact=manufacturer)

    # Retrieve query parameters
    selected_region = request.GET.get('region')
    name_query = request.GET.get('name', '')  # Get the search query (default is empty string)
    cities = request.GET.get('cities')  # Ensure this matches the name in your form
    trim = request.GET.get('trim')
    price_from = request.GET.get('price_from')  # Get the price from input
    price_to = request.GET.get('price_to')      # Get the price to input
    year_from = request.GET.get('year_from')    # Get the year from input
    year_to = request.GET.get('year_to')        # Get the year to input
    filters = request.GET.get('filters')

    # Apply filters based on request parameters
    if selected_region:
        heavy_vehicles = heavy_vehicles.filter(regions__icontains=selected_region)

    if name_query:
        heavy_vehicles = heavy_vehicles.filter(
            Q(name__icontains=name_query) | 
            Q(regions__icontains=name_query) | 
            Q(cities__icontains=name_query)
        )
            
    if cities:
        heavy_vehicles = heavy_vehicles.filter(cities__iexact=cities)  # Use the cities field for filtering
    if trim and trim != 'Search Trim':
        heavy_vehicles = heavy_vehicles.filter(trim__iexact=trim)

    # Price Range Filtering
    if price_from and price_to:
        heavy_vehicles = heavy_vehicles.filter(price__gte=price_from, price__lte=price_to)
    elif price_from:
        heavy_vehicles = heavy_vehicles.filter(price__gte=price_from)
    elif price_to:
        heavy_vehicles = heavy_vehicles.filter(price__lte=price_to)

    # Year Range Filtering
    if year_from and year_to:
        heavy_vehicles = heavy_vehicles.filter(year__gte=year_from, year__lte=year_to)
    elif year_from:
        heavy_vehicles = heavy_vehicles.filter(year__gte=year_from)
    elif year_to:
        heavy_vehicles = heavy_vehicles.filter(year__lte=year_to)

    if filters:
        heavy_vehicles = heavy_vehicles.filter(name__icontains=filters)

    for vehicle in heavy_vehicles:  # Iterate over the queryset
        vehicle.images_json = json.dumps([image.image.url for image in vehicle.images.all()])

    # Calculate category counts
    category_counts = {
        'motorcycles': Motorcycle.objects.filter(status='approved').count(),
        'automobiles_sell': Automobile.objects.filter(status='approved', listing_type='sell').count(),
        'automobiles_rent': Automobile.objects.filter(status='approved', listing_type='rent').count(),
        'heavy_vehicles': HeavyVehicle.objects.filter(status='approved').count(),
        'boats': Boat.objects.filter(status='approved').count(),
        'accessoriesparts': AutoAccessoryPart.objects.filter(status='approved').count(),
        'number_plate': NumberPlate.objects.filter(status='approved').count(),
    }

    # Paginate the queryset
    paginator = Paginator(heavy_vehicles, 10)  # Show 10 heavy vehicles per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # Prepare context for rendering the template
    context = {
        'page_obj': page_obj,
        'manufacturer': manufacturer,  # The manufacturer being filtered
        'category_counts': category_counts,
        'selected_region': selected_region,
        'name_query': name_query,
        'cities': cities,
        'trim': trim,
        'price_from': price_from,
        'price_to': price_to,
        'year_from': year_from,
        'year_to': year_to,
        'filters': filters,
    }

    return render(request, 'heavy_vehicle_type.html', context)
from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Q
from .models import Boat, Motorcycle, Automobile, HeavyVehicle, AutoAccessoryPart, NumberPlate  # Ensure you import your models
import json

def boat_manufacturer(request, manufacturer):
    # Start with the base query for approved boats of the specified manufacturer
    boats = Boat.objects.filter(status='approved', manufacturer__iexact=manufacturer)

    # Retrieve query parameters
    selected_region = request.GET.get('region')
    name_query = request.GET.get('name', '')  # Get the search query (default is empty string)
    cities = request.GET.get('cities')  # Ensure this matches the name in your form
    trim = request.GET.get('trim')
    price_from = request.GET.get('price_from')  # Get the price from input
    price_to = request.GET.get('price_to')      # Get the price to input
    year_from = request.GET.get('year_from')    # Get the year from input
    year_to = request.GET.get('year_to')        # Get the year to input
    filters = request.GET.get('filters')

    # Apply filters based on request parameters
    if selected_region:
        boats = boats.filter(regions__icontains=selected_region)

    if name_query:
        boats = boats.filter(
            Q(name__icontains=name_query) | 
            Q(manufacturer__icontains=name_query) | 
            Q(regions__icontains=name_query) | 
            Q(cities__icontains=name_query)
        )
            
    if cities:
        boats = boats.filter(cities__iexact=cities)  # Use the cities field for filtering
    if trim and trim != 'Search Trim':
        boats = boats.filter(trim__iexact=trim)

    # Price Range Filtering
    if price_from and price_to:
        boats = boats.filter(price__gte=price_from, price__lte=price_to)
    elif price_from:
        boats = boats.filter(price__gte=price_from)
    elif price_to:
        boats = boats.filter(price__lte=price_to)

    # Year Range Filtering
    if year_from and year_to:
        boats = boats.filter(year__gte=year_from, year__lte=year_to)
    elif year_from:
        boats = boats.filter(year__gte=year_from)
    elif year_to:
        boats = boats.filter(year__lte=year_to)

    if filters:
        boats = boats.filter(name__icontains=filters)

    for boat in boats:  # Iterate over the queryset
        boat.images_json = json.dumps([image.image.url for image in boat.images.all()])

    # Calculate category counts
    category_counts = {
        'motorcycles': Motorcycle.objects.filter(status='approved').count(),
        'automobiles_sell': Automobile.objects.filter(status='approved', listing_type='sell').count(),
        'automobiles_rent': Automobile.objects.filter(status='approved', listing_type='rent').count(),
        'heavy_vehicles': HeavyVehicle.objects.filter(status='approved').count(),
        'boats': Boat.objects.filter(status='approved').count(),
        'accessoriesparts': AutoAccessoryPart.objects.filter(status='approved').count(),
        'number_plate': NumberPlate.objects.filter(status='approved').count(),
    }

    # Paginate the queryset
    paginator = Paginator(boats, 10)  # Show 10 boats per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # Prepare context for rendering the template
    context = {
        'page_obj': page_obj,
        'manufacturer': manufacturer,  # The manufacturer being filtered
        'category_counts': category_counts,
        'selected_region': selected_region,
        'name_query': name_query,
        'cities': cities,
        'trim': trim,
        'price_from': price_from,
        'price_to': price_to,
        'year_from': year_from,
        'year_to': year_to,
        'filters': filters,
    }

    return render(request, 'boat_type.html', context)

from django.shortcuts import render
from .forms import ImageUploadForm
from .models import UploadedImage
from PIL import Image as PILImage, ImageFilter
import pytesseract
import re
from pyproj import Proj, Transformer

def upload_image(request):
    # Define a mapping of region codes to full names
    region_mapping = {
        'MS': 'Muscat',
        'DH': 'Dhofar',
        'BT': 'Batinah',
        'DA': 'Dakhiliyah',
        'SH': 'Sharqiyah',
        'BR': 'Buraimi',
        'ZU': 'Zufar',
        'DZ': 'Masandam',
        'WR': 'Wusta',
    }

    # Count items in each category
    category_counts = {
        'villa': Villa.objects.filter(status='approved').count(),
        'land': Land.objects.filter(status='approved').count(),
        'commercial': Commercial.objects.filter(status='approved').count(),
        'chalet': Chalet.objects.filter(status='approved').count(),
        'farm': Farm.objects.filter(status='approved').count(),
        'automobiles': Automobile.objects.filter(status='approved').count(),
        'motorcycle': Motorcycle.objects.filter(status='approved').count(),
        'heavyvehicle': HeavyVehicle.objects.filter(status='approved').count(),
        'boat': Boat.objects.filter(status='approved').count(),
        'accessoriesparts': AutoAccessoryPart.objects.filter(status='approved').count(),
        'numberplate': NumberPlate.objects.filter(status='approved').count(),
        'education': Education.objects.filter(status='approved').count(),
        'business': Business.objects.filter(status='approved').count(),
        'services': Service.objects.filter(status='approved').count(),
        'mobile': Mobile.objects.filter(status='approved').count(),
        'computer': Computer.objects.filter(status='approved').count(),
        'sound': Sound.objects.filter(status='approved').count(),
        'fashion': Fashion.objects.filter(status='approved').count(),
        'toys': Toys.objects.filter(status='approved').count(),
        'foods': Food.objects.filter(status='approved').count(),
        'fitness': Fitness.objects.filter(status='approved').count(),
        'pets': Pet.objects.filter(status='approved').count(),
        'books': Book.objects.filter(status='approved').count(),
        'appliances': Appliance.objects.filter(status='approved').count(),
    }

    # Get filter parameters from the request
    selected_category = request.GET.get('category')

    # Define categories and their models
    categories = {
        'lands': Land,
        'villas': Villa,
        'commercials': Commercial,
        'farms': Farm,
        'chalets': Chalet,
        'automobiles': Automobile,
        'motorcycle': Motorcycle,
        'heavyvehicle': HeavyVehicle,
        'boat': Boat,
        'accessoriesparts': AutoAccessoryPart,
        'numberplate': NumberPlate,
        'education': Education,
        'business': Business,
        'services': Service,
        'mobile': Mobile,
        'computer': Computer,
        'sound': Sound,
        'fashion': Fashion,
        'toys': Toys,
        'foods': Food,
        'fitness': Fitness,
        'pets': Pet,
        'books': Book,
        'appliances': Appliance,
    }

    # Initialize ads list
    all_ads = []

    # Filter based on selected region, city, category, and listing type
    for category_name, model in categories.items():
        if selected_category and category_name.lower() != selected_category.lower():
            continue  # Skip if the category does not match

        # Start filtering the model
        query = model.objects.filter(status='approved')

        # Fetch the latest items
        items = query.order_by('-id')

        for item in items:
           
            all_ads.append({
                'category': category_name.capitalize(),
                'data': item,
                'product_type': category_name.lower(),
                'region_name': region_mapping.get(item.regions, item.regions),
            })

    context = {
        'all_ads': all_ads,
        'category_counts': category_counts,
        'selected_category': selected_category,
        'property_locations': json.dumps([
            {
                'lat': ad['data'].latitude,
                'lng': ad['data'].longitude,
                'category': ad['product_type'].capitalize(),
                'url': reverse('browseads2', kwargs={'category': ad['product_type'].capitalize(), 'id': ad['data'].id})
            } for ad in all_ads if ad['data'].latitude and ad['data'].longitude
        ]),
    }

    return render(request, 'uploader/upload.html', context)

from .forms import DrivingTrainingForm
from django.shortcuts import render, redirect
from .forms import DrivingTrainingForm
from .models import DrivingTrainingImage
from django.contrib.auth.decorators import login_required

@login_required
def register_driving_training(request):
    if request.method == "POST":
        form = DrivingTrainingForm(request.POST, request.FILES)
        files = request.FILES.getlist("images")  # Get multiple uploaded images

        if form.is_valid():
            training = form.save(commit=False)
            training.user = request.user
            training.save()

            # Save images separately
            for file in files:
                image_instance = DrivingTrainingImage.objects.create(image=file)
                training.images.add(image_instance)  # Add image to ManyToManyField
            
            return redirect(adss, user_id=request.user.id)  # Redirect after success

    else:
        form = DrivingTrainingForm()

    return render(request, "drive.html", {"form": form})

def driving_training(request):
    # Start with the base query for approved driving training listings
    driving_query = DrivingTraining.objects.filter(status='approved')

    # Define a mapping of region codes to full names
    region_mapping = {
        'MS': 'Muscat',
        'DH': 'Dhofar',
        'BT': 'Batinah',
        'DA': 'Dakhiliyah',
        'SH': 'Sharqiyah',
        'BR': 'Buraimi',
        'ZU': 'Zufar',
        'DZ': 'Masandam',
        'WR': 'Wusta',
    }

    # Get filter parameters from the request
    selected_region_code = request.GET.get('region')  # Get selected region code
    selected_city = request.GET.get('city')  # Get selected city
    name_query = request.GET.get('name', '')  # Get the search query (default is empty string)
    cities = request.GET.get('cities')  # Ensure this matches the name in your form
    price_from = request.GET.get('price_from')  # Get the price from input
    price_to = request.GET.get('price_to')      # Get the price to input
    year_from = request.GET.get('year_from')    # Get the year from input
    year_to = request.GET.get('year_to')        # Get the year to input
    filters = request.GET.get('filters')

    # Apply filters based on request parameters
    if selected_region_code:
        driving_query = driving_query.filter(regions__icontains=selected_region_code)

    if name_query:
        driving_query = driving_query.filter(
            Q(title__icontains=name_query) |  # Assuming title is a field in the DrivingTraining model
            Q(regions__icontains=name_query) | 
            Q(cities__icontains=name_query)
        )
            
    if cities:
        driving_query = driving_query.filter(cities__iexact=cities)  # Use the cities field for filtering

    # Price Range Filtering
    if price_from and price_to:
        driving_query = driving_query.filter(price__gte=price_from, price__lte=price_to)
    elif price_from:
        driving_query = driving_query.filter(price__gte=price_from)
    elif price_to:
        driving_query = driving_query.filter(price__lte=price_to)

    # Year Range Filtering
    if year_from and year_to:
        driving_query = driving_query.filter(year__gte=year_from, year__lte=year_to)
    elif year_from:
        driving_query = driving_query.filter(year__gte=year_from)
    elif year_to:
        driving_query = driving_query.filter(year__lte=year_to)

    if filters:
        driving_query = driving_query.filter(title__icontains=filters)  # Filtering based on title

    # Calculate category counts
    category_counts = {
        'motorcycles': Motorcycle.objects.filter(status='approved').count(),
        'automobiles_sell': Automobile.objects.filter(status='approved', listing_type='sell').count(),
        'automobiles_rent': Automobile.objects.filter(status='approved', listing_type='rent').count(),
        'heavy_vehicles': HeavyVehicle.objects.filter(status='approved').count(),
        'boats': Boat.objects.filter(status='approved').count(),
        'accessoriesparts': AutoAccessoryPart.objects.filter(status='approved').count(),
        'number_plate': NumberPlate.objects.filter(status='approved').count(),
        'driving_training': DrivingTraining.objects.filter(status='approved').count(),
    }
    
    # Pagination
    paginator = Paginator(driving_query, 6)  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)  

    # Prepare context for rendering the template
    context = {
        'driving_training': driving_query,
        'page_obj': page_obj,
        'category_counts': category_counts,
        'selected_region': region_mapping.get(selected_region_code, selected_region_code) if selected_region_code else None,  # Pass the full region name
        'selected_city': selected_city,  # Pass the selected city to the template
        'name_query': name_query,
        'cities': cities,
        'price_from': price_from,
        'price_to': price_to,
        'year_from': year_from,
        'year_to': year_to,
        'filters': filters,
    }

    return render(request, 'Drive/training.html', context)



def driving_details(request, id):
    driving = get_object_or_404(DrivingTraining, id=id)
    return render(request, 'Drive/traningdetails.html', {'driving': driving})

def demo(request):
    return render(request, 'demo.html')







# --------------------------------------------------------------NEW---------------------------------------------------------------------------------
from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Q
from .models import Villa, Land, Commercial, Chalet, Farm, Apartment  # Ensure you import your models
import json


def apartment(request):
    region_mapping = {
        'MS': 'Muscat', 'DH': 'Dhofar', 'BT': 'Batinah', 'DA': 'Dakhiliyah',
        'SH': 'Sharqiyah', 'BR': 'Buraimi', 'ZU': 'Zufar', 'DZ': 'Masandam', 'WR': 'Wusta',
    }
    advertisement=Advertisement.objects.all()
    # Fetch query parameters
    selected_region_code = request.GET.get('region', None)
    selected_listing_type = request.GET.get('listing_type', None)
    selected_city = request.GET.getlist('city')
    name_query = request.GET.get('name', '')
    price_from = request.GET.get('price_from')
    price_to = request.GET.get('price_to')
    selected_property_type = request.GET.get('property_type', None)
    bedrooms = request.GET.get('bedrooms')
    bathrooms = request.GET.get('bathrooms')
    furnished = request.GET.get('furnished')
    rental_period = request.GET.get('rental_period')
    lister_type = request.GET.get('lister_type')
    property_mortgage = request.GET.get('property_mortgage')
    facade = request.GET.get('facade')  
    floors = request.GET.get('floors')
    building = request.GET.get('building')
    main_amenity = request.GET.get('main_amenity')
    additional_amenity = request.GET.get('additional_amenity')
    nearby = request.GET.get('nearby')

    # Additional Filters
    surface_area_from = request.GET.get('surface_area_from')
    surface_area_to = request.GET.get('surface_area_to')
    
    # Start with all approved apartment
    apartment = Apartment.objects.filter(status='approved')

    # Apply Filters
    if selected_region_code and selected_region_code != "all":
        apartment = apartment.filter(regions=selected_region_code)
   
    if selected_city:
        # Create a Q object to filter for any of the selected cities
        city_filter = Q()
        for city in selected_city:
            city_filter |= Q(cities__icontains=city)
        apartment = apartment.filter(city_filter)
    if selected_listing_type and selected_listing_type != "all":
        apartment = apartment.filter(listing_type=selected_listing_type)
    if selected_property_type and selected_property_type != "all":
        apartment = apartment.filter(property_type=selected_property_type)
    if name_query:
        apartment = apartment.filter(
            Q(property_title__icontains=name_query) |
            Q(regions__icontains=name_query) |
            Q(cities__icontains=name_query) |
            Q(listing_type__icontains=name_query) |
            Q(property_type__icontains=name_query)
        )
    if price_from:
        apartment = apartment.filter(price__gte=price_from)
    if price_to:
        apartment = apartment.filter(price__lte=price_to)
    if bedrooms:
        bedroom_list = bedrooms.split(',')
        apartment = apartment.filter(bedrooms__in=bedroom_list)
    if bathrooms:
        bathroom_list = bathrooms.split(',')
        apartment = apartment.filter(bathrooms__in=bathroom_list)
    if furnished and furnished != "all":
        apartment = apartment.filter(furnished=furnished)
    if floors:
        floor_list = floors.split(',')
        apartment = apartment.filter(floors__in=floor_list)
    if building:
        building_list = building.split(',')
        apartment = apartment.filter(building__in=building_list)
    if rental_period and rental_period != "all":
        apartment = apartment.filter(rental_period=rental_period)
    if lister_type and lister_type != "all":
        apartment = apartment.filter(lister_type=lister_type)
    if property_mortgage and property_mortgage != "all":
        apartment = apartment.filter(property_mortgage=property_mortgage)
    if facade:
        facade_list = facade.split(',')
        apartment = apartment.filter(facade__in=facade_list)

    # Apply surface area filter if provided
    if surface_area_from and surface_area_to:
       apartment = apartment.filter(plot_area__gte=surface_area_from, plot_area__lte=surface_area_to)
    elif surface_area_from:
       apartment = apartment.filter(plot_area__gte=surface_area_from)
    elif surface_area_to:
       apartment = apartment.filter(plot_area__lte=surface_area_to)
   
    # Main Amenities filter
    if main_amenity:
        main_amenity_list = main_amenity.split(',')
        apartment = apartment.filter(main_amenities__name__in=main_amenity_list).distinct()
    if additional_amenity:
        additional_amenity_list = additional_amenity.split(',')
        apartment = apartment.filter(additional_amenities__name__in=additional_amenity_list).distinct()
    if nearby:
        nearby_list = nearby.split(',')
        apartment = apartment.filter(nearby_location__name__in=nearby_list).distinct()

    # Add images JSON
    for villa in apartment:
        villa.images_json = json.dumps([image.image.url for image in villa.images.all()])

    # Pagination
    paginator = Paginator(apartment, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Fetch filter options
    regions = [("all", "All")] + list(Villa.REGION_CHOICES)
    listing_types = [("all", "All")] + list(Villa.TRANSACTION_CHOICES)
    furnished_options = [("all", "All")] + list(Villa.FURNISHED_CHOICES)
    building_options = [("all", "All")] + list(Villa.BUILDING_AGE_CHOICES)
    rental_period_options = [("all", "All")] + list(Villa.RENTAL_PERIOD_CHOICES)
    lister_type_options = [("all", "All")] + list(Villa.LISTER_TYPE_CHOICES)
    property_mortgage_options = [("all", "All")] + list(Villa.PROPERTY_MORTGAGE_CHOICES)
    facade_options = [("all", "All")] + list(Villa.FACADE_CHOICES)
    floors_options = [("all", "All")] + list(Villa.FLOOR_CHOICES)

    # Context
    context = {
        'page_obj': page_obj,
        'regions': regions,
        'listing_types': listing_types,
        'furnished_options': furnished_options,
        'building_options': building_options,
        'rental_period_options': rental_period_options,
        'lister_type_options': lister_type_options,
        'property_mortgage_options': property_mortgage_options,
        'facade_options': facade_options,
        'floors_options': floors_options,
        'selected_region': region_mapping.get(selected_region_code, selected_region_code) if selected_region_code else None,
        'selected_listing_type': selected_listing_type,
        'selected_city': selected_city,
        'selected_property_type': selected_property_type,
        'name_query': name_query,
        'price_from': price_from,
        'price_to': price_to,
        'bedrooms': bedrooms,
        'bathrooms': bathrooms,
        'selected_furnished': furnished,
        'selected_building': building,
        'selected_rental_period': rental_period,
        'selected_lister_type': lister_type,
        'selected_property_mortgage': property_mortgage,
        'selected_facade': facade,
        'selected_floors': floors,
        'main_amenity': main_amenity,
        'additional_amenity': additional_amenity,
        'nearby': nearby,
        'formatted_url_name': request.resolver_match.url_name.replace("_", " ").title(),
        'advertisement':advertisement,
    }

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'estate/apartment_list_partial.html', {'page_obj': page_obj,'formatted_url_name': request.resolver_match.url_name.replace("_", " ").title()})
    
    return render(request, 'estate/apartment.html', context)

def apartment_details(request, id):
    apartment = get_object_or_404(Apartment.objects.prefetch_related('nearby_location', 'main_amenities', 'additional_amenities'), id=id)
    return render(request, 'estate/apartment_details.html', {'apartment': apartment})

from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Q
from .models import Villa, Land, Commercial, Chalet, Farm, Factory, MainAmenities  # Ensure you import your models
import json

def factory(request):
    region_mapping = {
        'MS': 'Muscat', 'DH': 'Dhofar', 'BT': 'Batinah', 'DA': 'Dakhiliyah',
        'SH': 'Sharqiyah', 'BR': 'Buraimi', 'ZU': 'Zufar', 'DZ': 'Masandam', 'WR': 'Wusta',
    }

    # Fetch query parameters
    advertisement=Advertisement.objects.all()
    selected_region_code = request.GET.get('region', None)
    selected_listing_type = request.GET.get('listing_type', None)
    selected_city = request.GET.getlist('city')
    name_query = request.GET.get('name', '')
    price_from = request.GET.get('price_from')
    price_to = request.GET.get('price_to')
    furnished = request.GET.get('furnished')
    rental_period = request.GET.get('rental_period')
    lister_type = request.GET.get('lister_type')
    property_mortgage = request.GET.get('property_mortgage')
    facade = request.GET.get('facade')  
    floors = request.GET.get('floors')
    main_amenity = request.GET.get('main_amenity')
    additional_amenity = request.GET.get('additional_amenity')
    nearby = request.GET.get('nearby')

    # Additional Filters
    surface_area_from = request.GET.get('surface_area_from')
    surface_area_to = request.GET.get('surface_area_to')
   
    # Start with all approved factory
    factory = Factory.objects.filter(status='approved')

    # Apply Filters
    if selected_region_code and selected_region_code != "all":
        factory = factory.filter(regions=selected_region_code)
   
    if selected_city:
        # Create a Q object to filter for any of the selected cities
        city_filter = Q()
        for city in selected_city:
            city_filter |= Q(cities__icontains=city)
        factory = factory.filter(city_filter)
    if selected_listing_type and selected_listing_type != "all":
        factory = factory.filter(listing_type=selected_listing_type)
    if name_query:
        factory = factory.filter(
            Q(property_title__icontains=name_query) |
            Q(regions__icontains=name_query) |
            Q(cities__icontains=name_query) |
            Q(listing_type__icontains=name_query) |
            Q(property_type__icontains=name_query)
        )
    if price_from:
        factory = factory.filter(price__gte=price_from)
    if price_to:
        factory = factory.filter(price__lte=price_to)
    if furnished and furnished != "all":
        factory= factory.filter(furnished=furnished)
    if floors:
        floor_list = floors.split(',')
        factory = factory.filter(floors__in=floor_list)
    if rental_period and rental_period != "all":
        factory = factory.filter(rental_period=rental_period)
    if lister_type and lister_type != "all":
        factory = factory.filter(lister_type=lister_type)
    if property_mortgage and property_mortgage != "all":
        factory = factory.filter(property_mortgage=property_mortgage)
    if facade:
        facade_list = facade.split(',')
        factory = factory.filter(facade__in=facade_list)

    if surface_area_from and surface_area_to:
       factory = factory.filter(plot_area__gte=surface_area_from, plot_area__lte=surface_area_to)
    elif surface_area_from:
       factory = factory.filter(plot_area__gte=surface_area_from)
    elif surface_area_to:
       factory = factory.filter(plot_area__lte=surface_area_to)
   
    # Main Amenities filter
    if main_amenity:
        main_amenity_list = main_amenity.split(',')
        factory = factory.filter(main_amenities__name__in=main_amenity_list).distinct()
    if additional_amenity:
        additional_amenity_list = additional_amenity.split(',')
        factory = factory.filter(additional_amenities__name__in=additional_amenity_list).distinct()
    if nearby:
        nearby_list = nearby.split(',')
        factory = factory.filter(nearby_location__name__in=nearby_list).distinct()

    # Add images JSON
    for clin in factory:
        clin.images_json = json.dumps([image.image.url for image in clin.images.all()])

    # Pagination
    paginator = Paginator(factory, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Fetch filter options
    regions = [("all", "All")] + list(Factory.REGION_CHOICES)
    listing_types = [("all", "All")] + list(Factory.TRANSACTION_CHOICES)
    rental_period_options = [("all", "All")] + list(Factory.RENTAL_PERIOD_CHOICES)
    lister_type_options = [("all", "All")] + list(Factory.LISTER_TYPE_CHOICES)
    property_mortgage_options = [("all", "All")] + list(Factory.PROPERTY_MORTGAGE_CHOICES)

    # Context
    context = {
        'page_obj': page_obj,
        'regions': regions,
        'listing_types': listing_types,
        'rental_period_options': rental_period_options,
        'lister_type_options': lister_type_options,
        'property_mortgage_options': property_mortgage_options,
        'selected_region': region_mapping.get(selected_region_code, selected_region_code) if selected_region_code else None,
        'selected_listing_type': selected_listing_type,
        'selected_city': selected_city,
        'name_query': name_query,
        'price_from': price_from,
        'price_to': price_to,
        'selected_furnished': furnished,
        'selected_rental_period': rental_period,
        'selected_lister_type': lister_type,
        'selected_property_mortgage': property_mortgage,
        'selected_facade': facade,
        'selected_floors': floors,
        'main_amenity': main_amenity,
        'additional_amenity': additional_amenity,
        'nearby': nearby,'advertisement':advertisement,
        'formatted_url_name': request.resolver_match.url_name.replace("_", " ").title(),
    }

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'estate/factory_list_partial.html', {'page_obj': page_obj,'formatted_url_name': request.resolver_match.url_name.replace("_", " ").title()})
    
    return render(request, 'estate/factory.html', context)


def factory_details(request, id):
    factory = get_object_or_404(Factory.objects.prefetch_related('nearby_location', 'main_amenities', 'additional_amenities'), id=id)
    return render(request, 'estate/factory_details.html', {'factory': factory})


def complex(request):
    region_mapping = {
        'MS': 'Muscat', 'DH': 'Dhofar', 'BT': 'Batinah', 'DA': 'Dakhiliyah',
        'SH': 'Sharqiyah', 'BR': 'Buraimi', 'ZU': 'Zufar', 'DZ': 'Masandam', 'WR': 'Wusta',
    }

    # Fetch query parameters
    advertisement=Advertisement.objects.all()
    selected_region_code = request.GET.get('region', None)
    selected_listing_type = request.GET.get('listing_type', None)
    selected_city = request.GET.getlist('city')
    name_query = request.GET.get('name', '')
    price_from = request.GET.get('price_from')
    price_to = request.GET.get('price_to')
    furnished = request.GET.get('furnished')
    rental_period = request.GET.get('rental_period')
    lister_type = request.GET.get('lister_type')
    property_mortgage = request.GET.get('property_mortgage')
    facade = request.GET.get('facade')  
    floors = request.GET.get('floors')
    main_amenity = request.GET.get('main_amenity')
    additional_amenity = request.GET.get('additional_amenity')
    nearby = request.GET.get('nearby')

    # Additional Filters
    surface_area_from = request.GET.get('surface_area_from')
    surface_area_to = request.GET.get('surface_area_to')
   
    # Start with all approved clinic
    complex = Complex.objects.filter(status='approved')

    # Apply Filters
    if selected_region_code and selected_region_code != "all":
        complex = complex.filter(regions=selected_region_code)
   
    if selected_city:
        # Create a Q object to filter for any of the selected cities
        city_filter = Q()
        for city in selected_city:
            city_filter |= Q(cities__icontains=city)
        complex = complex.filter(city_filter)
    if selected_listing_type and selected_listing_type != "all":
        complex = complex.filter(listing_type=selected_listing_type)
    if name_query:
        complex = complex.filter(
            Q(property_title__icontains=name_query) |
            Q(regions__icontains=name_query) |
            Q(cities__icontains=name_query) |
            Q(listing_type__icontains=name_query) |
            Q(property_type__icontains=name_query)
        )
    if price_from:
        complex = complex.filter(price__gte=price_from)
    if price_to:
        complex = complex.filter(price__lte=price_to)
    if furnished and furnished != "all":
        complex = complex.filter(furnished=furnished)
    if floors:
        floor_list = floors.split(',')
        complex = complex.filter(floors__in=floor_list)
    if rental_period and rental_period != "all":
        complex = complex.filter(rental_period=rental_period)
    if lister_type and lister_type != "all":
        complex = complex.filter(lister_type=lister_type)
    if property_mortgage and property_mortgage != "all":
        complex = complex.filter(property_mortgage=property_mortgage)
    if facade:
        facade_list = facade.split(',')
        complex = complex.filter(facade__in=facade_list)

    if surface_area_from and surface_area_to:
       complex = complex.filter(plot_area__gte=surface_area_from, plot_area__lte=surface_area_to)
    elif surface_area_from:
       complex = complex.filter(plot_area__gte=surface_area_from)
    elif surface_area_to:
       complex = complex.filter(plot_area__lte=surface_area_to)
   
    # Main Amenities filter
    if main_amenity:
        main_amenity_list = main_amenity.split(',')
        complex = complex.filter(main_amenities__name__in=main_amenity_list).distinct()
    if additional_amenity:
        additional_amenity_list = additional_amenity.split(',')
        complex = complex.filter(additional_amenities__name__in=additional_amenity_list).distinct()
    if nearby:
        nearby_list = nearby.split(',')
        complex = complex.filter(nearby_location__name__in=nearby_list).distinct()

    # Add images JSON
    for clin in complex:
        clin.images_json = json.dumps([image.image.url for image in clin.images.all()])

    # Pagination
    paginator = Paginator(complex, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Fetch filter options
    regions = [("all", "All")] + list(Villa.REGION_CHOICES)
    listing_types = [("all", "All")] + list(Villa.TRANSACTION_CHOICES)
    furnished_options = [("all", "All")] + list(Villa.FURNISHED_CHOICES)
    building_options = [("all", "All")] + list(Villa.BUILDING_AGE_CHOICES)
    rental_period_options = [("all", "All")] + list(Villa.RENTAL_PERIOD_CHOICES)
    lister_type_options = [("all", "All")] + list(Villa.LISTER_TYPE_CHOICES)
    property_mortgage_options = [("all", "All")] + list(Villa.PROPERTY_MORTGAGE_CHOICES)
    facade_options = [("all", "All")] + list(Villa.FACADE_CHOICES)
    floors_options = [("all", "All")] + list(Villa.FLOOR_CHOICES)

    # Context
    context = {
        'page_obj': page_obj,
        'regions': regions,
        'listing_types': listing_types,
        'furnished_options': furnished_options,
        'building_options': building_options,
        'rental_period_options': rental_period_options,
        'lister_type_options': lister_type_options,
        'property_mortgage_options': property_mortgage_options,
        'facade_options': facade_options,
        'floors_options': floors_options,
        'selected_region': region_mapping.get(selected_region_code, selected_region_code) if selected_region_code else None,
        'selected_listing_type': selected_listing_type,
        'selected_city': selected_city,
        
        'name_query': name_query,
        'price_from': price_from,
        'price_to': price_to,
        'selected_furnished': furnished,
        'selected_rental_period': rental_period,'advertisement':advertisement,
        'selected_lister_type': lister_type,
        'selected_property_mortgage': property_mortgage,
        'selected_facade': facade,
        'selected_floors': floors,
        'main_amenity': main_amenity,
        'additional_amenity': additional_amenity,
        'nearby': nearby,
        'formatted_url_name': request.resolver_match.url_name.replace("_", " ").title(),
    }

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'estate/complex_list_partial.html', {'page_obj': page_obj,'formatted_url_name': request.resolver_match.url_name.replace("_", " ").title()})
    
    return render(request, 'estate/complex.html', context)


def complex_details(request, id):
    complex = get_object_or_404(Complex.objects.prefetch_related('nearby_location', 'main_amenities', 'additional_amenities'), id=id)
    return render(request, 'estate/complex_details.html', {'complex': complex})


def clinic(request):
    region_mapping = {
        'MS': 'Muscat', 'DH': 'Dhofar', 'BT': 'Batinah', 'DA': 'Dakhiliyah',
        'SH': 'Sharqiyah', 'BR': 'Buraimi', 'ZU': 'Zufar', 'DZ': 'Masandam', 'WR': 'Wusta',
    }

    # Fetch query parameters
    advertisement=Advertisement.objects.all()
    selected_region_code = request.GET.get('region', None)
    selected_listing_type = request.GET.get('listing_type', None)
    selected_city = request.GET.getlist('city')
    name_query = request.GET.get('name', '')
    price_from = request.GET.get('price_from')
    price_to = request.GET.get('price_to')
    furnished = request.GET.get('furnished')
    rental_period = request.GET.get('rental_period')
    lister_type = request.GET.get('lister_type')
    property_mortgage = request.GET.get('property_mortgage')
    facade = request.GET.get('facade')  
    floors = request.GET.get('floors')
    main_amenity = request.GET.get('main_amenity')
    additional_amenity = request.GET.get('additional_amenity')
    nearby = request.GET.get('nearby')

    # Additional Filters
    surface_area_from = request.GET.get('surface_area_from')
    surface_area_to = request.GET.get('surface_area_to')
   
    # Start with all approved clinic
    clinic = Clinic.objects.filter(status='approved')

    # Apply Filters
    if selected_region_code and selected_region_code != "all":
        clinic = clinic.filter(regions=selected_region_code)
   
    if selected_city:
        # Create a Q object to filter for any of the selected cities
        city_filter = Q()
        for city in selected_city:
            city_filter |= Q(cities__icontains=city)
        clinic = clinic.filter(city_filter)
    if selected_listing_type and selected_listing_type != "all":
        clinic = clinic.filter(listing_type=selected_listing_type)
    if name_query:
        clinic = clinic.filter(
            Q(property_title__icontains=name_query) |
            Q(regions__icontains=name_query) |
            Q(cities__icontains=name_query) |
            Q(listing_type__icontains=name_query) |
            Q(property_type__icontains=name_query)
        )
    if price_from:
        clinic = clinic.filter(price__gte=price_from)
    if price_to:
        clinic = clinic.filter(price__lte=price_to)
    if furnished and furnished != "all":
        clinic = clinic.filter(furnished=furnished)
    if floors:
        floor_list = floors.split(',')
        clinic = clinic.filter(floors__in=floor_list)
    if rental_period and rental_period != "all":
        clinic = clinic.filter(rental_period=rental_period)
    if lister_type and lister_type != "all":
        clinic = clinic.filter(lister_type=lister_type)
    if property_mortgage and property_mortgage != "all":
        clinic = clinic.filter(property_mortgage=property_mortgage)
    if facade:
        facade_list = facade.split(',')
        clinic = clinic.filter(facade__in=facade_list)

    if surface_area_from and surface_area_to:
       clinic = clinic.filter(plot_area__gte=surface_area_from, plot_area__lte=surface_area_to)
    elif surface_area_from:
       clinic = clinic.filter(plot_area__gte=surface_area_from)
    elif surface_area_to:
       clinic = clinic.filter(plot_area__lte=surface_area_to)
   
    # Main Amenities filter
    if main_amenity:
        main_amenity_list = main_amenity.split(',')
        clinic = clinic.filter(main_amenities__name__in=main_amenity_list).distinct()
    if additional_amenity:
        additional_amenity_list = additional_amenity.split(',')
        clinic = clinic.filter(additional_amenities__name__in=additional_amenity_list).distinct()
    if nearby:
        nearby_list = nearby.split(',')
        clinic = clinic.filter(nearby_location__name__in=nearby_list).distinct()

    # Add images JSON
    for clin in clinic:
        clin.images_json = json.dumps([image.image.url for image in clin.images.all()])

    # Pagination
    paginator = Paginator(clinic, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Fetch filter options
    regions = [("all", "All")] + list(Villa.REGION_CHOICES)
    listing_types = [("all", "All")] + list(Villa.TRANSACTION_CHOICES)
    furnished_options = [("all", "All")] + list(Villa.FURNISHED_CHOICES)
    building_options = [("all", "All")] + list(Villa.BUILDING_AGE_CHOICES)
    rental_period_options = [("all", "All")] + list(Villa.RENTAL_PERIOD_CHOICES)
    lister_type_options = [("all", "All")] + list(Villa.LISTER_TYPE_CHOICES)
    property_mortgage_options = [("all", "All")] + list(Villa.PROPERTY_MORTGAGE_CHOICES)
    facade_options = [("all", "All")] + list(Villa.FACADE_CHOICES)
    floors_options = [("all", "All")] + list(Villa.FLOOR_CHOICES)

    # Context
    context = {
        'page_obj': page_obj,
        'regions': regions,
        'listing_types': listing_types,
        'furnished_options': furnished_options,
        'building_options': building_options,
        'rental_period_options': rental_period_options,
        'lister_type_options': lister_type_options,
        'property_mortgage_options': property_mortgage_options,
        'facade_options': facade_options,
        'floors_options': floors_options,
        'selected_region': region_mapping.get(selected_region_code, selected_region_code) if selected_region_code else None,
        'selected_listing_type': selected_listing_type,
        'selected_city': selected_city,
        
        'name_query': name_query,
        'price_from': price_from,
        'price_to': price_to,
        'selected_furnished': furnished,
        'selected_rental_period': rental_period,
        'selected_lister_type': lister_type,
        'selected_property_mortgage': property_mortgage,
        'selected_facade': facade,
        'selected_floors': floors,'advertisement':advertisement,
        'main_amenity': main_amenity,
        'additional_amenity': additional_amenity,
        'nearby': nearby,
        'formatted_url_name': request.resolver_match.url_name.replace("_", " ").title(),
    }

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'estate/clinic_list_partial.html', {'page_obj': page_obj,'formatted_url_name': request.resolver_match.url_name.replace("_", " ").title(),
})
    
    return render(request, 'estate/clinic.html', context)


def clinic_details(request, id):
    clinic = get_object_or_404(Clinic.objects.prefetch_related('nearby_location', 'main_amenities', 'additional_amenities'), id=id)
    return render(request, 'estate/clinic_details.html', {'clinic': clinic})

def hostel(request):
    region_mapping = {
        'MS': 'Muscat', 'DH': 'Dhofar', 'BT': 'Batinah', 'DA': 'Dakhiliyah',
        'SH': 'Sharqiyah', 'BR': 'Buraimi', 'ZU': 'Zufar', 'DZ': 'Masandam', 'WR': 'Wusta',
    }

    # Fetch query parameters
    advertisement=Advertisement.objects.all()
    selected_region_code = request.GET.get('region', None)
    selected_listing_type = request.GET.get('listing_type', None)
    selected_city = request.GET.getlist('city')
    name_query = request.GET.get('name', '')
    price_from = request.GET.get('price_from')
    price_to = request.GET.get('price_to')
    selected_property_type = request.GET.get('property_type', None)
    bedrooms = request.GET.get('bedrooms')
    bathrooms = request.GET.get('bathrooms')
    furnished = request.GET.get('furnished')
    rental_period = request.GET.get('rental_period')
    lister_type = request.GET.get('lister_type')
    property_mortgage = request.GET.get('property_mortgage')
    facade = request.GET.get('facade')  
    floors = request.GET.get('floors')
    building = request.GET.get('building')
    main_amenity = request.GET.get('main_amenity')
    additional_amenity = request.GET.get('additional_amenity')
    nearby = request.GET.get('nearby')

    # Additional Filters
    surface_area_from = request.GET.get('surface_area_from')
    surface_area_to = request.GET.get('surface_area_to')
    
    # Start with all approved staff
    hostel = Hostel.objects.filter(status='approved')

    # Apply Filters
    if selected_region_code and selected_region_code != "all":
        hostel = hostel.filter(regions=selected_region_code)
   
    if selected_city:
        # Create a Q object to filter for any of the selected cities
        city_filter = Q()
        for city in selected_city:
            city_filter |= Q(cities__icontains=city)
        hostel = hostel.filter(city_filter)
    if selected_listing_type and selected_listing_type != "all":
        hostel = hostel.filter(listing_type=selected_listing_type)
    if selected_property_type and selected_property_type != "all":
        hostel = hostel.filter(property_type=selected_property_type)
    if name_query:
        hostel = hostel.filter(
            Q(property_title__icontains=name_query) |
            Q(regions__icontains=name_query) |
            Q(cities__icontains=name_query) |
            Q(listing_type__icontains=name_query) |
            Q(property_type__icontains=name_query)
        )
    if price_from:
        hostel = hostel.filter(price__gte=price_from)
    if price_to:
        hostel = hostel.filter(price__lte=price_to)
    if bedrooms:
        bedroom_list = bedrooms.split(',')
        hostel = hostel.filter(bedrooms__in=bedroom_list)
    if bathrooms:
        bathroom_list = bathrooms.split(',')
        hostel = hostel.filter(bathrooms__in=bathroom_list)
    if furnished and furnished != "all":
        hostel = hostel.filter(furnished=furnished)
    if floors:
        floor_list = floors.split(',')
        hostel = hostel.filter(floors__in=floor_list)
    if building:
        building_list = building.split(',')
        hostel = hostel.filter(building__in=building_list)
    if rental_period and rental_period != "all":
        hostel = hostel.filter(rental_period=rental_period)
    if lister_type and lister_type != "all":
        hostel = hostel.filter(lister_type=lister_type)
    if property_mortgage and property_mortgage != "all":
        hostel = hostel.filter(property_mortgage=property_mortgage)
    if facade:
        facade_list = facade.split(',')
        hostel = hostel.filter(facade__in=facade_list)

    # Apply surface area filter if provided
    if surface_area_from and surface_area_to:
       hostel = hostel.filter(plot_area__gte=surface_area_from, plot_area__lte=surface_area_to)
    elif surface_area_from:
       hostel = hostel.filter(plot_area__gte=surface_area_from)
    elif surface_area_to:
       hostel = hostel.filter(plot_area__lte=surface_area_to)
   
    # Main Amenities filter
    if main_amenity:
        main_amenity_list = main_amenity.split(',')
        hostel = hostel.filter(main_amenities__name__in=main_amenity_list).distinct()
    if additional_amenity:
        additional_amenity_list = additional_amenity.split(',')
        hostel = hostel.filter(additional_amenities__name__in=additional_amenity_list).distinct()
    if nearby:
        nearby_list = nearby.split(',')
        hostel = hostel.filter(nearby_location__name__in=nearby_list).distinct()

    # Add images JSON
    for villa in hostel:
        villa.images_json = json.dumps([image.image.url for image in villa.images.all()])

    # Pagination
    paginator = Paginator(hostel, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Fetch filter options
    regions = [("all", "All")] + list(Villa.REGION_CHOICES)
    listing_types = [("all", "All")] + list(Villa.TRANSACTION_CHOICES)
    furnished_options = [("all", "All")] + list(Villa.FURNISHED_CHOICES)
    building_options = [("all", "All")] + list(Villa.BUILDING_AGE_CHOICES)
    rental_period_options = [("all", "All")] + list(Villa.RENTAL_PERIOD_CHOICES)
    lister_type_options = [("all", "All")] + list(Villa.LISTER_TYPE_CHOICES)
    property_mortgage_options = [("all", "All")] + list(Villa.PROPERTY_MORTGAGE_CHOICES)
    facade_options = [("all", "All")] + list(Villa.FACADE_CHOICES)
    floors_options = [("all", "All")] + list(Villa.FLOOR_CHOICES)

    # Context
    context = {
        'page_obj': page_obj,
        'regions': regions,
        'listing_types': listing_types,
        'furnished_options': furnished_options,
        'building_options': building_options,
        'rental_period_options': rental_period_options,
        'lister_type_options': lister_type_options,
        'property_mortgage_options': property_mortgage_options,
        'facade_options': facade_options,
        'floors_options': floors_options,
        'selected_region': region_mapping.get(selected_region_code, selected_region_code) if selected_region_code else None,
        'selected_listing_type': selected_listing_type,
        'selected_city': selected_city,
        'selected_property_type': selected_property_type,
        'name_query': name_query,
        'price_from': price_from,'advertisement':advertisement,
        'price_to': price_to,
        'bedrooms': bedrooms,
        'bathrooms': bathrooms,
        'selected_furnished': furnished,
        'selected_building': building,
        'selected_rental_period': rental_period,
        'selected_lister_type': lister_type,
        'selected_property_mortgage': property_mortgage,
        'selected_facade': facade,
        'selected_floors': floors,
        'main_amenity': main_amenity,
        'additional_amenity': additional_amenity,
        'nearby': nearby,
        'formatted_url_name': request.resolver_match.url_name.replace("hostel", "hotel").replace("_", " ").title(),

    }

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'estate/hostel_list_partial.html', {'page_obj': page_obj,'formatted_url_name': request.resolver_match.url_name.replace("hostel", "hotel").replace("_", " ").title(),
})
    
    return render(request, 'estate/hostel.html', context)


def hostel_details(request, id):
    hostel = get_object_or_404(Hostel.objects.prefetch_related('nearby_location', 'main_amenities', 'additional_amenities'), id=id)
    return render(request, 'estate/hostel_details.html', {'hostel': hostel})

from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Q
from .models import Office, Villa, Land, Commercial, Chalet, Farm, MainAmenities, AdditionalAmenities, NearbyLocation
import json

def office(request):
    region_mapping = {
        'MS': 'Muscat', 'DH': 'Dhofar', 'BT': 'Batinah', 'DA': 'Dakhiliyah',
        'SH': 'Sharqiyah', 'BR': 'Buraimi', 'ZU': 'Zufar', 'DZ': 'Masandam', 'WR': 'Wusta',
    }

    # Fetch query parameters
    advertisement=Advertisement.objects.all()
    selected_region_code = request.GET.get('region', None)
    selected_listing_type = request.GET.get('listing_type', None)
    selected_city = request.GET.getlist('city')
    name_query = request.GET.get('name', '')
    price_from = request.GET.get('price_from')
    price_to = request.GET.get('price_to')
    furnished = request.GET.get('furnished')
    rental_period = request.GET.get('rental_period')
    lister_type = request.GET.get('lister_type')
    property_mortgage = request.GET.get('property_mortgage')
    facade = request.GET.get('facade')  
    floors = request.GET.get('floors')
    main_amenity = request.GET.get('main_amenity')
    additional_amenity = request.GET.get('additional_amenity')
    nearby = request.GET.get('nearby')

    # Additional Filters
    surface_area_from = request.GET.get('surface_area_from')
    surface_area_to = request.GET.get('surface_area_to')
   
    # Start with all approved clinic
    office = Office.objects.filter(status='approved')

    # Apply Filters
    if selected_region_code and selected_region_code != "all":
        office = office.filter(regions=selected_region_code)
   
    if selected_city:
        # Create a Q object to filter for any of the selected cities
        city_filter = Q()
        for city in selected_city:
            city_filter |= Q(cities__icontains=city)
        office = office.filter(city_filter)
    if selected_listing_type and selected_listing_type != "all":
        office = office.filter(listing_type=selected_listing_type)
    if name_query:
        office = office.filter(
            Q(property_title__icontains=name_query) |
            Q(regions__icontains=name_query) |
            Q(cities__icontains=name_query) |
            Q(listing_type__icontains=name_query) |
            Q(property_type__icontains=name_query)
        )
    if price_from:
        office = office.filter(price__gte=price_from)
    if price_to:
        office = office.filter(price__lte=price_to)
    if furnished and furnished != "all":
        office = office.filter(furnished=furnished)
    if floors:
        floor_list = floors.split(',')
        office = office.filter(floors__in=floor_list)
    if rental_period and rental_period != "all":
        office = office.filter(rental_period=rental_period)
    if lister_type and lister_type != "all":
        office = office.filter(lister_type=lister_type)
    if property_mortgage and property_mortgage != "all":
        office = office.filter(property_mortgage=property_mortgage)
    if facade:
        facade_list = facade.split(',')
        office = office.filter(facade__in=facade_list)

    if surface_area_from and surface_area_to:
       office = office.filter(plot_area__gte=surface_area_from, plot_area__lte=surface_area_to)
    elif surface_area_from:
       office = office.filter(plot_area__gte=surface_area_from)
    elif surface_area_to:
       office = office.filter(plot_area__lte=surface_area_to)
   
    # Main Amenities filter
    if main_amenity:
        main_amenity_list = main_amenity.split(',')
        office = office.filter(main_amenities__name__in=main_amenity_list).distinct()
    if additional_amenity:
        additional_amenity_list = additional_amenity.split(',')
        office = office.filter(additional_amenities__name__in=additional_amenity_list).distinct()
    if nearby:
        nearby_list = nearby.split(',')
        office = office.filter(nearby_location__name__in=nearby_list).distinct()

    # Add images JSON
    for clin in office:
        clin.images_json = json.dumps([image.image.url for image in clin.images.all()])

    # Pagination
    paginator = Paginator(office, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Fetch filter options
    regions = [("all", "All")] + list(Villa.REGION_CHOICES)
    listing_types = [("all", "All")] + list(Villa.TRANSACTION_CHOICES)
    furnished_options = [("all", "All")] + list(Villa.FURNISHED_CHOICES)
    building_options = [("all", "All")] + list(Villa.BUILDING_AGE_CHOICES)
    rental_period_options = [("all", "All")] + list(Villa.RENTAL_PERIOD_CHOICES)
    lister_type_options = [("all", "All")] + list(Villa.LISTER_TYPE_CHOICES)
    property_mortgage_options = [("all", "All")] + list(Villa.PROPERTY_MORTGAGE_CHOICES)
    facade_options = [("all", "All")] + list(Villa.FACADE_CHOICES)
    floors_options = [("all", "All")] + list(Villa.FLOOR_CHOICES)

    # Context
    context = {
        'page_obj': page_obj,
        'regions': regions,
        'listing_types': listing_types,
        'furnished_options': furnished_options,
        'building_options': building_options,
        'rental_period_options': rental_period_options,
        'lister_type_options': lister_type_options,
        'property_mortgage_options': property_mortgage_options,
        'facade_options': facade_options,
        'floors_options': floors_options,
        'selected_region': region_mapping.get(selected_region_code, selected_region_code) if selected_region_code else None,
        'selected_listing_type': selected_listing_type,
        'selected_city': selected_city,
        
        'name_query': name_query,
        'price_from': price_from,
        'price_to': price_to,'advertisement':advertisement,
        'selected_furnished': furnished,
        'selected_rental_period': rental_period,
        'selected_lister_type': lister_type,
        'selected_property_mortgage': property_mortgage,
        'selected_facade': facade,
        'selected_floors': floors,
        'main_amenity': main_amenity,
        'additional_amenity': additional_amenity,
        'nearby': nearby,
        'formatted_url_name': request.resolver_match.url_name.replace("_", " ").title(),
    }

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'estate/office_list_partial.html', {'page_obj': page_obj,'formatted_url_name': request.resolver_match.url_name.replace("_", " ").title()})
    
    return render(request, 'estate/office.html', context)


def office_details(request, id):
    office = get_object_or_404(Office.objects.prefetch_related('nearby_location', 'main_amenities', 'additional_amenities'), id=id)
    return render(request, 'estate/office_details.html', {'office': office})


from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
import json
from .models import Shop, NearbyLocation, MainAmenities, AdditionalAmenities


def shop(request):
    region_mapping = {
        'MS': 'Muscat', 'DH': 'Dhofar', 'BT': 'Batinah', 'DA': 'Dakhiliyah',
        'SH': 'Sharqiyah', 'BR': 'Buraimi', 'ZU': 'Zufar', 'DZ': 'Masandam', 'WR': 'Wusta',
    }

    # Fetch query parameters
    advertisement=Advertisement.objects.all()
    selected_region_code = request.GET.get('region', None)
    selected_listing_type = request.GET.get('listing_type', None)
    selected_city = request.GET.getlist('city')
    name_query = request.GET.get('name', '')
    price_from = request.GET.get('price_from')
    price_to = request.GET.get('price_to')
    furnished = request.GET.get('furnished')
    rental_period = request.GET.get('rental_period')
    lister_type = request.GET.get('lister_type')
    property_mortgage = request.GET.get('property_mortgage')
    facade = request.GET.get('facade')  
    floors = request.GET.get('floors')
    property = request.GET.get('property')
    main_amenity = request.GET.get('main_amenity')
    additional_amenity = request.GET.get('additional_amenity')
    nearby = request.GET.get('nearby')
    
    # Additional Filters
    surface_area_from = request.GET.get('surface_area_from')
    surface_area_to = request.GET.get('surface_area_to')
   
    # Start with all approved shop
    shop = Shop.objects.filter(status='approved')

    # Apply Filters
    if selected_region_code and selected_region_code != "all":
        shop = shop.filter(regions=selected_region_code)
   
    if selected_city:
        # Create a Q object to filter for any of the selected cities
        city_filter = Q()
        for city in selected_city:
            city_filter |= Q(cities__icontains=city)
        shop = shop.filter(city_filter)
    if selected_listing_type and selected_listing_type != "all":
        shop = shop.filter(listing_type=selected_listing_type)
    if name_query:
        shop = shop.filter(
            Q(property_title__icontains=name_query) |
            Q(regions__icontains=name_query) |
            Q(cities__icontains=name_query) |
            Q(listing_type__icontains=name_query) |
            Q(property_type__icontains=name_query)
        )
    if price_from:
        shop = shop.filter(price__gte=price_from)
    if price_to:
        shop = shop.filter(price__lte=price_to)
    if furnished and furnished != "all":
        shop = shop.filter(furnished=furnished)
    if floors:
        floor_list = floors.split(',')
        shop = shop.filter(floors__in=floor_list)
    if property:
        property_list = property.split(',')
        shop = shop.filter(property__in=property_list)
    if rental_period and rental_period != "all":
        shop = shop.filter(rental_period=rental_period)
    if lister_type and lister_type != "all":
        shop = shop.filter(lister_type=lister_type)
    if property_mortgage and property_mortgage != "all":
        shop = shop.filter(property_mortgage=property_mortgage)
    if facade:
        facade_list = facade.split(',')
        shop = shop.filter(facade__in=facade_list)

    if surface_area_from and surface_area_to:
       shop = shop.filter(plot_area__gte=surface_area_from, plot_area__lte=surface_area_to)
    elif surface_area_from:
       shop = shop.filter(plot_area__gte=surface_area_from)
    elif surface_area_to:
       shop = shop.filter(plot_area__lte=surface_area_to)
   
    # Main Amenities filter
    if main_amenity:
        main_amenity_list = main_amenity.split(',')
        shop = shop.filter(main_amenities__name__in=main_amenity_list).distinct()
    if additional_amenity:
        additional_amenity_list = additional_amenity.split(',')
        shop = shop.filter(additional_amenities__name__in=additional_amenity_list).distinct()
    if nearby:
        nearby_list = nearby.split(',')
        shop = shop.filter(nearby_location__name__in=nearby_list).distinct()

    # Add images JSON
    for clin in shop:
        clin.images_json = json.dumps([image.image.url for image in clin.images.all()])

    # Pagination
    paginator = Paginator(shop, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Fetch filter options
    regions = [("all", "All")] + list(Shop.REGION_CHOICES)
    listing_types = [("all", "All")] + list(Shop.TRANSACTION_CHOICES)
    rental_period_options = [("all", "All")] + list(Shop.RENTAL_PERIOD_CHOICES)
    lister_type_options = [("all", "All")] + list(Shop.LISTER_TYPE_CHOICES)
    property_mortgage_options = [("all", "All")] + list(Shop.PROPERTY_MORTGAGE_CHOICES)

    # Context
    context = {
        'page_obj': page_obj,
        'regions': regions,
        'listing_types': listing_types,
        'rental_period_options': rental_period_options,
        'lister_type_options': lister_type_options,
        'property_mortgage_options': property_mortgage_options, 
        'selected_region': region_mapping.get(selected_region_code, selected_region_code) if selected_region_code else None,
        'selected_listing_type': selected_listing_type,
        'selected_city': selected_city,
        'name_query': name_query,
        'price_from': price_from,'advertisement':advertisement,
        'price_to': price_to,
        'selected_furnished': furnished,
        'selected_rental_period': rental_period,
        'selected_lister_type': lister_type,
        'selected_property_mortgage': property_mortgage,
        'selected_facade': facade,
        'selected_floors': floors,
        'selected_property': property,
        'main_amenity': main_amenity,
        'additional_amenity': additional_amenity,
        'nearby': nearby,
        'formatted_url_name': request.resolver_match.url_name.replace("_", " ").title(),
    }

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'estate/shop_list_partial.html', {'page_obj': page_obj,'formatted_url_name': request.resolver_match.url_name.replace("_", " ").title()})
    
    return render(request, 'estate/shop.html', context)



def shop_details(request, id):
    shop = get_object_or_404(Shop.objects.prefetch_related('nearby_location', 'main_amenities', 'additional_amenities'), id=id)
    return render(request, 'estate/shop_details.html', {'shop': shop})


def cafe(request):
    region_mapping = {
        'MS': 'Muscat', 'DH': 'Dhofar', 'BT': 'Batinah', 'DA': 'Dakhiliyah',
        'SH': 'Sharqiyah', 'BR': 'Buraimi', 'ZU': 'Zufar', 'DZ': 'Masandam', 'WR': 'Wusta',
    }

    # Fetch query parameters
    advertisement=Advertisement.objects.all()
    selected_region_code = request.GET.get('region', None)
    selected_listing_type = request.GET.get('listing_type', None)
    selected_city = request.GET.getlist('city')
    name_query = request.GET.get('name', '')
    price_from = request.GET.get('price_from')
    price_to = request.GET.get('price_to')
    furnished = request.GET.get('furnished')
    rental_period = request.GET.get('rental_period')
    lister_type = request.GET.get('lister_type')
    property_mortgage = request.GET.get('property_mortgage')
    facade = request.GET.get('facade')  
    floors = request.GET.get('floors')
    property = request.GET.get('property')
    main_amenity = request.GET.get('main_amenity')
    additional_amenity = request.GET.get('additional_amenity')
    nearby = request.GET.get('nearby')
    
    # Additional Filters
    surface_area_from = request.GET.get('surface_area_from')
    surface_area_to = request.GET.get('surface_area_to')
   
    # Start with all approved cafe
    cafe = Cafe.objects.filter(status='approved')

    # Apply Filters
    if selected_region_code and selected_region_code != "all":
        cafe = cafe.filter(regions=selected_region_code)
   
    if selected_city:
        # Create a Q object to filter for any of the selected cities
        city_filter = Q()
        for city in selected_city:
            city_filter |= Q(cities__icontains=city)
        cafe = cafe.filter(city_filter)
    if selected_listing_type and selected_listing_type != "all":
        cafe = cafe.filter(listing_type=selected_listing_type)
    if name_query:
        cafe = cafe.filter(
            Q(property_title__icontains=name_query) |
            Q(regions__icontains=name_query) |
            Q(cities__icontains=name_query) |
            Q(listing_type__icontains=name_query) |
            Q(property_type__icontains=name_query)
        )
    if price_from:
        cafe = cafe.filter(price__gte=price_from)
    if price_to:
        cafe = cafe.filter(price__lte=price_to)
    if furnished and furnished != "all":
        cafe = cafe.filter(furnished=furnished)
    if floors:
        floor_list = floors.split(',')
        cafe = cafe.filter(floors__in=floor_list)
    if property:
        property_list = property.split(',')
        cafe = cafe.filter(property__in=property_list)
    if rental_period and rental_period != "all":
        cafe = cafe.filter(rental_period=rental_period)
    if lister_type and lister_type != "all":
        cafe = cafe.filter(lister_type=lister_type)
    if property_mortgage and property_mortgage != "all":
        cafe = cafe.filter(property_mortgage=property_mortgage)
    if facade:
        facade_list = facade.split(',')
        cafe = cafe.filter(facade__in=facade_list)

    if surface_area_from and surface_area_to:
       cafe = cafe.filter(plot_area__gte=surface_area_from, plot_area__lte=surface_area_to)
    elif surface_area_from:
       cafe = cafe.filter(plot_area__gte=surface_area_from)
    elif surface_area_to:
       cafe = cafe.filter(plot_area__lte=surface_area_to)
   
    # Main Amenities filter
    if main_amenity:
        main_amenity_list = main_amenity.split(',')
        cafe = cafe.filter(main_amenities__name__in=main_amenity_list).distinct()
    if additional_amenity:
        additional_amenity_list = additional_amenity.split(',')
        cafe = cafe.filter(additional_amenities__name__in=additional_amenity_list).distinct()
    if nearby:
        nearby_list = nearby.split(',')
        cafe = cafe.filter(nearby_location__name__in=nearby_list).distinct()

    # Add images JSON
    for clin in cafe:
        clin.images_json = json.dumps([image.image.url for image in clin.images.all()])

    # Pagination
    paginator = Paginator(cafe, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Fetch filter options
    regions = [("all", "All")] + list(Cafe.REGION_CHOICES)
    listing_types = [("all", "All")] + list(Cafe.TRANSACTION_CHOICES)
    rental_period_options = [("all", "All")] + list(Cafe.RENTAL_PERIOD_CHOICES)
    lister_type_options = [("all", "All")] + list(Cafe.LISTER_TYPE_CHOICES)
    property_mortgage_options = [("all", "All")] + list(Cafe.PROPERTY_MORTGAGE_CHOICES)
    property_options = [("all", "All")] + list(Cafe.PROPERTY_CHOICES)

    # Context
    context = {
        'page_obj': page_obj,
        'regions': regions,
        'listing_types': listing_types,
        'rental_period_options': rental_period_options,
        'lister_type_options': lister_type_options,
        'property_mortgage_options': property_mortgage_options,
        'property_options':property_options,
        'selected_region': region_mapping.get(selected_region_code, selected_region_code) if selected_region_code else None,
        'selected_listing_type': selected_listing_type,
        'selected_city': selected_city,
        
        'name_query': name_query,
        'price_from': price_from,
        'price_to': price_to,
        'selected_furnished': furnished,
        'selected_rental_period': rental_period,
        'selected_lister_type': lister_type,
        'selected_property_mortgage': property_mortgage,
        'selected_facade': facade,'advertisement':advertisement,
        'selected_floors': floors,
        'selected_property': property,
        'main_amenity': main_amenity,
        'additional_amenity': additional_amenity,
        'nearby': nearby,
        'formatted_url_name': request.resolver_match.url_name.replace("_", " ").title(),
    }

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'estate/cafe_list_partial.html', {'page_obj': page_obj,'formatted_url_name': request.resolver_match.url_name.replace("_", " ").title(),
})
    
    return render(request, 'estate/cafe.html', context)


def cafe_details(request, id):
    cafe = get_object_or_404(Cafe.objects.prefetch_related('nearby_location', 'main_amenities', 'additional_amenities'), id=id)
    return render(request, 'estate/cafe_details.html', {'cafe': cafe})

def staff(request):
    region_mapping = {
        'MS': 'Muscat', 'DH': 'Dhofar', 'BT': 'Batinah', 'DA': 'Dakhiliyah',
        'SH': 'Sharqiyah', 'BR': 'Buraimi', 'ZU': 'Zufar', 'DZ': 'Masandam', 'WR': 'Wusta',
    }

    # Fetch query parameters
    advertisement=Advertisement.objects.all()
    selected_region_code = request.GET.get('region', None)
    selected_listing_type = request.GET.get('listing_type', None)
    selected_city = request.GET.getlist('city')
    name_query = request.GET.get('name', '')
    price_from = request.GET.get('price_from')
    price_to = request.GET.get('price_to')
    selected_property_type = request.GET.get('property_type', None)
    bedrooms = request.GET.get('bedrooms')
    bathrooms = request.GET.get('bathrooms')
    furnished = request.GET.get('furnished')
    rental_period = request.GET.get('rental_period')
    lister_type = request.GET.get('lister_type')
    property_mortgage = request.GET.get('property_mortgage')
    facade = request.GET.get('facade')  
    floors = request.GET.get('floors')
    building = request.GET.get('building')
    main_amenity = request.GET.get('main_amenity')
    additional_amenity = request.GET.get('additional_amenity')
    nearby = request.GET.get('nearby')

    # Additional Filters
    surface_area_from = request.GET.get('surface_area_from')
    surface_area_to = request.GET.get('surface_area_to')
    
    # Start with all approved staff
    staff = Staff.objects.filter(status='approved')

    # Apply Filters
    if selected_region_code and selected_region_code != "all":
        staff = staff.filter(regions=selected_region_code)
   
    if selected_city:
        # Create a Q object to filter for any of the selected cities
        city_filter = Q()
        for city in selected_city:
            city_filter |= Q(cities__icontains=city)
        staff = staff.filter(city_filter)
    if selected_listing_type and selected_listing_type != "all":
        staff = staff.filter(listing_type=selected_listing_type)
    if selected_property_type and selected_property_type != "all":
        staff = staff.filter(property_type=selected_property_type)
    if name_query:
        staff = staff.filter(
            Q(property_title__icontains=name_query) |
            Q(regions__icontains=name_query) |
            Q(cities__icontains=name_query) |
            Q(listing_type__icontains=name_query) |
            Q(property_type__icontains=name_query)
        )
    if price_from:
        staff = staff.filter(price__gte=price_from)
    if price_to:
        staff = staff.filter(price__lte=price_to)
    if bedrooms:
        bedroom_list = bedrooms.split(',')
        staff = staff.filter(bedrooms__in=bedroom_list)
    if bathrooms:
        bathroom_list = bathrooms.split(',')
        staff = staff.filter(bathrooms__in=bathroom_list)
    if furnished and furnished != "all":
        staff = staff.filter(furnished=furnished)
    if floors:
        floor_list = floors.split(',')
        staff = staff.filter(floors__in=floor_list)
    if building:
        building_list = building.split(',')
        staff = staff.filter(building__in=building_list)
    if rental_period and rental_period != "all":
        staff = staff.filter(rental_period=rental_period)
    if lister_type and lister_type != "all":
        staff = staff.filter(lister_type=lister_type)
    if property_mortgage and property_mortgage != "all":
        staff = staff.filter(property_mortgage=property_mortgage)
    if facade:
        facade_list = facade.split(',')
        staff = staff.filter(facade__in=facade_list)

    # Apply surface area filter if provided
    if surface_area_from and surface_area_to:
       staff = staff.filter(plot_area__gte=surface_area_from, plot_area__lte=surface_area_to)
    elif surface_area_from:
       staff = staff.filter(plot_area__gte=surface_area_from)
    elif surface_area_to:
       staff = staff.filter(plot_area__lte=surface_area_to)
   
    # Main Amenities filter
    if main_amenity:
        main_amenity_list = main_amenity.split(',')
        staff = staff.filter(main_amenities__name__in=main_amenity_list).distinct()
    if additional_amenity:
        additional_amenity_list = additional_amenity.split(',')
        staff = staff.filter(additional_amenities__name__in=additional_amenity_list).distinct()
    if nearby:
        nearby_list = nearby.split(',')
        staff = staff.filter(nearby_location__name__in=nearby_list).distinct()

    # Add images JSON
    for villa in staff:
        villa.images_json = json.dumps([image.image.url for image in villa.images.all()])

    # Pagination
    paginator = Paginator(staff, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Fetch filter options
    regions = [("all", "All")] + list(Villa.REGION_CHOICES)
    listing_types = [("all", "All")] + list(Villa.TRANSACTION_CHOICES)
    furnished_options = [("all", "All")] + list(Villa.FURNISHED_CHOICES)
    building_options = [("all", "All")] + list(Villa.BUILDING_AGE_CHOICES)
    rental_period_options = [("all", "All")] + list(Villa.RENTAL_PERIOD_CHOICES)
    lister_type_options = [("all", "All")] + list(Villa.LISTER_TYPE_CHOICES)
    property_mortgage_options = [("all", "All")] + list(Villa.PROPERTY_MORTGAGE_CHOICES)
    facade_options = [("all", "All")] + list(Villa.FACADE_CHOICES)
    floors_options = [("all", "All")] + list(Villa.FLOOR_CHOICES)

    # Context
    context = {
        'page_obj': page_obj,
        'regions': regions,
        'listing_types': listing_types,
        'furnished_options': furnished_options,
        'building_options': building_options,
        'rental_period_options': rental_period_options,'advertisement':advertisement,
        'lister_type_options': lister_type_options,
        'property_mortgage_options': property_mortgage_options,
        'facade_options': facade_options,
        'floors_options': floors_options,
        'selected_region': region_mapping.get(selected_region_code, selected_region_code) if selected_region_code else None,
        'selected_listing_type': selected_listing_type,
        'selected_city': selected_city,
        'selected_property_type': selected_property_type,
        'name_query': name_query,
        'price_from': price_from,
        'price_to': price_to,
        'bedrooms': bedrooms,
        'bathrooms': bathrooms,
        'selected_furnished': furnished,
        'selected_building': building,
        'selected_rental_period': rental_period,
        'selected_lister_type': lister_type,
        'selected_property_mortgage': property_mortgage,
        'selected_facade': facade,
        'selected_floors': floors,
        'main_amenity': main_amenity,
        'additional_amenity': additional_amenity,
        'nearby': nearby,
        'formatted_url_name': request.resolver_match.url_name.replace("_", " ").title(),
    }

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'estate/staff_list_partial.html', {'page_obj': page_obj,'formatted_url_name': request.resolver_match.url_name.replace("_", " ").title()})
    
    return render(request, 'estate/staff.html', context)


def staff_details(request, id):
    staff = get_object_or_404(Staff.objects.prefetch_related('nearby_location', 'main_amenities', 'additional_amenities'), id=id)
    return render(request, 'estate/staff_details.html', {'staff': staff})

def warehouse(request):
    region_mapping = {
        'MS': 'Muscat', 'DH': 'Dhofar', 'BT': 'Batinah', 'DA': 'Dakhiliyah',
        'SH': 'Sharqiyah', 'BR': 'Buraimi', 'ZU': 'Zufar', 'DZ': 'Masandam', 'WR': 'Wusta',
    }

    # Fetch query parameters
    advertisement=Advertisement.objects.all()
    selected_region_code = request.GET.get('region', None)
    selected_listing_type = request.GET.get('listing_type', None)
    selected_city = request.GET.getlist('city')
    name_query = request.GET.get('name', '')
    price_from = request.GET.get('price_from')
    price_to = request.GET.get('price_to')
    furnished = request.GET.get('furnished')
    rental_period = request.GET.get('rental_period')
    lister_type = request.GET.get('lister_type')
    property_mortgage = request.GET.get('property_mortgage')
    facade = request.GET.get('facade')  
    floors = request.GET.get('floors')
    property = request.GET.get('property')
    main_amenity = request.GET.get('main_amenity')
    additional_amenity = request.GET.get('additional_amenity')
    nearby = request.GET.get('nearby')
    
    # Additional Filters
    surface_area_from = request.GET.get('surface_area_from')
    surface_area_to = request.GET.get('surface_area_to')
   
    # Start with all approved warehouse
    warehouse = Warehouse.objects.filter(status='approved')

    # Apply Filters
    if selected_region_code and selected_region_code != "all":
        warehouse = warehouse.filter(regions=selected_region_code)
   
    if selected_city:
        # Create a Q object to filter for any of the selected cities
        city_filter = Q()
        for city in selected_city:
            city_filter |= Q(cities__icontains=city)
        warehouse = warehouse.filter(city_filter)
    if selected_listing_type and selected_listing_type != "all":
        warehouse = warehouse.filter(listing_type=selected_listing_type)
    if name_query:
        warehouse = warehouse.filter(
            Q(property_title__icontains=name_query) |
            Q(regions__icontains=name_query) |
            Q(cities__icontains=name_query) |
            Q(listing_type__icontains=name_query) |
            Q(property_type__icontains=name_query)
        )
    if price_from:
        warehouse = warehouse.filter(price__gte=price_from)
    if price_to:
        warehouse = warehouse.filter(price__lte=price_to)
    if furnished and furnished != "all":
        warehouse = warehouse.filter(furnished=furnished)
    if floors:
        floor_list = floors.split(',')
        warehouse = warehouse.filter(floors__in=floor_list)
    if property:
        property_list = property.split(',')
        warehouse = warehouse.filter(property__in=property_list)
    if rental_period and rental_period != "all":
        warehouse = warehouse.filter(rental_period=rental_period)
    if lister_type and lister_type != "all":
        warehouse = warehouse.filter(lister_type=lister_type)
    if property_mortgage and property_mortgage != "all":
        warehouse = warehouse.filter(property_mortgage=property_mortgage)
    if facade:
        facade_list = facade.split(',')
        warehouse = warehouse.filter(facade__in=facade_list)

    if surface_area_from and surface_area_to:
       warehouse = warehouse.filter(plot_area__gte=surface_area_from, plot_area__lte=surface_area_to)
    elif surface_area_from:
       warehouse = warehouse.filter(plot_area__gte=surface_area_from)
    elif surface_area_to:
       warehouse = warehouse.filter(plot_area__lte=surface_area_to)
   
    # Main Amenities filter
    if main_amenity:
        main_amenity_list = main_amenity.split(',')
        warehouse = warehouse.filter(main_amenities__name__in=main_amenity_list).distinct()
    if additional_amenity:
        additional_amenity_list = additional_amenity.split(',')
        warehouse = warehouse.filter(additional_amenities__name__in=additional_amenity_list).distinct()
    if nearby:
        nearby_list = nearby.split(',')
        warehouse = warehouse.filter(nearby_location__name__in=nearby_list).distinct()

    # Add images JSON
    for clin in warehouse:
        clin.images_json = json.dumps([image.image.url for image in clin.images.all()])

    # Pagination
    paginator = Paginator(warehouse, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Fetch filter options
    regions = [("all", "All")] + list(Warehouse.REGION_CHOICES)
    listing_types = [("all", "All")] + list(Warehouse.TRANSACTION_CHOICES)
    rental_period_options = [("all", "All")] + list(Warehouse.RENTAL_PERIOD_CHOICES)
    lister_type_options = [("all", "All")] + list(Warehouse.LISTER_TYPE_CHOICES)
    property_mortgage_options = [("all", "All")] + list(Warehouse.PROPERTY_MORTGAGE_CHOICES)
    property_options = [("all", "All")] + list(Warehouse.PROPERTY_CHOICES)

    # Context
    context = {
        'page_obj': page_obj,
        'regions': regions,
        'listing_types': listing_types,
        'rental_period_options': rental_period_options,
        'lister_type_options': lister_type_options,
        'property_mortgage_options': property_mortgage_options,
        'property_options':property_options,
        'selected_region': region_mapping.get(selected_region_code, selected_region_code) if selected_region_code else None,
        'selected_listing_type': selected_listing_type,
        'selected_city': selected_city,'advertisement':advertisement,
        
        'name_query': name_query,
        'price_from': price_from,
        'price_to': price_to,
        'selected_furnished': furnished,
        'selected_rental_period': rental_period,
        'selected_lister_type': lister_type,
        'selected_property_mortgage': property_mortgage,
        'selected_facade': facade,
        'selected_floors': floors,
        'selected_property': property,
        'main_amenity': main_amenity,
        'additional_amenity': additional_amenity,
        'nearby': nearby,
        'formatted_url_name': request.resolver_match.url_name.replace("_", " ").title(),
    }

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'estate/warehouse_list_partial.html', {'page_obj': page_obj,'formatted_url_name': request.resolver_match.url_name.replace("_", " ").title()})
    
    return render(request, 'estate/warehouse.html', context)

def warehouse_details(request, id):
    warehouse = get_object_or_404(Warehouse.objects.prefetch_related('nearby_location', 'main_amenities', 'additional_amenities'), id=id)
    return render(request, 'estate/warehouse_details.html', {'warehouse': warehouse})

from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Q
from .models import Villa, Land, Commercial, Chalet, Farm, MainAmenities, AdditionalAmenities, NearbyLocation
import json
def townhouse(request):
    region_mapping = {
        'MS': 'Muscat', 'DH': 'Dhofar', 'BT': 'Batinah', 'DA': 'Dakhiliyah',
        'SH': 'Sharqiyah', 'BR': 'Buraimi', 'ZU': 'Zufar', 'DZ': 'Masandam', 'WR': 'Wusta',
    }

    # Fetch query parameters
    advertisement=Advertisement.objects.all()
    selected_region_code = request.GET.get('region', None)
    selected_listing_type = request.GET.get('listing_type', None)
    selected_city = request.GET.getlist('city')
    name_query = request.GET.get('name', '')
    price_from = request.GET.get('price_from')
    price_to = request.GET.get('price_to')
    selected_property_type = request.GET.get('property_type', None)
    bedrooms = request.GET.get('bedrooms')
    bathrooms = request.GET.get('bathrooms')
    furnished = request.GET.get('furnished')
    rental_period = request.GET.get('rental_period')
    lister_type = request.GET.get('lister_type')
    property_mortgage = request.GET.get('property_mortgage')
    facade = request.GET.get('facade')  
    floors = request.GET.get('floors')
    building = request.GET.get('building')
    main_amenity = request.GET.get('main_amenity')
    additional_amenity = request.GET.get('additional_amenity')
    nearby = request.GET.get('nearby')

    # Additional Filters
    surface_area_from = request.GET.get('surface_area_from')
    surface_area_to = request.GET.get('surface_area_to')
    land_area_from = request.GET.get('land_area_from')
    land_area_to = request.GET.get('land_area_to')

    # Start with all approved townhouse
    townhouse = Townhouse.objects.filter(status='approved')

    # Apply Filters
    if selected_region_code and selected_region_code != "all":
        townhouse = townhouse.filter(regions=selected_region_code)
   
    if selected_city:
        # Create a Q object to filter for any of the selected cities
        city_filter = Q()
        for city in selected_city:
            city_filter |= Q(cities__icontains=city)
        townhouse = townhouse.filter(city_filter)
    if selected_listing_type and selected_listing_type != "all":
        townhouse = townhouse.filter(listing_type=selected_listing_type)
    if selected_property_type and selected_property_type != "all":
        townhouse = townhouse.filter(property_type=selected_property_type)
    if name_query:
        townhouse = townhouse.filter(
            Q(property_title__icontains=name_query) |
            Q(regions__icontains=name_query) |
            Q(cities__icontains=name_query) |
            Q(listing_type__icontains=name_query) |
            Q(property_type__icontains=name_query)
        )
    if price_from:
        townhouse = townhouse.filter(price__gte=price_from)
    if price_to:
        townhouse = townhouse.filter(price__lte=price_to)
    if bedrooms:
        bedroom_list = bedrooms.split(',')
        townhouse = townhouse.filter(bedrooms__in=bedroom_list)
    if bathrooms:
        bathroom_list = bathrooms.split(',')
        townhouse = townhouse.filter(bathrooms__in=bathroom_list)
    if furnished and furnished != "all":
        townhouse = townhouse.filter(furnished=furnished)
    if floors:
        floor_list = floors.split(',')
        townhouse = townhouse.filter(floors__in=floor_list)
    if building:
        building_list = building.split(',')
        townhouse = townhouse.filter(building__in=building_list)
    if rental_period and rental_period != "all":
        townhouse = townhouse.filter(rental_period=rental_period)
    if lister_type and lister_type != "all":
        townhouse = townhouse.filter(lister_type=lister_type)
    if property_mortgage and property_mortgage != "all":
        townhouse = townhouse.filter(property_mortgage=property_mortgage)
    if facade:
        facade_list = facade.split(',')
        townhouse = townhouse.filter(facade__in=facade_list)

    # Apply surface area filter if provided
    if land_area_from and land_area_to:
       townhouse = townhouse.filter(plot_area__gte=land_area_from, plot_area__lte=land_area_to)
    elif land_area_from:
       townhouse = townhouse.filter(plot_area__gte=land_area_from)
    elif land_area_to:
       townhouse = townhouse.filter(plot_area__lte=land_area_to)
    if surface_area_from and surface_area_to:
       townhouse = townhouse.filter(surface_area__gte=surface_area_from, surface_area__lte=surface_area_to)
    elif surface_area_from:
       townhouse = townhouse.filter(surface_area__gte=surface_area_from)
    elif surface_area_to:
       townhouse = townhouse.filter(surface_area__lte=surface_area_to)
   
    # Main Amenities filter
    if main_amenity:
        main_amenity_list = main_amenity.split(',')
        townhouse = townhouse.filter(main_amenities__name__in=main_amenity_list).distinct()
    if additional_amenity:
        additional_amenity_list = additional_amenity.split(',')
        townhouse = townhouse.filter(additional_amenities__name__in=additional_amenity_list).distinct()
    if nearby:
        nearby_list = nearby.split(',')
        townhouse = townhouse.filter(nearby_location__name__in=nearby_list).distinct()

    # Add images JSON
    for town in townhouse:
        town.images_json = json.dumps([image.image.url for image in town.images.all()])

    # Pagination
    paginator = Paginator(townhouse, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Fetch filter options
    regions = [("all", "All")] + list(Villa.REGION_CHOICES)
    listing_types = [("all", "All")] + list(Villa.TRANSACTION_CHOICES)
    furnished_options = [("all", "All")] + list(Villa.FURNISHED_CHOICES)
    building_options = [("all", "All")] + list(Villa.BUILDING_AGE_CHOICES)
    rental_period_options = [("all", "All")] + list(Villa.RENTAL_PERIOD_CHOICES)
    lister_type_options = [("all", "All")] + list(Villa.LISTER_TYPE_CHOICES)
    property_mortgage_options = [("all", "All")] + list(Villa.PROPERTY_MORTGAGE_CHOICES)
    facade_options = [("all", "All")] + list(Villa.FACADE_CHOICES)
    floors_options = [("all", "All")] + list(Villa.FLOOR_CHOICES)
   
    # Context
    context = {
        'page_obj': page_obj,
        'regions': regions,
        'listing_types': listing_types,
        'furnished_options': furnished_options,
        'building_options': building_options,
        'rental_period_options': rental_period_options,
        'lister_type_options': lister_type_options,
        'property_mortgage_options': property_mortgage_options,
        'facade_options': facade_options,
        'selected_region': region_mapping.get(selected_region_code, selected_region_code) if selected_region_code else None,
        'selected_listing_type': selected_listing_type,
        'selected_city': selected_city,
        'selected_property_type': selected_property_type,
        'floors_options': floors_options,
        'name_query': name_query,
        'price_from': price_from,
        'price_to': price_to,
        'bedrooms': bedrooms,
        'bathrooms': bathrooms,
        'selected_furnished': furnished,
        'selected_building': building,
        'selected_rental_period': rental_period,
        'selected_lister_type': lister_type,
        'selected_property_mortgage': property_mortgage,
        'selected_facade': facade,
        'main_amenity': main_amenity,'advertisement':advertisement,
        'additional_amenity': additional_amenity,
        'nearby': nearby,
        'selected_floors': floors,
        'formatted_url_name': request.resolver_match.url_name.replace("_", " ").title(),
    }

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'estate/town-list-partial.html', {'page_obj': page_obj,'formatted_url_name': request.resolver_match.url_name.replace("_", " ").title()})
    
    return render(request, 'estate/town.html', context)


def townhouse_details(request, id):
    townhouse = get_object_or_404(Townhouse.objects.prefetch_related('nearby_location', 'main_amenities', 'additional_amenities'), id=id)
    return render(request, 'estate/town_details.html', {'townhouse': townhouse})


def fullfloors(request):
    region_mapping = {
        'MS': 'Muscat', 'DH': 'Dhofar', 'BT': 'Batinah', 'DA': 'Dakhiliyah',
        'SH': 'Sharqiyah', 'BR': 'Buraimi', 'ZU': 'Zufar', 'DZ': 'Masandam', 'WR': 'Wusta',
    }

    # Fetch query parameters
    advertisement=Advertisement.objects.all()
    selected_region_code = request.GET.get('region', None)
    selected_listing_type = request.GET.get('listing_type', None)
    selected_city = request.GET.getlist('city')
    name_query = request.GET.get('name', '')
    price_from = request.GET.get('price_from')
    price_to = request.GET.get('price_to')
    furnished = request.GET.get('furnished')
    rental_period = request.GET.get('rental_period')
    lister_type = request.GET.get('lister_type')
    property_mortgage = request.GET.get('property_mortgage')
    facade = request.GET.get('facade')  
    floors = request.GET.get('floors')
    main_amenity = request.GET.get('main_amenity')
    additional_amenity = request.GET.get('additional_amenity')
    nearby = request.GET.get('nearby')
    property = request.GET.get('property')

    # Additional Filters
    surface_area_from = request.GET.get('surface_area_from')
    surface_area_to = request.GET.get('surface_area_to')
   
    # Start with all approved clinic
    fullfloors = Fullfloors.objects.filter(status='approved')

    # Apply Filters
    if selected_region_code and selected_region_code != "all":
        fullfloors = fullfloors.filter(regions=selected_region_code)
   
    if selected_city:
        # Create a Q object to filter for any of the selected cities
        city_filter = Q()
        for city in selected_city:
            city_filter |= Q(cities__icontains=city)
        fullfloors = fullfloors.filter(city_filter)
    if selected_listing_type and selected_listing_type != "all":
        fullfloors = fullfloors.filter(listing_type=selected_listing_type)
    if name_query:
        fullfloors = fullfloors.filter(
            Q(property_title__icontains=name_query) |
            Q(regions__icontains=name_query) |
            Q(cities__icontains=name_query) |
            Q(listing_type__icontains=name_query) |
            Q(property_type__icontains=name_query)
        )
    if price_from:
        fullfloors = fullfloors.filter(price__gte=price_from)
    if price_to:
        fullfloors = fullfloors.filter(price__lte=price_to)
    if furnished and furnished != "all":
        fullfloors = fullfloors.filter(furnished=furnished)
    if floors:
        floor_list = floors.split(',')
        fullfloors = fullfloors.filter(floors__in=floor_list)
    if property:
        property_list = property.split(',')
        fullfloors = fullfloors.filter(property__in=property_list)
    if rental_period and rental_period != "all":
        fullfloors = fullfloors.filter(rental_period=rental_period)
    if lister_type and lister_type != "all":
        fullfloors = fullfloors.filter(lister_type=lister_type)
    if property_mortgage and property_mortgage != "all":
        fullfloors = fullfloors.filter(property_mortgage=property_mortgage)
    if facade:
        facade_list = facade.split(',')
        fullfloors = fullfloors.filter(facade__in=facade_list)

    if surface_area_from and surface_area_to:
       fullfloors = fullfloors.filter(plot_area__gte=surface_area_from, plot_area__lte=surface_area_to)
    elif surface_area_from:
       fullfloors = fullfloors.filter(plot_area__gte=surface_area_from)
    elif surface_area_to:
       fullfloors = fullfloors.filter(plot_area__lte=surface_area_to)
   
    # Main Amenities filter
    if main_amenity:
        main_amenity_list = main_amenity.split(',')
        fullfloors = fullfloors.filter(main_amenities__name__in=main_amenity_list).distinct()
    if additional_amenity:
        additional_amenity_list = additional_amenity.split(',')
        fullfloors = fullfloors.filter(additional_amenities__name__in=additional_amenity_list).distinct()
    if nearby:
        nearby_list = nearby.split(',')
        fullfloors = fullfloors.filter(nearby_location__name__in=nearby_list).distinct()

    # Add images JSON
    for clin in fullfloors:
        clin.images_json = json.dumps([image.image.url for image in clin.images.all()])

    # Pagination
    paginator = Paginator(fullfloors, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Fetch filter options
    regions = [("all", "All")] + list(Fullfloors.REGION_CHOICES)
    listing_types = [("all", "All")] + list(Fullfloors.TRANSACTION_CHOICES)
    rental_period_options = [("all", "All")] + list(Fullfloors.RENTAL_PERIOD_CHOICES)
    lister_type_options = [("all", "All")] + list(Fullfloors.LISTER_TYPE_CHOICES)
    property_mortgage_options = [("all", "All")] + list(Fullfloors.PROPERTY_MORTGAGE_CHOICES)
    floors_options = [("all", "All")] + list(Fullfloors.FLOOR_CHOICES)

    # Context
    context = {
        'page_obj': page_obj,
        'regions': regions,
        'listing_types': listing_types,
        'rental_period_options': rental_period_options,
        'lister_type_options': lister_type_options,
        'property_mortgage_options': property_mortgage_options,
        'floors_options': floors_options,
        'selected_region': region_mapping.get(selected_region_code, selected_region_code) if selected_region_code else None,
        'selected_listing_type': selected_listing_type,
        'selected_city': selected_city,
        
        'name_query': name_query,
        'price_from': price_from,
        'price_to': price_to,
        'selected_furnished': furnished,
        'selected_rental_period': rental_period,
        'selected_lister_type': lister_type,
        'selected_property_mortgage': property_mortgage,
        'selected_facade': facade,
        'selected_floors': floors,'advertisement':advertisement,
        'main_amenity': main_amenity,
        'additional_amenity': additional_amenity,
        'nearby': nearby,
        'formatted_url_name': request.resolver_match.url_name.replace("_", " ").title(),
    }

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'estate/fullfloors_list_partial.html', {'page_obj': page_obj,'formatted_url_name': request.resolver_match.url_name.replace("_", " ").title()})
    
    return render(request, 'estate/fullfloors.html', context)


def fullfloors_details(request, id):
    fullfloors = get_object_or_404(Fullfloors.objects.prefetch_related('nearby_location', 'main_amenities', 'additional_amenities'), id=id)
    return render(request, 'estate/fullfloors_details.html', {'fullfloors': fullfloors})

def showrooms(request):
    region_mapping = {
        'MS': 'Muscat', 'DH': 'Dhofar', 'BT': 'Batinah', 'DA': 'Dakhiliyah',
        'SH': 'Sharqiyah', 'BR': 'Buraimi', 'ZU': 'Zufar', 'DZ': 'Masandam', 'WR': 'Wusta',
    }

    # Fetch query parameters
    advertisement=Advertisement.objects.all()
    selected_region_code = request.GET.get('region', None)
    selected_listing_type = request.GET.get('listing_type', None)
    selected_city = request.GET.getlist('city')
    name_query = request.GET.get('name', '')
    price_from = request.GET.get('price_from')
    price_to = request.GET.get('price_to')
    furnished = request.GET.get('furnished')
    rental_period = request.GET.get('rental_period')
    lister_type = request.GET.get('lister_type')
    property_mortgage = request.GET.get('property_mortgage')
    facade = request.GET.get('facade')  
    floors = request.GET.get('floors')
    property = request.GET.get('property')
    main_amenity = request.GET.get('main_amenity')
    additional_amenity = request.GET.get('additional_amenity')
    nearby = request.GET.get('nearby')
    
    # Additional Filters
    surface_area_from = request.GET.get('surface_area_from')
    surface_area_to = request.GET.get('surface_area_to')
   
    # Start with all approved showroom
    showroom = Showrooms.objects.filter(status='approved')

    # Apply Filters
    if selected_region_code and selected_region_code != "all":
        showroom = showroom.filter(regions=selected_region_code)
   
    if selected_city:
        # Create a Q object to filter for any of the selected cities
        city_filter = Q()
        for city in selected_city:
            city_filter |= Q(cities__icontains=city)
        showroom = showroom.filter(city_filter)
    if selected_listing_type and selected_listing_type != "all":
        showroom = showroom.filter(listing_type=selected_listing_type)
    if name_query:
        showroom = showroom.filter(
            Q(property_title__icontains=name_query) |
            Q(regions__icontains=name_query) |
            Q(cities__icontains=name_query) |
            Q(listing_type__icontains=name_query) |
            Q(property_type__icontains=name_query)
        )
    if price_from:
        showroom = showroom.filter(price__gte=price_from)
    if price_to:
        showroom = showroom.filter(price__lte=price_to)
    if furnished and furnished != "all":
        showroom = showroom.filter(furnished=furnished)
    if floors:
        floor_list = floors.split(',')
        showroom = showroom.filter(floors__in=floor_list)
    if property:
        property_list = property.split(',')
        showroom = showroom.filter(property__in=property_list)
    if rental_period and rental_period != "all":
        showroom = showroom.filter(rental_period=rental_period)
    if lister_type and lister_type != "all":
        showroom = showroom.filter(lister_type=lister_type)
    if property_mortgage and property_mortgage != "all":
        showroom = showroom.filter(property_mortgage=property_mortgage)
    if facade:
        facade_list = facade.split(',')
        showroom = showroom.filter(facade__in=facade_list)

    if surface_area_from and surface_area_to:
       showroom = showroom.filter(plot_area__gte=surface_area_from, plot_area__lte=surface_area_to)
    elif surface_area_from:
       showroom = showroom.filter(plot_area__gte=surface_area_from)
    elif surface_area_to:
       showroom = showroom.filter(plot_area__lte=surface_area_to)
   
    # Main Amenities filter
    if main_amenity:
        main_amenity_list = main_amenity.split(',')
        showroom = showroom.filter(main_amenities__name__in=main_amenity_list).distinct()
    if additional_amenity:
        additional_amenity_list = additional_amenity.split(',')
        showroom = showroom.filter(additional_amenities__name__in=additional_amenity_list).distinct()
    if nearby:
        nearby_list = nearby.split(',')
        showroom = showroom.filter(nearby_location__name__in=nearby_list).distinct()

    # Add images JSON
    for clin in showroom:
        clin.images_json = json.dumps([image.image.url for image in clin.images.all()])

    # Pagination
    paginator = Paginator(showroom, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Fetch filter options
    regions = [("all", "All")] + list(Showrooms.REGION_CHOICES)
    listing_types = [("all", "All")] + list(Showrooms.TRANSACTION_CHOICES)
    rental_period_options = [("all", "All")] + list(Showrooms.RENTAL_PERIOD_CHOICES)
    lister_type_options = [("all", "All")] + list(Showrooms.LISTER_TYPE_CHOICES)
    property_mortgage_options = [("all", "All")] + list(Showrooms.PROPERTY_MORTGAGE_CHOICES)
    property_options = [("all", "All")] + list(Showrooms.PROPERTY_CHOICES)

    # Context
    context = {
        'page_obj': page_obj,
        'regions': regions,
        'listing_types': listing_types,
        'rental_period_options': rental_period_options,
        'lister_type_options': lister_type_options,
        'property_mortgage_options': property_mortgage_options,
        'property_options':property_options,
        'selected_region': region_mapping.get(selected_region_code, selected_region_code) if selected_region_code else None,
        'selected_listing_type': selected_listing_type,
        'selected_city': selected_city,
        
        'name_query': name_query,
        'price_from': price_from,
        'price_to': price_to,
        'selected_furnished': furnished,
        'selected_rental_period': rental_period,
        'selected_lister_type': lister_type,
        'selected_property_mortgage': property_mortgage,'advertisement':advertisement,
        'selected_facade': facade,
        'selected_floors': floors,
        'selected_property': property,
        'main_amenity': main_amenity,
        'additional_amenity': additional_amenity,
        'nearby': nearby,
        'formatted_url_name': request.resolver_match.url_name.replace("_", " ").title(),
    }

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'estate/showrooms_list_partial.html', {'page_obj': page_obj,'formatted_url_name': request.resolver_match.url_name.replace("_", " ").title()})
    
    return render(request, 'estate/showrooms.html', context)


def showrooms_details(request, id):
    showrooms = get_object_or_404(Showrooms.objects.prefetch_related('nearby_location', 'main_amenities', 'additional_amenities'), id=id)
    return render(request, 'estate/showrooms_details.html', {'showrooms': showrooms})

def wholebuilding(request):
    region_mapping = {
        'MS': 'Muscat', 'DH': 'Dhofar', 'BT': 'Batinah', 'DA': 'Dakhiliyah',
        'SH': 'Sharqiyah', 'BR': 'Buraimi', 'ZU': 'Zufar', 'DZ': 'Masandam', 'WR': 'Wusta',
    }

    # Fetch query parameters
    advertisement=Advertisement.objects.all()
    selected_region_code = request.GET.get('region', None)
    selected_listing_type = request.GET.get('listing_type', None)
    selected_city = request.GET.getlist('city')
    name_query = request.GET.get('name', '')
    price_from = request.GET.get('price_from')
    price_to = request.GET.get('price_to')
    furnished = request.GET.get('furnished')
    rental_period = request.GET.get('rental_period')
    lister_type = request.GET.get('lister_type')
    property_mortgage = request.GET.get('property_mortgage')
    facade = request.GET.get('facade')  
    floors = request.GET.get('floors')
    main_amenity = request.GET.get('main_amenity')
    additional_amenity = request.GET.get('additional_amenity')
    nearby = request.GET.get('nearby')
    property = request.GET.get('property')
    building = request.GET.get('building')

    # Additional Filters
    surface_area_from = request.GET.get('surface_area_from')
    surface_area_to = request.GET.get('surface_area_to')
    land_area_from = request.GET.get('land_area_from')
    land_area_to = request.GET.get('land_area_to')
   
    # Start with all approved clinic
    wholebuilding = Wholebuilding.objects.filter(status='approved')

    # Apply Filters
    if selected_region_code and selected_region_code != "all":
        wholebuilding = wholebuilding.filter(regions=selected_region_code)
   
    if selected_city:
        # Create a Q object to filter for any of the selected cities
        city_filter = Q()
        for city in selected_city:
            city_filter |= Q(cities__icontains=city)
        wholebuilding = wholebuilding.filter(city_filter)
    if selected_listing_type and selected_listing_type != "all":
        wholebuilding = wholebuilding.filter(listing_type=selected_listing_type)
    if name_query:
        wholebuilding = wholebuilding.filter(
            Q(property_title__icontains=name_query) |
            Q(regions__icontains=name_query) |
            Q(cities__icontains=name_query) |
            Q(listing_type__icontains=name_query) |
            Q(property_type__icontains=name_query)
        )
    if price_from:
        wholebuilding = wholebuilding.filter(price__gte=price_from)
    if price_to:
        wholebuilding = wholebuilding.filter(price__lte=price_to)
    if furnished and furnished != "all":
        wholebuilding = wholebuilding.filter(furnished=furnished)
    if floors:
        floor_list = floors.split(',')
        wholebuilding = wholebuilding.filter(floors__in=floor_list)
    if property:
        property_list = property.split(',')
        wholebuilding = wholebuilding.filter(property__in=property_list)
    if rental_period and rental_period != "all":
        wholebuilding = wholebuilding.filter(rental_period=rental_period)
    if lister_type and lister_type != "all":
        wholebuilding = wholebuilding.filter(lister_type=lister_type)
    if property_mortgage and property_mortgage != "all":
        wholebuilding = wholebuilding.filter(property_mortgage=property_mortgage)
    if facade:
        facade_list = facade.split(',')
        wholebuilding = wholebuilding.filter(facade__in=facade_list)

    if building:
        building_list = building.split(',')
        wholebuilding = wholebuilding.filter(building__in=building_list)

    if surface_area_from and surface_area_to:
       wholebuilding = wholebuilding.filter(surface_area__gte=surface_area_from, surface_area__lte=surface_area_to)
    elif surface_area_from:
       wholebuilding = wholebuilding.filter(surface_area__gte=surface_area_from)
    elif surface_area_to:
       wholebuilding = wholebuilding.filter(surface_area__lte=surface_area_to)
    if land_area_from and land_area_to:
        wholebuilding = wholebuilding.filter(plot_area__gte=land_area_from, plot_area__lte=land_area_to)
    elif land_area_from:
       wholebuilding = wholebuilding.filter(plot_area__gte=land_area_from)
    elif land_area_to:
       wholebuilding = wholebuilding.filter(plot_area__lte=land_area_to)
   
    # Main Amenities filter
    if main_amenity:
        main_amenity_list = main_amenity.split(',')
        wholebuilding = wholebuilding.filter(main_amenities__name__in=main_amenity_list).distinct()
    if additional_amenity:
        additional_amenity_list = additional_amenity.split(',')
        wholebuilding = wholebuilding.filter(additional_amenities__name__in=additional_amenity_list).distinct()
    if nearby:
        nearby_list = nearby.split(',')
        wholebuilding = wholebuilding.filter(nearby_location__name__in=nearby_list).distinct()

    # Add images JSON
    for clin in wholebuilding:
        clin.images_json = json.dumps([image.image.url for image in clin.images.all()])

    # Pagination
    paginator = Paginator(wholebuilding, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Fetch filter options
    regions = [("all", "All")] + list(Wholebuilding.REGION_CHOICES)
    listing_types = [("all", "All")] + list(Wholebuilding.TRANSACTION_CHOICES)
    rental_period_options = [("all", "All")] + list(Wholebuilding.RENTAL_PERIOD_CHOICES)
    lister_type_options = [("all", "All")] + list(Wholebuilding.LISTER_TYPE_CHOICES)
    property_mortgage_options = [("all", "All")] + list(Wholebuilding.PROPERTY_MORTGAGE_CHOICES)
    floors_options = [("all", "All")] + list(Wholebuilding.FLOOR_CHOICES)
    building_options = [("all", "All")] + list(Wholebuilding.BUILDING_AGE_CHOICES)

    # Context
    context = {
        'page_obj': page_obj,
        'regions': regions,
        'listing_types': listing_types,
        'rental_period_options': rental_period_options,
        'lister_type_options': lister_type_options,
        'property_mortgage_options': property_mortgage_options,
        'floors_options': floors_options,
        'selected_region': region_mapping.get(selected_region_code, selected_region_code) if selected_region_code else None,
        'selected_listing_type': selected_listing_type,
        'selected_city': selected_city,
        'name_query': name_query,
        'price_from': price_from,
        'price_to': price_to,
        'selected_furnished': furnished,
        'selected_rental_period': rental_period,
        'selected_lister_type': lister_type,
        'selected_property_mortgage': property_mortgage,
        'selected_facade': facade,
        'selected_floors': floors,
        'building_options': building_options,
        'selected_building': building,
        'main_amenity': main_amenity,
        'additional_amenity': additional_amenity,
        'nearby': nearby,'advertisement':advertisement,
        'formatted_url_name': request.resolver_match.url_name.replace("_", " ").title(),
    }

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'estate/wholebuilding_listing_partial.html', {'page_obj': page_obj,'formatted_url_name': request.resolver_match.url_name.replace("_", " ").title()})
    
    return render(request, 'estate/wholebuilding.html', context)


def wholebuilding_details(request, id):
    wholebuilding = get_object_or_404(Wholebuilding.objects.prefetch_related('nearby_location'), id=id)
    return render(request, 'estate/wholebuilding_details.html', {'wholebuilding': wholebuilding})

def supermarket(request):
    region_mapping = {
        'MS': 'Muscat', 'DH': 'Dhofar', 'BT': 'Batinah', 'DA': 'Dakhiliyah',
        'SH': 'Sharqiyah', 'BR': 'Buraimi', 'ZU': 'Zufar', 'DZ': 'Masandam', 'WR': 'Wusta',
    }

    # Fetch query parameters
    advertisement=Advertisement.objects.all()
    selected_region_code = request.GET.get('region', None)
    selected_listing_type = request.GET.get('listing_type', None)
    selected_city = request.GET.getlist('city')
    name_query = request.GET.get('name', '')
    price_from = request.GET.get('price_from')
    price_to = request.GET.get('price_to')
    furnished = request.GET.get('furnished')
    rental_period = request.GET.get('rental_period')
    lister_type = request.GET.get('lister_type')
    property_mortgage = request.GET.get('property_mortgage')
    facade = request.GET.get('facade')  
    floors = request.GET.get('floors')
    property = request.GET.get('property')
    main_amenity = request.GET.get('main_amenity')
    additional_amenity = request.GET.get('additional_amenity')
    nearby = request.GET.get('nearby')
    
    # Additional Filters
    surface_area_from = request.GET.get('surface_area_from')
    surface_area_to = request.GET.get('surface_area_to')
   
    # Start with all approved supermarket
    supermarket = Supermarket.objects.filter(status='approved')

    # Apply Filters
    if selected_region_code and selected_region_code != "all":
        supermarket = supermarket.filter(regions=selected_region_code)
   
    if selected_city:
        # Create a Q object to filter for any of the selected cities
        city_filter = Q()
        for city in selected_city:
            city_filter |= Q(cities__icontains=city)
        supermarket = supermarket.filter(city_filter)
    if selected_listing_type and selected_listing_type != "all":
        supermarket = supermarket.filter(listing_type=selected_listing_type)
    if name_query:
        supermarket = supermarket.filter(
            Q(property_title__icontains=name_query) |
            Q(regions__icontains=name_query) |
            Q(cities__icontains=name_query) |
            Q(listing_type__icontains=name_query) |
            Q(property_type__icontains=name_query)
        )
    if price_from:
        supermarket = supermarket.filter(price__gte=price_from)
    if price_to:
        supermarket = supermarket.filter(price__lte=price_to)
    if furnished and furnished != "all":
        supermarket = supermarket.filter(furnished=furnished)
    if floors:
        floor_list = floors.split(',')
        supermarket = supermarket.filter(floors__in=floor_list)
    if property:
        property_list = property.split(',')
        supermarket = supermarket.filter(property__in=property_list)
    if rental_period and rental_period != "all":
        supermarket = supermarket.filter(rental_period=rental_period)
    if lister_type and lister_type != "all":
        supermarket = supermarket.filter(lister_type=lister_type)
    if property_mortgage and property_mortgage != "all":
        supermarket = supermarket.filter(property_mortgage=property_mortgage)
    if facade:
        facade_list = facade.split(',')
        supermarket = supermarket.filter(facade__in=facade_list)

    if surface_area_from and surface_area_to:
       supermarket = supermarket.filter(plot_area__gte=surface_area_from, plot_area__lte=surface_area_to)
    elif surface_area_from:
       supermarket = supermarket.filter(plot_area__gte=surface_area_from)
    elif surface_area_to:
       supermarket = supermarket.filter(plot_area__lte=surface_area_to)
   
    # Main Amenities filter
    if main_amenity:
        main_amenity_list = main_amenity.split(',')
        supermarket = supermarket.filter(main_amenities__name__in=main_amenity_list).distinct()
    if additional_amenity:
        additional_amenity_list = additional_amenity.split(',')
        supermarket = supermarket.filter(additional_amenities__name__in=additional_amenity_list).distinct()
    if nearby:
        nearby_list = nearby.split(',')
        supermarket = supermarket.filter(nearby_location__name__in=nearby_list).distinct()

    # Add images JSON
    for clin in supermarket:
        clin.images_json = json.dumps([image.image.url for image in clin.images.all()])

    # Pagination
    paginator = Paginator(supermarket, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Fetch filter options
    regions = [("all", "All")] + list(Supermarket.REGION_CHOICES)
    listing_types = [("all", "All")] + list(Supermarket.TRANSACTION_CHOICES)
    rental_period_options = [("all", "All")] + list(Supermarket.RENTAL_PERIOD_CHOICES)
    lister_type_options = [("all", "All")] + list(Supermarket.LISTER_TYPE_CHOICES)
    property_mortgage_options = [("all", "All")] + list(Supermarket.PROPERTY_MORTGAGE_CHOICES)
    property_options = [("all", "All")] + list(Supermarket.PROPERTY_CHOICES)

    # Context
    context = {
        'page_obj': page_obj,
        'regions': regions,
        'listing_types': listing_types,
        'rental_period_options': rental_period_options,
        'lister_type_options': lister_type_options,
        'property_mortgage_options': property_mortgage_options,
        'property_options':property_options,
        'selected_region': region_mapping.get(selected_region_code, selected_region_code) if selected_region_code else None,
        'selected_listing_type': selected_listing_type,
        'selected_city': selected_city,
        
        'name_query': name_query,
        'price_from': price_from,
        'price_to': price_to,
        'selected_furnished': furnished,
        'selected_rental_period': rental_period,
        'selected_lister_type': lister_type,
        'selected_property_mortgage': property_mortgage,
        'selected_facade': facade,
        'selected_floors': floors,
        'selected_property': property,
        'main_amenity': main_amenity,
        'additional_amenity': additional_amenity,
        'nearby': nearby,'advertisement':advertisement,
        'formatted_url_name': request.resolver_match.url_name.replace("_", " ").title(),
    }

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'estate/supermarket_list_partial.html', {'page_obj': page_obj,'formatted_url_name': request.resolver_match.url_name.replace("_", " ").title()})
    
    return render(request, 'estate/supermarket.html', context)


def supermarket_details(request, id):
    supermarket = get_object_or_404(Supermarket.objects.prefetch_related('nearby_location', 'main_amenities', 'additional_amenities'), id=id)
    return render(request, 'estate/supermarket_details.html', {'supermarket': supermarket})


from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
import json
from .models import Foreign, Villa, Land, Commercial, Chalet, Farm
from django_countries import countries  

def foreign(request):
    region_mapping = {
        'MS': 'Muscat', 'DH': 'Dhofar', 'BT': 'Batinah', 'DA': 'Dakhiliyah',
        'SH': 'Sharqiyah', 'BR': 'Buraimi', 'ZU': 'Zufar', 'DZ': 'Masandam', 'WR': 'Wusta',
    }

    # Fetch query parameters
    advertisement=Advertisement.objects.all()
    selected_region_code = request.GET.get('region', None)
    selected_listing_type = request.GET.get('listing_type', None)
    selected_city = request.GET.getlist('city')
    name_query = request.GET.get('name', '')
    price_from = request.GET.get('price_from')
    price_to = request.GET.get('price_to')
    selected_property_type = request.GET.get('property_type', None)
    bedrooms = request.GET.get('bedrooms')
    bathrooms = request.GET.get('bathrooms')
    furnished = request.GET.get('furnished')
    rental_period = request.GET.get('rental_period')
    lister_type = request.GET.get('lister_type')
    property_mortgage = request.GET.get('property_mortgage')
    facade = request.GET.get('facade')  
    floors = request.GET.get('floors')
    building = request.GET.get('building')
    main_amenity = request.GET.get('main_amenity')
    additional_amenity = request.GET.get('additional_amenity')
    nearby = request.GET.get('nearby')
    selected_country = request.GET.getlist('country')
    estate_types = request.GET.get('estate_type') 
    # Additional Filters
    surface_area_from = request.GET.get('surface_area_from')
    surface_area_to = request.GET.get('surface_area_to')
    land_area_from = request.GET.get('land_area_from')
    land_area_to = request.GET.get('land_area_to')

    # Start with all approved foreign
    foreign = Foreign.objects.filter(status='approved')

    # Apply Filters
    if selected_region_code and selected_region_code != "all":
        foreign = foreign.filter(regions=selected_region_code)
   
    if selected_city:
        # Create a Q object to filter for any of the selected cities
        city_filter = Q()
        for city in selected_city:
            city_filter |= Q(cities__icontains=city)
        foreign = foreign.filter(city_filter)
    if selected_listing_type and selected_listing_type != "all":
        foreign = foreign.filter(listing_type=selected_listing_type)
    if selected_property_type and selected_property_type != "all":
        foreign = foreign.filter(property_type=selected_property_type)
    if name_query:
        foreign = foreign.filter(
            Q(property_title__icontains=name_query) |
            Q(regions__icontains=name_query) |
            Q(cities__icontains=name_query) |
            Q(listing_type__icontains=name_query) |
            Q(property_type__icontains=name_query)
        )
    if price_from:
        foreign = foreign.filter(price__gte=price_from)
    if price_to:
        foreign = foreign.filter(price__lte=price_to)
    if bedrooms:
        bedroom_list = bedrooms.split(',')
        foreign = foreign.filter(bedrooms__in=bedroom_list)
    if bathrooms:
        bathroom_list = bathrooms.split(',')
        foreign = foreign.filter(bathrooms__in=bathroom_list)
    if furnished and furnished != "all":
        foreign = foreign.filter(furnished=furnished)
    if floors:
        floor_list = floors.split(',')
        foreign = foreign.filter(floors__in=floor_list)
    if building:
        building_list = building.split(',')
        foreign = foreign.filter(building__in=building_list)
    if rental_period and rental_period != "all":
        foreign = foreign.filter(rental_period=rental_period)
    if lister_type and lister_type != "all":
        foreign = foreign.filter(lister_type=lister_type)
    if property_mortgage and property_mortgage != "all":
        foreign = foreign.filter(property_mortgage=property_mortgage)
    if facade:
        facade_list = facade.split(',')
        foreign = foreign.filter(facade__in=facade_list)

    # Apply surface area filter if provided
    if land_area_from and land_area_to:
       foreign = foreign.filter(plot_area_gte=land_area_from, plot_area_lte=land_area_to)
    elif land_area_from:
       foreign = foreign.filter(plot_area__gte=land_area_from)
    elif land_area_to:
       foreign = foreign.filter(plot_area__lte=land_area_to)
    if surface_area_from and surface_area_to:
       foreign = foreign.filter(surface_area_gte=surface_area_from, surface_area_lte=surface_area_to)
    elif surface_area_from:
       foreign = foreign.filter(surface_area__gte=surface_area_from)
    elif surface_area_to:
       foreign = foreign.filter(surface_area__lte=surface_area_to)
   
    if selected_country:
        # Remove "all" if present (since it's not a real country code)
        selected_country = [c for c in selected_country if c != "all"]
        if selected_country:  # Only filter if there are actual countries selected
            foreign = foreign.filter(country__in=selected_country)
    if estate_types:
        estate_types_list =estate_types.split(',')
        foreign = foreign.filter(estate_type__in=estate_types_list)
  

    # Get the list of all available countries
    all_countries = list(countries)
    # Main Amenities filter
    if main_amenity:
        main_amenity_list = main_amenity.split(',')
        foreign = foreign.filter(main_amenities__name__in=main_amenity_list).distinct()
    if additional_amenity:
        additional_amenity_list = additional_amenity.split(',')
        foreign = foreign.filter(additional_amenities_name_in=additional_amenity_list).distinct()
    if nearby:
        nearby_list = nearby.split(',')
        foreign = foreign.filter(nearby_location__name__in=nearby_list).distinct()

    # Add images JSON
    for villa in foreign:
        villa.images_json = json.dumps([image.image.url for image in villa.images.all()])

    # Pagination
    paginator = Paginator(foreign, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Fetch filter options
    regions = [("all", "All")] + list(Foreign.REGION_CHOICES)
    listing_types = [("all", "All")] + list(Foreign.TRANSACTION_CHOICES)
    rental_period_options = [("all", "All")] + list(Foreign.RENTAL_PERIOD_CHOICES)
    lister_type_options = [("all", "All")] + list(Foreign.LISTER_TYPE_CHOICES)
    property_mortgage_options = [("all", "All")] + list(Foreign.PROPERTY_MORTGAGE_CHOICES)

    # Context
    context = {
        'page_obj': page_obj,
        'regions': regions,
        'listing_types': listing_types,
        'rental_period_options': rental_period_options,
        'lister_type_options': lister_type_options,
        'property_mortgage_options': property_mortgage_options,
        'selected_region': region_mapping.get(selected_region_code, selected_region_code) if selected_region_code else None,
        'selected_listing_type': selected_listing_type,
        'selected_city': selected_city,
        'selected_property_type': selected_property_type,
        'name_query': name_query,
        'price_from': price_from,
        'price_to': price_to,
        'bedrooms': bedrooms,
        'selected_country': selected_country,
        'all_countries': all_countries,'advertisement':advertisement,
        'bathrooms': bathrooms,
        'selected_furnished': furnished,
        'selected_building': building,
        'selected_rental_period': rental_period,
        'selected_lister_type': lister_type,
        'selected_property_mortgage': property_mortgage,
        'selected_facade': facade,
        'selected_floors': floors,
        'main_amenity': main_amenity,
        'additional_amenity': additional_amenity,
        'nearby': nearby,
        'formatted_url_name': request.resolver_match.url_name.replace("_", " ").title(),
    }

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'estate/foreign_list_partial.html', {'page_obj': page_obj,'formatted_url_name': request.resolver_match.url_name.replace("foreign", "foreign real estate").replace("_", " ").title()})
    
    return render(request, 'estate/foreign.html', context)



def foreign_details(request, id):
    foreign = get_object_or_404(Foreign.objects.prefetch_related('nearby_location'), id=id)
    return render(request, 'estate/foreign_details.html', {'foreign': foreign})


from django.shortcuts import render
from django.db.models import Q
from django.urls import reverse
import json
import re
from pyproj import Proj, Transformer
from PIL import Image as PILImage, ImageFilter
import pytesseract
from .models import Land, Villa, Apartment, Shop, Cafe
from .forms import ImageUploadForm

def index_sale(request):
    # Mapping region codes to full names
    region_mapping = {
        'MS': 'Muscat', 'DH': 'Dhofar', 'BT': 'Batinah',
        'DA': 'Dakhiliyah', 'SH': 'Sharqiyah', 'BR': 'Buraimi',
        'ZU': 'Zufar', 'DZ': 'Masandam', 'WR': 'Wusta',
    }

    # Count approved ads in each category
    category_counts = {
        'villa': Villa.objects.filter(status='approved', listing_type='sell').count(),
        'land': Land.objects.filter(status='approved', listing_type='sell').count(),
        'apartment': Apartment.objects.filter(status='approved', listing_type='sell').count(),
        'shop': Shop.objects.filter(status='approved', listing_type='sell').count(),
        'cafe': Cafe.objects.filter(status='approved', listing_type='sell').count(),
        
        # 'commercial': Commercial.objects.filter(status='approved', listing_type='sell').count(),
        
        # 'farm': Farm.objects.filter(status='approved', listing_type='sell').count(),
        # 'factory': Factory.objects.filter(status='approved', listing_type='sell').count(),
        # 'complexes': Complex.objects.filter(status='approved', listing_type='sell').count(),
        # 'clinic': Clinic.objects.filter(status='approved', listing_type='sell').count(),
        # 'hostel': Hostel.objects.filter(status='approved', listing_type='sell').count(),
        # 'Office': Office.objects.filter(status='approved', listing_type='sell').count(),
       

       
        # 'staff': Staff.objects.filter(status='approved', listing_type='sell').count(),
        # 'warehouse': Warehouse.objects.filter(status='approved', listing_type='sell').count(),
        # 'townhouse': Townhouse.objects.filter(status='approved', listing_type='sell').count(),
        # 'fullfloors': Fullfloors.objects.filter(status='approved', listing_type='sell').count(),
        # 'showrooms': Showrooms.objects.filter(status='approved', listing_type='sell').count(),

        # 'wholebuilding': Wholebuilding.objects.filter(status='approved', listing_type='sell').count(),
        # 'supermarket': Supermarket.objects.filter(status='approved', listing_type='sell').count(),
        # 'foreign': Foreign.objects.filter(status='approved', listing_type='sell').count(),
    }

    # Fetch filter parameters from request
    selected_region_code = request.GET.get('region')
    selected_city = request.GET.get('city')
    selected_category = request.GET.get('category')
    name_query = request.GET.get('name', '')
    advertisement=Advertisement.objects.all()

    # Convert region code to full name
    selected_region = region_mapping.get(selected_region_code, selected_region_code) if selected_region_code else None

    # Define models for each category
    categories = {
    'lands': Land,
    'villas': Villa,
    'apartments': Apartment,
    'shops': Shop,
    'cafes': Cafe,
    # 'commercial': Commercial,
    # 'farms': Farm,
    # 'factories': Factory,
    # 'complexes': Complex,
    # 'clinics': Clinic,
    # 'hostels': Hostel,
    # 'offices': Office,
    # 'staff': Staff,
    # 'warehouses': Warehouse,
    # 'townhouses': Townhouse,
    # 'fullfloors': Fullfloors,
    # 'showrooms': Showrooms,
    # 'wholebuildings': Wholebuilding,
    # 'supermarkets': Supermarket,
    # 'foreign': Foreign,
}


    # Gather all ads with applied filters
    all_ads = []
    for category_name, model in categories.items():
        if selected_category and category_name.lower() != selected_category.lower():
            continue  # Skip categories that don't match

        query = model.objects.filter(status='approved', listing_type='sell')  # Only 'sell' properties

        if selected_region_code:
            query = query.filter(regions__icontains=selected_region_code)

        if selected_city and selected_city != "All Cities":
            query = query.filter(cities__icontains=selected_city)

        if name_query:
            query = query.filter(
                Q(property_title__icontains=name_query) | 
                Q(regions__icontains=name_query) | 
                Q(cities__icontains=name_query)
            )

        # Fetch ads and extract images
        items = query.order_by('-id')
        for item in items:
            images = [{"image": img.image.url} for img in item.images.all()]
            main_image_url = images[0]["image"] if images else "/static/assets/images/resource/default.jpg"
            images_json = json.dumps(images) if images else "[]"

            all_ads.append({
                'category': category_name.capitalize(),
                'data': item,
                'main_image_url': main_image_url,
                'images_json': images_json,
                'product_type': category_name.lower(),
                'region_name': region_mapping.get(item.regions, item.regions),
            })

    # 🔹 OCR & Coordinate Extraction Section 🔹
    extracted_text = ""
    table_data = []
    converted_coords = []

    if request.method == 'POST' and 'image' in request.FILES:
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.save()
            image_path = uploaded_image.image.path

            # **Step 1: Preprocess Image for Better OCR**
            image = PILImage.open(image_path).convert('L').filter(ImageFilter.MedianFilter(size=3))
            image = image.point(lambda x: 0 if x < 128 else 255, '1')

            # **Step 2: Extract Text Using OCR**
            extracted_text = pytesseract.image_to_string(image)

            # **Step 3: Parse Easting & Northing from Extracted Text**
            lines = extracted_text.split("\n")
            for line in lines:
                numbers = re.findall(r"\d+\.\d+|\d+", line)  # Extract numerical values
                if len(numbers) >= 2:  # Ensure we have at least Easting & Northing
                    table_data.append((numbers[0], numbers[1]))

            # **Step 4: Convert UTM to Latitude & Longitude**
            utm_proj = Proj(proj="utm", zone=40, ellps="WGS84", south=False)
            wgs_proj = Proj(proj="latlong", datum="WGS84")
            transformer = Transformer.from_proj(utm_proj, wgs_proj)

            for easting, northing in table_data:
                try:
                    lon, lat = transformer.transform(float(easting), float(northing))
                    converted_coords.append((lat, lon))
                except Exception as e:
                    print(f"⚠️ Coordinate conversion error: {e}")
    else:
        form = ImageUploadForm()

    # Prepare context for rendering
    context = {
        'all_ads': all_ads,
        'category_counts': category_counts,
        'selected_region': selected_region,'advertisement':advertisement,
        'selected_city': selected_city,
        'selected_category': selected_category,
        'name_query': name_query,
        'property_locations': json.dumps([
            {
                'title': ad['data'].property_title,
                'lat': ad['data'].latitude,
                'lng': ad['data'].longitude,
                'category': ad['product_type'].capitalize(),
                'url': reverse('browseads1', kwargs={'category': ad['product_type'].capitalize(), 'id': ad['data'].id})
            } for ad in all_ads if ad['data'].latitude and ad['data'].longitude
        ]),
        # OCR-related context
        'form': form,
        'extracted_text': extracted_text,
        'table_data': table_data,
        'converted_coords': converted_coords,
    }

    return render(request, 'index_sale.html', context)





def index_rent(request):
    # Mapping region codes to full names
    region_mapping = {
        'MS': 'Muscat', 'DH': 'Dhofar', 'BT': 'Batinah',
        'DA': 'Dakhiliyah', 'SH': 'Sharqiyah', 'BR': 'Buraimi',
        'ZU': 'Zufar', 'DZ': 'Masandam', 'WR': 'Wusta',
    }

    # Count approved ads in each category
    category_counts = {
        'villa': Villa.objects.filter(status='approved', listing_type='rent').count(),
        'land': Land.objects.filter(status='approved', listing_type='rent').count(),
        'apartment': Apartment.objects.filter(status='approved', listing_type='rent').count(),
        'shop': Shop.objects.filter(status='approved', listing_type='rent').count(),
        'cafe': Cafe.objects.filter(status='approved', listing_type='rent').count(),
        
       
    }

    # Fetch filter parameters from request
    selected_region_code = request.GET.get('region')
    selected_city = request.GET.get('city')
    selected_category = request.GET.get('category')
    name_query = request.GET.get('name', '')
    advertisement=Advertisement.objects.all()

    # Convert region code to full name
    selected_region = region_mapping.get(selected_region_code, selected_region_code) if selected_region_code else None

    # Define models for each category
    categories = {
    'lands': Land,
    'villas': Villa,
    'apartments': Apartment,
    'shops': Shop,
    'cafes': Cafe,
   
}


    # Gather all ads with applied filters
    all_ads = []
    for category_name, model in categories.items():
        if selected_category and category_name.lower() != selected_category.lower():
            continue  # Skip categories that don't match

        query = model.objects.filter(status='approved', listing_type='rent')  # Only 'sell' properties

        if selected_region_code:
            query = query.filter(regions__icontains=selected_region_code)

        if selected_city and selected_city != "All Cities":
            query = query.filter(cities__icontains=selected_city)

        if name_query:
            query = query.filter(
                Q(property_title__icontains=name_query) | 
                Q(regions__icontains=name_query) | 
                Q(cities__icontains=name_query)
            )

        # Fetch ads and extract images
        items = query.order_by('-id')
        for item in items:
            images = [{"image": img.image.url} for img in item.images.all()]
            main_image_url = images[0]["image"] if images else "/static/assets/images/resource/default.jpg"
            images_json = json.dumps(images) if images else "[]"

            all_ads.append({
                'category': category_name.capitalize(),
                'data': item,
                'main_image_url': main_image_url,
                'images_json': images_json,
                'product_type': category_name.lower(),
                'region_name': region_mapping.get(item.regions, item.regions),
            })

    # 🔹 OCR & Coordinate Extraction Section 🔹
    extracted_text = ""
    table_data = []
    converted_coords = []

    if request.method == 'POST' and 'image' in request.FILES:
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.save()
            image_path = uploaded_image.image.path

            # **Step 1: Preprocess Image for Better OCR**
            image = PILImage.open(image_path).convert('L').filter(ImageFilter.MedianFilter(size=3))
            image = image.point(lambda x: 0 if x < 128 else 255, '1')

            # **Step 2: Extract Text Using OCR**
            extracted_text = pytesseract.image_to_string(image)

            # **Step 3: Parse Easting & Northing from Extracted Text**
            lines = extracted_text.split("\n")
            for line in lines:
                numbers = re.findall(r"\d+\.\d+|\d+", line)  # Extract numerical values
                if len(numbers) >= 2:  # Ensure we have at least Easting & Northing
                    table_data.append((numbers[0], numbers[1]))

            # **Step 4: Convert UTM to Latitude & Longitude**
            utm_proj = Proj(proj="utm", zone=40, ellps="WGS84", south=False)
            wgs_proj = Proj(proj="latlong", datum="WGS84")
            transformer = Transformer.from_proj(utm_proj, wgs_proj)

            for easting, northing in table_data:
                try:
                    lon, lat = transformer.transform(float(easting), float(northing))
                    converted_coords.append((lat, lon))
                except Exception as e:
                    print(f"⚠️ Coordinate conversion error: {e}")
    else:
        form = ImageUploadForm()

    # Prepare context for rendering
    context = {
        'all_ads': all_ads,
        'category_counts': category_counts,
        'selected_region': selected_region,
        'selected_city': selected_city,
        'selected_category': selected_category,
        'name_query': name_query,'advertisement':advertisement,
        'property_locations': json.dumps([
            {
                'title': ad['data'].property_title,
                'lat': ad['data'].latitude,
                'lng': ad['data'].longitude,
                'category': ad['product_type'].capitalize(),
                'url': reverse('browseads1', kwargs={'category': ad['product_type'].capitalize(), 'id': ad['data'].id})
            } for ad in all_ads if ad['data'].latitude and ad['data'].longitude
        ]),
        # OCR-related context
        'form': form,
        'extracted_text': extracted_text,
        'table_data': table_data,
        'converted_coords': converted_coords,
    }

    return render(request, 'index_rent.html', context)



def shared(request):
    region_mapping = {
        'MS': 'Muscat', 'DH': 'Dhofar', 'BT': 'Batinah', 'DA': 'Dakhiliyah',
        'SH': 'Sharqiyah', 'BR': 'Buraimi', 'ZU': 'Zufar', 'DZ': 'Masandam', 'WR': 'Wusta',
    }

    # Fetch query parameters
    selected_region_code = request.GET.get('region', None)
    selected_listing_type = request.GET.get('listing_type', None)
    selected_city = request.GET.getlist('city')
    name_query = request.GET.get('name', '')
    price_from = request.GET.get('price_from')
    price_to = request.GET.get('price_to')
    selected_property_type = request.GET.get('property_type', None)
    bedrooms = request.GET.get('bedrooms')
    bathrooms = request.GET.get('bathrooms')
    furnished = request.GET.get('furnished')
    rental_period = request.GET.get('rental_period')
    lister_type = request.GET.get('lister_type')
    property_mortgage = request.GET.get('property_mortgage')
    facade = request.GET.get('facade')  
    floors = request.GET.get('floors')
    building = request.GET.get('building')
    main_amenity = request.GET.get('main_amenity')
    additional_amenity = request.GET.get('additional_amenity')
    nearby = request.GET.get('nearby')
    advertisement=Advertisement.objects.all()

    # Additional Filters
    surface_area_from = request.GET.get('surface_area_from')
    surface_area_to = request.GET.get('surface_area_to')
    land_area_from = request.GET.get('land_area_from')
    land_area_to = request.GET.get('land_area_to')

    # Start with all approved sharedroom
    sharedroom =Shared.objects.filter(status='approved')

    # Apply Filters
    if selected_region_code and selected_region_code != "all":
        sharedroom = sharedroom.filter(regions=selected_region_code)
   
    if selected_city:
        # Create a Q object to filter for any of the selected cities
        city_filter = Q()
        for city in selected_city:
            city_filter |= Q(cities__icontains=city)
        sharedroom = sharedroom.filter(city_filter)
    if selected_listing_type and selected_listing_type != "all":
        sharedroom = sharedroom.filter(listing_type=selected_listing_type)
    if selected_property_type and selected_property_type != "all":
        sharedroom = sharedroom.filter(property_type=selected_property_type)
    if name_query:
        sharedroom = sharedroom.filter(
            Q(property_title__icontains=name_query) |
            Q(regions__icontains=name_query) |
            Q(cities__icontains=name_query) |
            Q(listing_type__icontains=name_query) |
            Q(property_type__icontains=name_query)
        )
    if price_from:
        sharedroom = sharedroom.filter(price__gte=price_from)
    if price_to:
        sharedroom = sharedroom.filter(price__lte=price_to)
    if bedrooms:
        bedroom_list = bedrooms.split(',')
        sharedroom = sharedroom.filter(bedrooms__in=bedroom_list)
    if bathrooms:
        bathroom_list = bathrooms.split(',')
        sharedroom = sharedroom.filter(bathrooms__in=bathroom_list)
    if furnished and furnished != "all":
        sharedroom = sharedroom.filter(furnished=furnished)
    if floors:
        floor_list = floors.split(',')
        sharedroom = sharedroom.filter(floors__in=floor_list)
    if building:
        building_list = building.split(',')
        sharedroom = sharedroom.filter(building__in=building_list)
    if rental_period:
        rental_period_list = rental_period.split(',')
        sharedroom = sharedroom.filter(rental_period__in=rental_period_list)
    if lister_type and lister_type != "all":
        sharedroom = sharedroom.filter(lister_type=lister_type)
    if property_mortgage and property_mortgage != "all":
        sharedroom = sharedroom.filter(property_mortgage=property_mortgage)
    if facade:
        facade_list = facade.split(',')
        sharedroom = sharedroom.filter(facade__in=facade_list)

    # Apply surface area filter if provided
    if land_area_from and land_area_to:
       sharedroom = sharedroom.filter(plot_area_gte=land_area_from, plot_area_lte=land_area_to)
    elif land_area_from:
       sharedroom = sharedroom.filter(plot_area__gte=land_area_from)
    elif land_area_to:
       sharedroom = sharedroom.filter(plot_area__lte=land_area_to)
    if surface_area_from and surface_area_to:
       sharedroom = sharedroom.filter(surface_area_gte=surface_area_from, surface_area_lte=surface_area_to)
    elif surface_area_from:
       sharedroom = sharedroom.filter(surface_area__gte=surface_area_from)
    elif surface_area_to:
       sharedroom = sharedroom.filter(surface_area__lte=surface_area_to)
   
    # Main Amenities filter
    if main_amenity:
        main_amenity_list = main_amenity.split(',')
        sharedroom = sharedroom.filter(main_amenities_name_in=main_amenity_list).distinct()
    if additional_amenity:
        additional_amenity_list = additional_amenity.split(',')
        sharedroom = sharedroom.filter(additional_amenities_name_in=additional_amenity_list).distinct()
    if nearby:
        nearby_list = nearby.split(',')
        sharedroom = sharedroom.filter(nearby_location_name_in=nearby_list).distinct()

    # Add images JSON
    for villa in sharedroom:
        villa.images_json = json.dumps([image.image.url for image in villa.images.all()])

    # Pagination
    paginator = Paginator(sharedroom, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Fetch filter options
    regions = [("all", "All")] + list(Shared.REGION_CHOICES)
    listing_types = [("all", "All")] + list(Shared.TRANSACTION_CHOICES)
    furnished_options = [("all", "All")] + list(Shared.FURNISHED_CHOICES)
    rental_period_options = [("all", "All")] + list(Shared.RENTAL_PERIOD_CHOICES)
    

    # Context
    context = {
        'page_obj': page_obj,
        'regions': regions,
        'listing_types': listing_types,
        'furnished_options': furnished_options,
        'rental_period_options': rental_period_options,
        'selected_region': region_mapping.get(selected_region_code, selected_region_code) if selected_region_code else None,
        'selected_listing_type': selected_listing_type,
        'selected_city': selected_city,
        'selected_property_type': selected_property_type,
        'name_query': name_query,
        'price_from': price_from,
        'price_to': price_to,
        'bedrooms': bedrooms,
        'bathrooms': bathrooms,
        'selected_furnished': furnished,
        'selected_building': building,
        'selected_rental_period': rental_period,
        'selected_lister_type': lister_type,
        'selected_property_mortgage': property_mortgage,
        'selected_facade': facade,
        'selected_floors': floors,
        'main_amenity': main_amenity,'advertisement':advertisement,
        'additional_amenity': additional_amenity,
        'nearby': nearby,
        'formatted_url_name': request.resolver_match.url_name.replace("_", " ").title(),
    }

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'estate/sharedroom_list_partial.html', {'page_obj': page_obj,'formatted_url_name': request.resolver_match.url_name.replace("shared", "shared rooms").replace("_", " ").title()})
    
    return render(request, 'estate/sharedroom.html', context)


def shared_details(request, id):
    shared = get_object_or_404(Shared.objects.prefetch_related('images', 'videos'), id=id)
    return render(request, 'estate/sharedroom_details.html', {'shared': shared})


def suits(request):
    region_mapping = {
        'MS': 'Muscat', 'DH': 'Dhofar', 'BT': 'Batinah', 'DA': 'Dakhiliyah',
        'SH': 'Sharqiyah', 'BR': 'Buraimi', 'ZU': 'Zufar', 'DZ': 'Masandam', 'WR': 'Wusta',
    }

    # Fetch query parameters
    advertisement=Advertisement.objects.all()
    selected_region_code = request.GET.get('region', None)
    selected_listing_type = request.GET.get('listing_type', None)
    selected_city = request.GET.getlist('city')
    name_query = request.GET.get('name', '')
    price_from = request.GET.get('price_from')
    price_to = request.GET.get('price_to')
    selected_property_type = request.GET.get('property_type', None)
    bedrooms = request.GET.get('bedrooms')
    bathrooms = request.GET.get('bathrooms')
    furnished = request.GET.get('furnished')
    rental_period = request.GET.get('rental_period')
    lister_type = request.GET.get('lister_type')
    property_mortgage = request.GET.get('property_mortgage')
    facade = request.GET.get('facade')  
    floors = request.GET.get('floors')
    building = request.GET.get('building')
    main_amenity = request.GET.get('main_amenity')
    additional_amenity = request.GET.get('additional_amenity')
    nearby = request.GET.get('nearby')

    # Additional Filters
    surface_area_from = request.GET.get('surface_area_from')
    surface_area_to = request.GET.get('surface_area_to')
    land_area_from = request.GET.get('land_area_from')
    land_area_to = request.GET.get('land_area_to')

    # Start with all approved suits
    suits =Suits.objects.filter(status='approved')

    # Apply Filters
    if selected_region_code and selected_region_code != "all":
        suits = suits.filter(regions=selected_region_code)
   
    if selected_city:
        # Create a Q object to filter for any of the selected cities
        city_filter = Q()
        for city in selected_city:
            city_filter |= Q(cities__icontains=city)
        suits = suits.filter(city_filter)
    if selected_listing_type and selected_listing_type != "all":
        suits = suits.filter(listing_type=selected_listing_type)
    if selected_property_type and selected_property_type != "all":
        suits = suits.filter(property_type=selected_property_type)
    if name_query:
        suits = suits.filter(
            Q(property_title__icontains=name_query) |
            Q(regions__icontains=name_query) |
            Q(cities__icontains=name_query) |
            Q(listing_type__icontains=name_query) |
            Q(property_type__icontains=name_query)
        )
    if price_from:
        suits = suits.filter(price__gte=price_from)
    if price_to:
        suits = suits.filter(price__lte=price_to)
    if bedrooms:
        bedroom_list = bedrooms.split(',')
        suits = suits.filter(bedrooms__in=bedroom_list)
    if bathrooms:
        bathroom_list = bathrooms.split(',')
        suits = suits.filter(bathrooms__in=bathroom_list)
    if furnished and furnished != "all":
        suits = suits.filter(furnished=furnished)
    if floors:
        floor_list = floors.split(',')
        suits = suits.filter(floors__in=floor_list)
    if building:
        building_list = building.split(',')
        suits = suits.filter(building__in=building_list)
    if rental_period:
        rental_period_list = rental_period.split(',')
        suits = suits.filter(rental_period__in=rental_period_list)
    if lister_type and lister_type != "all":
        suits = suits.filter(lister_type=lister_type)
    if property_mortgage and property_mortgage != "all":
        suits = suits.filter(property_mortgage=property_mortgage)
    if facade:
        facade_list = facade.split(',')
        suits = suits.filter(facade__in=facade_list)

    # Apply surface area filter if provided
    if land_area_from and land_area_to:
       suits = suits.filter(plot_area_gte=land_area_from, plot_area_lte=land_area_to)
    elif land_area_from:
       suits = suits.filter(plot_area__gte=land_area_from)
    elif land_area_to:
       suits = suits.filter(plot_area__lte=land_area_to)
    if surface_area_from and surface_area_to:
       suits = suits.filter(surface_area_gte=surface_area_from, surface_area_lte=surface_area_to)
    elif surface_area_from:
       suits = suits.filter(surface_area__gte=surface_area_from)
    elif surface_area_to:
       suits = suits.filter(surface_area__lte=surface_area_to)
   
    # Main Amenities filter
    if main_amenity:
        main_amenity_list = main_amenity.split(',')
        suits = suits.filter(main_amenities_name_in=main_amenity_list).distinct()
    if additional_amenity:
        additional_amenity_list = additional_amenity.split(',')
        suits = suits.filter(additional_amenities_name_in=additional_amenity_list).distinct()
    if nearby:
        nearby_list = nearby.split(',')
        suits = suits.filter(nearby_location_name_in=nearby_list).distinct()

    # Add images JSON
    for villa in suits:
        villa.images_json = json.dumps([image.image.url for image in villa.images.all()])

    # Pagination
    paginator = Paginator(suits, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Fetch filter options
    regions = [("all", "All")] + list(Suits.REGION_CHOICES)
    listing_types = [("all", "All")] + list(Suits.TRANSACTION_CHOICES)
    furnished_options = [("all", "All")] + list(Suits.FURNISHED_CHOICES)
    rental_period_options = [("all", "All")] + list(Suits.RENTAL_PERIOD_CHOICES)
    

    # Context
    context = {
        'page_obj': page_obj,
        'regions': regions,
        'listing_types': listing_types,
        'furnished_options': furnished_options,
        'rental_period_options': rental_period_options,
        'selected_region': region_mapping.get(selected_region_code, selected_region_code) if selected_region_code else None,
        'selected_listing_type': selected_listing_type,
        'selected_city': selected_city,
        'selected_property_type': selected_property_type,
        'name_query': name_query,
        'price_from': price_from,
        'price_to': price_to,
        'bedrooms': bedrooms,
        'bathrooms': bathrooms,
        'selected_furnished': furnished,
        'selected_building': building,
        'selected_rental_period': rental_period,
        'selected_lister_type': lister_type,'advertisement':advertisement,
        'selected_property_mortgage': property_mortgage,
        'selected_facade': facade,
        'selected_floors': floors,
        'main_amenity': main_amenity,
        'additional_amenity': additional_amenity,
        'nearby': nearby,
        'formatted_url_name': request.resolver_match.url_name.replace("_", " ").title(),
    }

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'estate/hotelapartments_list_partial.html', {'page_obj': page_obj,'formatted_url_name': request.resolver_match.url_name.replace("_", " ").title()})
    
    return render(request, 'estate/hotelapartment.html', context)


def suits_details(request, id):
    suits = get_object_or_404(Suits.objects.prefetch_related('images', 'videos'), id=id)
    return render(request, 'estate/hotelapartmen_details.html', {'suits': suits})
