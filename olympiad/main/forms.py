from django import forms


class ExcelUploadForm(forms.Form):
    """Форма для импорта excel файла"""
    excel_file = forms.FileField()
