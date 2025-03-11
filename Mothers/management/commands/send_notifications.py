from django.core.management.base import BaseCommand
from datetime import timedelta
from django.utils.timezone import now
from Mothers.models import MaternalProfile, Notification, Vaccination, Appointment

class Command(BaseCommand):  # ✅ Ensure this class exists!
    help = "Send notifications to mothers 2 days before vaccination or doctor appointment"

    def handle(self, *args, **kwargs):
        today = now().date()
        reminder_date = today + timedelta(days=2)

        # Check for upcoming vaccinations
        vaccinations = Vaccination.objects.filter(date=reminder_date)
        for vaccination in vaccinations:
            mother = vaccination.mother
            Notification.objects.create(
                mother=mother,
                message=f"Reminder: Your child's vaccination is scheduled for {vaccination.date}. Please attend."
            )
            self.stdout.write(self.style.SUCCESS(f"Notification sent to {mother.name} for vaccination."))

        # Check for upcoming doctor appointments
        appointments = Appointment.objects.filter(date=reminder_date)
        for appointment in appointments:
            mother = appointment.mother
            Notification.objects.create(
                mother=mother,
                message=f"Reminder: Your appointment with the doctor is on {appointment.date}. Please attend."
            )
            self.stdout.write(self.style.SUCCESS(f"Notification sent to {mother.name} for appointment."))

        self.stdout.write(self.style.SUCCESS("All notifications sent successfully!"))
