from django import forms
from .model import Rooms

class CreateRoomForm(forms.ModelForm):
    class Meta:
        model = Rooms

        fields = (
            'room_name',
            'representative_person_name',
            'category',
            'work_time',
            'subject_to',
            'room_image',
            'week_at',
        )


    def clean_room_name(self):
        value = self.cleaned_data['room_name']
        if len(value) >= 11:
            raise  forms.ValidationError(
                '10文字以内で入力してください',
            )

        return value

    def clean_representative_person_name(self):
        value = self.cleaned_data['representative_person_name']
        if len(value) >= 11:
            raise forms.ValidationError(
                '10文字以内で入力してください',
            )
        return value

    def clean_category(self):
        value = self.cleaned_data['category']
        if len(value) >= 11:
            raise forms.ValidationError(
                '10文字以内で入力してください',
            )
        return value

    def clean_work_time(self):
        value = self.cleaned_data['work_time']
        if value >= 7:
            raise forms.ValidationError(
                '適切な時間を入力してください',
            )
        return value

    def clean_subject_to(self):
        value = self.cleaned_data['subject_to']
        if value >= 11:
            raise forms.ValidationError(
                '10文字以内で入力してください',
            )
        return value

    def clean_week_at(self):
        value = self.cleaned_data['week_at']
        if value >= 11:
            raise forms.ValidationError(
                '10文字以内で入力してください',
            )
        return value

    def clean_room_image(self):
        value = self.cleaned_data['room_image']
        return value





class EditRoomForm(forms.ModelForm):
    class Meta:
        model = Rooms

        fields = (
            'room_name',
            'representative_person_name',
            'category',
            'work_time',
            'subject_to',
            'room_image',
            'week_at',
        )


    def clean_room_name(self):
        value = self.cleaned_data['room_name']
        if len(value) >= 11:
            raise  forms.ValidationError(
                '10文字以内で入力してください',
            )

        return value

    def clean_representative_person_name(self):
        value = self.cleaned_data['representative_person_name']
        if len(value) >= 11:
            raise forms.ValidationError(
                '10文字以内で入力してください',
            )
        return value

    def clean_category(self):
        value = self.cleaned_data['category']
        if len(value) >= 11:
            raise forms.ValidationError(
                '10文字以内で入力してください',
            )
        return value

    def clean_work_time(self):
        value = self.cleaned_data['work_time']
        if value >= 7:
            raise forms.ValidationError(
                '適切な時間を入力してください',
            )
        return value

    def clean_week_at(self):
        value = self.cleaned_data['week_at']
        if value >= 11:
            raise forms.ValidationError(
                '10文字以内で入力してください',
            )
        return value

    def clean_room_image(self):
        value = self.cleaned_data['room_image']
        return value
