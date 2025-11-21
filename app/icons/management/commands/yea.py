# File: yourapp/management/commands/upload_svgs_to_r2.py

import os
import uuid
import xml.etree.ElementTree as ET
from django.core.management.base import BaseCommand
from django.conf import settings
from file_upload.client import R2Client
from icons.models import VectorIcon, SVGIcon,FlatIcon
from io import BytesIO

class Command(BaseCommand):

    def handle(self, *args, **options):
        # Get full path to the directory
        FlatIcon2 = FlatIcon.objects.all()
        print([vector.title for vector in FlatIcon2])
       