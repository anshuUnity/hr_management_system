from django.forms import ModelForm
from accounts.models import File

class UploadForm(ModelForm):
    class Meta:
        model = File
        fields = ['file']

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)
        self.fields['file'].label = ""