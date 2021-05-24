from django.urls import path

from api.views_compressor_unit import GetStatusConnectionsRemeza, GetConnectionsRemeza, GetConnectionsVariablesRemeza


urlpatterns = [
    path('connections/status/', GetStatusConnectionsRemeza.as_view()),
    path('connections/', GetConnectionsRemeza.as_view()),
    path('connections/variables/<int:id>/', GetConnectionsVariablesRemeza.as_view()),
]