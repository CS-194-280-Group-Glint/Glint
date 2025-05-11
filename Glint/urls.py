"""
URL configuration for Glint project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from api.views import index, podcast, analyze_text_endpoint, summarize_text_endpoint, classify_news_endpoint

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('api/generate-podcast/', podcast, name='podcast'),
    path('api/analyze-text/', analyze_text_endpoint, name='analyze_text'),
    path('api/summarize-text/', summarize_text_endpoint, name='summarize_text'),
    path('api/classify-news/', classify_news_endpoint, name='classify_news'),
]
