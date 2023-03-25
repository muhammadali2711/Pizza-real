from django.urls import path
from api.v1.auth.views import AuthView
from api.v1.discount.views import DiscountView
from api.v1.user_actions.views import UserActions, UserView
from api.v1.ctg.views import CategoryView
from api.v1.product.views import ProductView
from api.v1.tag.views import TagView


urlpatterns = [
    path("auth/", AuthView.as_view()),

    path("ctg/", CategoryView.as_view(), name="ctg_list"),
    path("ctg/<int:pk>/", CategoryView.as_view(), name="ctg_one_and_delete"),

    path("product/", ProductView.as_view(), name="product_list"),
    path("product/<int:pk>/", ProductView.as_view(), name="product_one_and_delete"),

    path("tag/", TagView.as_view(), name="tag_list"),

    path("user_actions/", UserActions.as_view(), name="actions"),
    path("user_actions/<int:pk>/", UserActions.as_view(), name="actions_delete"),

    path("user/", UserView.as_view(), name="user"),

    path("discount/", DiscountView.as_view(), name="discount"),
]



