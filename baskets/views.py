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

from .models import Like, Basket, BasketItem
from products.models import ProductPost
from .serializers import LikeSerializer, BasketSerializer, BasketItemSerializer


class BasketDetail(APIView):
    def get_basket(self, pk):
        try:
            return Basket.objects.get(pk=pk)
        except Basket.DoesNotExist:
            return Basket.objects.create(pk=pk)

    def get_product_post(self, pk):
        try:
            return ProductPost.objects.get(pk=pk)
        except ProductPost.DoesNotExist:
            return NotFound(detail="ProductPost does not exist")

    def get_basket_item(self, basket, product_post):
        try:
            return BasketItem.objects.get(basket=basket, product_post=product_post)
        except BasketItem.DoesNotExist:
            return None

    def get(self, request, pk):
        basket = self.get_basket(pk)
        serializer = BasketSerializer(basket)
        return Response(serializer.data)

    # 카트에 이미 있는 상품을 추가하려고 하면, 수량만 증가시킵니다.
    # user는 request.user를 통해 가져옵니다.
    # 카트에 상품을 추가할 때, 카트가 없으면 새로 만들어줍니다.
    def post(self, request, pk):
        basket = self.get_basket(pk)
        quantity = request.data["quantity"]
        # reuqest data에서 referral_id가 있으면 int형으로 referral_id를 가져오고 없으면 None을 가져옵니다.
        product_post = self.get_product_post(request.data.get("product_post"))
        # self.get_basket_item메서드에 basket와 product_post를 전달하여 basketitem중 같은 basket와 product_post를 가진 basketitem을 가져옵니다.
        if basket.basket_items.filter(product_post=product_post).exists():
            basket_item = self.get_basket_item(basket, product_post)
            if basket_item is not None:
                basket_item.quantity += int(quantity)
                basket_item.save()
            serializer = BasketSerializer(basket)
            return Response(serializer.data)
        else:
            basket_item = BasketItem.objects.create(
                basket=basket,
                product_post=product_post,
                quantity=quantity,
            )
            serializer = BasketSerializer(basket)
            return Response(serializer.data)

    # 카트에 없던 상품을 추가할 수 있으며, 동시에 partial=True를 통해
    # 상품의 갯수나 레퍼럴코드를 수정할 수 있습니다.
    # 상품의 갯수를 변경할수 있습니다.
    # user는 request.user를 통해 가져옵니다.

    # put 메서드는 전체 데이터를 수정할 때 사용합니다.


class BasketItemDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_basket(self, pk):
        try:
            return Basket.objects.get(pk=pk)
        except Basket.DoesNotExist:
            return Basket.objects.create(pk=pk)

    def get_basket_item(self, pk):
        try:
            return BasketItem.objects.get(pk=pk)
        except BasketItem.DoesNotExist:
            return None

    def get(self, request, basket_item_pk):
        basket_item = self.get_basket_item(basket_item_pk)
        serializer = BasketItemSerializer(basket_item)
        return Response(serializer.data)

    def put(self, request, basket_item_pk):
        basket_item = self.get_basket_item(basket_item_pk)
        if basket_item is not None:
            quantity = request.data["quantity"]
            basket_item.quantity = int(quantity)
            basket_item.save()
        serializer = BasketItemSerializer(basket_item)
        return Response(serializer.data)

    def delete(self, request, pk):
        basket = self.get_basket(pk)
        basket_item = BasketItem.objects.get(pk=pk)
        basket_item.delete()
        serializer = BasketItemSerializer(basket)
        return Response(serializer.data)


class LikeList(APIView):
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
