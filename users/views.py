# users/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.conf import settings
from django.urls import reverse # reverse функциясын импорттойбуз
from urllib.parse import urlencode # urlencode функциясын импорттойбуз
from django.utils.http import url_has_allowed_host_and_scheme # Коопсуздук үчүн

from .forms import PhoneNumberForm, OTPVerificationForm, UserUpdateForm, UserProfileUpdateForm
from .models import OTPToken, UserProfile
from .utils import send_sms_via_provider

def request_otp_view(request):
    # Эгер колдонуучу мурунтан эле кирген болсо, 'next' дарегине же негизги бетке багыттоо
    if request.user.is_authenticated:
        next_url = request.GET.get('next')
        # Коопсуздук текшерүүсү: 'next' URL'и биздин сайттын ичиндеги дарекпи?
        if next_url and url_has_allowed_host_and_scheme(url=next_url, allowed_hosts={request.get_host()}):
            return redirect(next_url)
        return redirect(getattr(settings, 'LOGIN_REDIRECT_URL', 'learning_hub:home'))

    if request.method == 'POST':
        form = PhoneNumberForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            
            # Телефон номерин стандартташтыруу
            if phone_number.startswith('0') and len(phone_number) == 10:
                phone_number = '+996' + phone_number[1:]
            elif phone_number.startswith('996') and len(phone_number) == 12 and not phone_number.startswith('+'):
                phone_number = '+' + phone_number
            
            # Жаңы OTP түзүү
            otp_entry = OTPToken(phone_number=phone_number)
            otp_entry.generate_otp()
            otp_entry.set_expiration(minutes=settings.OTP_EXPIRE_MINUTES if hasattr(settings, 'OTP_EXPIRE_MINUTES') else 5) # Мисалы, 5 мүнөт
            otp_entry.save()

            message_body = f"IT University'ге катталуу үчүн сиздин бир жолку кодуңуз: {otp_entry.otp_code}"
            if settings.DEBUG:
                print(f"DEBUG: OTP for {phone_number} is {otp_entry.otp_code}")

            success, sms_message_status = send_sms_via_provider(phone_number, message_body)

            if success:
                messages.success(request, f"Код {phone_number} номериңизге жөнөтүлдү. Сураныч, текшериңиз.")
                request.session['registration_phone_number'] = phone_number
                
                next_url_param = request.GET.get('next', '')
                # verify_otp барагына багыттоочу URL'ди түзүү
                verify_otp_base_url = reverse('users:verify_otp')
                
                if next_url_param and url_has_allowed_host_and_scheme(url=next_url_param, allowed_hosts={request.get_host()}):
                    query_string = urlencode({'next': next_url_param})
                    final_redirect_url = f"{verify_otp_base_url}?{query_string}"
                else:
                    final_redirect_url = verify_otp_base_url
                
                return redirect(final_redirect_url)
            else:
                messages.error(request, f"SMS жөнөтүүдө ката кетти: {sms_message_status}")
        else:
            # Форма жараксыз болсо, ар бир талаанын катасын көрсөтүү
            for field_name, error_list in form.errors.items():
                label = form.fields[field_name].label if form.fields[field_name].label else field_name.replace('_', ' ').title()
                for error in error_list:
                    messages.error(request, f"{label}: {error}")
    else:
        form = PhoneNumberForm()

    context = {
        'form': form,
        'next_url_param': request.GET.get('next', '') # Шаблонго 'next' параметрин өткөрүү
    }
    return render(request, 'users/request_otp.html', context)


