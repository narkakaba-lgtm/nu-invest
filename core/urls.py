"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.conf.urls.i18n import i18n_patterns

from platform_invest import views as v


# ===============================
# 🌍 LANGUE (IMPORTANT)
# ===============================
urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
]


# ===============================
# 🚀 ROUTES PRINCIPALES
# ===============================
urlpatterns += i18n_patterns(

    # ADMIN
    path('admin/', admin.site.urls),

    # HOME / DASHBOARD
    path('', v.home, name='home'),
    path('dashboard/', v.dashboard, name='dashboard'),

    # AUTH
    path('inscription/', v.inscription, name='inscription'),

    path('login/', auth_views.LoginView.as_view(
        template_name='registration/login.html'
    ), name='login'),

    path('logout/', auth_views.LogoutView.as_view(
        next_page='home'
    ), name='logout'),

    # MARKETPLACE
    path('market/publier/', v.publier_vente, name='publier_vente'),
    path('market/asset/<int:asset_id>/', v.detail_asset, name='detail_asset'),
    path('market/delete/<int:asset_id>/', v.supprimer_annonce, name='supprimer_annonce'),

    # PROJETS
    path('projets/deposer/', v.deposer_projet, name='deposer_projet'),
    path('projets/confirmation/', v.confirmation_paiement, name='confirmation'),
    path('projets/delete/<int:project_id>/', v.supprimer_projet, name='supprimer_projet'),

    # PAYMENT ⚠️ IMPORTANT (nom corrigé)
    path('payment/create/<int:asset_id>/', v.create_payment, name='create_payment'),
    path('payment/<int:asset_id>/', v.payment_page, name='payment_page'),

    # QUIZ
    path('quiz/', v.jouer_quiz, name='quiz'),

    # PAGES STATIC
    path('about/', v.about, name='about'),
    path('privacy/', v.privacy, name='privacy'),
    path('support/', v.support, name='support'),
    path('help/', v.help_page, name='help'),
)


# ===============================
# 📁 MEDIA
# ===============================
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
