# users/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
import random

# UserProfile модели
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    phone_number = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        null=True,
        verbose_name="Телефон номери"
    )
    is_phone_verified = models.BooleanField(default=False, verbose_name="Телефон тастыкталганбы?")
    
    first_name = models.CharField(max_length=100, blank=True, verbose_name="Аты")
    last_name = models.CharField(max_length=100, blank=True, verbose_name="Фамилиясы")
    bio = models.TextField(blank=True, verbose_name="Кыскача маалымат (өзү жөнүндө)")
    
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True,
        verbose_name="Профиль сүрөтү"
    )
    date_of_birth = models.DateField(blank=True, null=True, verbose_name="Туулган күнү")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Түзүлгөн күнү")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Жаңыртылган күнү")

    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name} ({self.user.username})"
        return self.user.username

    @property
    def get_full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.user.username

    @property
    def get_profile_picture_url(self):
        if self.profile_picture and hasattr(self.profile_picture, 'url'):
            return self.profile_picture.url
        # Бул жерге static папкаңыздагы демейки сүрөттүн жолун көрсөтүңүз, мисалы:
        # from django.templatetags.static import static
        # return static('images/default_avatar.png')
        return None # Азырынча None, шаблондо чечебиз

# User модели түзүлгөндө автоматтык түрдө UserProfile түзүү үчүн сигнал
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    try:
        instance.profile.save()
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=instance)

# OTPToken модели
class OTPToken(models.Model):
    phone_number = models.CharField(max_length=20, help_text="Код жөнөтүлгөн телефон номери")
    otp_code = models.CharField(max_length=6, help_text="6 орундуу OTP код")
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(help_text="Коддун жарактуулук мөөнөтү")
    is_used = models.BooleanField(default=False, help_text="Код колдонулганбы?")

    def __str__(self):
        return f"OTP for {self.phone_number} - {self.otp_code} (Used: {self.is_used})"

    def is_valid(self):
        return not self.is_used and self.expires_at > timezone.now()

    def generate_otp(self, length=6):
        self.otp_code = "".join([str(random.randint(0, 9)) for _ in range(length)])

    def set_expiration(self, minutes=5):
        self.expires_at = timezone.now() + datetime.timedelta(minutes=minutes)