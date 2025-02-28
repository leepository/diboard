from contextlib import contextmanager
from sqlalchemy.orm import Session
from typing import Any, Callable, TypeVar

T = TypeVar('T')

class TransactionManager:
    def __init__(self, session: Session):
        self.session = session

    @contextmanager
    def transaction(self):
        """ 트랜잭션 컨텍스트 매니저 """
        try:
            yield self.session
            self.session.commit()

        except Exception as ex:
            self.session.rollback()
            raise ex
