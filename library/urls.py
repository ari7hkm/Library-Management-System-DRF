from django.urls import path
from rest_framework_nested import routers
from . import views


router = routers.DefaultRouter()

router.register('books', views.BookViewSet, basename='books')
router.register('genres', views.GenreViewSet)
router.register('languages', views.LanguageViewSet)
router.register('students', views.StudentViewSet)
router.register('orders', views.OrderViewSet)
router.register('borrows', views.BorrowViewSet, basename='borrows')

book_router = routers.NestedDefaultRouter(router, 'books', lookup='book')
book_router.register('reviews', views.ReviewViewSet, basename='book-reviews')

order_router = routers.NestedDefaultRouter(router, 'orders', lookup='order')
order_router.register('items', views.OrderItemViewSet, basename='order-items')

urlpatterns = router.urls + book_router.urls + order_router.urls






# urlpatterns = [
#     path('books/', views.BookViewSet, name = 'books'),
# ]
