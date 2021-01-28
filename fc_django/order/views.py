from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from fcuser.decorators import login_required
from .forms import RegisterForm
from .models import Order

# Create your views here.
@method_decorator(login_required, name='dispatch')
class OrderCreate(FormView):
    form_class = RegisterForm
    success_url = '/product/'

    def form_invalid(self, form):
        return redirect('/product/' + str(form.product))

    def get_form_kwargs(self, **kwargs):
        kw=super().get_form_kwargs(**kwargs)
        kw.update({
            'request':self.request
        })
        return kw

@method_decorator(login_required, name='dispatch')
class OrderList(ListView):
    # model = Product을 사용안한이유는 이렇게하게되면 남의정보까지 보게되기때문에 queryset을 사용하여 구현함
    template_name='order.html'
    # object_list라는 변수명을 바꾸는 함수
    context_object_name = 'order_list'

    def get_queryset(self, **kwargs):
        queryset = Order.objects.filter(fcuser__email=self.request.session.get('user'))
        return queryset