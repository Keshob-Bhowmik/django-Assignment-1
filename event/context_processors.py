def user_roles(request):
    if not request.user.is_authenticated:
        return {'is_admin': False, 'is_organizer': False, 'is_particepant' : False}

    groups = set(request.user.groups.values_list('name', flat=True))
    return {
        'is_admin': 'Admin' in groups,
        'is_organizer': 'Organizer' in groups,
        'is_particepant' : 'Particepant' in groups
    }
