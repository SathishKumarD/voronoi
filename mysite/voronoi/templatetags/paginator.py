from django import template
register = template.Library()

def paginator(context,objname, adjacent_pages=2):
	objects = context[objname]
	startPage = max(objects.number - adjacent_pages, 1)
	if startPage <= 3: startPage = 1
	endPage = objects.number + adjacent_pages + 1
	if endPage >= objects.paginator.num_pages - 1: endPage = objects.paginator.num_pages + 1
	page_numbers = [n for n in range(startPage, endPage) \
		if n > 0 and n <= objects.paginator.num_pages]

	return {
	'page': objects.number,
	'pages': objects.paginator.num_pages,
	'page_numbers': page_numbers,
	'next': objects.next_page_number,
	'previous': objects.previous_page_number,
	'has_next': objects.has_next,
	'has_previous': objects.has_previous,
	'show_first': 1 not in page_numbers,
	'show_last': objects.paginator.num_pages not in page_numbers,
	'context':context
	}
register.inclusion_tag('voronoi/paginator.html', takes_context=True)(paginator)