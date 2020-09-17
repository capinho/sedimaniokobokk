from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Max, Min, Sum
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect

from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

from cart.cart import Cart
from .forms import *
from .models import *
from .task import *
from datetime import timedelta
import datetime
from datetime import date

def reset_template(request):
    return render(request, 'orders/registration/reset.html')


class PasswordResetView(auth_views.PasswordResetView):
    template_name = 'orders/registration/password_reset_form.html'
    success_url = reverse_lazy('orders:password_reset_done')
    email_template_name='orders/registration/password_reset_email.html'
    subject_template_name='orders/registration/password_reset_subject.txt'
    from_email='commandesedima@sedima.com'



class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name='orders/registration/password_reset_complete.html'


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name='orders/registration/password_reset_confirm.html'
    success_url= 'orders:password_reset_complete'

class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'orders/registration/password_reset_done.html'

@login_required
def pagelogout(request):
    user=request.user
    try:
        for key in list(request.session.keys()):
            if key == 'cart':
                continue
            del request.session[key]
    except KeyError:
        pass
    return HttpResponseRedirect('/')


@login_required
def list_commande(request):
    #filter = OrderFilter(request.GET, queryset=OrderItem.objects.select_related('product').filter(order__user=request.user))
    listorderuser = Order.objects.filter(user=request.user).order_by('created')
    return render(request, 'orders/order/list.html', {'listorderuser':listorderuser})

@login_required
def view_list(request,pk):
    #if pk:
        #order= OrderItem.objects.values_list('price').get(pk=pk)
    #    order= Order.objects.get(pk=pk)
    #else:
    order = Order.objects.get(pk=pk)
    orderitems = order.items.all()
    total = order.items.aggregate(Sum('price'))

    return render(request, 'orders/order/detail_list.html', {'orderitems':orderitems,'total':total,})

@login_required
def order_create(request):
    user=request.user
    todayDate = datetime.date.today()
    current_month = todayDate.month
    current_day = todayDate.day
    #datedebut = datedispo.objects.only('datedebut')
    #datefin =  datedispo.objects.only('datefin')
    #date =  datedispo.objects.filter(datedebut__lte=todayDate,datefin__gte=todayDate)
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            #if date:
                #if Order.objects.filter(user__profile__matricule__iexact=user.profile.matricule):
            #if Order.objects.filter(created__month=current_month,user=user,user__profile__is_administration=False):
            if Order.objects.filter(created__month=current_month,user=user):
                return redirect('/', messages.error(request, 'Vous avez deja fait une commande ce mois ci','alert-danger'))
            else:
                order.user=user
                order.save()
                for item in cart:
                    #product_ids = cart.keys()
                    #products = Product.objects.filter(id__in=product_ids)
                    #if products.count()>0:
                    #    return redirect('/', messages.success(request, 'Panier vide', 'alert-success'))
                    #else:
                        OrderItem.objects.create(order=order,
                                                product=item['product'],
                                                price=item['price'],
                                                quantity=item['quantity'])
                # effacer panier
                cart.clear()
                if user.email!='':
                    order_created(order.id)
                    request.session['order_id'] = order.id
                    return redirect('/', messages.success(request, 'Votre commande a été prise avec succes', 'alert-success'))
                else:
                    request.session['order_id'] = order.id
                    # redirect to the payment
                    #return redirect('payment:process')
                    return redirect('/', messages.success(request, 'Votre commande a été prise avec succes', 'alert-success'))

            #else:
            #     return redirect('/', messages.error(request, 'la periode de commande est depasse','alert-danger'))



    else:
        form = OrderCreateForm()
    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'form': form})


#################################################################

from django.contrib.auth import authenticate, login
