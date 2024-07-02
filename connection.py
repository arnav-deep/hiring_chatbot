import pymysql.cursors

# Database connection
connection = pymysql.connect(
    host="35.224.61.48",
    user="trial_user",
    password="trial_user_12345#",
    database="MERCOR_TRIAL_SCHEMA",
    cursorclass=pymysql.cursors.DictCursor,
)
