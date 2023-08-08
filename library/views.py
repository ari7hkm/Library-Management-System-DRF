from django.db.models.aggregates import Count
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from . models import Book, Genre, Language, Review, Student, Borrow, Order, OrderItem
from . serializers import BookSerializer, OrderSerializer, CreateBorrowSerializer, UpdateBorrowSerializer, AddOrderItemSerializer, OrderItemSerializer, StudentSerializer, BorrowSerializer, GenreSerializer, LanguageSerializer, ReviewSerializer
from . permissions import IsAdminOrReadOnly



class BookViewSet(ModelViewSet):
    queryset = Book.objects.select_related('language').all()
    serializer_class = BookSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['inventory']
    permission_classes = [IsAdminOrReadOnly]


    def get_serializer_context(self):
        return {'request': self.request}

    

class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.annotate(books_count=Count('book')).all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_context(self):
        return {'request': self.request}
    


class LanguageViewSet(ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_context(self):
        return {'request': self.request}
    


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(book_id=self.kwargs['book_pk'])

    def get_serializer_context(self):
        return {'book_id': self.kwargs['book_pk']}
    


class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAdminUser]


    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        student = Student.objects.get(user_id=request.user.id)
        if request.method == 'GET':
            serializer = StudentSerializer(student)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = StudentSerializer(student, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)




class OrderViewSet(ModelViewSet):
    queryset = Order.objects.prefetch_related('items__book').all()
    serializer_class = OrderSerializer



class OrderItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddOrderItemSerializer
        return OrderItemSerializer


    def get_queryset(self):
        return OrderItem.objects \
            .filter(order_id=self.kwargs['order_pk']).select_related('book')
    
    def get_serializer_context(self):
        return {'order_id': self.kwargs['order_pk']}




class BorrowViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options']

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
    

    def create(self, request, *args, **kwargs):
        serializer = CreateBorrowSerializer(
            data=request.data,
            context={'user_id': self.request.user.id}
        )
        serializer.is_valid(raise_exception=True)
        borrow = serializer.save()
        serializer = BorrowSerializer(borrow)
        return Response(serializer.data)
    

    def update(self, request, *args, **kwargs):
        serializer = UpdateBorrowSerializer(
            data=request.data,
            context={'borrow_id': self.kwargs['pk']}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateBorrowSerializer
        elif self.request.method == 'PATCH':
            return UpdateBorrowSerializer
        return BorrowSerializer
    

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Borrow.objects.all()
        
        student_id = Student.objects.only('id').get(user_id=user.id)
        return Borrow.objects.filter(student_id=student_id)
    


    
    