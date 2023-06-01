from django import forms
from mainapp.models import Post

class PostForm(forms.ModelForm):
    image = forms.ImageField(label='📎',required = False)
    class Meta:
        model = Post
        fields = ( 'text', 'image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.clear_checkbox_label = 'clear'
        self.fields['image'].widget.initial_text = "currently"
        self.fields['image'].widget.input_text = "change"

