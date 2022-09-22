from django.urls import path
from . import views

urlpatterns = [
    path('', views.school, name='school'),
    path('school/create/', views.school_create, name='school_create'),

    path('<int:school_id>', views.board, name='board'),
    path('<int:school_id>/board/create/', views.board_create, name='board_create'),

    path('<int:school_id>/<int:board_id>', views.post, name='post'),
    path('<int:school_id>/<int:board_id>/post/create/', views.post_create, name='post_create'),

    path('<int:school_id>/<int:board_id>/<int:post_id>', views.post_detail, name='post_detail'),
    path('<int:school_id>/<int:board_id>/<int:post_id>/post/delete', views.post_delete, name='post_delete'),

    path('<int:school_id>/<int:board_id>/<int:post_id>/comment/create/', views.comment_create, name='comment_create'),

    path('signup/', views.signup, name='signup'),
]
