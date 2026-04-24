from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


# ===============================
# 🔧 UTILITAIRE SLUG
# ===============================
def generate_unique_slug(instance, field_value):
    base_slug = slugify(field_value)
    slug = base_slug
    model = instance.__class__
    counter = 1

    while model.objects.filter(slug=slug).exclude(id=instance.id).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1

    return slug


# ===============================
# 💰 ASSET
# ===============================
class Asset(models.Model):

    CATEGORY_CHOICES = [
        ('YT', 'YouTube'),
        ('FB', 'Facebook'),
        ('IG', 'Instagram'),
        ('WEB', 'Site Web'),
        ('APP', 'Application'),
    ]

    STATUS_CHOICES = [
        ('AVAILABLE', 'Disponible'),
        ('PENDING', 'En cours'),
        ('SOLD', 'Vendu'),
    ]

    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assets')

    title = models.CharField(max_length=200)
    slug = models.SlugField(blank=True, null=True)

    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    description = models.TextField()

    price = models.DecimalField(max_digits=12, decimal_places=2)

    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='AVAILABLE')
    is_verified = models.BooleanField(default=False)

    image = models.ImageField(upload_to='assets/', blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)

    views = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self, self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# ===============================
# 💳 TRANSACTION
# ===============================
class Transaction(models.Model):

    STATUS_CHOICES = [
        ('INITIATED', 'Initiée'),
        ('PROCESSING', 'En cours'),
        ('COMPLETED', 'Terminée'),
        ('CANCELLED', 'Annulée'),
    ]

    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='transactions')

    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='INITIATED')

    payment_method = models.CharField(max_length=50, blank=True, null=True)
    payment_id = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(fields=['buyer', 'asset'], name='unique_purchase')
        ]

    def __str__(self):
        return f"{self.buyer} -> {self.asset}"


# ===============================
# 🚀 PROJECT
# ===============================
class Project(models.Model):

    STATUS_CHOICES = [
        ('PENDING', 'En attente'),
        ('REVIEW', 'En analyse'),
        ('APPROVED', 'Approuvé'),
        ('FUNDED', 'Financé'),
        ('REJECTED', 'Rejeté'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')

    project_name = models.CharField(max_length=200)
    slug = models.SlugField(blank=True, null=True)

    description = models.TextField()

    jobs_to_create = models.PositiveIntegerField()
    amount_needed = models.DecimalField(max_digits=12, decimal_places=2)
    amount_raised = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='PENDING')

    location = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='projects/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self, self.project_name)
        super().save(*args, **kwargs)

    def progress(self):
        if not self.amount_needed or self.amount_needed == 0:
            return 0
        return min(int((self.amount_raised / self.amount_needed) * 100), 100)

    def __str__(self):
        return self.project_name


# ===============================
# 🧠 QUESTION
# ===============================
class Question(models.Model):
    text = models.CharField(max_length=500)

    choice1 = models.CharField(max_length=200)
    choice2 = models.CharField(max_length=200)
    choice3 = models.CharField(max_length=200)
    choice4 = models.CharField(max_length=200)

    correct_answer = models.IntegerField()
    points = models.PositiveIntegerField(default=10)

    def __str__(self):
        return self.text


# ===============================
# 🏆 SCORE
# ===============================
class QuizScore(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    score = models.IntegerField(default=0)
    weekly_score = models.IntegerField(default=0)
    total_games = models.IntegerField(default=0)

    last_played = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} - {self.score} pts"


# ===============================
# 💳 PAYMENT (NOUVEAU PRO)
# ===============================
class Payment(models.Model):

    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('paid', 'Payé'),
        ('failed', 'Échoué'),
    ]

    METHOD_CHOICES = [
        ('manual', 'Manuel'),
        ('maxicash', 'MaxiCash'),
        ('stripe', 'Stripe'),
        ('crypto', 'Crypto'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    asset = models.ForeignKey(Asset, on_delete=models.SET_NULL, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)

    amount = models.DecimalField(max_digits=12, decimal_places=2)

    method = models.CharField(max_length=20, choices=METHOD_CHOICES, default='manual')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    reference = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.amount} - {self.status}"
