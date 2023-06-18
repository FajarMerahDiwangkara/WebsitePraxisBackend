config_data = {
    "databasewebsitepraxis_host" : "localhost",
    "databasewebsitepraxis_port" : "5432",
    "databasewebsitepraxis_schema" : "public",
    "user_login_session_timeout_seconds" : 3600,
    "timestamp_format" : "%Y-%m-%d %H:%M:%S",
    "account_name_max_length" : 320,
    # https://stackoverflow.com/questions/9289451/regular-expression-for-alphabets-with-spaces
    "account_name_regex" : "[a-zA-Z][a-zA-Z ]+",
    "account_password_max_length" : 320,
    # email max length is 320, search on internet
    "account_email_max_length" : 320,
    "account_address_max_length" : 1000,
    "account_education_max_length" : 1000,
    "account_phone_number_regex" : "^[+0-9]+$",
    "account_phone_number_max_length" : 15
}