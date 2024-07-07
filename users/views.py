from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import auth, messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
# from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView
from carts.models import Cart
from orders.models import Order, OrderItem

from users.forms import UserLoginForm, UserRegistrationForm, ProfileForm

class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    # success_url = reverse_lazy('main:index')
    
    def get_success_url(self):
        redirect_page = self.request.POST.get('next', None)
        if redirect_page and redirect_page != reverse('user:logout'):
            return redirect_page
        return reverse_lazy('main:index')
    
    def form_valid(self, form):
        session_key = self.request.session.session_key
        
        user = form.get_user()
        if user:
            auth.login(self.request, user)
            if session_key:
                old_carts = Cart.objects.filter(user=user)
                if old_carts.exists():
                    old_carts.delete()
                Cart.objects.filter(session_key=session_key).update(user=user)
                messages.success(self.request, f'{user.username} successfully logged in')
                
                return redirect(self.get_success_url())
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login'
        return context
    
    
class UserRegistrationView(CreateView):
    template_name = 'users/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('user:profile')
    
    def form_valid(self, form):
        session_key = self.request.session.session_key
        user = form.instance
        
        if user:
            form.save()
            auth.login(self.request, user)
            
        if session_key:
            Cart.objects.filter(session_key=session_key).update(user=user)
            
        messages.success(self.request, f'{user.username} successfully signed up')
        return redirect(self.success_url)    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registration'
        return context
    
    
class UserProfileView(LoginRequiredMixin, UpdateView): # or FormView
    template_name = 'users/profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('user:profile')
    
    def get_object(self, queryset=None):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, f'Profile successfully updated')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, f'Error while updating profile')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Profile'
        context['orders'] = Order.objects.filter(user=self.request.user).prefetch_related(
            Prefetch(
                "orderitem_set", # additional queryset
                queryset=OrderItem.objects.select_related("product"),
            )
        ).order_by("-id")
        return context
    

class UserCartView(TemplateView):
    template_name = 'users/users_cart.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Cart'
        return context
    

@login_required
def logout(request):
    messages.warning(request, f'{request.user.username} logged out')
    auth.logout(request)
    return redirect(reverse('main:index'))

    
    
# @login_required
# def profile(request):
#     form = ProfileForm()
#     if request.method == 'POST':
#         form = ProfileForm(data=request.POST, instance=request.user, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             messages.success(request, f'Profile successfully updated')
#             return redirect(reverse('user:profile'))
#     else:
#         form = ProfileForm(instance=request.user)
        
#     orders = Order.objects.filter(user=request.user).prefetch_related( # prefetch_related -  т.к. foreignkey идёт от OrderItem к Order (в обратном порядке (не select))
#             Prefetch(
#                 "orderitem_set", # additional queryset
#                 queryset=OrderItem.objects.select_related("product"),
#             )
#         ).order_by("-id")
        
#     context = {
#         'title': 'Profile',
#         'form': form,
#         'orders': orders
#     }
#     return render(request, 'users/profile.html', context)


# def users_cart(request):
#     return render(request, 'users/users_cart.html')


# def login(request):
#     form = UserLoginForm()
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             username = request.POST['username']
#             password = request.POST['password']
#             user = auth.authenticate(username=username, password=password) # check in db
            
#             session_key = request.session.session_key
            
#             if user:
#                 auth.login(request, user)
#                 messages.success(request, f'{user.username} successfully logged in')
                
#                 if session_key:
#                     # delete old authorized user carts
#                     forgot_carts = Cart.objects.filter(user=user)
#                     if forgot_carts.exists():
#                         forgot_carts.delete()
#                     # add new authorized user carts from anonimous session
#                     Cart.objects.filter(session_key=session_key).update(user=user)
                
#                 redirect_page = request.POST.get('next', None) # if not authorized user try to visit profile
#                 if redirect_page and redirect_page != reverse('user:logout'):
#                     return redirect(request.POST.get('next')) # '/user/profile/'

#                 return redirect(reverse('main:index'))
#     else:
#         form = UserLoginForm()
        
#     context = {
#         'title': 'Log in',
#         'form': form
#     }
#     return render(request, 'users/login.html', context)


# def registration(request):
#     form = UserRegistrationForm()
#     if request.method == 'POST':
#         form = UserRegistrationForm(data=request.POST)
#         if form.is_valid():
#             form.save()
            
#             session_key = request.session.session_key
            
#             user = form.instance
#             auth.login(request, user)
                        
#             if session_key:
#                 Cart.objects.filter(session_key=session_key).update(user=user)
            
#             messages.success(request, f'{user.username} successfully signed up')
#             return redirect(reverse('main:index'))
#     else:
#         form = UserRegistrationForm()
        
#     context = {
#         'title': 'Registration',
#         'form': form
#     }
#     return render(request, 'users/registration.html', context)
