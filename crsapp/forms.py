from django import forms
from .models import ModelFile
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

class ImageForm(forms.ModelForm):
    class Meta:
        model = ModelFile
        fields = ('image',)


class LoginForm(AuthenticationForm):
    # ここからコンストラクタ（メンバ変数とかを設定する）
    # 各フィールドの初期化。
    def __init__(self, *args, **kwargs):
        # 基底クラス（継承元）のコンストラクタをオーバーライドする
        # コンストラクタの上書きはsuper().__init__()米メソッドの上書きはsuper().メソッド名()とのこと
        
        super().__init__(*args, **kwargs)

        for field in self.fields.values():

            # 入力フィールドのクラスに、form-controlを入れる
            field.widget.attrs['class']='form-control'
            # placeholderにはlabelを入れる
            field.widget.attrs['placeholder']=field.label


            
class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            # 入力フィールドのクラスに、form-controlを入れる
            field.widget.attrs['class']='form-control'
            # placeholderにはlabelを入れる
            field.widget.attrs['placeholder']=field.label
    class Meta:
        model=User
        fields=('username','password1','password2')

            