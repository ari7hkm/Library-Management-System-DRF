from rest_framework import serializers
from django.db import transaction
from . models import Book, Genre, Language, Review, Student, Borrow, BorrowItem, Order, OrderItem
from . signals import borrow_created



class SimpleBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title']



class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'genre', 'description', 'language', 'inventory', 'picture']  



class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'title', 'books_count']

    
    books_count = serializers.IntegerField(read_only=True)


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'



class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'name', 'date_review', 'description']

    def create(self, validated_data):
        book_id = self.context['book_id']
        return Review.objects.create(book_id=book_id, **validated_data)



class StudentSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'user_id', 'phone', 'birth_date', 'total_books_due']




class OrderItemSerializer(serializers.ModelSerializer):
    book = SimpleBookSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'book']


class OrderSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'items']


class AddOrderItemSerializer(serializers.ModelSerializer):
    book_id = serializers.IntegerField()

    def validate_book_id(self, value):
        if not Book.objects.filter(pk=value).exists():
            raise serializers.ValidationError("No book with given id was found.")
        return value
    

    def save(self, **kwargs):
        order_id = self.context['order_id']
        book_id = self.validated_data['book_id']


        try:
            order_item = OrderItem.objects.get(order_id=order_id, book_id=book_id)
            order_item.save()
            self.instance = order_item
        
        except:
            self.instance = OrderItem.objects.create(order_id=order_id, **self.validated_data)

        return self.instance
    

    class Meta:
        model = OrderItem
        fields = ['id', 'book_id', 'date_of_return']




class BorrowItemSerializer(serializers.ModelSerializer):
    book = SimpleBookSerializer()

    class Meta:
        model = BorrowItem
        fields = ['id', 'book', 'date_of_return']



class BorrowSerializer(serializers.ModelSerializer):
    items = BorrowItemSerializer(many=True, read_only=True)

    class Meta:
        model = Borrow
        fields = ['id', 'student', 'borrowed_status', 'date_issue', 'items']


class UpdateBorrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrow
        fields = ['borrowed_status']

    def save(self, **kwargs):
        borrow_id = self.context['borrow_id']
        borrow_items = BorrowItem.objects.select_related('book').filter(borrow_id=borrow_id)

        for item in borrow_items:
            inventory = item.book.inventory + 1
            Book.objects.filter(id=item.book.id).update(inventory=inventory)

        return Borrow.objects.filter(id=borrow_id).update(borrowed_status="C")

            


class CreateBorrowSerializer(serializers.Serializer):
    order_id = serializers.UUIDField()

    def validate_order_id(self, order_id):
        if not Order.objects.filter(pk=order_id).exists():
            raise serializers.ValidationError("No order with given ID was found.")
        if OrderItem.objects.filter(order_id=order_id).count() == 0:
            raise serializers.ValidationError("The order is empty.")
        
        return order_id


    def save(self, **kwargs):
        with transaction.atomic():
            order_id = self.validated_data['order_id']

            student = Student.objects.get(user_id=self.context['user_id'])
            borrow = Borrow.objects.create(student=student)

            order_items = OrderItem.objects.select_related('book').filter(order_id=order_id)

            
            borrow_items = [
                BorrowItem(
                    book=item.book,
                    borrow=borrow,
                    date_of_return=item.date_of_return
                ) for item in order_items
            ]

            for item in order_items:
               inventory = item.book.inventory - 1
               Book.objects.filter(id=item.book.id).update(inventory=inventory)
               
               if inventory < 0:
                   raise serializers.ValidationError(f"We don't have {item.book.title}, keep in touch.")

            BorrowItem.objects.bulk_create(borrow_items)

            Order.objects.filter(pk=order_id).delete()

            borrow_created.send_robust(self.__class__, borrow=borrow)


            return borrow

