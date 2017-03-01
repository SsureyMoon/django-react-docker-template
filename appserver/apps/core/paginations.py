from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class BaseResultsSetPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100
    page_size_query_param = 'paginate_by'

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('number', self.page.number),
            ('per_page', self.page.paginator.per_page),
            ('num_pages', self.page.paginator.num_pages),
            ('count', self.page.paginator.count),
            ('next', self.page.number+1 if self.page.number < self.page.paginator.num_pages else None),
            ('previous', self.page.number-1 if self.page.number > 1 else None),
            ('results', data)
        ]))

