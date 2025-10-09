from django.urls import path
from users.views import *
from events.views import *

urlpatterns = [
    path('sign-up/', SignUpView.as_view(), name='sign-up'),
    path('sign-in/', SignInView.as_view(), name='sign-in'),
    path('sign-out/', SignOutView.as_view(), name='logout'),
    path('activate/<int:user_id>/<str:token>/', activate_user),
    path('admin/<int:user_id>/assign-role/', AssignRoleView.as_view(), name='assign-role'),
    path('admin/create-group/', CreateGroupView.as_view(), name='create-group'),
    path('admin/group-list/', GroupListView.as_view(), name='group-list'),
    path('admin/user-list/', UserListView.as_view(), name='user-list')
]


