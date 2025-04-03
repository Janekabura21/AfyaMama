from django.db import migrations

def set_mother_ids(apps, schema_editor):
    ChildProfile = apps.get_model('MamaCare', 'ChildProfile')
    MaternalProfile = apps.get_model('MamaCare', 'MaternalProfile')
    
    for child in ChildProfile.objects.all():
        if child.mothers_profile:
            child.id = child.mothers_profile.identification_number
            child.save()

class Migration(migrations.Migration):
    dependencies = [
        ('MamaCare', '0001_initial'),  # Note capital 'MamaCare'
    ]
    
    operations = [
        migrations.RunPython(set_mother_ids),
    ]