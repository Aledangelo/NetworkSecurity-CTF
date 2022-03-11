import re

# from email_validator import validate_email, EmailNotValidError

from db_modules.connector import dbSql
import base64
import imghdr

'''
keyDict = {'login': ['userId', 'username', 'password'],
           'registration': ['name', 'surname', 'username', 'email', 'password', 'birthday', 'birthplace', 'residence',
                            'residenceId'],
           'reports': ['name', 'description', 'place', 'cityId', 'date', 'images']}
regExDict = {
    'registration': {
        "userId": "^\d+$",
        "username": "^[\w'\-,.][^0-9_!¡?÷?¿/\\+=@#$%ˆ&*(){}|~<>;:[\]]{2,20}$",
        "password": "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,20}$",
        "name": "^[\w'\-,.][^0-9_!¡?÷?¿/\\+=@#$%ˆ&*(){}|~<>;:[\]]{2,20}$",
        "surname": "^[\w'\-,.][^0-9_!¡?÷?¿/\\+=@#$%ˆ&*(){}|~<>;:[\]]{2,20}$",
        "email": "(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])",
        "birthday": "(?:0[1-9]|[12][0-9]|3[01])[-/.](?:0[1-9]|1[012])[-/.](?:19\d{2}|20[01][0-9]|2020)\b",
        "birthplace": "^[\w'\-,.][^0-9_!¡?÷?¿/\\+=@#$%ˆ&*(){}|~<>;:[\]]{2,30}$",
        "residence": "^[\w'\-,.][^0-9_!¡?÷?¿/\\+=@#$%ˆ&*(){}|~<>;:[\]]{2,30}$",
        "residenceId": "^\d+$"
    },
    'reports': {
        "name": "^[\w'\-,.][^0-9_!¡?÷?¿/\\+=@#$%ˆ&*(){}|~<>;:[\]]{2,20}$",
        "description": "^[\w'\-,.][^0-9_!¡?÷?¿/\\+=@#$%ˆ&*(){}|~<>;:[\]]{2,100}$",
        "place": "^[\w'\-,.][^0-9_!¡?÷?¿/\\+=@#$%ˆ&*(){}|~<>;:[\]]{2,30}$",
        "cityId": "^[0-9]{4,6}$",
        "date": "^(3[01]|[12][0-9]|0[1-9])/(1[0-2]|0[1-9])/[0-9]{4} (2[0-3]|[01]?[0-9]):([0-5]?[0-9])$",
        "images": "^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{4})$"
    }
}

imageTypes = ['jpeg', 'jpg', 'png']
'''
'''
class UtilsInput():
    def __init__(self, id: str) -> None:
        self.__id = id
        self.__keys = keyDict[id][:]
        self.__values = regExDict[id]

    def checkKeys(self, dataInput: dict) -> bool:
        keys = self.__keys[:]
        for k in dataInput.keys():
            if k not in keys:
                return False
            keys.remove(k)
        if len(keys) != 0:
            return False
        return True

    def checkValues(self, dataInput: dict) -> bool:
        for k in dataInput.keys():
            print(k, dataInput[k])
            if k != 'images':
                if not re.match(str(self.__values[k]), str(dataInput[k])):
                    print(self.__values[k], dataInput[k])
                    return False
        return True

    def checkImages(self, imagesInput: str) -> bool:
        if not isinstance(imagesInput, str):
            return False
        if not re.match(str(self.__values['images']), imagesInput):
            return False
        decImg = base64.b64decode(imagesInput)
        if imghdr.what('file', h=decImg) not in imageTypes:
            return False
        return True

class VerifyInput():
    def __init__(self) -> None:
        pass

    def checkEmpty(self, nome: str, cognome: str, city: str, pwd: str) -> bool:
        if nome == "" or cognome == "" or city == "" or pwd == "":
            return False
        else:
            return True
    def checkEmail(self, email: str) -> bool:
        try:
            valid = validate_email(email)
            email = valid.email
            return True
        except EmailNotValidError as e:
            print(str(e))
            return False
'''
class Auth():
    def __init__(self, apiKey: str, userId: str, paramKey: str, table: str) -> None:
        self.__apiKey = apiKey 
        self.__userId = userId
        self.__paramKey = paramKey 
        self.__table = table

    def verify(self) -> bool:
        row = dbSql.selectRowByParam(self.__paramKey, self.__apiKey, self.__table)
        if len(row) == 0:
            return False
        if self.__userId != row['id']:
            return False
        return True

    def validateEmail(self) -> bool:
        row = dbSql.selectRowByParam(self.__paramKey, self.__apiKey, self.__table)
        if len(row) != 0:
            dbSql.updateRowByParam(self.__paramKey, self.__apiKey, self.__table, self.__paramKey, "yes")
            return True
        else:
            return False

    def verifyGeneric(self) -> bool:
        row = dbSql.selectRowByParam(self.__paramKey, self.__apiKey, self.__table)
        if len(row) != 0:
            return False
        else:
            return True

    def multiSelect1(self) -> str:
        row1 = dbSql.selectRowByParam(self.__paramKey, self.__apiKey, self.__table)
        if len(row1) != 0:
            pwd = row1["pwd"]
            return pwd
        else:
            return ""

    def multiSelect2(self) -> list:
        row1 = dbSql.selectRowByParam(self.__paramKey, self.__apiKey, self.__table)
        return row1


if __name__ == '__main__':
    obj = UtilsInput('login')
    d = {'username': 'root', 'password': ''}
    print(obj.checkKeys(d))
