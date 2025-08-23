from django import forms
from .models import Jogador, Jogo, Jogo_daily, Jogo_custom, Jogo_VF

class JogadorForm(forms.ModelForm):
    name_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Jogador
        fields = ['name_public', 'name_user', 'name_email', 'name_password']
        labels = {
            'name_public': 'Nome Público',
            'name_user': 'Nome de Usuário',
            'name_email': 'Email',
            'name_password': 'Senha',
        }

    def save(self, commit=True):
        jogador = super().save(commit=False)
        jogador.set_password(self.cleaned_data['name_password'])
        if commit:
            jogador.save()
        return jogador

class JogadorLoginForm(forms.Form):
    name_user = forms.CharField(label="Nome de Usuário")
    password = forms.CharField(widget=forms.PasswordInput, label="Senha")
    
class MessageForm(forms.Form):
<<<<<<< Updated upstream
    texto = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Digite sua mensagem...'}), max_length=1000)
=======
    texto = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Digite sua mensagem...'}), max_length=1000)


class JogoForm(forms.ModelForm):
    class Meta:
        model = Jogo
        fields =  ['session', 'players', 'data_fim','tentativas']
        # id e data_inicio são automáticos, então não entram aqui


class JogoDailyForm(forms.ModelForm):
    class Meta:
        model = Jogo_daily
        fields = ['session', 'players', 'data_fim','tentativas']  
        # daily_date é auto_now_add, então não aparece no form

class JogoDailyForm2(forms.ModelForm):
    class Meta:
        model = Jogo_daily
        fields = ['tentativas']
        readonly_fields = ['tentativas']
        
        # daily_date é auto_now_add, então não aparece no form
class JogoCustomForm(forms.ModelForm):
    class Meta:
        model = Jogo_custom
        fields = ['session', 'players', 'data_fim']  
        # se quiser campos adicionais para custom_name, precisa adicionar no model
        
class JogoVFForm(forms.ModelForm):
    class Meta:
        model = Jogo_VF
        fields = ['session', 'players', 'data_fim', 'pontuacao', 'acertos']  
        # se quiser campos adicionais para custom_name, precisa adicionar no model
        
        
        

TIPOS_JOGO = (
    ('daily', 'Jogo Diário'),
    ('custom', 'Jogo Custom'),
    ('vf', 'Jogo Verdadeiro/Falso'),
)

class CriarSessaoForm(forms.Form):
    tipo_jogo = forms.ChoiceField(choices=TIPOS_JOGO, label="Tipo de Jogo")
>>>>>>> Stashed changes
