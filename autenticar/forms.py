from django import forms


class PasswordResetRequestForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 
                'style': 'margin-top: 20px; width: 700px; display:initial;',
                'placeholder': 'Digite seu nome de usuário',
            }
        ),
        label='Usuario',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Adiciona classes ao form-group e ao campo username
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['aria-label'] = 'Usuario'
        self.fields['username'].widget.attrs['aria-describedby'] = 'username-addon'
        self.fields['username'].widget.attrs['style'] = 'margin-top: 20px; width: 700px; display: initial;'

    def as_div(self):
        """Customize a renderização do formulário para adicionar a classe 'form-label' à label."""
        return self._html_output(
            normal_row='<div%(html_class_attr)s>%(label)s %(field)s%(help_text)s</div>',
            error_row='<div%(html_class_attr)s>%s</div>',
            row_ender='</div>',
            help_text_html=' <span class="helptext">%s</span>',
            errors_on_separate_row=True,
        )
    
