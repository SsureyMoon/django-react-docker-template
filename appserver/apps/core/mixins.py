import operator
from functools import reduce

from django.db.models import Q


class DefaultContextMixin(object):
    def get_context_data(self, **kwargs):
        context = super(DefaultContextMixin, self).get_context_data(**kwargs)
        context.update(self.default_context)
        return context


class PaginateMixin(object):
    def get_paginate_by(self, queryset):
        """
        Paginate by specified value in querystring, or use default class property value.
        """
        return self.request.GET.get('paginate_by', self.paginate_by)


class QuerysetWithCountMixin(object):
    def get_queryset(self):
        return self.model.objects.fetch_with_counts()


class NonEmptyFormsetMixin(object):
    def __init__(self, *args, **kwargs):
        super(NonEmptyFormsetMixin, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False


class SearchByMixin(object):
    def search_by(self, query_only=False, **kwargs):
        _total_query = []
        for key in kwargs:
            if key in self.ALLOWED_SEARCH_FIELDS:
                fields = self.ALLOWED_SEARCH_FIELDS[key]
                _queries = []
                if not fields:
                    _query = {}
                    _query[key] = kwargs[key]
                    _queries.append(Q(**_query))
                else:
                    for field in fields:
                        _query = {}
                        _query[field] = kwargs[key]
                        _queries.append(Q(**_query))
                _total_query.append(reduce(operator.or_, _queries))

        if query_only:
            if _total_query:
                return reduce(operator.and_, _total_query)
            return None

        if not _total_query:
            return self.all()
        return self.filter(reduce(operator.and_, _total_query))
