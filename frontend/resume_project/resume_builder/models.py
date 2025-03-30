# resume_builder/models.py
from django.db import models


class Resume(models.Model):
    # Left column
    professional_title = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    portfolio_link_1 = models.URLField(blank=True)
    portfolio_link_2 = models.URLField(blank=True, null=True)
    portfolio_link_3 = models.URLField(blank=True, null=True)
    professional_profile = models.TextField()
    technical_skills_title = models.CharField(max_length=100,
                                              default="TECHNICAL SKILLS")
    skills = models.TextField(help_text="Enter each skill on a new line")

    # Professional Experience
    experience_title = models.CharField(max_length=100,
                                        default="PROFESSIONAL EXPERIENCE")

    # Right column
    education_title = models.CharField(max_length=100, default="EDUCATION")
    education = models.TextField(
        help_text="Enter each education item on a new line")
    why_hire_me_title = models.CharField(max_length=100, default="WHY HIRE ME")
    why_hire_me = models.TextField()
    cta = models.CharField(max_length=200, blank=True,
                           help_text="Call to action")
    socials = models.TextField(blank=True,
                               help_text="Enter social media links, one per line")

    def __str__(self):
        return f"{self.name}'s Resume"


class Experience(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE,
                               related_name='experiences')
    title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    year = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return f"{self.title} at {self.company}"