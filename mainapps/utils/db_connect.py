import pymysql


def db_connect():
    conn = pymysql.Connect(host='localhost', user='root', password="123456",
                           database='XinJuKe', cursorclass=pymysql.cursors.DictCursor)

    return conn

def db_excute(sql):
    conn = db_connect()
    cur = conn.cursor()
    try:

        cur.execute(sql)
        conn.commit()
        return 1
    except:
        return 0
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def db_query(sql):
    conn = db_connect()
    cur = conn.cursor()
    try:
        cur.execute(sql)
        return cur.fetchall()
    except:
        return []
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def convert_objects(sql):
    result = db_query(sql)
    class Dict(dict):
        __setattr__ = dict.__setitem__
        __getattr__ = dict.__getitem__
    convert_result = []
    for res in result:
        d = Dict()
        for key, value in res.items():
            d[key] = value
        convert_result.append(d)
    # print(convert_result)
    return convert_result


if __name__ == '__main__':
    result = convert_objects('select * from t_myuser where id=1;')
    print(result[0].id)
