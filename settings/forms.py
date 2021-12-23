from django import forms
from room.models import Rooms

class ChangeRoomInfoForm(forms.ModelForm):
    class Meta:
        model = Rooms

        fields = (
            'room_name',
            'representative_person_name',
            'room_image',
            'category',
            'work_time',
            'week_at',
            'subject_to',
        )
