from django.urls import include, path
from rest_framework import routers
from .views import (CategoryViewSet, CreateUser, get_jwt_token,
                    TitleViewSet, CategoryViewSet, GenreViewSet,
                    ReviewViewSet, CommentViewSet, UserViewSet)

router_v1 = routers.DefaultRouter()
router_v1.register(r'titles', TitleViewSet)
router_v1.register(r'categories', CategoryViewSet)
router_v1.register(r'genres', GenreViewSet)
router_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet, basename='review')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
                   CommentViewSet, basename='comment')
router_v1.register(r'users', UserViewSet)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', CreateUser.as_view()),
    path('v1/auth/token/', get_jwt_token),
]
