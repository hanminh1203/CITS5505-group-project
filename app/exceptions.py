class SkillswapException(Exception):
    def __init__(self, message, code):
        super().__init__(message, code)
        self.code = code
        self.message = message

    def get_addition_info(self):
        return {}


class ValidationException(SkillswapException):
    def __init__(self, errors, message="Validation failed."):
        super().__init__(message, 400)
        self.errors = errors

    def get_addition_info(self):
        return self.errors


class NotAuthorizedActionException(SkillswapException):
    def __init__(self,
                 message="You are not authorized to perform this action."):
        super().__init__(message, 403)


class InvalidActionException(SkillswapException):
    def __init__(self,
                 message="This action is invalid in the current context."):
        super().__init__(message, 400)


class NotFoundException(SkillswapException):
    def __init__(self, message="The requested resource was not found."):
        super().__init__(message, 404)
