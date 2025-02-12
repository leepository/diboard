from app.common.errors import CustomErrors

class AuthErrors(CustomErrors):
    NotExistUser = ("NotExistUser", 404, "User is not exist")
    InvalidPassword = ("InvalidPassword", 400, "Invalid password")
    InvalidUsername = ("InvalidUsername", 400, "Invalid username")
