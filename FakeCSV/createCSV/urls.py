from django.urls import path
from .views import Schemas, Login, logout_user, CreateSchema, Schema, download_csv_file

urlpatterns = [
    path('login', Login.as_view(), name='login'),
    path('logout', logout_user, name='logout'),
    path('schema/<int:pk>', Schema.as_view(), name='schema'),
    path('', Schemas.as_view(), name='schemas'),
    path('create_schema', CreateSchema.as_view(), name='create_schema'),
    path('download/<int:pk>', download_csv_file, name='download_csv')
]
