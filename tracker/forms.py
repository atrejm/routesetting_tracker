from django import forms
from django.forms import formset_factory, BaseFormSet
from .models import Routesetter, BoulderProblem, ZoneModel
from django.forms.models import inlineformset_factory
from django.core import validators
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column, Field, Fieldset, Button


class RoutesetterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RoutesetterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit','Add Routesetter'))
        

    class Meta:
        model = Routesetter
        fields = ("name",)

class BoulderProblemForm(forms.ModelForm): 
    # use django-crispy-forms to make this look less like shit: https://django-crispy-forms.readthedocs.io/en/latest/index.html

    class Meta:
        model = BoulderProblem
        fields = ("setter","grade","color",)

class AddBoulderForm(forms.ModelForm):
    class Meta:
        model = BoulderProblem
        fields = ['setter','grade','color']

class AddBoulderFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_method = 'post'
        self.form_action = 'boulderchart'
        self.layout = Field('field_name', style="color: #333;", css_class="whatever", id="field_name")
        self.layout = Layout(
            Row(
                Column('setter', css_class='form-group col-md-4 mb-0'),
                Column('grade', css_class='form-group col-md-4 mb-0'),
                Column('color', css_class='form-group col-md-4 mb-0'),
                css_class = 'form-row'
            )
        )
        self.add_input(Submit('submit','Save'))
        self.render_required_fields = True

class ManageBoulderFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_method = 'post'
        self.form_action = 'boulderchart'
        self.form_show_labels = False
        self.layout = Layout(
            Row(
                Column('grade', css_class='form-group col-md-3 mb-0'),
                Column('color', css_class='form-group col-md-3 mb-0'),
                Column('zone_name', css_class='form-group col-md-3 mb-0'),
                Column('DELETE', css_class='form-group col-md-3 mb-0'),
                css_class = 'form-row'
            )
        )
        self.add_input(Submit('submit','Save'))
        self.render_required_fields = True

class EditZoneFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_method = 'post'
        self.form_action = 'boulderchart'
        self.form_show_labels = False
        self.layout = Layout(
            Row(
                Column('grade', css_class='form-group col-md-3 mb-0'),
                Column('setter', css_class='form-group col-md-3 mb-0'),
                Column('color', css_class='form-group col-md-3 mb-0'),
                Column('DELETE', css_class='form-group col-md-3 mb-0'),
                css_class = 'form-row'
            )
        )
        self.add_input(Submit('submit','Save'))
        self.render_required_fields = True

class DateInputForm(forms.Form):
    start_date = forms.DateField(widget=forms.SelectDateWidget)
    end_date = forms.DateField(widget=forms.SelectDateWidget)

class ZoneChoiceForm(forms.Form):
    #zone_obj = forms.ModelChoiceField(ZoneModel.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        zones = ZoneModel.objects.all()



        self.helper = FormHelper()
        self.form_method = 'post'
        #self.form_action = 'boulderchart'
        for zone in zones:
            self.helper.add_input(Submit(zone.zone_name, "Zone {}".format(zone.zone_name)))
    
class ArchiveZoneForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.form_method = 'post'
        self.helper.add_input(Submit('submit', "Archive this set?"))    
