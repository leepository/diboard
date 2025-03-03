from app.common.constants import StatusCode
from app.common.exceptions import APIException

## For Article
class NotExistArticle(APIException):
    def __init__(self):
        exception_detail = "Not exist article"
        super().__init__(
            status_code=StatusCode.HTTP_404,
            detail=exception_detail,
            ex=Exception(exception_detail)
        )

## For Comment
class NotExistComment(APIException):
    def __init__(self):
        exception_detail = "Not exist comment"
        super().__init__(
            status_code=StatusCode.HTTP_404,
            detail=exception_detail,
            ex=Exception(exception_detail)
        )

## For Attached file
class NotExistAttachedFile(APIException):
    def __init__(self):
        exception_detail = "Not exist attached file"
        super().__init__(
            status_code=StatusCode.HTTP_404,
            detail=exception_detail,
            ex=Exception(exception_detail)
        )

class NotExistTag(APIException):
    def __init__(self):
        exception_detail = "Not exist tag"
        super().__init__(
            status_code=StatusCode.HTTP_404,
            detail=exception_detail,
            ex=Exception(exception_detail)
        )

class NotUpdateAuth(APIException):
    def __init__(self):
        exception_detail = "Not update authorization"
        super().__init__(
            status_code=StatusCode.HTTP_400,
            detail=exception_detail,
            ex=Exception(exception_detail)
        )

class NotDeleteAuth(APIException):
    def __init__(self):
        exception_detail = "Not delete authorization"
        super().__init__(
            status_code=StatusCode.HTTP_400,
            detail=exception_detail,
            ex=Exception(exception_detail)
        )
