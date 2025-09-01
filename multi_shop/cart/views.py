from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from product.models import Product
from cart.cart_module import Cart
from cart.models import Order, OrderItem, DiscountCode
from account.models import Address
from django.conf import settings
import requests
import json
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin

class CartDetailView(View):
    def get(self, request):
        cart = Cart(request)
        return render(request, "cart/cart_detail.html", {'cart': cart})
    

class CartAddView(View):
    def post(self, request, pk):
        # product = Product.objects.get(id=pk)
        product = get_object_or_404(Product, id=pk)
        size, color, quantity = request.POST.get('size', "ندارد"), request.POST.get('color', 'ندارد'), request.POST.get('quantity')
        cart = Cart(request)
        cart.add(product, quantity, color, size)
        return redirect('cart:cart_detail')
    
class CartDeleteView(View):
    def get(self, request, id):
        cart = Cart(request)
        cart.delete(id)
        return redirect('cart:cart_detail')
    
class OrderDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        order = get_object_or_404(Order, id=pk)
        return render(request, "cart/order_detail.html", {'order': order})


class OrderCreationView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
        order = Order.objects.create(user=request.user, total_price=cart.total()) 
        for item in cart: 
            OrderItem.objects.create(order=order, product=item['product'], color=item['color'], size=item['size'],
                                    quantity=item['quantity'], price=item['price'])
            
        cart.remove_cart()
        return redirect('cart:order_detail', order.id)
    
class ApplyDiscountCodeView(LoginRequiredMixin, View):
    def post(self, request, pk):
        order = get_object_or_404(Order, id=pk)
        code = request.POST.get('discount_code')
        discount_code = get_object_or_404(DiscountCode, name=code)

        if discount_code.quantity == 0:
            return redirect('cart:order_detail', order.id)
        order.total_price -= order.total_price * discount_code.discount/100
        order.save()
        discount_code.quantity -= 1
        discount_code.save()
        return redirect('cart:order_detail', order.id)


# #? sandbox merchant 
# if settings.SANDBOX:
#     sandbox = 'sandbox'
# else:
#     sandbox = 'www'


# ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
# ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
# ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"
ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"

# amount = 1000  # Rial / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
# email = 'email@example.com'  # Optional
# phone = 'YOUR_PHONE_NUMBER'  # Optional
# Important: need to edit for realy server.
CallbackURL = 'http://127.0.0.1:8000/cart/verify/'


class SendRequestView(View):
    def post(self, request, pk):
        order = get_object_or_404(Order, id=pk, user=request.user)
        address = get_object_or_404(Address, id=request.POST.get('address'))
        order.address = f"{address.address} - {address.phone}- {address.email}"
        order.save()
        request.session['order_id'] = str(order.id)
        req_data = {
            "merchant_id": settings.MERCHANT,
            "amount": order.price,
            "callback_url": CallbackURL,
            "description": description,
            # "phone": request.user.phone,
            "metadata": {"mobile": request.user.phone},
        }
        req_header = {
            "accept": "applications/json",
            "content-type": "applications/json",
        }
        req = request.post(url=ZP_API_REQUEST, data=json.dumps(
            req_data), headers=req_header)
        authority = req.json()['data']['authority']
        if len(req.json()['errors']) == 0:
            return redirect(ZP_API_STARTPAY.format(authority=authority))
        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")   


        # data = json.dumps(data)
        # # set content length by data
        # headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
        # try:
        #     response = requests.post(ZP_API_REQUEST, data=data,headers=headers, timeout=10)

        #     if response.status_code == 200:
        #         response = response.json()
        #         if response['Status'] == 100:
        #             return {'status': True, 'url': ZP_API_STARTPAY + str(response['Authority']), 'authority': response['Authority']}
        #         else:
        #             return {'status': False, 'code': str(response['Status'])}
        #     return response
        
        # except requests.exceptions.Timeout:
        #     return {'status': False, 'code': 'timeout'}
        # except requests.exceptions.ConnectionError:
        #     return {'status': False, 'code': 'connection error'}


class VerifyView(View):
    def get(self, request):
        t_status = request.GET.get('Status')
        t_authority = request.GET['Authority']
        order_id = request.session['order_id']
        order = Order.objects.get(id=int(order_id))
        if request.GET.get('Status') == 'OK':
            req_header = {"accept": "application/json",
                        "content-type": "application/json'"}
            req_data = {
                "merchant_id": settings.MERCHANT,
                "amount": order.total_price,
                "authority": t_authority
            }
            req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
            if len(req.json()['errors']) == 0:
                t_status = req.json()['data']['code']
                if t_status == 100:
                    order.is_paid = True
                    order.save()
                    return HttpResponse('Transaction success.\nRefID: ' + str(
                        req.json()['data']['ref_id']
                    ))
                elif t_status == 101:
                    return HttpResponse('Transaction submitted : ' + str(
                        req.json()['data']['message']
                    ))
                else:
                    return HttpResponse('Transaction failed.\nStatus: ' + str(
                        req.json()['data']['message']
                    ))
            else:
                e_code = req.json()['errors']['code']
                e_message = req.json()['errors']['message']
                return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
        else:
            return HttpResponse('Transaction failed or canceled by user')