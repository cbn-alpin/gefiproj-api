def validate_post(project):
    print(project)
    errors = []

    try:
        project['id_u'] = int(project['id_u'])
    except ValueError:
        errors.append({
            'code': 'VALIDATION_ERROR',
            'field': 'id_u',
            'message': 'id_u must be a number',
        })

    if len(project['code_p']) > 4:
        errors.append({
            'code': 'VALIDATION_ERROR',
            'field': 'code_p',
            'message': 'code_p must be at most 4 char',
        })

    return errors
