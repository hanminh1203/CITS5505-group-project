class SkillswapException(Exception):
    def __init__(self, message, code):
        super().__init__(message, code)
        self.code = code
        self.message = message

    def get_addition_info(self):
        return {}


class SkillswapExpectedException(SkillswapException):
    pass


class ValidationException(SkillswapExpectedException):
    def __init__(self, errors, message="Validation failed."):
        super().__init__(message, 400)
        self.errors = errors

    def get_addition_info(self):
        return self.errors


class InvalidCredientialException(SkillswapExpectedException):
    def __init__(self, message="Invalid Crediential"):
        super().__init__(message, 401)


class IntegrityException(SkillswapException):
    def __init__(self, message="Unable to delete due to integrity exception"):
        super().__init__(message, 409)


class NotAuthorizedActionException(SkillswapException):
    def __init__(self,
                 message="You are not authorized to perform this action."):
        super().__init__(message, 403)


class IllegalArgumentException(SkillswapException):
    def __init__(self, message):
        super().__init__(message, 400)


class InvalidActionException(SkillswapException):
    def __init__(self,
                 message="This action is invalid in the current context."):
        super().__init__(message, 400)


class NotFoundException(SkillswapException):
    def __init__(self, message="The requested resource was not found."):
        super().__init__(message, 404)
