from django import forms
from mailng.admin.models import Domain, Mailbox, Alias
from django.utils.translation import ugettext as _
from mailng.admin.templatetags.admin_extras import gender

class DomainForm(forms.ModelForm):
    class Meta:
        model = Domain
        
    def __init__(self, *args, **kwargs):
        super(DomainForm, self).__init__(*args, **kwargs)
        for f in ['name', 'quota']:
            self.fields[f].widget.attrs['size'] = 14

class MailboxForm(forms.ModelForm):
    quota = forms.IntegerField(label=_("Quota"), required=False)
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Confirmation"), widget=forms.PasswordInput)
    enabled = forms.BooleanField(label=gender("Enabled", "f"), required=False)

    class Meta:
        model = Mailbox
        fields = ('name', 'address')

    def __init__(self, *args, **kwargs):
        super(MailboxForm, self).__init__(*args, **kwargs)
        for f in ['name', 'address', 'quota', 'password1', 'password2']:
            self.fields[f].widget.attrs['size'] = 14

    def clean_password2(self):
        if self.cleaned_data["password1"] != self.cleaned_data["password2"]:
            raise forms.ValidationError(_("Passwords mismatch"))
        return self.cleaned_data["password2"]

class AliasForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        domain = None
        if kwargs.has_key("domain"):
            domain = kwargs["domain"]
            del kwargs["domain"]
        super(AliasForm, self).__init__(*args, **kwargs)
        self.fields['address'].widget.attrs['size'] = 14
        if domain:
            self.fields['mbox'].queryset = Mailbox.objects.filter(domain=domain.id)

    class Meta:
        model = Alias
        fields = ('address', 'mbox', 'enabled')

class PermissionForm(forms.Form):
    domain = forms.ModelChoiceField(queryset=Domain.objects.all(), label=_("Domain"), 
                                    required=True)
    user = forms.ChoiceField(label=_("User"), required=True)
    role = forms.ChoiceField(label=_("Role"), required=True, 
                             choices=(("SuperAdmins", _("Super administrator")),
                                      ("DomainAdmins", _("Domain administrator"))))