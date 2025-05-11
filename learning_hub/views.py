# learning_hub/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course, Mentor, Category, Testimonial, Enrollment, ContactMessage, MentorReview
from .forms import ContactForm, MentorReviewForm
from urllib.parse import quote_plus
from django.conf import settings # Эгер LOGIN_REDIRECT_URL ж.б. колдонсоңуз
from django.db.models import Q # Татаал издөө үчүн

def home_view(request):
    mentors = Mentor.objects.filter(is_active=True).order_by('?')[:4] if hasattr(Mentor, 'is_active') else Mentor.objects.all().order_by('?')[:4]
    latest_courses_qs = Course.objects.all()
    if hasattr(Course, 'is_active'):
        latest_courses_qs = latest_courses_qs.filter(is_active=True)
    latest_courses = latest_courses_qs.filter(start_date__isnull=False).order_by('-start_date', '-id')[:3]
    
    testimonials_qs = Testimonial.objects.all()
    if hasattr(Testimonial, 'is_active'):
        testimonials_qs = testimonials_qs.filter(is_active=True)
    testimonials = testimonials_qs.order_by('-created_at')[:3]

    context = {
        'page_title': 'TechPerson: Келечегиңди бүгүн кур!',
        'mentors': mentors,
        'latest_courses': latest_courses,
        'testimonials': testimonials,
    }
    return render(request, 'learning_hub/home.html', context)

def course_list_view(request):
    category_slug = request.GET.get('category')
    categories_qs = Category.objects.all()
    if hasattr(Category, 'is_active'):
        categories_qs = categories_qs.filter(is_active=True)
    categories = categories_qs.order_by('name')

    courses_qs = Course.objects.all()
    if hasattr(Course, 'is_active'):
        courses_qs = courses_qs.filter(is_active=True)
    
    current_category_name = "Бардык Курстар"
    if category_slug:
        category_filter_kwargs = {'slug': category_slug}
        if hasattr(Category, 'is_active'):
            category_filter_kwargs['is_active'] = True
        category = get_object_or_404(Category, **category_filter_kwargs)
        courses = courses_qs.filter(category=category)
        current_category_name = category.name
    else:
        courses = courses_qs

    courses = courses.order_by('title')

    context = {
        'courses': courses,
        'categories': categories,
        'current_category_name': current_category_name,
        'page_title': current_category_name
    }
    return render(request, 'learning_hub/course_list.html', context)

def mentor_list_view(request):
    mentors_qs = Mentor.objects.all()
    if hasattr(Mentor, 'is_active'):
        mentors_qs = mentors_qs.filter(is_active=True)
    mentors = mentors_qs.order_by('full_name')
    
    context = {
        'mentors': mentors,
        'page_title': 'Биздин Менторлор'
    }
    return render(request, 'learning_hub/mentor_list.html', context)

def course_detail_view(request, course_id):
    course_qs = Course.objects.all()
    if hasattr(Course, 'is_active'):
        course_qs = course_qs.filter(is_active=True)
    course = get_object_or_404(course_qs, id=course_id)
    
    related_courses = None
    if course.category:
        related_courses_qs = Course.objects.filter(category=course.category)
        if hasattr(Course, 'is_active'):
            related_courses_qs = related_courses_qs.filter(is_active=True)
        related_courses = related_courses_qs.exclude(id=course_id)[:3]

    course_is_purchased_by_user = False
    if request.user.is_authenticated:
        course_is_purchased_by_user = Enrollment.objects.filter(user=request.user, course=course).exists()

    context = {
        'course': course,
        'related_courses': related_courses,
        'course_is_purchased_by_user': course_is_purchased_by_user,
        'page_title': course.title
    }
    return render(request, 'learning_hub/course_detail.html', context)

def mentor_detail_view(request, mentor_id):
    mentor_qs = Mentor.objects.all()
    if hasattr(Mentor, 'is_active'):
        mentor_qs = mentor_qs.filter(is_active=True)
    mentor = get_object_or_404(mentor_qs, id=mentor_id)
    
    courses_taught_qs = mentor.courses_taught.all()
    if hasattr(Course, 'is_active'):
        courses_taught_qs = courses_taught_qs.filter(is_active=True)
    courses_taught_by_mentor = courses_taught_qs.order_by('title')

    reviews = mentor.reviews.filter(is_approved=True).order_by('-created_at')
    review_form = None
    can_add_review = False
    has_already_reviewed = False

    if request.user.is_authenticated:
        if hasattr(MentorReview._meta, 'unique_together') and ('mentor', 'reviewer') in MentorReview._meta.unique_together:
            has_already_reviewed = MentorReview.objects.filter(mentor=mentor, reviewer=request.user).exists()
        
        if not has_already_reviewed:
            can_add_review = True
            review_form = MentorReviewForm()

    context = {
        'mentor': mentor,
        'courses_taught': courses_taught_by_mentor,
        'reviews': reviews,
        'review_form': review_form,
        'can_add_review': can_add_review,
        'has_already_reviewed': has_already_reviewed,
        'page_title': mentor.full_name
    }
    return render(request, 'learning_hub/mentor_detail.html', context)

