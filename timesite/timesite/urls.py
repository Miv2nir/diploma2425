"""
URL configuration for timesite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from backend import views, api_views
from django.conf import settings
from django.urls import re_path
from django.views.static import serve
from django.conf.urls.static import static

urlpatterns = [
        re_path(
        r'^statics/(?P<path>.*)$',
        serve,
        {
            'document_root': settings.STATIC_URL,
            'show_indexes': True,  # must be True to render file list
        },
    ),
        path('',views.home,name='home_page'),
    path('admin/', admin.site.urls),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('profile/',views.profile_page_redirect,name='profile_redirect'),
    path('profile/<str:username>/', views.profile_page, name='profile'),
    path('profile/<str:username>/edit/', views.profile_page_edit, name='profile_edit'),
    path('projects/', views.project_list, name='project_list'),
    path('projects/new/', views.project_item_new, name='project_item_new'),
    path('projects/<uuid:id>/', views.project_item, name='project_item'),
    path('projects/<uuid:id>/metadata_edit/', views.project_item_edit, name='project_item_edit'),
    path('projects/<uuid:id>/delete/', views.project_item_delete, name='project_item_delete'),
    path('datastore/', views.datastore, name='datastore'),
    path('datastore/<uuid:id>/', views.datastore_item, name='datastore_item'),
    path('datastore/<uuid:id>/edit/', views.datastore_edit, name='datastore_edit'),
    path('datastore/<uuid:id>/delete/', views.datastore_delete, name='datastore_delete'),
    path('logout/', views.logout_user, name='logout'),
    #api stuff
    path('api/project/<uuid:id>/',api_views.get_project),
    path('api/project/<uuid:id>/upd_date/', api_views.upd_proj_date),
    path('api/user/data/',api_views.get_user_info),
    path('api/user/data/<int:pk>/',api_views.get_specific_user_info),
    path('api/functions/get_all/',api_views.get_functions_all),
    path('api/functions/<str:func_name>/get_info/',api_views.get_function_info),
    path('api/functions/get_csv_files/',api_views.get_datastore_items_csv),
    path('api/functions/<uuid:id>/accept_csv_load/',api_views.accept_csv_load),
    path('api/functions/<uuid:id>/accept_renderer/',api_views.accept_renderer),
    path('api/functions/<uuid:id>/accept_processor/',api_views.accept_processor),
    path('api/functions/<uuid:id>/accept_model/',api_views.accept_model),
    path('api/functions/<uuid:id>/get_pipeline/',api_views.get_pipeline),
    path('api/functions/<uuid:id>/get_runtime_status/',api_views.get_runtime_status),
    path('api/functions/<uuid:id>/get_results/',api_views.get_results),
    path('api/functions/<uuid:id>/stop_runtime/',api_views.stop_runtime),
    path('api/functions/<uuid:func_id>/get_foreign_datastore_item/',api_views.get_foreign_datastore_item),
    path('api/functions/<uuid:id>/execute/',api_views.invoke_runtime),
    path('api/functions/<uuid:func_id>/move_function_up/',api_views.move_function_up),
    path('api/functions/<uuid:func_id>/move_function_down/',api_views.move_function_down),
    path('api/params/<uuid:params_id>/get_params/',api_views.get_params),
    path('api/params/<uuid:params_id>/delete_params/',api_views.delete_params),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
