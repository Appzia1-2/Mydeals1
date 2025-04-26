from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .import views
from .forms import CustomPasswordResetForm
from .views import CustomPasswordResetConfirmView
from django.contrib.auth import views as auth_views
urlpatterns = [
# path('map/', views.map_view, name='map_view'),
path('map1/', views.upload_image, name='upload_image'),

path('', views.index, name='index'),
path('indexarabic', views.indexarabic, name='indexarabic'),

path('login/', views.login1, name='login'),
path('sign/', views.sign, name='sign'),
path('cars/<str:make>/', views.car_make, name='car_make'),
path('motorcycles/<str:make>/', views.motorcycle_make, name='motorcycle_make'),
path('heavyvehicles/<str:manufacturer>/', views.heavy_vehicle_manufacturer, name='heavy_vehicle_manufacturer'),
path('boats/<str:manufacturer>/', views.boat_manufacturer, name='boat_manufacturer'),

path('index2/', views.index2, name='index2'),
path('index3/', views.index3, name='index3'),
path('job/', views.job, name='job'),
path('index5/', views.index5, name='index5'),
path('index6/', views.index6, name='index6'),
path('mobilelist/', views.mobilelist, name='mobilelist'),
path('community/', views.community, name='community'),

#property
path('villas', views.villa, name='villa'),
path('land', views.land, name='land'),
path('commercial', views.commercial, name='commercial'),
path('farm', views.farm, name='farm'),
path('chalet', views.chalet, name='chalet'),
path('browseads2/<str:category>/<int:id>/', views.browseads2, name='browseads2'),

#property_details
path('farm/<int:id>/', views.farm_details, name='farm_details'),
path('villa/<int:id>/', views.villa_details, name='villa_details'),
path('land/<int:id>/', views.land_details, name='land_details'),
path('commercial/<int:id>/', views.commercial_details, name='commercial_details'),
path('chalet/<int:id>/', views.chalet_details, name='chalet_details'),

#classifieds
path('fashion', views.fashion, name='fashion'),
path('toys', views.toys, name='toys'),
path('food', views.foods, name='foods'),
path('fitness', views.fitness, name='fitness'),
path('pets', views.pets, name='pets'),
path('books', views.books, name='books'),
path('appliances', views.appliances, name='appliances'),

path('fashion/<int:id>/', views.fashion_details, name='fashion_details'),
path('toy/<int:id>/', views.toy_details, name='toy_details'),
path('food/<int:id>/', views.food_details, name='food_details'),
path('fitness/<int:id>/', views.fitness_details, name='fitness_details'),
path('pet/<int:id>/', views.pet_details, name='pet_details'),
path('book/<int:id>/', views.book_details, name='book_details'),
path('appliance/<int:id>/', views.appliance_details, name='appliance_details'),


#electronics
path('mobiles', views.mobiles, name='mobiles'),
path('computer', views.computer, name='computer'),
path('sounds', views.sounds, name='sounds'),


#electronics_details
path('mobiles/<int:id>/', views.mobiles_details, name='mobiles_details'),
path('computer/<int:id>/', views.computer_details, name='computer_details'),
path('sounds/<int:id>/', views.sounds_details, name='sounds_details'),

#community
path('business', views.business, name='business'),
path('education', views.education, name='education'),
path('service', views.service, name='service'),


#community_details
path('business/<int:id>/', views.business_details, name='business_details'),
path('education/<int:id>/', views.education_details, name='education_details'),
path('service/<int:id>/', views.service_details, name='service_details'),

#motors
path('car', views.car, name='car'),
path('motorcycle', views.motorcycle, name='motorcycle'),
path('heavyvehicle', views.heavyvehicle, name='heavyvehicle'),
path('accessoriesparts', views.accessoriesparts, name='accessoriesparts'),
path('boat', views.boat, name='boat'),
path('numberplate', views.numberplate, name='numberplate'),

#motors_details
path('car/<int:id>/', views.car_details, name='car_details'),
path('motorcycle/<int:id>/', views.motorcycle_details, name='motorcycle_details'),
path('heavyvehicle/<int:id>/', views.heavyvehicle_details, name='heavyvehicle_details'),
path('accessoriesparts/<int:id>/', views.accessoriesparts_details, name='accessoriesparts_details'),
path('boat/<int:id>/', views.boat_details, name='boat_details'),
path('numberplate/<int:id>/', views.numberplate_details, name='numberplate_details'),


path('browse-ads-2/', views.browseads2, name='browse-ads-2'),
path('browse-ads-3/', views.browseads3, name='browse-ads-3'),
path('joblist/', views.joblist, name='joblist'),
path('classifiedlist/', views.classifiedlist, name='classifiedlist'),
path('communitylist', views.communitylist, name='communitylist'),


path('browse-ads-details/', views.browseadsdetails, name='browse-ads-details'),
path('browse-ads-1/<str:category>/<int:id>/', views.browseads1, name='browseads1'),
path('jobdetails/', views.jobdetails, name='jobdetails'),
 path('classified/<str:ad_type>/<int:ad_id>/', views.classified_details, name='classified_details'),
 path('classified/<str:ad_type>/<int:ad_id>/', views.classified_details, name='classified_details'),

path('details/<str:category>/<int:id>/', views.mobiledetails, name='mobiledetails'),
# path('community/<str:ad_type>/<int:ad_id>/', views.communitydetails, name='communitydetails'),
path('community/<str:ad_type>/<int:ad_id>/', views.communitydetails, name='communitydetails'),



#user
path('profile/<int:user_id>/', views.userprofile, name='userprofile'),
path('job-application/<int:user_id>/', views.jobapplication, name='jobapplication'),
path('listingads/', views.listingads, name='listingads'),
path('account/settings/<int:user_id>/', views.account_settings, name='account_settings'),
path('ads/<int:user_id>/', views.listingadss, name='listingadss'),
path('user/<int:user_id>/listing/', views.adss, name='adss1'),
path('listingclassified/', views.listingclassified, name='listingclassified'),
path('listingsub/', views.listingsub, name='listingsub'),
path('listingsub1/', views.listingsub1, name='listingsub1'),
path('listingcommunity/', views.listingcommunity, name='listingcommunity'),



path('favorites/<int:user_id>/', views.favorites, name='favorites'),
path('listingmobile/', views.listingmobile, name='listingmobile'),

#job
path('jobcategories/', views.jobcategories, name='jobcategories'),
 path('jobcategory/<int:category_id>/', views.jobcategorylist, name='jobcategorylist'),# ADMIN 
path('company/<int:company_id>/posts/ajax/', views.view_company_posts_ajax, name='view_company_posts_ajax'),
 path('jobdetails/<int:user_id>/<int:job_id>/', views.jobdetails, name='jobdetails'),
# ADMIN 

path('admin/',views.admin,name='admin'),
path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
path('adminlogout/',views. logoutadmin,name='adminlogout'),


path('category/', views.category, name='category'),
path('subcategory/', views.subcategory, name='subcategory'),

path('add-to-favorites/<str:product_type>/<int:product_id>/<str:action>/', views.add_to_favorites, name='add_to_favorites'),



# authenticated user reg,login,logout

path('signup/', views.signup_view1, name='signup'),
path('login1/', views.custom_login_view1, name='login1'),
path('logout/', views.custom_logout_view, name='logout'),

# forgot passwrd

path('password_reset/', views.password_reset_view, name='password_reset'),
path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'), 
path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),

