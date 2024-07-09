from django import forms

class CustomModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.name} - {obj.stage} - {obj.class_olympiad} - {obj.subject}"
