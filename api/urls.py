from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"users", views.UserViewSet)
router.register(r"products", views.ProductViewSet)
router.register(r"subscriptions", views.SubscriptionViewSet)
router.register(r"price-history", views.PriceHistoryViewSet)
