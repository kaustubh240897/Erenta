from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from .models import Notification,Order_Notification,Supplier_Order_Notification,Low_Quantity_Notification

# Create your views here.

def show_notification(request,notification_id):
    n = Notification.objects.get(id=notification_id)
    return render(request, 'notification/notification.html',{'notification': n})

def delete_notification(request, notification_id):
    n = Notification.objects.get(id = notification_id)
    n.viewed = True
    n.save()
    return redirect("home")


def show_order_notification(request,notification_id):
    n1 = Order_Notification.objects.get(id=notification_id)
    return render(request, 'notification/order_notification.html',{'order_notification': n1})


def delete_order_notification(request, notification_id):
    n1 = Order_Notification.objects.get(id = notification_id)
    n1.viewed = True
    n1.save()
    return redirect("home")

def supplier_order_notification(request,notification_id):
    n2 = Supplier_Order_Notification.objects.get(id = notification_id)
    return render(request, 'notification/supplier_order_notification.html',{'supplier_order_notification': n2})


def delete_supplier_order_notification(request, notification_id):
    n2 = Supplier_Order_Notification.objects.get(id = notification_id)
    n2.viewed = True
    n2.save()
    return redirect("home")

def low_quantity_supplier_notification(request,notification_id):
    n3 = Low_Quantity_Notification.objects.get(id = notification_id)
    return render(request, 'notification/low_quantity_notification.html',{'low_quantity_notification': n3})


def delete_supplier_lowquantity_notification(request, notification_id):
    n3 = Low_Quantity_Notification.objects.get(id = notification_id)
    n3.viewed = True
    n3.save()
    return redirect("home")
