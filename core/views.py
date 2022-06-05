import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.generic import ListView, DetailView, View

from .forms import PaymentForm, AddressForm
from .models import Item, OrderItem, Order, Address, Payment, UserProfile, CATEGORY_CHOICES
stripe.api_key = settings.STRIPE_SECRET_KEY


def products(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "products.html", context)


def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid


class CheckoutView(View):
    def get(self, request, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        pay_form = PaymentForm()
        address_form = AddressForm()
        context = {
            'pay_form': pay_form,
            'address_form': address_form,
            'order': order,
        }
        return render(self.request, "checkout.html", context)

    def post(self, request, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        address_form = AddressForm(request.POST)
        pay_form = PaymentForm(request.POST)
        if address_form.is_valid() and pay_form.is_valid():
            cleaned_data_a = address_form.cleaned_data
            cleaned_data_a["order"] = order
            cleaned_data_a["user"] = request.user._wrapped if hasattr(request.user,'_wrapped') else request.user
            address_model = Address(**cleaned_data_a)
            address_model.save()
            cleaned_data_p = pay_form.cleaned_data
            cleaned_data_p["order"] = order
            cleaned_data_p["user"] = request.user._wrapped if hasattr(request.user,'_wrapped') else request.user
            pay_model = Payment(**cleaned_data_p)
            pay_model.save()
            return redirect("/")


class HomeView(ListView):
    model = Item
    template_name = "home.html"

    def get_context_data(self, *args, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['CATEGORY_CHOICES'] = CATEGORY_CHOICES
        if self.request.GET:
            context['object_list'] = Item.objects.filter(category__contains=self.request.GET["category"])
        return context


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "Zatím nemáte zádný produkt v košíku.")
            return redirect("/")


class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            messages.info(request, "Tento produkt už v nákupním košíku máš.")
            return redirect("core:order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, "Tento produkt byl přidán do nákupního košíku.")
            return redirect("core:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "Tento produkt byl přidán do nákupního košíku.")
        return redirect("core:order-summary")


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "Tento produkt byl odstraněn z nákupního košíku.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "Tento produkt ještě nebyl v nákupního košíku.")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "Nemáte aktivní objednávku.")
        return redirect("core:product", slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "Počet tohoto produktu byl změnen v objednávce.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "Tento produkt ještě nebyl v nákupního košíku.")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "Nemáte nic v košíku.")
        return redirect("core:product", slug=slug)







