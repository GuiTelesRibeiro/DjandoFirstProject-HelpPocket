from django.urls import path
from . import views
urlpatterns = [
    path('', views.index,name='index'),
    path('home', views.home, name='home'),
    
    path('sign_in', views.sign_in, name='sign_in'),
    path('sign_up', views.sign_up, name='sign_up'),
    path('sign_out', views.sign_out, name='sign_out'),
    path('usuario/', views.usuario_detalhes, name='usuario_detalhes'),
    path("editar_usuario/", views.editar_usuario, name="editar_usuario"),
    path("soft_delete_usuario/", views.soft_delete_usuario, name="soft_delete_usuario"),
    
    path('dashboard', views.dashboard, name='dashboard'),
    path('dashboard/<int:month>/', views.dashboard, name='dashboard_month'),


    path('test', views.test, name='test'),
    path('about', views.about, name='about'),  # URL para 'Sobre'
    path('privacy_policy', views.privacy_policy, name='privacy_policy'),  # URL para 'Política de Privacidade'
    path('terms', views.terms, name='terms'),  # URL para 'Termos de Uso'
     # URLs novas para CRUD de Entradas
    path('entradas/criar', views.criar_entrada, name='criar_entrada'),
    path('entradas/detalhes/<int:entrada_id>/', views.entrada_detalhes, name='entrada_detalhes'),
    path('entradas/editar/<int:entrada_id>/', views.editar_entrada, name='editar_entrada'),
    path('entradas/excluir/<int:entrada_id>/', views.excluir_entrada, name='excluir_entrada'),
    path('entradas/confirmar_exclusao/<int:entrada_id>/', views.confirmar_exclusao, name='confirmar_exclusao'),
    path('estatisticas', views.estatisticas, name='estatisticas'),
    
    path('buscar-graficos/', views.buscar_graficos, name='buscar_graficos'),

    
]
