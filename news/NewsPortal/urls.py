from django.urls import path
# Импортируем созданное нами представление
from .views import PostsList, PostDetail, PostSearch, PostAdd, PostUpdateView, PostDeleteView


urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('', PostsList.as_view()), 
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('search', PostSearch.as_view()),
   path('add', PostAdd.as_view(), name='post_create'),
   path('<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
   path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
]