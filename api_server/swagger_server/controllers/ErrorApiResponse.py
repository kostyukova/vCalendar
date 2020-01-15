from swagger_server.models.api_response import ApiResponse


def AuthError(type='user'):
    return ApiResponse(code=1000, type=type,
                       message='Either username or password is incorrect')


def NoRoleGrantedError(role: str, type='user'):
    return ApiResponse(code=1001, type=type,
                       message='The role \'{}\' must be granted'.format(role))


def TokenInvalidError(type='user'):
    return ApiResponse(code=1002, type=type,
                       message='The empty or invalid authorization token is supplied')


def TokenExpiredError(type='user'):
    return ApiResponse(code=1003, type=type,
                       message='Authorization token has been expired')
