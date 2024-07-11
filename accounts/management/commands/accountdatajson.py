import os
import json
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import UserProfile

User = get_user_model()

class Command(BaseCommand):
    help = 'Export data from User and UserProfile models to JSON files'

    def handle(self, *args, **options):
        try:
            # Export User data
            users_data = self.get_users_data()
            self.write_to_file('users.json', users_data)

            # Export UserProfile data
            user_profiles_data = self.get_user_profiles_data()
            self.write_to_file('user_profiles.json', user_profiles_data)

            self.stdout.write(self.style.SUCCESS('Successfully exported data to JSON files'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to export data: {str(e)}'))

    def get_users_data(self):
        users = User.objects.all()
        return json.dumps([{
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'email': user.email,
            'phone_number': str(user.phone_number) if user.phone_number else None,
            'role': user.get_role(),
            'date_joined': user.date_joined.isoformat(),
            'last_login': user.last_login.isoformat() if user.last_login else None,
            'created_date': user.created_date.isoformat(),
            'modified_date': user.modified_date.isoformat(),
            'is_admin': user.is_admin,
            'is_active': user.is_active,
            'is_staff': user.is_staff,
            'is_superadmin': user.is_superadmin,
        } for user in users], indent=4)

    def get_user_profiles_data(self):
        user_profiles = UserProfile.objects.all()
        return json.dumps([{
            'id': user_profile.id,
            'user': user_profile.user.id,
            'profile_picture': user_profile.profile_picture.url if user_profile.profile_picture else None,
            'cover_photo': user_profile.cover_photo.url if user_profile.cover_photo else None,
            'county': user_profile.county,
            'town': user_profile.town,
            'pin_code': user_profile.pin_code,
            'created_at': user_profile.created_at.isoformat(),
            'modified_at': user_profile.modified_at.isoformat(),
        } for user_profile in user_profiles], indent=4)

    def write_to_file(self, filename, data):
        file_path = os.path.join('accounts/data_exports', filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
            file.write(data)
