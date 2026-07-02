"""User lookup -- FIXED (parameterized query).

The username is passed as a bound parameter, so it is always treated as data
and can never alter the structure of the SQL statement.
"""


def find_users(conn, name):
    cur = conn.cursor()
    cur.execute("SELECT username, role FROM users WHERE username = ?", (name,))
    return cur.fetchall()