# user product details
path('product/<str:product_type>/<int:product_id>/', views.product_detail, name='product_detail'),
path('product/<str:product_type>/<int:product_id>/delete/', views.delete_product, name='delete_product'),

# dashboard
path('property/<str:property_type>/<int:pk>/', views.property_detail_view, name='property_detail_view'),
path('automobile/<int:pk>/', views.automobile_detail_view, name='automobile_detail_view'),
path('product-dashboard/', views.product_dashboard, name='product_dashboard'),
path('get_product_details/<str:product_type>/<int:product_id>/', views.get_product_details, name='get_product_details'),

# admin category
path('category/', views.category, name='category'),
path('admin/category/add/', views.add_category, name='add_category'),
path('admin/category/<int:cat_id>/edit/', views.edit_category, name='edit_category'),
path('admin/category/<int:cat_id>/', views.view_category, name='view_category'),
path('admin/category/<int:cat_id>/delete/', views.delete_category, name='delete_category'),

# user admin dashboard
path('user/', views.user, name='user'),
path('admin/user/add/', views.add_user, name='add_user'),
path('admin/user/<int:pk>/edit/', views.edit_user, name='edit_user'),
path('admin/user/<int:user_id>/', views.view_user, name='view_user'),
path('admin/user/<int:user_id>/delete/', views.delete_user, name='delete_user'),

