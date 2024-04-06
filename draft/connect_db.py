import sqlite3

# 连接到数据库
conn = sqlite3.connect('app.db')
cursor = conn.cursor()

# 获取表列表
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables:")
for table in tables:
    print(table[0])

# 查看表结构
for table in tables:
    table_name = table[0]
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()
    print(f"\nTable {table_name} structure:")
    for column in columns:
        print(column)

# 查看数据
for table in tables:
    table_name = table[0]
    cursor.execute(f"SELECT * FROM {table_name};")
    rows = cursor.fetchall()
    print(f"\nTable {table_name} data:")
    for row in rows:
        print(row)

# 关闭数据库连接
conn.close()
