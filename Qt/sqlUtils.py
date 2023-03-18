import pymysql


class sqlUtils:
    @classmethod
    # 初始化连接
    def initDB(cls):
        # 打开数据库连接
        config = {
            "user": "root",
            "password": "xilan666",
            "host": "localhost",
            "database": "face-identify"
        }
        db = pymysql.connect(**config)
        return db

    @classmethod
    # 登录
    def Login(cls, args):
        # 获取数据库连接
        db = sqlUtils.initDB()
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()
        # sql语句
        sql = "select * from user where user.username = %s and user.password = %s"
        result = cursor.execute(sql, args)
        user = cursor.fetchone()
        db.commit()
        db.close()
        return result, user

    @classmethod
    # 注册
    def register(cls, args):
        # 获取数据库连接
        db = sqlUtils.initDB()
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()
        # sql语句
        sql = "insert into user(username,password) values (%s, %s)"
        result = cursor.execute(sql, args)
        db.commit()
        db.close()
        return result

    @classmethod
    # 保存photo和name
    def save_photo_name(cls, base64_str, userId, name):
        db = sqlUtils.initDB()
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()
        # 插入
        sql = "UPDATE user set photo = %s,name = %s WHERE id = %s"
        val = (base64_str, name, userId)
        try:
            cursor.execute(sql, val)
            db.commit()
            db.close()
            return True  # 返回保存成功
        except:
            db.rollback()
            db.close()
            return False  # 返回保存失败

    @classmethod
    # 根据id查询用户的 信息  主要是为了更新UserHolder
    def update_userHolder(cls, args):
        # 获取数据库连接
        db = sqlUtils.initDB()
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()
        # sql语句
        sql = "SELECT * FROM user WHERE id = %s"
        result = cursor.execute(sql, args)
        now_user = cursor.fetchone()
        db.commit()
        db.close()
        return result, now_user


if __name__ == '__main__':
    print(sqlUtils.change_table("matter", "specs", "99x99", "1"))
