# 这是界面层的命令行端呈现
print("每周日负责周总结，如是周日当天所作，需标注（当天）")

from datetime import datetime,date
import db_v2

conn_v1 = db_v2.get_conn() #建连接
cur = db_v2.cur(conn_v1)   #拿游标

db_v2.create_table(cur)    #验证表是否存在
print("正常为(写入/删除)为1行！","时间输入格式要求：YYYY-MM-DD",sep="\n")

while True:
    stop = input("是否写入/查询/修改/删除，还是停止：")
    if stop == "停止":
        break
    elif stop =="写入":
        today_time = date.today()
        task = input("今日任务：")
        event = input("今日事件：")
        discover = input("今日发现：")
        today = datetime.now().strftime("%Y-%m-%d %H:%M")
        row = db_v2.write(cur,today_time,task,event,discover,today)
        print("已写入",f"写入{row}行",sep="\n")

    elif stop == "查询":
        str_time = input("请输入你要查询的时间（YYYY-MM-DD）：")
        row = db_v2.select_diary_notes(cur,str_time)
        if row in None:
            print("没有记录")
        else:
            print("查询到的信息如下：")
            for k,v in dict(row).items():
                print(f"{k}:{v}")

    elif stop == "修改":
        while True:
            connect = input("是否开始/继续，还是停止：")
            if connect == "开始" or connect == "继续":
                column_name = input("你需要修改的列名是（填写 任务/事件/发现 这三个文字）：")
                new_values = input("修改内容：")
                modify_time = datetime.now().strftime("%Y-%m-%d")
                row = db_v2.modify(cur,column_name,new_values,modify_time)
                print("已修改",f"修改{row}行",sep="\n")
            else:
                break
    elif stop == "删除":
        str_time = input("你要删除的时间为（YYYY-MM-DD）：")
        row = db_v2.delete(cur,str_time)
        print("已删除",f"删除{row}行",sep="\n")

    else:
        print("请填入正确信息！")

#查询和删除只提供字符串即可      

conn_v1.close()
