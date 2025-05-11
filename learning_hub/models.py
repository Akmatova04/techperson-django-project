# learning_hub/models.py
from django.db import models
from django.contrib.auth.models import User # User моделин импорттоо
from django.utils import timezone
from django.utils.text import slugify # Слаг түзүү үчүн
from django.core.validators import MinValueValidator, MaxValueValidator # Рейтинг үчүн

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Аталышы")
    slug = models.SlugField(max_length=110, unique=True, blank=True, verbose_name="Слаг (авто)")
    is_active = models.BooleanField(default=True, verbose_name="Активдүүбү?") # <-- КОШУЛДУ

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категориялар"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            original_slug = self.slug
            counter = 1
            while Category.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f'{original_slug}-{counter}'
                counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Mentor(models.Model):
    # Эгер User модели менен байланыштырсак (ар бир ментор системада колдонуучу болсо)
    # user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='mentor_profile', verbose_name="Колдонуучу (эгер бар болсо)")
    full_name = models.CharField(max_length=100, verbose_name="Толук аты-жөнү")
    bio = models.TextField(verbose_name="Кыскача маалымат/Биографиясы")
    photo = models.ImageField(upload_to='mentors_photos/', blank=True, null=True, verbose_name="Сүрөтү")
    experience_years = models.PositiveIntegerField(default=0, verbose_name="Тажрыйба жылы")
    specialization = models.CharField(max_length=200, blank=True, verbose_name="Адистиги")
    is_active = models.BooleanField(default=True, verbose_name="Активдүүбү?") # <-- КОШУЛДУ
    # Кошумча: email, телефон, социалдык тармактардын шилтемелери ж.б.
    # email = models.EmailField(blank=True, null=True)
    # phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Ментор"
        verbose_name_plural = "Менторлор"
        ordering = ['full_name']

class Course(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='courses',
        verbose_name="Категория"
    )
    title = models.CharField(max_length=200, verbose_name="Курстун аталышы")
    description = models.TextField(verbose_name="Курстун толук сүрөттөлүшү") # description бул жерде, short_description өзүнчө кылсак болот
    short_description = models.TextField(blank=True, verbose_name="Кыскача сүрөттөлүшү (карточка үчүн)")
    what_you_will_learn = models.TextField(blank=True, verbose_name="Эмнелерди үйрөнөсүз (ар бир пункт жаңы саптан)")
    image = models.ImageField(upload_to='courses_images/', blank=True, null=True, verbose_name="Курстун сүрөтү/баннери")
    duration_months = models.PositiveIntegerField(default=1, verbose_name="Узактыгы (ай)")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Баасы (сом)")
    start_date = models.DateField(blank=True, null=True, verbose_name="Башталуу күнү")
    mentor = models.ForeignKey(
        Mentor,
        on_delete=models.SET_NULL, # Эгер ментор өчүрүлсө, курс калат, бирок ментору жок
        null=True,
        blank=True, # Менторсуз курс болушу мүмкүн
        related_name='courses_taught',
        verbose_name="Ментор/Мугалим"
    )
    is_active = models.BooleanField(default=True, verbose_name="Активдүүбү? (Сайтта көрсөтүлсүнбү?)") # <-- КОШУЛДУ
    # Кошумча талаалар: difficulty_level, prerequisites ж.б.

    def __str__(self):
        return self.title

    @property
    def what_you_will_learn_list(self):
        """ "Эмне үйрөнөсүз" талаасын саптарга бөлөт """
        if self.what_you_will_learn:
            return [item.strip() for item in self.what_you_will_learn.splitlines() if item.strip()]
        return []

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курстар"
        ordering = ['-start_date', 'title'] # Эң жаңы же жакында баштала тургандары биринчи

class Testimonial(models.Model):
    author_name = models.CharField(max_length=100, verbose_name="Автордун аты-жөнү")
    text = models.TextField(verbose_name="Пикирдин тексти")
    # author_position = models.CharField(max_length=100, blank=True, verbose_name="Кызматы/Статусу")
    # course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Кайсы курска?")
    # photo = models.ImageField(upload_to='testimonials_photos/', blank=True, null=True, verbose_name="Автордүн сүрөтү")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Түзүлгөн күнү")
    is_active = models.BooleanField(default=True, verbose_name="Активдүүбү? (Сайтта көрсөтүлсүнбү?)") # Бул жерде мурунтан бар экен

    class Meta:
        verbose_name = "Пикир (Отзыв)"
        verbose_name_plural = "Пикирлер (Отзывдар)"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.author_name} жөнүндө пикир"
    
class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments', verbose_name="Колдонуучу")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrolled_users', verbose_name="Курс")
    enrolled_at = models.DateTimeField(auto_now_add=True, verbose_name="Жазылган күнү")

    class Meta:
        unique_together = ('user', 'course')
        verbose_name = "Курска жазылуу"
        verbose_name_plural = "Курска жазылуулар"
        ordering = ['-enrolled_at']

    def __str__(self):
        return f"{self.user.username} жазылды '{self.course.title}' курсуна"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100, verbose_name="Аты")
    email = models.EmailField(verbose_name="Email дареги")
    subject = models.CharField(max_length=200, blank=True, null=True, verbose_name="Темасы")
    message = models.TextField(verbose_name="Билдирүү")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Жөнөтүлгөн убактысы")
    is_read = models.BooleanField(default=False, verbose_name="Окулдубу?")

    class Meta:
        verbose_name = "Байланыш билдирүүсү"
        verbose_name_plural = "Байланыш билдирүүлөрү"
        ordering = ['-created_at']

    def __str__(self):
        return f"Кат: {self.name} ({self.email}) - Тема: {self.subject or 'Темасы жок'}"
    
class MentorReview(models.Model):
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, related_name='reviews', verbose_name="Ментор")
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_mentor_reviews', verbose_name="Пикир калтыруучу")
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Рейтинг (1-5)",
        help_text="Менторго 1ден 5ке чейин баа бериңиз"
    )
    comment = models.TextField(verbose_name="Пикириңиз")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Калтырылган күнү")
    is_approved = models.BooleanField(default=False, verbose_name="Админ тарабынан жактырылдыбы?")

    class Meta:
        verbose_name = "Менторго пикир"
        verbose_name_plural = "Менторлорго пикирлер"
        ordering = ['-created_at']
        # unique_together = ('mentor', 'reviewer') # Эгер бир колдонуучу бир менторго бир гана пикир калтырса

    def __str__(self):
        return f"{self.reviewer.username} пикири {self.mentor.full_name} үчүн ({self.rating} жылдыз)"