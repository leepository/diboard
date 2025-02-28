class Transactional:

    def __init__(self, function, session):
        self.function = function
        self.session = session

    def __call__(self, *args, **kwargs):
        try:
            self.session.begin()
            result = self.function()
            self.session.commit()
        except Exception as ex:
            self.session.rollback()
            raise ex

        return result
