from django.contrib import admin
from django.urls import path
from .views import OrderListView, OrderDetailView,SupplierOrdersListView,SupplierOrderDetailView,add_coupon,CreatedOrderDetailView,CreatedOrderView,shipping_address_update_view,billing_address_update_view,update_status_to_shipped_view,update_status_to_returned_view,ShippedOrderListView,RefundedOrderListView,ReturnedOrderListView,CancelOrderListView,track_item_user_view,supplier_cancellation_order_view,confirm_order_view,reject_order_view

urlpatterns = [
   
    path('', OrderListView.as_view(), name='list'),
    path('shipped/', ShippedOrderListView.as_view(), name='shippedlist'),
    path('refunded/', RefundedOrderListView.as_view(), name='refundedlist'),
    path('returned/', ReturnedOrderListView.as_view(), name='returnedlist'),
    path('cancelled/', CancelOrderListView.as_view(), name='cancelledlist'),
    path('detail/<order_id>/', OrderDetailView.as_view(), name='detail'),
    path('created/', CreatedOrderView.as_view(), name='created'),
    path('created/<order_id>/', CreatedOrderDetailView.as_view(), name='createddetail'),
    path('orders/',SupplierOrdersListView.as_view(),name='orders'),
    # path('orders/application',SupplierOrdersApplicationListView.as_view(),name='ordersapplication'),
    # path('orders/shipped/', ShippedSupplierOrdersListView.as_view(), name='shippedsupplierorders'),
    # path('orders/refunded/', RefundedSupplierOrdersListView.as_view(), name='refundedsupplierorders'),
    # path('orders/returned/', ReturnedSupplierOrdersListView.as_view(), name='returnedsupplierorders'),
    # path('orders/cancelled/', CancelSupplierOrdersListView.as_view(), name='cancelsupplierorders'),
    path('orders/detail/<id>/', SupplierOrderDetailView.as_view(), name='supplierorderdetail'),
    path('trackitem/<cart_id>/<order_id>', track_item_user_view, name='user_item_tracker'),
    path('add_coupon/<cart>/',add_coupon,name='add-coupon'),
    #path('created_orders/<order_id>/',created_order_checkout_home,name='created_orders'),
    path('update_address/<order_id>/',shipping_address_update_view,name='update_address'),
    path('update_billingaddress/<order_id>/',billing_address_update_view,name='update_billingaddress'),
    path('update_status_to_shipped/<order_id>/<cartitem_id>/',update_status_to_shipped_view,name='update_status_to_shipped'),
    path('update_status_to_returned/<order_id>/<cartitem_id>/',update_status_to_returned_view,name='update_status_to_returned'),
    path('supplier_cancel_order/<order_id>/<cartitem_id>/',supplier_cancellation_order_view,name='supplier_cancellation_order'),
    path('confirm_order/<order_id>/<cartitem_id>/',confirm_order_view,name='confirm_order'),
    path('reject_order/<order_id>/<cartitem_id>/',reject_order_view,name='reject_order'),
    


    
   
]