#jobcategory
path('jobcategory/', views.jobcategory, name='jobcategory'),
path('jobpost/', views.jobpost, name='jobpost'),
path('admin/jobcategory/add/', views.add_jobcategory, name='add_jobcategory'),
path('admin/jobcategory/<int:jobcat_id>/edit/', views.edit_jobcategory, name='edit_jobcategory'),
path('admin/jobcategory/<int:jobcat_id>/', views.view_jobcategory, name='view_jobcategory'),
path('admin/jobcategory/<int:jobcat_id>/delete/', views.delete_jobcategory, name='delete_jobcategory'),

#region
path('region/', views.region, name='region'),
path('region/', views.region, name='region'),
path('admin/region/add/', views.add_region, name='add_region'),
path('admin/region/<int:region_id>/edit/', views.edit_region, name='edit_region'),
path('admin/region/<int:region_id>/', views.view_region, name='view_region'),
path('admin/region/<int:region_id>/delete/', views.delete_region, name='delete_region'),

#nearby_location
path('nearbylocation/', views.nearbylocation, name='nearbylocation'),
path('admin/nearbylocation/add/', views.add_nearbylocation, name='add_nearbylocation'),
path('admin/nearbylocation/<int:nearbylocation_id>/edit/', views.edit_nearbylocation, name='edit_nearbylocation'),
path('admin/nearbylocation/<int:nearbylocation_id>/', views.view_nearbylocation, name='view_nearbylocation'),
path('admin/nearbylocation/<int:nearbylocation_id>/delete/', views.delete_nearbylocation, name='delete_nearbylocation'),

#main_amenities
path('mainamenities/', views.mainamenities, name='mainamenities'),
path('admin/mainamenities/add/', views.add_mainamenities, name='add_mainamenities'),
path('admin/mainamenities/<int:mainamenities_id>/edit/', views.edit_mainamenities, name='edit_mainamenities'),
path('admin/mainamenities/<int:mainamenities_id>/', views.view_mainamenities, name='view_mainamenities'),
path('admin/mainamenities/<int:mainamenities_id>/delete/', views.delete_mainamenities, name='delete_mainamenities'),

#additional_amenities
path('additionalamenities/', views.additionalamenities, name='additionalamenities'),
path('admin/additionalamenities/add/', views.add_additionalamenities, name='add_additionalamenities'),
path('admin/additionalamenities/<int:additionalamenities_id>/edit/', views.edit_additionalamenities, name='edit_additionalamenities'),
path('admin/additionalamenities/<int:additionalamenities_id>/', views.view_additionalamenities, name='view_additionalamenities'),
path('admin/additionalamenities/<int:additionalamenities_id>/delete/', views.delete_additionalamenities, name='delete_additionalamenities'),

#advertisements
path('advertisement/', views.advertisement, name='advertisement'),
path('admin/advertisements/add/', views.add_advertisements, name='add_advertisements'),
path('admin/advertisements/<int:advertisement_id>/edit/', views.edit_advertisements, name='edit_advertisements'),
path('admin/advertisements/<int:advertisement_id>/', views.view_advertisements, name='view_advertisements'),
path('admin/advertisements/<int:advertisement_id>/delete/', views.delete_advertisements, name='delete_advertisements'),

#city
path('city/', views.city, name='city'),
path('admin/city/add/', views.add_city, name='add_city'),
path('admin/city/<int:city_id>/edit/', views.edit_city, name='edit_city'),
path('admin/city/<int:city_id>/', views.view_city, name='view_city'),
path('admin/city/<int:city_id>/delete/', views.delete_city, name='delete_city'),

# job we are hiring
path('we_are_hiring/', views.we_are_hiring, name='we_are_hiring'),
path('personal-registration/', views.personal_registration, name='personal_registration'),
path('company-registration/<int:user_id>/', views.register_company, name='company_registration'),
path('dashboard/<int:user_id>/<int:company_id>/', views.company_dashboard, name='company_dashboard'),



# product soldout
path('<str:product_type>/<int:product_id>/soldout/',views.mark_sold_out, name='mark_sold_out'),


 path('chat/', views.user_chat_view, name='user_chat'),

 path('chat/<int:receiver_id>/', views.user_chat_view, name='user_chat_user'),  # Chat with specific user
path('admin/chats/', views.admin_chat_list_view, name='admin_chat_list'),
    path('admin/chats/<int:user_id>/', views.admin_chat_view, name='admin_chat_view'),

