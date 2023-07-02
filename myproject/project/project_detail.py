import sqlite3

conn_pd = sqlite3.connect('project_details.db')
cur_pd= conn_pd.cursor()
cur_pd.execute('''
    CREATE TABLE IF NOT EXISTS projects (
        project_name TEXT,
        description TEXT,
        start_date TEXT,
        end_date TEXT,
        team_member TEXT,
        resource BYTEA
    )
''')

conn_pd.commit()
conn_pd.close()

conn_user = sqlite3.connect('user.db')
cur_user = conn_user.cursor()
cur_user.execute('''
    CREATE TABLE IF NOT EXISTS user(
        username TEXT,
        password TEXT,
        project TEXT
    )
''')
conn_user.commit()
conn_user.close()


