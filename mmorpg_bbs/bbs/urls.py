from django.urls import path

from .views import (
    AdDelete,
    AdDetail,
    AdEdit,
    AdSearch,
    AdsList,
    create_ad,
    # AdImagesCreate,
    response_accept,
    response_delete,
)

app_name = 'bbs'

urlpatterns = [
    path('', AdsList.as_view(), name='main'),
    path('<int:pk>', AdDetail.as_view(), name='detail'),
    path('search', AdSearch.as_view(), name='search'),
    path('add', create_ad, name='add'),
    path('<int:pk>/edit', create_ad, name='edit'),
    path('<int:pk>/delete', AdDelete.as_view(), name='delete'),
    path('response_accept/<int:pk>', response_accept, name='response_accept'),
    path('response_delete/<int:pk>', response_delete, name='response_delete'),
]