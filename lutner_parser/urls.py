from django.conf.urls import url
from lutner_parser.views import *

urlpatterns = [
    url(r'^balalaiker/(?P<pk>\d+)/$', one_product, name='one_product'),
    url(r'^balalaiker/$', balalaiker_catalog, name='balalaiker_catalog'),
    url(r'^$', redir, name='redir'),
    


    ]
