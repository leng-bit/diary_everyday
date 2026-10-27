# 本文件只负责打开数据库，执行SQL，返回结果！
"""
流程：
    1.选数据库；
    2.连接数据库；
    3.表设计；
    4.建表；
    5.写入；
    6.查询；
    7.修改删除；
    8.参数化查询。
列名中文注解：
    diary_notes:表名字
    id:主键，每行的唯一编号
    today_date:日期，加UNIQUE，每天只能有一行
    tasks:任务，今天要做的事
    events:事件，今天发生的事
    discoveries:发现，今天的收获
    created_at:创建时间
    updated_at:更新时间
"""

import sqlite3

sql = "every_day.db"
connect = {
    "任务":"tasks",
    "事件":"events",
    "发现":"discoveries"
    }
def _raise_v1(connect,column_name):
    if column_name not in connect:
        raise ValueError(f"不支持'{column_name}'，只允许：{'/'.join(connect.keys())}")

def get_conn():
    conn = sqlite3.connect(sql)
    conn.row_factory = sqlite3.Row
    return conn

def cur(conn):
    cur = conn.cursor()
    return cur

def create_table(cur):
    Mesh_grid = cur.execute("""
        CREATE TABLE IF NOT EXISTS
    diary_notes(
        id INTEGER PRIMARY KEY,
        today_date TEXT UNIQUE,
        tasks TEXT,
        events TEXT,
        discoveries TEXT,
        created_at TEXT,
        updated_at TEXT
        )
    """)
    cur.connection.commit()
    return Mesh_grid

def write(cur,today_time,task,event,discover,today):
    sql = """
        INSERT OR REPLACE INTO diary_notes(
            today_date,tasks,events, discoveries,created_at,updated_at
            )
        VALUES (?,?,?,?,'2026-10-02',?)
        """
    cur.execute(sql,(today_time,task,event,discover,today))
    cur.connection.commit()
    return cur.rowcount
# 这里的时间填入根据界面端的的当前时间进行填入

def select_diary_notes(cur,time):
    sql = "SELECT * FROM diary_notes WHERE today_date=?"
    cur.execute(sql,(time,))
    #cur.connection.commit()，只是读取，不需要“提交”
    return cur.fetchone()
# 根据唯一的日期来查询一天记录

def modify(cur,column_name,new_values,modify_time):
    _raise_v1(connect,column_name)
    db_column = connect[column_name]
    sql = f"""
        UPDATE diary_notes
        SET {db_column}=?
        WHERE today_date=?
        """
    cur.execute(sql,(new_values,modify_time))
    cur.connection.commit()
    return cur.rowcount

def delete(cur,time):
    sql = """
        DELETE FROM diary_notes WHERE today_date=?
        """
    cur.execute(sql,(time,))
    cur.connection.commit()
    return cur.rowcount
