from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('resume/', include('resume_builder.urls')),  # This is fine as it points to your resume_builder app
    path('', include('resume_builder.urls')),  # Add this line to link the root path to your app's URLs
]
