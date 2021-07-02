import asyncio
from io import StringIO
from typing import List

import yaml
from django.utils.encoding import force_str
from django.utils.xmlutils import SimplerXMLGenerator
from ninja import NinjaAPI, Router, Schema
from ninja.parser import Parser
from ninja.renderers import BaseRenderer

from .models import Blog


class XMLRenderer(BaseRenderer):
    media_type = "text/xml"

    def render(self, request, data, *, response_status):
        stream = StringIO()
        xml = SimplerXMLGenerator(stream, "utf-8")
        xml.startDocument()
        xml.startElement("data", {})
        self._to_xml(xml, data)
        xml.endElement("data")
        xml.endDocument()
        return stream.getvalue()

    def _to_xml(self, xml, data):
        if isinstance(data, (list, tuple)):
            for item in data:
                xml.startElement("item", {})
                self._to_xml(xml, item)
                xml.endElement("item")

        elif isinstance(data, dict):
            for key, value in data.items():
                xml.startElement(key, {})
                self._to_xml(xml, value)
                xml.endElement(key)

        elif data is None:
            # Don't output any value
            pass

        else:
            xml.characters(force_str(data))


api = NinjaAPI(renderer=XMLRenderer())


class MyYamlParser(Parser):
    def parse_body(self, request):
        return yaml.safe_load(request.body)


router = Router(tags=["Blog"])
api = NinjaAPI(parser=MyYamlParser(), urls_namespace="blog",
               renderer=XMLRenderer())


class Payload(Schema):
    ints: List[int]
    string: str
    f: float


@api.post("/yaml")
def operation(request, payload: Payload):
    return payload.dict()


@api.get("/say-after")
async def say_after(request, delay: int, word: str):
    await asyncio.sleep(delay)
    return {"saying": word}


@router.get("/")
def list_blogs(request):
    return [{"id": e.id, "title": e.title} for e in Blog.objects.all()]


@router.get("/{event_id}")
def blog_details(request, event_id: int):
    event = Blog.objects.get(id=event_id)
    return {"title": event.title, "details": event.details}
