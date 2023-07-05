from rest_framework import serializers
from django.contrib.auth.models  import User 
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Product, Order, OrderItems, ShippingAddress ,Review, ForgotPassword, FindPet, VerifyEmail, FindDog,catImage,dogImage


class ReviewSerializer(serializers.ModelSerializer): 
    
    class Meta:
        model = Review
        fields = '__all__'



class CatImageSerializer(serializers.ModelSerializer): 
    
    class Meta:
        model = catImage
        fields = '__all__'


class DogImageSerializer(serializers.ModelSerializer): 
    
    class Meta:
        model = dogImage
        fields = '__all__'

        
class ProductSerializer(serializers.ModelSerializer):
    reviews= serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Product
        fields = '__all__'  

    def get_reviews(self,obj):
        reviews = obj.review_set.all()
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data

class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = '__all__'

class OrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    orderItems = serializers.SerializerMethodField(read_only=True)
    shippingAddress = serializers.SerializerMethodField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = '__all__' 

    def get_orderItems(self, obj):
        items = obj.orderitems_set.all()
        serializer = OrderItemsSerializer(items, many=True)
        return serializer.data

    def get_shippingAddress(self, obj):
        try:
            address = ShippingAddressSerializer(obj.shippingaddress, many=False).data
        except:
            address =  False

        return address
    
    def get_user(self, obj):
        user = obj.user
        serializer = UserSerializer(user, many=False)
        return serializer.data



class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    _id = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            '_id',
            'username',
            'email',
            'name',
            'isAdmin'
        ]

    def get__id(self, obj):
        return obj.id

    def get_isAdmin(self, obj):
        return obj.is_staff
 
    def get_name(self, obj):
        name = obj.first_name
        if name == '':
            name = obj.email

        return name


class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = [
            'id',
            '_id',
            'username',
            'email',
            'name',
            'isAdmin',
            'token'
        ]

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)
    

class ForgotPasswordSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField(read_only=True)
    _id = serializers.SerializerMethodField(read_only=True)
    secret = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ForgotPassword
        fields = [
            '_id',
            'email',
            'secret',
        ]

    def get__id(self, obj):
        return obj._id

    def get_email(self,obj):
        return obj.email

    def get_secret(self, obj):
        return obj.secret
    
class FindPetSerializer(serializers.ModelSerializer):
    class Meta:
        model = FindPet
        fields = '__all__'

        def get_pTag(seld,obj):
            return obj.pTag

class FindDogSerializer(serializers.ModelSerializer):
    class Meta:
        model = FindDog
        fields = '__all__'

        def get_pTag(seld,obj):
            return obj.pTag

class VerifyEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerifyEmail
        fields = '__all__'

        def get_code(seld,obj):
            return obj.code