from django.urls import path
# Импортируем созданное нами представление
from .views import PostsList, PostDetail, PostSearch, PostAdd 
from .views import PostUpdateView, PostDeleteView, add_subscribe, del_subscribe, CategoryList

urlpatterns = [
   path('', PostsList.as_view()), 
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('search', PostSearch.as_view()),
   path('add', PostAdd.as_view(), name='post_create'),
   path('<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
   path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
   path('<int:pk>/add_subscribe/', add_subscribe, name='add_subscribe'),
   path('<int:pk>/del_subscribe/', del_subscribe, name='del_subscribe'),
   path('category', CategoryList.as_view()), 

]