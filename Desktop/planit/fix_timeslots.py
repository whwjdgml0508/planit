import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'planit_project.settings.production')
django.setup()

from timetable.models import TimeSlot, Semester
from accounts.models import User

# Fix all users' timeslots
for user in User.objects.all():
    current_semester = Semester.objects.filter(user=user, is_current=True).first()
    if current_semester:
        # Update all user's timeslots to use their current semester
        updated = TimeSlot.objects.filter(subject__user=user).update(semester=current_semester)
        print(f"{user.username}: {updated} TimeSlot(s) updated to {current_semester}")
    else:
        print(f"{user.username}: No current semester found")

print("\nDone!")
