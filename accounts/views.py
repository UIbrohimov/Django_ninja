from django.contrib.auth.models import User
from ninja import Form, NinjaAPI
from ninja.security import HttpBearer, django_auth, APIKeyQuery


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        if token == "supersecret":
            return token


auth = NinjaAPI(auth=django_auth, csrf=True, urls_namespace="accounts")


@auth.get("/bearer", auth=AuthBearer())
def bearer(request):
    return {"Token": request.auth}


@auth.post("/token", auth=None)  # overriding
def get_token(request, username: str = Form(...), password: str = Form(...)):
    if username == "admin" and password == "1":
        return {"token": "supersecret"}


@auth.get("/pets")
def pets(request):
    return f"Authenticated user {request.auth}"


# AVAILABLE AUTH OPTIONS


def ipwitelist(request):
    # just tried out the django user agents package
    # print("Mobile ------------", request.user_agent.is_mobile)
    # print("Pc ------------", request.user_agent.is_pc)
    # print("browser ------------", request.user_agent.browser)
    # print("browser family ------------",
    # request.user_agent.browser.family
    # print("browser version ------------",
    # request.user_agent.browser.version)
    # print("browser version string ------------",
    # request.user_agent.browser.version_string
    # print("os ------------", request.user_agent.os
    # print("os family ------------", request.user_agent.os.family)
    # print("os version ------------", request.user_agent.os.version)
    # print("os version string ------------",
    # request.user_agent.os.version_string)
    # print("os device ------------", request.user_agent.device)
    # print("os device family ------------",
    # request.user_agent.device.family)
    if request.META["REMOTE_ADDR"] == "127.0.0.1":
        return request.META["REMOTE_ADDR"]


@auth.get("/ipwhitelist", auth=ipwitelist)
def ip_whitelist(request):
    return f"Authenticated client, IP = {request.auth}"


class ApiKey(APIKeyQuery):
    param_name = "api_key"

    def authenticate(self, request, key):
        try:
            return User.objects.get(username=key)
        except User.DoesNotExist:
            pass


api_key = ApiKey()


@auth.get("/apikey", auth=api_key)
def apikey(request):
    assert isinstance(request.auth, User)
    return f"Hello {request.auth}"
