# resume_builder/views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Resume, Experience
from .forms import ResumeForm, ExperienceFormSet
from fpdf import FPDF
import os


def resume_create(request):
    if request.method == 'POST':
        form = ResumeForm(request.POST)
        formset = ExperienceFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            resume = form.save()
            formset.instance = resume
            formset.save()

            # Generate PDF
            pdf_path = generate_resume_pdf(resume)

            # Serve PDF as a download
            with open(pdf_path, 'rb') as f:
                response = HttpResponse(f.read(),
                                        content_type='application/pdf')
                response[
                    'Content-Disposition'] = f'attachment; filename="{resume.name}_resume.pdf"'

                # Clean up the file after sending it
                os.remove(pdf_path)

                return response

    else:
        form = ResumeForm()
        formset = ExperienceFormSet()

    return render(request, 'resume_builder/index.html', {
        'form': form,
        'formset': formset,
    })


def generate_resume_pdf(resume):
    # Create PDF with FPDF
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=False, margin=0)
    pdf.add_page()

    # Set font properties
    pdf.set_font(family="Helvetica", style="B", size=14)
    pdf.set_text_color(80, 80, 80)

    # Left column (width: 100mm)
    x_left = 10
    y_current = 15

    # Professional title
    pdf.set_xy(x_left, y_current)
    pdf.cell(w=100, h=10, txt=resume.professional_title.upper(), ln=1)
    y_current += 15

    # Name
    pdf.set_xy(x_left, y_current)
    pdf.cell(w=100, h=10, txt=resume.name, ln=1)
    y_current += 10

    # Email
    pdf.set_font(family="Helvetica", size=10)
    pdf.set_xy(x_left, y_current)
    pdf.cell(w=100, h=10, txt=resume.email, ln=1)
    y_current += 10

    # Portfolio links
    if resume.portfolio_link_1:
        pdf.set_xy(x_left, y_current)
        pdf.cell(w=100, h=10, txt=f"Portfolio: {resume.portfolio_link_1}",
                 ln=1)
        y_current += 6

    if resume.portfolio_link_2:
        pdf.set_xy(x_left, y_current)
        pdf.cell(w=100, h=10, txt=f"Portfolio 2: {resume.portfolio_link_2}",
                 ln=1)
        y_current += 6

    if resume.portfolio_link_3:
        pdf.set_xy(x_left, y_current)
        pdf.cell(w=100, h=10, txt=f"Portfolio 3: {resume.portfolio_link_3}",
                 ln=1)
        y_current += 6

    y_current += 5

    # Professional Profile
    pdf.set_font(family="Helvetica", style="B", size=12)
    pdf.set_xy(x_left, y_current)
    pdf.cell(w=100, h=10, txt="PROFESSIONAL PROFILE", ln=1)
    y_current += 10

    pdf.set_font(family="Helvetica", size=10)

    # Split text into multiple lines
    profile_lines = resume.professional_profile.split('\n')
    for line in profile_lines:
        pdf.set_xy(x_left, y_current)
        pdf.multi_cell(w=90, h=5, txt=line)
        y_current += pdf.get_y() - y_current + 2

    y_current += 5

    # Technical Skills
    pdf.set_font(family="Helvetica", style="B", size=12)
    pdf.set_xy(x_left, y_current)
    pdf.cell(w=100, h=10, txt=resume.technical_skills_title, ln=1)
    y_current += 10

    pdf.set_font(family="Helvetica", size=10)
    skills_lines = resume.skills.split('\n')
    for skill in skills_lines:
        pdf.set_xy(x_left, y_current)
        pdf.cell(w=90, h=5, txt=f"• {skill}")
        y_current += 6

    y_current += 5

    # Professional Experience
    pdf.set_font(family="Helvetica", style="B", size=12)
    pdf.set_xy(x_left, y_current)
    pdf.cell(w=100, h=10, txt=resume.experience_title, ln=1)
    y_current += 10

    # Experience entries
    pdf.set_font(family="Helvetica", style="B", size=10)
    for exp in resume.experiences.all():
        pdf.set_xy(x_left, y_current)
        pdf.cell(w=90, h=5, txt=f"{exp.title} | {exp.company}")
        y_current += 6

        pdf.set_font(family="Helvetica", style="I", size=10)
        pdf.set_xy(x_left, y_current)
        pdf.cell(w=90, h=5, txt=exp.year)
        y_current += 6

        pdf.set_font(family="Helvetica", size=10)
        exp_lines = exp.description.split('\n')
        for line in exp_lines:
            pdf.set_xy(x_left, y_current)
            pdf.multi_cell(w=90, h=5, txt=line)
            y_current += pdf.get_y() - y_current + 2

        y_current += 5

    # Right column (width: 100mm)
    x_right = 110
    y_right = 15

    # Education
    pdf.set_font(family="Helvetica", style="B", size=12)
    pdf.set_xy(x_right, y_right)
    pdf.cell(w=100, h=10, txt=resume.education_title, ln=1)
    y_right += 10

    pdf.set_font(family="Helvetica", size=10)
    education_lines = resume.education.split('\n')
    for edu in education_lines:
        pdf.set_xy(x_right, y_right)
        pdf.multi_cell(w=90, h=5, txt=edu)
        y_right += pdf.get_y() - y_right + 2

    y_right += 10

    # Why Hire Me
    pdf.set_font(family="Helvetica", style="B", size=12)
    pdf.set_xy(x_right, y_right)
    pdf.cell(w=100, h=10, txt=resume.why_hire_me_title, ln=1)
    y_right += 10

    pdf.set_font(family="Helvetica", size=10)
    hire_me_lines = resume.why_hire_me.split('\n')
    for line in hire_me_lines:
        pdf.set_xy(x_right, y_right)
        pdf.multi_cell(w=90, h=5, txt=line)
        y_right += pdf.get_y() - y_right + 2

    y_right += 10

    # Call to Action
    if resume.cta:
        pdf.set_font(family="Helvetica", style="B", size=11)
        pdf.set_xy(x_right, y_right)
        pdf.cell(w=90, h=5, txt=resume.cta)
        y_right += 8

    # Social Links
    if resume.socials:
        pdf.set_font(family="Helvetica", size=10)
        social_lines = resume.socials.split('\n')
        for social in social_lines:
            pdf.set_xy(x_right, y_right)
            pdf.cell(w=90, h=5, txt=social)
            y_right += 6

    # Save the PDF
    output_path = f"resume_{resume.id}.pdf"
    pdf.output(output_path)
    return output_path
