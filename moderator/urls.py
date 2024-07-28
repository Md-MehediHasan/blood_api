from django.urls import path
from .views import GetDonar,RegisterDonar,AuthView,AuthenticatedUser,UpdateUserInfo,RegisterOrganization,AuthenticatedUsersOrganization


urlpatterns=[
    path('auth/', AuthView.as_view()),
    path('authenticated_user/', AuthenticatedUser.as_view()),
    path('update/',UpdateUserInfo.as_view()),
    path('find-donar/',GetDonar.as_view()),
    path('register/',RegisterDonar.as_view()),
    path('register-organization/',RegisterOrganization.as_view()),
    path('my-organizations/',AuthenticatedUsersOrganization.as_view())
]