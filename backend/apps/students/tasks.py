from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def send_student_registration_email(self, student_id, student_email, student_name, college_name):
    """
    Celery task to send registration confirmation email to new student
    """
    try:
        subject = 'Welcome to Student Management System'
        
        # HTML email content
        html_message = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #4CAF50; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; background-color: #f9f9f9; }}
                .info-box {{ background-color: white; padding: 15px; margin: 15px 0; border-left: 4px solid #4CAF50; }}
                .footer {{ text-align: center; padding: 20px; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Welcome to Student Management System</h1>
                </div>
                <div class="content">
                    <h2>Hello {student_name},</h2>
                    <p>Congratulations! Your registration has been successfully completed.</p>
                    
                    <div class="info-box">
                        <h3>Your Registration Details:</h3>
                        <p><strong>Student ID:</strong> {student_id}</p>
                        <p><strong>Email:</strong> {student_email}</p>
                        <p><strong>College:</strong> {college_name}</p>
                    </p>
                    
                    <p>Please keep your Student ID safe as you will need it for future reference.</p>
                    
                    <p>If you have any questions or need assistance, please don't hesitate to contact our support team.</p>
                    
                    <p>Best regards,<br>Student Management Team</p>
                </div>
                <div class="footer">
                    <p>This is an automated email. Please do not reply to this message.</p>
                    <p>&copy; 2024 Student Management System. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Plain text version
        plain_message = f"""
        Welcome to Student Management System
        
        Hello {student_name},
        
        Congratulations! Your registration has been successfully completed.
        
        Your Registration Details:
        - Student ID: {student_id}
        - Email: {student_email}
        - College: {college_name}
        
        Please keep your Student ID safe as you will need it for future reference.
        
        If you have any questions or need assistance, please don't hesitate to contact our support team.
        
        Best regards,
        Student Management Team
        
        ---
        This is an automated email. Please do not reply to this message.
        """
        
        # Send email
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[student_email],
            html_message=html_message,
            fail_silently=False,
        )
        
        logger.info(f"Registration email sent successfully to {student_email}")
        return f"Email sent to {student_email}"
        
    except Exception as exc:
        logger.error(f"Failed to send email to {student_email}: {str(exc)}")
        # Retry the task with exponential backoff
        raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))


@shared_task
def send_student_update_email(student_email, student_name, update_type):
    """
    Celery task to send notification email when student information is updated
    """
    try:
        subject = 'Student Information Updated'
        
        html_message = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #2196F3; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; background-color: #f9f9f9; }}
                .footer {{ text-align: center; padding: 20px; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Student Information Updated</h1>
                </div>
                <div class="content">
                    <h2>Hello {student_name},</h2>
                    <p>Your student information has been updated in our system.</p>
                    <p><strong>Update Type:</strong> {update_type}</p>
                    <p>If you did not request this change, please contact our support team immediately.</p>
                    <p>Best regards,<br>Student Management Team</p>
                </div>
                <div class="footer">
                    <p>This is an automated email. Please do not reply to this message.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        plain_message = f"""
        Student Information Updated
        
        Hello {student_name},
        
        Your student information has been updated in our system.
        Update Type: {update_type}
        
        If you did not request this change, please contact our support team immediately.
        
        Best regards,
        Student Management Team
        """
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[student_email],
            html_message=html_message,
            fail_silently=False,
        )
        
        logger.info(f"Update notification email sent to {student_email}")
        return f"Update email sent to {student_email}"
        
    except Exception as exc:
        logger.error(f"Failed to send update email to {student_email}: {str(exc)}")
        raise exc


@shared_task
def send_bulk_email_to_students(student_emails, subject, message):
    """
    Celery task to send bulk emails to multiple students
    """
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=student_emails,
            fail_silently=False,
        )
        
        logger.info(f"Bulk email sent to {len(student_emails)} students")
        return f"Bulk email sent to {len(student_emails)} students"
        
    except Exception as exc:
        logger.error(f"Failed to send bulk email: {str(exc)}")
        raise exc
