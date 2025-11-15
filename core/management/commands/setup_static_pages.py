"""
Django management command to create default static pages (About Us and Content Policies).
Usage: python manage.py setup_static_pages
"""
from django.core.management.base import BaseCommand
from core.models import StaticPage


class Command(BaseCommand):
    help = 'Creates default static pages (About Us and Content Policies) if they do not exist'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Setting up static pages...'))

        # About Us Page
        about_us, created = StaticPage.objects.get_or_create(
            slug='about-us',
            defaults={
                'title': 'About Us',
                'content': '''Welcome to Asanbay Society for Social Justice

We are a dedicated organization committed to promoting social justice, equality, and positive change in our community. Our mission is to address systemic inequalities and work towards creating a more just and equitable society for all.

Our Vision

We envision a world where every individual has equal access to opportunities, resources, and rights, regardless of their background, identity, or circumstances.

Our Mission

Through advocacy, education, and community engagement, we strive to:
- Raise awareness about social justice issues
- Support marginalized communities
- Promote inclusive policies and practices
- Foster dialogue and understanding
- Create lasting positive change

Our Values

- Justice: We believe in fairness and equity for all
- Integrity: We act with honesty and transparency
- Inclusion: We welcome and value diverse perspectives
- Empowerment: We support individuals and communities in achieving their goals
- Collaboration: We work together to create meaningful impact

Get Involved

We welcome individuals and organizations who share our commitment to social justice. Together, we can make a difference and create a better future for all.

For more information or to get involved, please contact us through our website or social media channels.''',
                'is_active': True,
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ Created "About Us" page'))
        else:
            self.stdout.write(self.style.WARNING(f'⚠ "About Us" page already exists (slug: about-us)'))

        # Content Policies Page
        content_policies, created = StaticPage.objects.get_or_create(
            slug='content-policies',
            defaults={
                'title': 'Content Policies',
                'content': '''Content Policies and Guidelines

Welcome to our content policies page. This document outlines the guidelines and standards we follow for content published on our platform.

Content Standards

All content published on our platform must adhere to the following standards:

1. Accuracy and Truthfulness
   - All information must be factually accurate
   - Sources should be cited when appropriate
   - Claims should be verifiable

2. Respect and Inclusivity
   - Content must respect all individuals and communities
   - Language should be inclusive and non-discriminatory
   - Diverse perspectives are welcomed and valued

3. Relevance and Purpose
   - Content should align with our mission of promoting social justice
   - Articles should provide value to our community
   - Topics should be relevant to our organizational goals

4. Professionalism
   - Content should maintain a professional tone
   - Constructive criticism is encouraged; personal attacks are not
   - Disagreements should be expressed respectfully

Editorial Guidelines

- All content is reviewed before publication
- We reserve the right to edit content for clarity, accuracy, and adherence to our policies
- Authors are responsible for the accuracy of their submissions
- Plagiarism is strictly prohibited

Content Moderation

We are committed to maintaining a respectful and constructive environment. Content that:
- Contains hate speech or discriminatory language
- Promotes violence or illegal activities
- Violates privacy or confidentiality
- Is spam or irrelevant
- Infringes on intellectual property rights

...may be removed or not published.

Intellectual Property

- Authors retain ownership of their original content
- By submitting content, authors grant us the right to publish and distribute it
- Proper attribution will always be given to content creators
- We respect the intellectual property rights of others

Privacy and Confidentiality

- We respect the privacy of individuals and communities
- Personal information will not be published without consent
- Confidential information will be protected
- We follow applicable privacy laws and regulations

Updates to Policies

These policies may be updated periodically. We encourage you to review this page regularly to stay informed about our content guidelines.

Contact

If you have questions about our content policies or wish to report a concern, please contact us through our website.

Last Updated: This policy is reviewed and updated regularly to reflect our evolving standards and practices.''',
                'is_active': True,
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ Created "Content Policies" page'))
        else:
            self.stdout.write(self.style.WARNING(f'⚠ "Content Policies" page already exists (slug: content-policies)'))

        self.stdout.write(self.style.SUCCESS('\n✓ Static pages setup complete!'))
        self.stdout.write(self.style.SUCCESS('\nYou can now:'))
        self.stdout.write(self.style.SUCCESS('- View pages at /page/about-us/ and /page/content-policies/'))
        self.stdout.write(self.style.SUCCESS('- Edit pages in Django admin at /admin/core/staticpage/'))
        self.stdout.write(self.style.SUCCESS('- Pages will appear in the footer automatically'))

