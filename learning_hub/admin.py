from django.contrib import admin
from django.utils.html import format_html
from .models import Mentor, Course, Category, Testimonial,ContactMessage,MentorReview # Category, Testimonial импорттолду


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)} # Слагды автоматтык толтуруу

@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):

     list_display = ('display_photo', 'full_name', 'specialization', 'experience_years')
     search_fields = ('full_name', 'specialization')
     list_filter = ('specialization', 'experience_years')
     readonly_fields = ('photo_preview',)

     def display_photo(self, obj):
         if obj.photo:
             return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 50%;" />', obj.photo.url)
         return "Сүрөт жок"
     display_photo.short_description = 'Сүрөт'

     def photo_preview(self, obj):
         if obj.photo:
             return format_html('<img src="{}" width="150" height="150" style="object-fit: cover; border-radius: 10px;" />', obj.photo.url)
         return "(Сүрөт жүктөлө элек)"
     photo_preview.short_description = 'Сүрөттүн алдын-ала көрүнүшү'

     fieldsets = (
         (None, { 'fields': ('full_name', 'specialization', 'experience_years') }),
         ('Биография', { 'fields': ('bio',) }),
         ('Сүрөт', { 'fields': ('photo', 'photo_preview') }),
     )


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('display_image', 'title', 'category', 'mentor', 'price', 'duration_months') # category коштук
    search_fields = ('title', 'description')
    list_filter = ('category', 'mentor', 'duration_months') # category коштук
    autocomplete_fields = ['mentor', 'category'] # category коштук
    readonly_fields = ('image_preview',)

    # ... (display_image жана image_preview функциялары мурункудай калат) ...
    def display_image(self, obj):
         if obj.image:
             return format_html('<img src="{}" width="80" height="50" style="object-fit: cover; border-radius: 5px;" />', obj.image.url)
         return "Сүрөт жок"
    display_image.short_description = 'Сүрөт'

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="200" style="object-fit: cover; border-radius: 10px;" />', obj.image.url)
        return "(Сүрөт жүктөлө элек)"
    image_preview.short_description = 'Сүрөттүн алдын-ала көрүнүшү'


    fieldsets = (
         (None, { 'fields': ('title', 'category', 'mentor', 'price', 'duration_months', 'start_date') }), # category коштук
         ('Сүрөттөлүшү', { 'fields': ('description',) }),
         ('Курстун Сүрөтү', { 'fields': ('image', 'image_preview') }),
    )

# Пикирлер үчүн админ классы
@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'created_at', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('author_name', 'text')
    list_editable = ('is_active',) # Тизмеден эле активдүүлүгүн өзгөртүү

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('name', 'email', 'subject', 'message', 'created_at') # Админкадан өзгөртүүгө болбойт
    list_editable = ('is_read',) # Тизмеден эле "Окулдубу?" белгисин өзгөртүүгө болот

    # Админкада "is_read" белгисин өзгөртүү үчүн аракет (action)
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Тандалган билдирүүлөрдү 'Окулду' деп белгилөө"

    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = "Тандалган билдирүүлөрдү 'Окула элек' деп белгилөө"

    actions = [mark_as_read, mark_as_unread]

@admin.register(MentorReview)
class MentorReviewAdmin(admin.ModelAdmin):
    list_display = ('mentor', 'reviewer_display_name', 'rating', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'rating', 'created_at', 'mentor')
    search_fields = ('mentor__full_name', 'reviewer__username', 'comment')
    list_editable = ('is_approved',) # Админкадан эле жактыруу/жактырбоо
    actions = ['approve_reviews', 'disapprove_reviews']

    def reviewer_display_name(self, obj):
        return obj.reviewer.username # Же UserProfile'дан full_name алсаңыз болот
    reviewer_display_name.short_description = "Пикир калтыруучу"

    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)
    approve_reviews.short_description = "Тандалган пикирлерди жактыруу"

    def disapprove_reviews(self, request, queryset):
        queryset.update(is_approved=False)
    disapprove_reviews.short_description = "Тандалган пикирлерди жактырбоо"