from rest_framework import pagination
from rest_framework.response import Response


class CustomPagination(pagination.PageNumberPagination):
    page_size = 2
    page_size_query_param = 'per_page'
    max_page_size = 10
    page_query_param = 'page'
    def get_paginated_response(self, data):
        page_count = self.page.paginator.count
        page_size = self.page_size

        if page_count % page_size == 0:
            last_page = page_count // page_size
        else:
            last_page = page_count // page_size + 1
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'last_page': last_page,
            },
            'count': page_count,
            'page': self.page.number,
            'per_page': len(self.page),
            'results': data
        })