from flask import g


def _ensure_admin():
    jwt_user = getattr(g, 'current_user', None)

    if jwt_user:
        if jwt_user.get('role') != 'admin':
            raise PermissionError('Admin role required (JWT)')
        return


    if getattr(jwt_user, 'role', None) != 'admin':
        raise PermissionError('Admin role required')


def _ensure_student():
    jwt_user = getattr(g, 'current_user', None)

    if jwt_user:
        if jwt_user.get('role') != 'student':
            raise PermissionError(
                'Only students can view their progress (JWT)'
            )
        return

    if getattr(jwt_user, 'role', None) != 'student':
        raise PermissionError(
            'Only students can view their progress'
        )


def _ensure_instructor():
    jwt_user = getattr(g, 'current_user', None)

    print(jwt_user.get('sub'))

    if jwt_user:
        if jwt_user.get('role') != 'instructor':
            raise PermissionError(
                'Only instructors can perform this action (JWT)'
            )
        return


    # if jwt_user["role"] != 'instructor':
    #     raise PermissionError(
    #         'Only instructors can perform this action'
    #     )


def get_current_user_id():
    jwt_user = getattr(g, 'current_user', None)
    print(int(jwt_user.get('sub')))

    if not jwt_user:
        print("reached here")
        raise PermissionError('Authentication required')

    return int(jwt_user.get('sub'))
