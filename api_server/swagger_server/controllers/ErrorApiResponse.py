from swagger_server.models.api_response import ApiResponse


def InternalServerError(ex: Exception, type='user'):
    return ApiResponse(code=1000, type=type,
                       message='Internal server error: {}'.format(ex))


def AuthError(type='user'):
    return ApiResponse(code=1001, type=type,
                       message='Either username or password is incorrect')


def NoRoleGrantedError(role: str, type='user'):
    return ApiResponse(code=1002, type=type,
                       message='The role \'{}\' must be granted'.format(role))


def TokenInvalidError(type='user'):
    return ApiResponse(code=1003, type=type,
                       message='The empty or invalid authorization token is supplied')


def TokenExpiredError(type='user'):
    return ApiResponse(code=1004, type=type,
                       message='Authorization token has been expired')


def UsernameExistError(username: str, type='user'):
    return ApiResponse(code=1005, type=type,
                       message='User with username \'{}\' already exists'.format(username))


def UseremailExistError(email: str, type='user'):
    return ApiResponse(code=1006, type=type,
                       message='User with email \'{}\' already exists'.format(email))


def NoUsernameError(type='user'):
    return ApiResponse(code=1007, type=type, message='No username supplied')


def UserNotFoundError(type='user'):
    return ApiResponse(code=1008, type=type, message='User not found')


def EmployeeEmailExistError(email: str, type='employee'):
    return ApiResponse(code=1009, type=type,
                       message='Employee with email \'{}\' already exists'.format(email))


def EmployeeNotFoundError(id: int = None, email: str = None, type='employee'):
    return ApiResponse(code=1010, type=type, message='Employee not found, id: \'{}\', email: \'{}\''.format(id, email))
