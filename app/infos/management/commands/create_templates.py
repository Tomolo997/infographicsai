from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from infos.models import InfoGraph
from infos.templates import get_all_templates
from account.models import Account
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Create template infographics from predefined templates'
    
    def add_arguments(self, parser):
        parser.add_argument('--user', type=str, help='Username of admin user to own the templates')
    
    def handle(self, *args, **options):
        username = options.get('user', 'admin')
        User = get_user_model()
        
        try:
            user = User.objects.get(username=username)
            account = Account.objects.get(user=user)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User {username} does not exist'))
            return
        except Account.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Account for user {username} does not exist'))
            return
        
        templates = get_all_templates()
        
        for name, template in templates.items():
            try:
                # Create a template infographic for each template
                content = {"canvas_data": template["canvas_data"]}
                
                # Replace placeholders with example content
                self._replace_placeholders(content)
                
                InfoGraph.objects.create(
                    title=f"Template: {name}",
                    content=content,
                    width=template["width"],
                    height=template["height"],
                    account=account,
                    is_template=True
                )
                self.stdout.write(self.style.SUCCESS(f'Created template: {name}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error creating template {name}: {str(e)}'))
                logger.error(f'Error creating template {name}: {str(e)}')
        
        self.stdout.write(self.style.SUCCESS('All templates created successfully'))
    
    def _replace_placeholders(self, content):
        """Replace placeholders with example content"""
        elements = content["canvas_data"]["elements"]
        
        for element in elements:
            if element["type"] == "text" and "content" in element:
                text = element["content"]
                if "{{" in text and "}}" in text:
                    placeholder = text[2:-2]  # Remove {{ and }}
                    
                    # Replace with sample content
                    if "headline" in placeholder or "title" in placeholder:
                        element["content"] = "Sample Headline"
                    elif "point" in placeholder or "message" in placeholder:
                        element["content"] = "This is a sample main point to showcase the template design."
                    elif "supporting_points_formatted" in placeholder:
                        element["content"] = "• First supporting point\n• Second supporting point\n• Third supporting point"
                    elif "key_points_formatted" in placeholder:
                        element["content"] = "• Key point one\n• Key point two\n• Key point three\n• Key point four"
                    elif "hashtags_formatted" in placeholder:
                        element["content"] = "#sample #template #infographic"
                    elif "call_to_action" in placeholder:
                        element["content"] = "Click Here to Learn More"
                    else:
                        element["content"] = "Sample Text"