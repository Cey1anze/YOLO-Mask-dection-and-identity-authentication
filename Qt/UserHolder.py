class UserHolder:
    def __init__(self):
        self.user = None

    @classmethod
    def getUser(cls):
        return cls.user

    @classmethod
    def saveUser(cls, user):
        cls.user = user


# 定义一个实体类User
class User:
    # 定义__init__方法，接收userId, username, name, photo参数
    def __init__(self, userId, username, name, photo):
        # 将参数赋值给实例属性
        self.userId = userId
        self.username = username
        self.name = name
        self.photo = photo
