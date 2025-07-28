import re

VIEWS_FILE = 'views.py'

# List of missing endpoints from the latest output of check_template_endpoints.py
MISSING_ENDPOINTS = [  # <-- insert missing endpoint names here

]


def endpoint_to_route_and_func(endpoint):
    # Remove 'views.' prefix if it exists
    if endpoint.startswith('views.'):
        endpoint = endpoint[6:]

    # Convert endpoint suffixes (_create, _edit, _delete, etc.) to Flask routes
    if endpoint.endswith('_create'):
        route = f"/{endpoint[:-7].replace('_', 's/')}/create"
        methods = ['GET', 'POST']
    elif endpoint.endswith('_edit'):
        route = f"/{endpoint[:-5].replace('_', 's/')}/<int:id>/edit"
        methods = ['GET', 'POST']
    elif endpoint.endswith('_delete'):
        route = f"/{endpoint[:-7].replace('_', 's/')}/<int:id>/delete"
        methods = ['POST']
    elif endpoint.endswith('_detail'):
        route = f"/{endpoint[:-7].replace('_', 's/')}/<int:id>/detail"
        methods = ['GET']
    elif endpoint.endswith('_list'):
        route = f"/{endpoint[:-5].replace('_', 's/')}/list"
        methods = ['GET']
    else:
        route = f"/{endpoint.replace('_', '/')}"
        methods = ['GET']

    return route, endpoint, methods


def stub_code(route, func_name, methods):
    methods_str = f", methods={methods}" if methods != ['GET'] else ''
    return f"""\n@views_bp.route('{route}'{methods_str})\ndef {func_name}():\n    return 'Not implemented', 501\n"""


def main():
    with open(VIEWS_FILE, encoding='utf-8') as f:
        content = f.read()

    for endpoint in MISSING_ENDPOINTS:
        route, func_name, methods = endpoint_to_route_and_func(endpoint)
        pattern = re.compile(rf'def {func_name}\b')
        if not pattern.search(content):
            content += stub_code(route, func_name, methods)

    with open(VIEWS_FILE, 'w', encoding='utf-8') as f:
        f.write(content)

    print('Added stubs for missing endpoints.')


if __name__ == '__main__':
    main()
