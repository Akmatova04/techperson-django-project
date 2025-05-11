# learning_hub/forms.py
from django import forms
from .models import ContactMessage # Жаңы түзгөн моделибизди импорттойбуз
from .models import ContactMessage, MentorReview

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Мисалы, Асан', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'email@example.com', 'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Курс боюнча суроо', 'class': 'form-control'}),
            'message': forms.Textarea(attrs={'placeholder': 'Сурооңузду же сунушуңузду ушул жерге жазыңыз...', 'rows': 5, 'class': 'form-control'}),
        }
        labels = { # Талаалардын аталыштары (эгер модельдеги verbose_name'ден башкача болгуңуз келсе)
            'name': 'Атыңыз*',
            'email': 'Email дарегиңиз*',
            'subject': 'Темасы (милдеттүү эмес)',
            'message': 'Сиздин билдирүүңүз*',
        }
        help_texts = { # Талаалардын астындагы жардамчы тексттер (керек болсо)
            # 'name': 'Сураныч, атыңызды толук жазыңыз.',
        }
    
    # Эгер кээ бир талааларды милдеттүү эмес кылгыңыз келсе:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subject'].required = False # Темасы милдеттүү эмес
        # name, email, message демейки боюнча милдеттүү (ModelForm аларды моделден алат)
    
class MentorReviewForm(forms.ModelForm):
    rating = forms.IntegerField(
        min_value=1,
        max_value=5,
        widget=forms.NumberInput(attrs={'type': 'number', 'min': '1', 'max': '5', 'class': 'form-control form-control-sm w-auto'}), # Же жылдызча виджетин колдонсо болот
        label="Сиздин бааңыз (1-5)"
    )
    comment = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Ментор жөнүндө пикириңизди жазыңыз...'}),
        label="Пикириңиз"
    )

    class Meta:
        model = MentorReview
        fields = ['rating', 'comment'] # reviewer жана mentor view'дан алынат