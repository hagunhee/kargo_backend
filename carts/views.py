from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
)
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, DestroyAPIView

from .models import Like, Cart, CartItem
from products.models import ProductPost
from .serializers import LikeSerializer, CartSerializer, CartItemSerializer


class CartDetail(APIView):
    def get_object(self, pk):
        try:
            return Cart.objects.get(pk=pk)
        except Cart.DoesNotExist:
            return Cart.objects.create(pk=pk)

    def get_product_post(self, pk):
        try:
            return ProductPost.objects.get(pk=pk)
        except ProductPost.DoesNotExist:
            return NotFound(detail="ProductPost does not exist")

    def get_cart_item(self, cart, product_post):
        try:
            return CartItem.objects.get(cart=cart, product_post=product_post)
        except CartItem.DoesNotExist:
            return None

    def get(self, request, pk):
        cart = self.get_object(pk)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    # 카트에 이미 있는 상품을 추가하려고 하면, 수량만 증가시킵니다.
    # user는 request.user를 통해 가져옵니다.
    # 카트에 상품을 추가할 때, 카트가 없으면 새로 만들어줍니다.
    def post(self, request, pk):
        cart = self.get_object(pk)
        quantity = request.data["quantity"]
        # reuqest data에서 referral_id가 있으면 int형으로 referral_id를 가져오고 없으면 None을 가져옵니다.
        product_post = self.get_product_post(request.data.get("product_post"))
        cart_item = self.get_cart_item(cart, product_post)
        if cart_item.exists():
            cart_item = cart_item.get()
            cart_item.quantity += int(quantity)
            cart_item.save()
            serializer = CartSerializer(cart)
            return Response(serializer.data)
        else:
            cart_item = CartItem.objects.create(
                cart=cart,
                product_post=product_post,
                quantity=quantity,
            )
            serializer = CartSerializer(cart)
            return Response(serializer.data)

    # 카트에 없던 상품을 추가할 수 있으며, 동시에 partial=True를 통해
    # 상품의 갯수나 레퍼럴코드를 수정할 수 있습니다.
    # 상품의 갯수를 변경할수 있습니다.
    # user는 request.user를 통해 가져옵니다.


class CartItemDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_cart_item(self, pk):
        try:
            return CartItem.objects.get(pk=pk)
        except CartItem.DoesNotExist:
            return None

    def get(self, request, cart_item_pk):
        cart_item = self.get_cart_item(cart_item_pk)
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data)

    def put(self, request, cart_item_pk):
        cart_item = self.get_cart_item(cart_item_pk)
        quantity = request.data["quantity"]
        # referral 은 request.data에서 가져옵니다.
        # request.data에 referral이 없으면 None을 가져옵니다.
        # self.get_referral메서드에 pk를 int로 전달합니다.
        # 이 줄에서는 CartItem 객체를 가져오거나 생성합니다.
        # get_or_create 메서드는 주어진 인수와 일치하는 객체를
        # 데이터베이스에서 찾습니다.
        # 만약 찾을 수 있다면 그 객체를 반환하고 created 값은 False가 됩니다.
        # 만약 찾을 수 없다면 새로운 객체를 생성하고 created 값은 True가 됩니다.
        # created 값이 False인 경우, 즉 CartItem 이 존재하는 경우.
        cart_item.quantity = int(quantity)
        cart_item.save()
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data)

    def delete(self, request, pk):
        cart = self.get_object(pk)
        cart_item = CartItem.objects.get(pk=pk)
        cart_item.delete()
        serializer = CartItemSerializer(cart)
        return Response(serializer.data)


class LikeDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Like.objects.get(pk=pk)
        except Like.DoesNotExist:
            return Like.objects.create(pk=pk)

    def get(self, request, pk):
        like = self.get_object(pk)
        serializer = LikeSerializer(like)
        return Response(serializer.data)


class LikeToggle(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Like.objects.get(pk=pk)
        except Like.DoesNotExist:
            return Like.objects.create(pk=pk)

    def get_product_post(self, product_post_pk):
        try:
            return ProductPost.objects.get(pk=product_post_pk)
        except ProductPost.DoesNotExist:
            return NotFound(detail="ProductPost does not exist")

    def put(self, request, pk, product_post_pk):
        likes = self.get_object(pk)
        product_post = self.get_product_post(product_post_pk)

        if likes.product_post.exists():
            likes.product_post.remove(product_post)
            return Response({"message": "Like removed"}, status=HTTP_204_NO_CONTENT)
        else:
            likes.product_post.add(product_post)
            return Response({"message": "Liked"}, status=HTTP_201_CREATED)
