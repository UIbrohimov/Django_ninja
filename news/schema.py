from ninja.orm import create_schema

from .models import New

NewsSchema = create_schema(New)