@login_required
def add_mentor_review_view(request, mentor_id):
    mentor = get_object_or_404(Mentor, id=mentor_id, is_active=True if hasattr(Mentor, 'is_active') else True)
    
    if hasattr(MentorReview._meta, 'unique_together') and ('mentor', 'reviewer') in MentorReview._meta.unique_together:
        if MentorReview.objects.filter(mentor=mentor, reviewer=request.user).exists():
            messages.error(request, "Сиз бул менторго мурунтан эле пикир калтыргансыз.")
            return redirect('learning_hub:mentor_detail', mentor_id=mentor.id)

    if request.method == 'POST':
        form = MentorReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.mentor = mentor
            review.reviewer = request.user
            review.is_approved = False
            review.save()
            messages.success(request, "Пикириңиз кабыл алынды жана модерациядан кийин жарыяланат.")
            return redirect('learning_hub:mentor_detail', mentor_id=mentor.id)
        else:
            # UX жакшыртуу үчүн, каталуу форманы ошол эле бетте көрсөтүү керек
            # Бул үчүн mentor_detail_view'дун контекстин кайра түзүп, форманы кошуу керек
            messages.error(request, "Формада каталар бар. Сураныч, оңдоңуз.") # Жалпы ката
            # Азырынча redirect кылабыз, бул колдонуучунун киргизгендерин жоготот
            return redirect('learning_hub:mentor_detail', mentor_id=mentor.id) 
    else:
        return redirect('learning_hub:mentor_detail', mentor_id=mentor.id)

@login_required
def enroll_in_course_view(request, course_id):
    course = get_object_or_404(Course, id=course_id, is_active=True if hasattr(Course, 'is_active') else True)
    user = request.user
    already_enrolled = Enrollment.objects.filter(user=user, course=course).exists()

    if already_enrolled:
        messages.info(request, f"Сиз '{course.title}' курсуна мурунтан эле жазылгансыз.")
        return redirect('learning_hub:course_detail', course_id=course.id)

    if request.method == 'POST':
        Enrollment.objects.create(user=user, course=course)
        messages.success(request, f"Куттуктайбыз! Сиз '{course.title}' курсуна ийгиликтүү жазылдыңыз.")
        return redirect('learning_hub:course_detail', course_id=course.id)
    else:
        messages.warning(request, "Курска жазылуу үчүн тиешелүү баскычты колдонуңуз.")
        return redirect('learning_hub:course_detail', course_id=course.id)

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save() 
            messages.success(request, "Сиздин билдирүүңүз ийгиликтүү жөнөтүлдү! Жакынкы арада жооп беребиз.")
            return redirect('learning_hub:contact_success') 
    else:
        form = ContactForm()

    site_address_text = "Кыргызстан, Баткен ш., 8-март проспектиси, 123"
    display_phone_1 = "+996 (704) 54-27-66"
    display_phone_2 = "+996 (704) 54-27-67" 
    site_email_1 = "info@techperson.kg"
    site_email_2 = "support@techperson.kg"
    site_working_hours = "Дш-Жм: 9:00 - 18:00"
    
    social_links = {
        'instagram': 'https://instagram.com/TechPerson_it', 'facebook': '#', 
        'telegram': 'https://t.me/Altynbubu', 'whatsapp': 'https://wa.me/996704542766'
    }
    encoded_address = quote_plus(site_address_text)
    google_maps_url_for_address = f"https://www.google.com/maps/search/?api=1&query={encoded_address}"
    
    def clean_phone_for_tel(phone_str):
        return "".join(filter(lambda char: char.isdigit() or char == '+', phone_str or ""))

    tel_link_phone_1 = clean_phone_for_tel(display_phone_1)
    tel_link_phone_2 = clean_phone_for_tel(display_phone_2)

    context = {
        'form': form, 'page_title': 'Биз менен байланышыңыз',
        'address_text': site_address_text, 'google_maps_url': google_maps_url_for_address,
        'phone_1_display': display_phone_1, 'phone_1_tel': tel_link_phone_1,
        'phone_2_display': display_phone_2, 'phone_2_tel': tel_link_phone_2,
        'email_1': site_email_1, 'email_2': site_email_2,
        'working_hours': site_working_hours, 'social_links': social_links,
    }
    return render(request, 'learning_hub/contact.html', context)

def contact_success_view(request):
    context = { 'page_title': 'Билдирүүңүз Жөнөтүлдү' }
    return render(request, 'learning_hub/contact_success.html', context)

# --- ИЗДӨӨ VIEW'У УШУЛ ЖЕРДЕ ---
def search_results_view(request):
    query = request.GET.get('q', '').strip()
    courses_results = []
    
    page_title = "Издөө натыйжалары"
    results_found = False # Натыйжа табылдыбы же жокпу текшерүү үчүн

    if query:
        page_title = f"'{query}' боюнча издөө"
        
        # Курстарды издөө
        course_query = Q(title__icontains=query) | \
                       Q(description__icontains=query)
        if hasattr(Course, 'short_description'): # Эгер short_description талаасы бар болсо
             course_query |= Q(short_description__icontains=query)
        if hasattr(Course, 'what_you_will_learn'): # Эгер what_you_will_learn талаасы бар болсо
             course_query |= Q(what_you_will_learn__icontains=query)

        courses_qs = Course.objects.filter(course_query)
        if hasattr(Course, 'is_active'):
            courses_qs = courses_qs.filter(is_active=True)
        courses_results = courses_qs.distinct()
        
        if courses_results.exists():
            results_found = True
            
    context = {
        'query': query,
        'courses_results': courses_results,
        'page_title': page_title,
        'results_found': results_found, # Шаблонго өткөрүү
        'results_count': courses_results.count() if courses_results else 0
    }
    return render(request, 'learning_hub/search_results.html', context)