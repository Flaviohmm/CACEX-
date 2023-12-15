from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('gerar_relatorio_pdf/', views.gerar_relatorio_pdf, name='gerar_relatorio_pdf'),
    path('exportar_csv/', views.exportar_csv, name='exportar_csv'),
]
