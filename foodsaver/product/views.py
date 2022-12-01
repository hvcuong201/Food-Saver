from django.http import Http404
from rest_framework import status
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status, authentication, permissions

from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer

class ProductsList(APIView):
    def get(self, request, format=None):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class ProductDetail(APIView):
    def get_object(self, category_slug, product_slug):
        try:
            return Product.objects.filter(category__slug=category_slug).get(slug=product_slug)
        except Product.DoesNotExist:
            raise Http404
    
    def get(self, request, category_slug, product_slug, format=None):
        product = self.get_object(category_slug, product_slug)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

class CategoryDetail(APIView):
    def get_object(self, category_slug):
        try:
            return Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            raise Http404
    
    def get(self, request, category_slug, format=None):
        category = self.get_object(category_slug)
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    
@api_view(['POST'])
def search(request):
    query = request.data.get('query', '')

    if query:
        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    else:
        return Response({"products": []})
    
@api_view(['GET'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def get_products_by_vendorid(request, format=None):
    vendorid = request.user.id
    if vendorid:
        products = Product.objects.filter(vendor_id=vendorid)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    else:
        return Response({"products": []})
    
class ProductVendor(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self, pk):
        try:
            return Product.objects.get(id=pk)
        except Product.DoesNotExist:
            raise Http404
    
    def get(self, request, format=None):
        return Response(request.user.id)
    
    def post(self, request, format=None):
        #print(request.user.id)
        serializer = ProductSerializer(data=request.data)
        base64_img = request.data['base64_img']
        if serializer.is_valid():
            serializer.save(vendor=request.user, image=decode_base64_file(base64_img))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, format=None):
        product = self.get_object(pk=request.data['pk'])
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
def decode_base64_file(data):

    def get_file_extension(file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension

    from django.core.files.base import ContentFile
    import base64
    import six
    import uuid

    # Check if this is a base64 string
    if isinstance(data, six.string_types):
        # Check if the base64 string is in the "data:" format
        if 'data:' in data and ';base64,' in data:
            # Break out the header from the base64 content
            header, data = data.split(';base64,')

        # Try to decode the file. Return validation error if it fails.
        try:
            decoded_file = base64.b64decode(data)
        except TypeError:
            TypeError('invalid_image')

        # Generate file name:
        file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
        # Get the file name extension:
        file_extension = get_file_extension(file_name, decoded_file)

        complete_file_name = "%s.%s" % (file_name, file_extension, )

        return ContentFile(decoded_file, name=complete_file_name)