def verify_otp_view(request):
    if request.user.is_authenticated:
        next_url = request.GET.get('next')
        if next_url and url_has_allowed_host_and_scheme(url=next_url, allowed_hosts={request.get_host()}):
            return redirect(next_url)
        return redirect(getattr(settings, 'LOGIN_REDIRECT_URL', 'learning_hub:home'))

    phone_number_from_session = request.session.get('registration_phone_number')

    if not phone_number_from_session:
        messages.warning(request, "Сессия табылган жок же эскирген. Сураныч, катталууну кайрадан баштаңыз.")
        # Эгер 'next' бар болсо, аны request_otp'га кайра өткөрөбүз
        next_param_for_request = request.GET.get('next', '')
        request_otp_url = reverse('users:request_otp')
        if next_param_for_request and url_has_allowed_host_and_scheme(url=next_param_for_request, allowed_hosts={request.get_host()}):
            query_string = urlencode({'next': next_param_for_request})
            request_otp_url = f"{request_otp_url}?{query_string}"
        return redirect(request_otp_url)

    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            otp_code_entered = form.cleaned_data['otp_code']
            try:
                otp_entry = OTPToken.objects.filter(
                    phone_number=phone_number_from_session,
                    is_used=False
                ).latest('created_at')

                if otp_entry.otp_code == otp_code_entered:
                    if otp_entry.is_valid():
                        otp_entry.is_used = True
                        otp_entry.save()

                        user, user_created = User.objects.get_or_create(username=phone_number_from_session)
                        if user_created:
                            user.set_unusable_password()
                            user.save()
                            # UserProfile сигналы автоматтык түрдө түзөт, бирок маалыматтарды бул жерде жаңыртабыз
                            profile = user.profile 
                            profile.phone_number = phone_number_from_session
                            profile.is_phone_verified = True
                            # Эгер UserProfile'да first_name, last_name сыяктуу талаалар болсо,
                            # аларды бул жерде демейки маанилер менен толтурсак болот же кийин профиль өзгөртүүдө
                            profile.save()
                        else:
                            profile, profile_created = UserProfile.objects.get_or_create(user=user) # Эгер кокусунан жок болсо
                            if profile.phone_number != phone_number_from_session or not profile.is_phone_verified:
                                profile.phone_number = phone_number_from_session
                                profile.is_phone_verified = True
                                profile.save()
                        
                        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                        messages.success(request, "Сиз ийгиликтүү катталдыңыз жана системага кирдиңиз!")
                        if 'registration_phone_number' in request.session:
                            del request.session['registration_phone_number']
                        
                        next_url = request.GET.get('next')
                        if next_url and url_has_allowed_host_and_scheme(url=next_url, allowed_hosts={request.get_host()}):
                            return redirect(next_url)
                        else:
                            redirect_url_setting = getattr(settings, 'LOGIN_REDIRECT_URL', 'learning_hub:home')
                            return redirect(redirect_url_setting)
                    else:
                        messages.error(request, "Коддун мөөнөтү өтүп кеткен. Сураныч, жаңы код алыңыз.")
                else:
                    messages.error(request, "Код туура эмес. Кайталап көрүңүз.")
            except OTPToken.DoesNotExist:
                messages.error(request, "Бул номерге жарактуу код табылган жок. Сураныч, кайрадан баштаңыз.")
                next_param_for_request = request.GET.get('next', '')
                request_otp_url = reverse('users:request_otp')
                if next_param_for_request and url_has_allowed_host_and_scheme(url=next_param_for_request, allowed_hosts={request.get_host()}):
                    query_string = urlencode({'next': next_param_for_request})
                    request_otp_url = f"{request_otp_url}?{query_string}"
                return redirect(request_otp_url)
        else:
            for field_name, error_list in form.errors.items():
                label = form.fields[field_name].label if form.fields[field_name].label else field_name.replace('_', ' ').title()
                for error in error_list:
                    messages.error(request, f"{label}: {error}")
    else:
        form = OTPVerificationForm()

    context = {
        'form': form,
        'phone_number_for_template': phone_number_from_session,
        'next_url_param': request.GET.get('next', '')
    }
    return render(request, 'users/verify_otp.html', context)


@login_required
def user_profile_view(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Профилиңиз ийгиликтүү жаңыртылды!")
            return redirect('users:profile')
        else:
            messages.error(request, "Сураныч, формадагы каталарды оңдоңуз.")
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileUpdateForm(instance=profile)
    context = {
        'u_form': user_form,
        'p_form': profile_form,
        'profile': profile
    }
    return render(request, 'users/profile.html', context)

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "Сиз системадан ийгиликтүү чыктыңыз.")
    return redirect(getattr(settings, 'LOGOUT_REDIRECT_URL', 'learning_hub:home'))