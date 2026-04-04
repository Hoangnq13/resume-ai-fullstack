from django.db import models

# Create your models here.
class Candidate(models.Model):
    ho_ten = models.CharField(max_length=255, null=True, blank= True)
    email = models.EmailField(null=True, blank=True)
    so_dien_thoai = models.CharField(max_length=20, null=True, blank=True)

    pdf_file = models.FileField(upload_to='resumes/')

    parsed_data = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ho_ten or "Chưa rõ tên"

        