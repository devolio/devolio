from django import forms


class ProfileForm(forms.Form):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    summary = forms.CharField(required=False, widget=forms.Textarea)
    good_skills = forms.CharField(required=False)
    learning_skills = forms.CharField(required=False)
    slack_handle = forms.CharField(required=False)
    code_url = forms.URLField(required=False)
    website = forms.URLField(required=False)

    