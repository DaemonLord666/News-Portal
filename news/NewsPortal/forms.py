from django import forms
from .models import Post


# Создаём модельную форму
class PostForm(forms.ModelForm):
    check_box = forms.BooleanField(label='Ало, Галочка для подтверждения!')  # добавляем галочку, или же true-false поле
    # в класс мета, как обычно, надо написать модель, по которой будет строится форма и нужные нам поля. Мы уже делали что-то похожее с фильтрами.
    class Meta:
        model = Post
        fields = ['title', 'text', 'author', 'categoryType', 'check_box']