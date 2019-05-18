from django.http import Http404
from django.core.paginator import Paginator

# Пагинатор, постраничное разбиение больших перечней
def pagin(request, qs, lim, url): 
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        raise Http404
    paginator = Paginator(qs, lim)
    paginator.baseurl = url
    try:
        page = paginator.page(page)
    except:
        page = paginator.page(paginator.num_pages)
    return page, paginator