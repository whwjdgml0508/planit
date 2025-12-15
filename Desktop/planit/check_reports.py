import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'planit_project.settings.production')
django.setup()

from community.models import Report

reports = Report.objects.all()
print(f"Total reports: {reports.count()}")
print("\nReport IDs:")
for report in reports[:10]:
    print(f"- {report.id} | {report.get_report_type_display()} | {report.status}")
