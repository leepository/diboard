def except_path_regex_string():
    path_list = [
        '/docs',
        '/favicon/ico',
        '/openapi.json',
        '/health',
        '/membership',
        '/auth'
    ]

    return "|".join(path_list)

EXCEPT_PATH_REGEX = "^({})".format(except_path_regex_string())