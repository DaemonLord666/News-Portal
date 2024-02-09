from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Post, Author, Category
from datetime import datetime
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string
from django.core.mail import send_mail
from datetime import datetime
from django.shortcuts import redirect
from django.core.mail import EmailMultiAlternatives


class CategoryList(ListView):
    model = Category
    template_name = 'category.html'
    context_object_name = 'category'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class PostsList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('-dateCreation')
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['value1'] = None
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        context['authors'] = Author.objects.all()
        context['form'] = PostForm()
        return context
    
class PostDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'

class PostSearch(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'search'
    queryset = Post.objects.order_by('-dateCreation')
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['value1'] = None
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context



class PostAdd(PermissionRequiredMixin, CreateView):
    model = Post
    template_name = 'add.html'
    context_object_name = 'add'
    queryset = Post.objects.order_by('-dateCreation')
    form_class = PostForm  # добавляем форм класс, чтобы получать доступ к форме через метод POST
    permission_required = ('NewsPortal.add_post',)
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['value1'] = None
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        context['authors'] = Author.objects.all()
        context['form'] = PostForm()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)  # создаём новую форму, забиваем в неё данные из POST-запроса

        if form.is_valid():  # если пользователь ввёл всё правильно и нигде не ошибся, то сохраняем новый товар
            form.save()
        return super().get(request, *args, **kwargs)

class PostUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'add.html'
    form_class = PostForm
    permission_required = ('NewsPortal.change_post',)

    #  метод get_object мы используем вместо queryset, чтобы получить информацию об объекте, который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


# дженерик для удаления товара
class PostDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'post_delete.html'
    queryset = Post.objects.all
    success_url = '/news/'
    permission_required = ('NewsPortal.delete_post',)
    
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


    

@login_required
def add_subscribe(request, **kwargs):
    apk = kwargs.get('pk',)
    Category.objects.get(pk=apk).subscribers.add(request.user)
    return redirect('/news/')


# функция отписки от группы
@login_required
def del_subscribe(request, **kwargs):
    apk = kwargs.get('pk',)
    Category.objects.get(pk=apk).subscribers.remove(request.user)
    return redirect('/news/')




def send_mail_for_sub(instance, created):

    sub_text = instance.text
    
    for a in instance.postCategory.all():
        subscribers = a.subscribers.all()
        for subscriber in subscribers:
            html_content = render_to_string(
                'mail.html', {'user': subscriber, 'text': sub_text[:50], 'post': instance})
            sub_username = subscriber.username
            sub_useremail = subscriber.email
            if created:
                subject=f'Здравствуй, {sub_username}. Новая статья в вашем разделе! {a}'
            else:
                subject=f'Здравствуй, {sub_username}. Статья в вашем разделе была изменена! {a}'
            msg = EmailMultiAlternatives(
                subject,
                body = sub_text,
                from_email='levafive.876@yandex.ru',
                to=[sub_useremail]
                )
            msg.attach_alternative(html_content, 'text/html')
            msg.send()
            print (sub_useremail)
    
    return redirect('/news/')

# Create your views here.
