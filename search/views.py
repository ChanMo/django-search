import logging
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.conf import settings
from django.template import loader
from taggit.models import TaggedItem
from django.contrib import admin

logger = logging.getLogger(__name__)

DEFAULT_TEMPLATE = 'search/default.html'

@staff_member_required
def index_view(request):
    context = {
        **admin.site.each_context(request),
        'title': _('Search')
    }
    logger.debug(context)
    key = request.GET.get('search', None)
    if 'SEARCH_TEMPLATE' in settings.__dict__.keys():
        template = loader.select_template((settings.SEARCH_TEMPLATE, DEFAULT_TEMPLATE))
    else:
        template = loader.get_template(DEFAULT_TEMPLATE)
    if key:
        res = TaggedItem.objects.filter(tag__name__contains=key)
        paginator = Paginator(res, 12)
        context = {
            **context,
            'key': key,
            'results': paginator.get_page(request.GET.get('page'))
        }
    return HttpResponse(template.render(context, request))
