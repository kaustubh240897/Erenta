from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from .models import Notification,Order_Notification,Supplier_Order_Notification,Order_current_status,User_Order_Status_Notification
from orders.models import Low_Quantity_Notification

# Create your views here.

def show_notification(request,notification_id):
    n = Notification.objects.get(id=notification_id)
    n.seen = True
    n.save()
    return render(request, 'notification/notification.html',{'notification': n})

def delete_notification(request, notification_id):
    n = Notification.objects.get(id = notification_id)
    n.viewed = True
    n.save()
    return redirect("notification_page")


def show_order_notification(request,notification_id):
    n1 = Order_Notification.objects.get(id=notification_id)
    n1.seen = True
    n1.save()
    return render(request, 'notification/order_notification.html',{'order_notification': n1})


def delete_order_notification(request, notification_id):
    n1 = Order_Notification.objects.get(id = notification_id)
    n1.viewed = True
    n1.save()
    return redirect("notification_page")

def user_order_status_notification(request,notification_id):
    n10 = User_Order_Status_Notification.objects.get(id = notification_id)
    n10.seen = True
    n10.save()
    return render(request, 'notification/user_order_status.html',{'user_order_status': n10})

def delete_user_order_status_notification(request, notification_id):
    n10 = User_Order_Status_Notification.objects.get(id = notification_id)
    n10.viewed = True
    n10.save()
    return redirect("notification_page")


def supplier_order_notification(request,notification_id):
    n2 = Supplier_Order_Notification.objects.get(id = notification_id)
    n2.seen = True
    n2.save()
    return render(request, 'notification/supplier_order_notification.html',{'supplier_order_notification': n2})


def delete_supplier_order_notification(request, notification_id):
    n2 = Supplier_Order_Notification.objects.get(id = notification_id)
    n2.viewed = True
    n2.save()
    return redirect("supplier_notification_page")

def low_quantity_supplier_notification(request,notification_id):
    n3 = Low_Quantity_Notification.objects.get(id = notification_id)
    n3.seen = True
    n3.save()
    return render(request, 'notification/low_quantity_notification.html',{'low_quantity_notification': n3})


def delete_supplier_lowquantity_notification(request, notification_id):
    n3 = Low_Quantity_Notification.objects.get(id = notification_id)
    n3.viewed = True
    n3.save()
    return redirect("supplier_notification_page")

def order_item_status(request,notification_id):
    n4 = Order_current_status.objects.get(id = notification_id)
    n4.seen = True
    n4.save()
    return render(request,'notification/order_item_status.html',{'order_item_status': n4})

def delete_order_item_status(request, notification_id):
    n4 = Order_current_status.objects.get(id=notification_id)
    n4.viewed = True
    n4.save()
    return redirect("notification_page")


def supplier_order_item_status(request,notification_id):
    n5 = Order_current_status.objects.get(id=notification_id)
    n5.supplier_seen = True
    n5.save()
    return render(request,'notification/supplier_order_item_status.html',{'supplier_order_item_status': n5})

def supplier_delete_order_item_status(request, notification_id):
    n5 = Order_current_status.objects.get(id=notification_id)
    n5.supplier_viewed = True
    n5.save()
    return redirect("supplier_notification_page")
