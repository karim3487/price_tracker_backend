from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from . import models, serializers
from .tasks import run_scraper


class UserViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer


class PriceHistoryViewSet(viewsets.ModelViewSet):
    queryset = models.PriceHistory.objects.all()
    serializer_class = serializers.PriceHistorySerializer

    @action(detail=False, methods=["post"])
    def update_price(self, request):
        url = request.data.get("url")
        price = request.data.get("price")

        if not url or not price:
            return Response(
                {"detail": "Please provide url and price."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        product = get_object_or_404(models.Product, url=url)

        last_history = (
            models.PriceHistory.objects.filter(product=product)
            .order_by("-checked_at")
            .first()
        )

        is_price_dropped = False
        if last_history and price < last_history.price:
            is_price_dropped = True

        price_history = models.PriceHistory.objects.create(product=product, price=price)

        price_history.save()

        return Response(
            {"detail": "Price updated", "price_dropped": is_price_dropped},
            status=status.HTTP_200_OK,
        )


class ProductViewSet(viewsets.ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer

    @action(detail=True, methods=["post"])
    def update_price(self, request, pk=None):
        product = self.get_object()
        run_scraper.delay(product.url)
        return Response(
            {"message": "Запрос на обновление отправлен"},
            status=status.HTTP_202_ACCEPTED,
        )


class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = models.Subscription.objects.all()
    serializer_class = serializers.SubscriptionSerializer

    def create(self, request, *args, **kwargs):
        user_id = request.data.get("user_id")
        product_id = request.data.get("product_id")

        user = get_object_or_404(models.User, id=user_id)
        product = get_object_or_404(models.Product, id=product_id)

        subscription, created = models.Subscription.objects.get_or_create(
            user=user, product=product
        )

        if created:
            models.TrackedProduct.objects.get_or_create(
                product=product
            )

            return Response(
                serializers.SubscriptionSerializer(subscription).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"message": "Вы уже подписаны на этот товар"}, status=status.HTTP_200_OK
        )

    @action(detail=False, methods=["get"])
    def user_subscriptions(self, request):
        telegram_id = request.query_params.get("telegram_id")
        user = get_object_or_404(models.User, telegram_id=telegram_id)
        subscriptions = models.Subscription.objects.filter(user=user)
        return Response(
            serializers.SubscriptionSerializer(subscriptions, many=True).data
        )
