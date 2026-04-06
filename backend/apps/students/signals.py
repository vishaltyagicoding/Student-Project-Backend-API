from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import Student, CollegeBranch, CollegeCourse
from .tasks import send_student_registration_email, send_student_update_email
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Student)
def student_created(sender, instance, created, **kwargs):
    """
    Signal handler for when a student is created or updated
    Sends email notification to the student
    """
    if created:
        logger.info(f"New student created: {instance.student_id} - {instance.email}")
        
        # Send registration email asynchronously using Celery
        college_name = instance.college.name if instance.college else "N/A"
        student_name = f"{instance.first_name} {instance.last_name}"
        
        try:
            send_student_registration_email.delay(
                student_id=instance.student_id,
                student_email=instance.email,
                student_name=student_name,
                college_name=college_name
            )
            logger.info(f"Registration email task queued for {instance.email}")
        except Exception as e:
            logger.error(f"Failed to queue registration email for {instance.email}: {str(e)}")
    else:
        logger.info(f"Student updated: {instance.student_id} - {instance.email}")
        
        # Send update notification email
        student_name = f"{instance.first_name} {instance.last_name}"
        
        try:
            send_student_update_email.delay(
                student_email=instance.email,
                student_name=student_name,
                update_type="Profile Information"
            )
            logger.info(f"Update email task queued for {instance.email}")
        except Exception as e:
            logger.error(f"Failed to queue update email for {instance.email}: {str(e)}")


@receiver(pre_delete, sender=Student)
def student_deleted(sender, instance, **kwargs):
    """
    Signal handler for when a student is deleted
    """
    logger.info(f"Student deleted: {instance.student_id} - {instance.email}")


@receiver(post_save, sender=CollegeBranch)
def college_branch_created(sender, instance, created, **kwargs):
    """
    Signal handler for college-branch relationship
    """
    if created:
        logger.info(f"College-Branch relationship created: {instance.college.name} - {instance.branch.name}")


@receiver(post_save, sender=CollegeCourse)
def college_course_created(sender, instance, created, **kwargs):
    """
    Signal handler for college-course relationship
    """
    if created:
        logger.info(f"College-Course relationship created: {instance.college.name} - {instance.course.name}")
