from django_filters import FilterSet
from .models import Ad


class AdFilter(FilterSet):    
    class Meta:
        model = Ad
        fields = {
           'user': ['exact'],
           'title': ['icontains'],
           'text': ['icontains'],
           'created': ['gte'],
           'category': ['exact'],
        }
    