from django import forms
from django.contrib.auth import get_user_model

from board.models import Board

User = get_user_model()


class CreateBoardForm(forms.ModelForm):
    cross_or_circle = forms.ChoiceField(choices=((1, "Circle"), (2, "Cross")))
    opponent = forms.ModelChoiceField(queryset=None, to_field_name="username")

    def __init__(self, user_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["opponent"].queryset = User.objects.exclude(id=user_id)

    class Meta:
        model = Board
        fields = ["cross_or_circle", "opponent"]