# jpb 30-12-24
path('jobdetailsindex/<int:job_id>/', views.job_details_index, name='jobdetailsindex'),
path('job/<int:job_id>/', views.job_details_non_authenticated, name='jobdetailsnon'),
path('jobs/full-time/', views.full_time_jobs, name='full_time_jobs'),
path('jobs/part-time/', views.part_time_jobs, name='part_time_jobs'),
path('job_post/<int:pk>/', views.job_post_detail, name='job_post_detail'),

path('browse-ads-11/<str:category>/<int:id>/', views.browseads11, name='browseads11'),
 

       #  mobiles by brand
path('mobiles/<str:brand>/', views.mobiles_by_brand, name='mobiles_by_brand'),
path('computer/<str:brand>/', views.computer_by_brand, name='computer_by_brand'),
 path('sound/<str:brand>/', views.sound_by_brand, name='sound_by_brand'),

 
 path('cars/<str:make>/', views.car_make, name='car_make'),
path('motorcycle/<str:make>/', views.motorcycle_make, name='motorcycle_make'),
 path('heavy-vehicles/<str:manufacturer>/', views.heavy_vehicle_manufacturer, name='heavy_vehicle'),  
  path('boat/<str:manufacturer>/', views.boat_manufacturer, name='boat'), 

path('company/<int:user_id>/<int:company_id>/edit/', views.edit_company, name='edit_company'),
  path('application/approve/<int:application_id>/', views.approve_application, name='approve_application'),
    path('application/reject/<int:application_id>/', views.reject_application, name='reject_application'),
      path('companies/',views.company_list_view, name='company_list'),
path('delete_company/<int:company_id>/', views.delete_company, name='delete_company'),




 path('register/', views.register_driving_training, name='register_driving_training'),

path('driving-training/', views.driving_training, name='driving_training'),
 path('driving/<int:id>/', views.driving_details, name='driving_details'),


path('demo',views.demo,name='demo'),








# ---------------------------------------------new--------------------------------------------

path('index_sale/', views.index_sale, name='index_sale'),
path('index_rent/', views.index_rent, name='index_rent'),


path('apartment', views.apartment, name='apartment'),
path('apartment/<int:id>/', views.apartment_details, name='apartment_details'),

path('shared', views.shared, name='shared'),
path('shared/<int:id>/', views.shared_details, name='shared_details'),

path('suits', views.suits, name='suits'),
path('suits/<int:id>/', views.suits_details, name='suits_details'),


path('complex', views.complex, name='complex'),
path('complex/<int:id>/', views.complex_details, name='complex_details'),


path('clinic', views.clinic, name='clinic'),
path('clinic/<int:id>/', views.clinic_details, name='clinic_details'),

path('hostel', views.hostel, name='hostel'),
path('hostel/<int:id>/', views.hostel_details, name='hostel_details'),

path('office', views.office, name='office'),
path('office/<int:id>/', views.office_details, name='office_details'),

path('shop', views.shop, name='shop'),
path('shop/<int:id>/', views.shop_details, name='shop_details'),

path('cafe', views.cafe, name='cafe'),
path('cafe/<int:id>/', views.cafe_details, name='cafe_details'),

path('staff', views.staff, name='staff'),
path('staff/<int:id>/', views.staff_details, name='staff_details'),

path('warehouse', views.warehouse, name='warehouse'),
path('warehouse/<int:id>/', views.warehouse_details, name='warehouse_details'),

path('townhouse', views.townhouse, name='townhouse'),
path('townhouse/<int:id>/', views.townhouse_details, name='townhouse_details'),

path('fullfloors', views.fullfloors, name='fullfloors'),
path('fullfloors/<int:id>/', views.fullfloors_details, name='fullfloors_details'),

path('showrooms', views.showrooms, name='showrooms'),
path('showrooms/<int:id>/', views.showrooms_details, name='showrooms_details'),

path('wholebuilding', views.wholebuilding, name='wholebuilding'),
path('wholebuilding/<int:id>/', views.wholebuilding_details, name='wholebuilding_details'),

path('supermarket', views.supermarket, name='supermarket'),
path('supermarket/<int:id>/', views.supermarket_details, name='supermarket_details'),

path('factory', views.factory, name='factory'),
path('factory/<int:id>/', views.factory_details, name='factory_details'),

path('foreign', views.foreign, name='foreign'),
path('foreign/<int:id>/', views.foreign_details, name='foreign_details'),


 ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)