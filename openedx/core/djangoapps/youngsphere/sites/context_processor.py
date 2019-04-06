import stream
from django.conf import settings
client = stream.connect(settings.STREAM_API_KEY, settings.STREAM_API_SECRET)

def socialcontext(request):
    user = request.user
    user_token = client.create_user_token(user.username)
    print(user_token)
    context = {
        'user_token': user_token,
        'appId': settings.STREAM_APP_ID,
        'apiKey': settings.STREAM_API_KEY,
        'user': request.user
    }
    return context
