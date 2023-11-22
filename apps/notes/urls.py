from django.urls import path, re_path, include
from apps.notes import views


urlpatterns = [  
    path('', views.notes_view, name='notes'),

    re_path(r'^notes/', include([
        path('create-or-update-notes', views.CreateOrUpdateNotesAPIView.as_view()),
        path('create-or-update-notes/<int:id>', views.CreateOrUpdateNotesAPIView.as_view()),
        path('get-notes', views.GetAllNotesAPIView.as_view()),
        path('destroy-notes',views.DestroyNotesApiView.as_view()),
    ])),
]
