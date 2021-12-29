from django import forms
from server.models import ServerReservation
from django.db.models import Q


class AddReservation(forms.ModelForm):
    class Meta:
        model = ServerReservation
        fields = ['server_id', 'user_id', 'reservation_time', 'end_time']

    def clean_reservation_time(self):
        start = self.cleaned_data.get('reservation_time')
        if ServerReservation.objects.filter(Q(end_time__gte=start),
                                            Q(reservation_time__lte=start)).filter(server_id=self.cleaned_data.get('server_id')).exists():
            raise forms.ValidationError("Reservation time is booked by someone else!")
        else:
            return start

    def clean_end_time(self):
        end = self.cleaned_data.get('end_time')
        if ServerReservation.objects.filter(Q(end_time__gte=end),
                                            Q(reservation_time__lte=end)).filter(server_id=self.cleaned_data.get('server_id')).exists():
            raise forms.ValidationError("End time is booked by someone else!")
        else:
            return end
