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