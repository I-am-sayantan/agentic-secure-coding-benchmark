"""User lookup -- VULNERABLE (CWE-89 SQL Injection).

The query is assembled with an f-string, so a crafted ``name`` changes the
meaning of the SQL and can return rows the caller should never see.
"""


def find_users(conn, name):
    cur = conn.cursor()
    cur.execute(f"SELECT username, role FROM users WHERE username = '{name}'")
    return cur.fetchall()
