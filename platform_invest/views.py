from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
import random

from .models import Asset, Project, Question, QuizScore, Payment
from .forms import InscriptionForm, AssetForm, ProjectForm


# ===============================
# 🏠 HOME
# ===============================
def home(request):
    assets = Asset.objects.order_by('-created_at')[:6]
    projets = Project.objects.order_by('-created_at')[:6]

    return render(request, 'platform_invest/home.html', {
        'assets': assets,
        'projets': projets,
        'total_assets': Asset.objects.count(),
        'total_projets': Project.objects.count(),
    })


# ===============================
# 🔐 INSCRIPTION
# ===============================
def inscription(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = InscriptionForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('dashboard')

    return render(request, 'registration/inscription.html', {'form': form})


# ===============================
# 📊 DASHBOARD SAAS PRO
# ===============================
@login_required
def dashboard(request):

    projets = Project.objects.filter(owner=request.user).order_by('-id')
    actifs = Asset.objects.filter(seller=request.user).order_by('-id')
    score, _ = QuizScore.objects.get_or_create(user=request.user)
    payments = Payment.objects.filter(user=request.user).order_by('-created_at')

    # KPI
    total_projets = projets.count()
    total_assets = actifs.count()
    total_payments = payments.count()

    total_value = sum([a.price for a in actifs]) if actifs else 0
    total_funding = sum([p.amount_needed for p in projets]) if projets else 0

    return render(request, 'platform_invest/dashboard.html', {
        'projets': projets,
        'actifs': actifs,
        'score': score,
        'payments': payments,

        'stats': {
            'total_projets': total_projets,
            'total_assets': total_assets,
            'total_payments': total_payments,
            'total_value': total_value,
            'total_funding': total_funding,
        }
    })


# ===============================
# 🛒 MARKETPLACE
# ===============================
@login_required
def publier_vente(request):
    form = AssetForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        asset = form.save(commit=False)
        asset.seller = request.user
        asset.save()
        messages.success(request, "Annonce publiée avec succès 🚀")
        return redirect('dashboard')

    return render(request, 'platform_invest/publier_vente.html', {'form': form})


def detail_asset(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)
    related_assets = Asset.objects.exclude(id=asset.id)[:3]

    return render(request, 'platform_invest/detail_asset.html', {
        'asset': asset,
        'related_assets': related_assets
    })


@login_required
def supprimer_annonce(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id, seller=request.user)

    if request.method == "POST":
        asset.delete()
        messages.success(request, "Annonce supprimée")
        return redirect('dashboard')

    return render(request, 'platform_invest/confirmer_suppression.html', {
        'object': asset
    })


# ===============================
# 🚀 PROJETS
# ===============================
@login_required
def deposer_projet(request):
    form = ProjectForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        projet = form.save(commit=False)
        projet.owner = request.user
        projet.save()
        messages.success(request, "Projet publié 🚀")
        return redirect('dashboard')

    return render(request, 'platform_invest/deposer_projet.html', {'form': form})


@login_required
def confirmation_paiement(request):
    project = Project.objects.filter(owner=request.user).last()

    return render(request, 'platform_invest/confirmation.html', {
        'project': project
    })


@login_required
def supprimer_projet(request, project_id):
    projet = get_object_or_404(Project, id=project_id, owner=request.user)

    if request.method == "POST":
        projet.delete()
        messages.success(request, "Projet supprimé")
        return redirect('dashboard')

    return render(request, 'platform_invest/confirmer_suppression.html', {
        'object': projet
    })


# ===============================
# 🎮 QUIZ
# ===============================
@login_required
def jouer_quiz(request):
    questions = Question.objects.all()

    if not questions.exists():
        return render(request, 'platform_invest/quiz.html', {
            'error': "Aucune question disponible."
        })

    question = random.choice(questions)
    score_obj, _ = QuizScore.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        selected = int(request.POST.get('answer', 0))

        if selected == question.correct_answer:
            score_obj.score += question.points

        score_obj.total_games += 1
        score_obj.save()

        return redirect('quiz')

    return render(request, 'platform_invest/quiz.html', {
        'question': question,
        'score': score_obj
    })


# ===============================
# 💳 PAIEMENT (SAAS PRO)
# ===============================
@login_required
def create_payment(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)

    payment, created = Payment.objects.get_or_create(
        user=request.user,
        asset=asset,
        defaults={
            'amount': asset.price,
            'method': 'manual',
            'status': 'pending'
        }
    )

    messages.success(request, "💰 Paiement créé")
    return redirect('payment_page', asset_id=asset.id)


@login_required
def payment_page(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)

    payment = Payment.objects.filter(user=request.user, asset=asset).first()

    if request.method == "POST":
        if payment:
            payment.status = "paid"
            payment.save()

        messages.success(request, "💰 Paiement confirmé")
        return redirect('dashboard')

    return render(request, 'platform_invest/payment.html', {
        'asset': asset,
        'payment': payment
    })


# ===============================
# 📄 PAGES STATIC
# ===============================
def about(request):
    return render(request, 'platform_invest/about.html')

def privacy(request):
    return render(request, 'platform_invest/privacy.html')

def support(request):
    return render(request, 'platform_invest/support.html')

def help_page(request):
    return render(request, 'platform_invest/help.html')
