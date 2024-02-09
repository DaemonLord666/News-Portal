from django import forms
from django.forms import CheckboxSelectMultiple, ModelMultipleChoiceField
from .models import Post, Category


# Создаём модельную форму
class PostForm(forms.ModelForm):
    check_box = forms.BooleanField(label='Ало, Галочка для подтверждения!')  # добавляем галочку, или же true-false поле
    postCategory = ModelMultipleChoiceField(label='Категория:', 
        queryset=Category.objects.all(), 
        widget=CheckboxSelectMultiple
        )
    
    
    # в класс мета, как обычно, надо написать модель, по которой будет строится форма и нужные нам поля. Мы уже делали что-то похожее с фильтрами.
    class Meta:
        model = Post
        fields = ['title', 'categoryType' ,'text', 'author', 'postCategory', 'check_box']
        
