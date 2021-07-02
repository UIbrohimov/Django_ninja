from ninja import Router

from accounts.views import AuthBearer

from .models import New
from .schema import NewsSchema

router = Router(tags=["News"], auth=AuthBearer())


# amana bu funcsiya swaggerda korinmaydida,
# sababi include_in_schema False da ))
@router.get(
    "/", operation_id="vaabsheboshqanarsa",
    deprecated=True,
    include_in_schema=False
)
def list_of_news(request):
    return [{"id": e.id, "title": e.title} for e in New.objects.all()]


@router.get("/{event_id}")
def new_details(request, event_id: int):
    """
    Biror yangilikni batafsil ko'rish uchun, iltimos,
    quyidagi malumotlarni kiritishingiz zarur:<br>
        <ul>
            <li>-id</li>
        </ul>
    va pastdagi **Execute** yani *(amalga oshirish)* tugmasini bosing

    <h3>Shu bilan sizlarga yetkazmoqchi bo'lgan malumotlarimiz
    nihoyasiga yetdi</h3>
    """
    event = New.objects.get(id=event_id)
    return {"title": event.title, "details": event.details}


create_new_description = """
    Bu funksiya yangilik yaratish uchun zor narsada,
    blyat 8 - marta tushuntirishim ):-(
    """


@router.post(
    "/create/",
    response=NewsSchema,
    description=create_new_description
    )
def create_new(request, title: str, details: str):
    new = New.objects.create(title=title, details=details)
    return new
