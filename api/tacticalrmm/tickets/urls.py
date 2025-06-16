from rest_framework.routers import DefaultRouter

from .views import TicketViewSet, TicketCommentViewSet

router = DefaultRouter()
router.register(r"tickets", TicketViewSet, basename="ticket")
router.register(r"comments", TicketCommentViewSet, basename="ticketcomment")

urlpatterns = router.urls
