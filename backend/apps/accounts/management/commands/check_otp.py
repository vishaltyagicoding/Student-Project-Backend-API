from django.core.management.base import BaseCommand
from apps.accounts.models import OTPVerification, CustomUser


class Command(BaseCommand):
    help = 'Check OTP for a user email'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            help='Email address to check OTP for',
            required=True
        )

    def handle(self, *args, **options):
        email = options['email']

        try:
            user = CustomUser.objects.get(email=email)
            self.stdout.write(self.style.SUCCESS(f'\n✓ User found: {user.email}'))
            self.stdout.write(f'  Username: {user.username}')
            self.stdout.write(f'  Active: {user.is_active}')
            self.stdout.write(f'  Date joined: {user.date_joined}')

            # Get latest OTP
            otp = OTPVerification.objects.filter(user=user, is_used=False).order_by('-created_at').first()
            
            if otp:
                self.stdout.write(self.style.WARNING(f'\n📧 OTP Details:'))
                self.stdout.write(self.style.SUCCESS(f'  OTP: {otp.otp}'))
                self.stdout.write(f'  Created: {otp.created_at}')
                self.stdout.write(f'  Expired: {otp.is_expired()}')
                self.stdout.write(f'  Used: {otp.is_used}')
                
                if not otp.is_expired():
                    self.stdout.write(self.style.SUCCESS(f'\n✓ Valid OTP: {otp.otp}'))
                    self.stdout.write(self.style.WARNING('\nUse this OTP to verify:'))
                    self.stdout.write(f'POST /api/auth/verify-otp/')
                    self.stdout.write(f'{{"email": "{email}", "otp": "{otp.otp}"}}')
                else:
                    self.stdout.write(self.style.ERROR('\n✗ OTP has expired!'))
                    self.stdout.write('Use resend-otp endpoint to get a new one.')
            else:
                self.stdout.write(self.style.ERROR('\n✗ No OTP found for this user'))
                
            # Show all OTPs for debugging
            all_otps = OTPVerification.objects.filter(user=user).order_by('-created_at')
            if all_otps.count() > 1:
                self.stdout.write(f'\n📋 All OTPs ({all_otps.count()} total):')
                for idx, o in enumerate(all_otps[:5], 1):
                    status = '✓' if not o.is_used and not o.is_expired() else '✗'
                    self.stdout.write(f'  {status} {o.otp} - {o.created_at} (Used: {o.is_used}, Expired: {o.is_expired()})')

        except CustomUser.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'\n✗ User not found: {email}'))
            self.stdout.write('\nMake sure you registered first:')
            self.stdout.write('POST /api/auth/register/')
