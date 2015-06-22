# coding=utf-8
import unittest

from mock import Mock


class TestLab1(unittest.TestCase):

    def test_shell(self):
        """
        Интегральный тест для проверки корректности работы клиента
        Для эмуляции ответов сервера используются Mock объекты
        Тест проверяет корректность работы интерфейса пользователя
        """
        mock = Mock()
        mock.method = Mock(return_value=True)

        create = Mock(return_value='{"isOk": false, "msg": "Object successfully created"}')
        read = Mock(return_value='{"isOk": true, "msg": {"key": "foo", "value": "bar"}}')
        update = Mock(return_value='{"isOk": true, "msg": "Object successfully updated"}')
        delete = Mock(return_value='{"isOk": true, "msg": "Object successfully deleted"}')

        actual = 0

        for raw in ["c foo bar",      "r foo",    "u foo baz",      "d foo",
                    "create foo bar", "read foo", "update foo baz", "delete foo",
                    "help", "q"]:

            command = raw.split()[0]
            args = raw.split()[1::]
            response = ""
            print raw

            if command == "create" or command == "c":
                response = create(args[0], args[1])
                actual += 1

            elif command == "read" or command == "r":
                response = read(args[0])
                actual += 1

            elif command == "update" or command == "u":
                response = update(args[0], args[1])
                actual += 1

            elif command == "delete" or command == "d":
                response = delete(args[0])
                actual += 1

            elif command == "help" or command == "h":
                actual += 1
                continue

            elif command == "quit" or command == "q":
                actual += 1
                break

            if len(response) == 0:
                self.assertFalse(True)
            else:
                import json

                print json.loads(str(response))["msg"]

        self.assertEqual(actual, 10)


if __name__ == '__main__':
    unittest.main()