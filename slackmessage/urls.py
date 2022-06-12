from django.urls import path

from slackmessage.views import Events, Messages, FilesOperation, Health

app_name = 'slackmessage'

urlpatterns = [
    path('health/', Health.as_view(), name='health'),
    path('event/', Events.as_view(), name='event'),
    path('prev_msgs/', Messages.as_view(), name='message'),
    path('get_file/', FilesOperation.as_view(), name='files'),
]