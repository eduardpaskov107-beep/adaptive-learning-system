"""
База знаний с теорией и тестами
"""

THEORY_DATABASE = {
    "python_basics": {
        "topic": "Основы Python",
        "subtopics": {
            "variables": {
                "level": "beginner",
                "name": "Переменные и типы данных",
                "content": "# Переменные и типы данных в Python\n\n## Что такое переменная?\nПеременная - это именованная область памяти для хранения данных.\nПример:\nname = 'Анна'          # строка (str)\nage = 25               # целое число (int)\nprice = 19.99          # число с плавающей точкой (float)\nis_student = True      # булево значение (bool)\n\n## Основные типы данных:\n1. int - целые числа: 42, -3, 0\n2. float - числа с плавающей точкой: 3.14, 2.5, -0.5\n3. str - строки: 'Привет', 'Python'\n4. bool - логические значения: True, False\n5. list - списки: [1, 2, 3]\n6. dict - словари: {'name': 'Иван', 'age': 25}\n\n## Правила именования переменных:\n- Могут содержать буквы, цифры и знак подчеркивания\n- Не могут начинаться с цифры\n- Чувствительны к регистру (age != Age)\n- Нельзя использовать ключевые слова Python (if, for, while)\n\n## Преобразование типов:\nx = 10          # int\ny = float(x)    # 10.0 (float)\nz = str(x)      # '10' (str)",
                "questions": [
                    {
                        "text": "Какой символ НЕльзя использовать в имени переменной Python?",
                        "options": ["Буквы", "Цифры", "Знак подчеркивания (_)", "Дефис (-)"],
                        "correct": 3,
                        "explanation": "Дефис (-) нельзя использовать, он используется для вычитания."
                    },
                    {
                        "text": "Какой тип данных у значения 3.14?",
                        "options": ["int", "str", "float", "bool"],
                        "correct": 2,
                        "explanation": "3.14 - число с плавающей точкой, тип float."
                    },
                    {
                        "text": "Что выведет код: print(type(True))?",
                        "options": ["<class 'int'>", "<class 'bool'>", "<class 'str'>", "Ошибка"],
                        "correct": 1,
                        "explanation": "True - булево значение, тип bool."
                    }
                ],
                "specializations": {
                    "data_science": "В Data Science переменные хранят данные для анализа: массивы NumPy, DataFrames Pandas, результаты вычислений.",
                    "web_dev": "В веб-разработке переменные хранят данные пользователей, состояния форм, параметры запросов к серверу.",
                    "bioinformatics": "В биоинформатике переменные хранят генетические последовательности, результаты анализа ДНК, статистические данные."
                }
            },
            "lists": {
                "level": "beginner",
                "name": "Списки и операции с ними",
                "content": "# Списки (Lists) в Python\n\n## Создание списков:\nnumbers = [1, 2, 3, 4, 5]          # список чисел\nfruits = ['яблоко', 'банан', 'апельсин']  # список строк\nmixed = [1, 'текст', True, 3.14]   # смешанный список\nempty = []                         # пустой список\n\n## Основные операции:\n# Доступ к элементам\nfruits = ['яблоко', 'банан', 'апельсин']\nprint(fruits[0])    # 'яблоко' (индексация с 0)\nprint(fruits[-1])   # 'апельсин' (отрицательный индекс)\n\n# Изменение элементов\nfruits[1] = 'груша'  # ['яблоко', 'груша', 'апельсин']\n\n# Добавление элементов\nfruits.append('киви')      # добавить в конец\nfruits.insert(1, 'виноград')  # вставить на позицию 1\n\n# Удаление элементов\nfruits.remove('банан')     # удалить по значению\npopped = fruits.pop()      # удалить и вернуть последний\ndel fruits[0]              # удалить по индексу\n\n## Методы списков:\n- append(x) - добавить элемент в конец\n- extend(iterable) - добавить несколько элементов\n- insert(i, x) - вставить элемент на позицию i\n- remove(x) - удалить первый элемент со значением x\n- pop([i]) - удалить и вернуть элемент по индексу i\n- sort() - отсортировать список\n- reverse() - развернуть список\n- count(x) - подсчитать количество x\n- index(x) - найти индекс первого вхождения x\n\n## Срезы (slicing):\nnumbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]\nprint(numbers[2:5])    # [2, 3, 4] (с 2 до 5, не включая 5)\nprint(numbers[:3])     # [0, 1, 2] (с начала до 3)\nprint(numbers[6:])     # [6, 7, 8, 9] (с 6 до конца)\nprint(numbers[::2])    # [0, 2, 4, 6, 8] (каждый второй)\nprint(numbers[::-1])   # [9, 8, 7, 6, 5, 4, 3, 2, 1, 0] (обратный порядок)",
                "questions": [
                    {
                        "text": "Как получить последний элемент списка nums?",
                        "options": ["nums[0]", "nums[-1]", "nums[last]", "nums.end()"],
                        "correct": 1,
                        "explanation": "Отрицательные индексы идут с конца: -1 - последний, -2 - предпоследний."
                    },
                    {
                        "text": "Что делает метод append()?",
                        "options": ["Удаляет элемент", "Добавляет элемент в конец", "Сортирует список", "Находит элемент"],
                        "correct": 1,
                        "explanation": "append() добавляет элемент в конец списка."
                    },
                    {
                        "text": "Что вернет [1, 2, 3, 4][1:3]?",
                        "options": ["[1, 2]", "[2, 3]", "[1, 2, 3]", "[2, 3, 4]"],
                        "correct": 1,
                        "explanation": "Срез [1:3] берет элементы с индексами 1 и 2 (3 не включается)."
                    }
                ],
                "specializations": {
                    "data_science": "В Data Science списки преобразуются в массивы NumPy для быстрых вычислений. Используются для хранения выборок данных, временных рядов, признаков объектов.",
                    "web_dev": "В веб-разработке списки хранят элементы меню, результаты поиска, посты в ленте, комментарии пользователей.",
                    "bioinformatics": "В биоинформатике списки хранят последовательности аминокислот, результаты экспериментов, статистические выборки."
                }
            },
            "dictionaries": {
                "level": "beginner",
                "name": "Словари (dictionaries)",
                "content": "# Словари в Python\n\n## Создание словарей:\nstudent = {'name': 'Анна', 'age': 20, 'grade': 'A'}\nempty_dict = {}\n\n# С помощью dict()\ndict_from_list = dict([('name', 'Иван'), ('age', 25)])\n\n## Доступ к элементам:\nprint(student['name'])     # 'Анна'\nprint(student.get('age'))  # 20\nprint(student.get('city', 'Не указан'))  # 'Не указан' (значение по умолчанию)\n\n## Добавление и изменение:\nstudent['city'] = 'Москва'      # добавить новый ключ\nstudent['age'] = 21            # изменить существующий\n\n## Удаление элементов:\ndel student['grade']           # удалить ключ 'grade'\nage = student.pop('age')       # удалить и вернуть значение\nstudent.clear()                # очистить весь словарь\n\n## Методы словарей:\n- keys() - возвращает все ключи\n- values() - возвращает все значения\n- items() - возвращает пары (ключ, значение)\n- update(other_dict) - обновляет словарь\n- copy() - создает копию\n\n## Итерация по словарю:\nfor key in student.keys():\n    print(key)\n\nfor value in student.values():\n    print(value)\n\nfor key, value in student.items():\n    print(f'{key}: {value}')",
                "questions": [
                    {
                        "text": "Как получить значение из словаря по ключу 'name'?",
                        "options": ["dict.name", "dict['name']", "dict.get('name')", "dict(name)"],
                        "correct": 2,
                        "explanation": "Можно использовать dict['name'] или dict.get('name')."
                    },
                    {
                        "text": "Что вернет student.get('phone', 'Нет телефона') если ключа 'phone' нет?",
                        "options": ["None", "Ошибка", "'Нет телефона'", "Пустая строка"],
                        "correct": 2,
                        "explanation": "get() возвращает значение по умолчанию, если ключ не найден."
                    },
                    {
                        "text": "Какой метод возвращает пары ключ-значение?",
                        "options": ["keys()", "values()", "items()", "pairs()"],
                        "correct": 2,
                        "explanation": "items() возвращает пары (ключ, значение)."
                    }
                ],
                "specializations": {
                    "data_science": "В Data Science словари хранят параметры моделей, метаданные датасетов, результаты вычислений в виде JSON.",
                    "web_dev": "В веб-разработке словари представляют JSON данные, параметры запросов, сессии пользователей.",
                    "bioinformatics": "В биоинформатике словари хранят свойства генов, параметры экспериментов, метаданные образцов."
                }
            }
        }
    },
    "functions": {
        "topic": "Функции в Python",
        "subtopics": {
            "basic_functions": {
                "level": "intermediate",
                "name": "Основы функций",
                "content": "# Функции в Python\n\n## Определение функции:\ndef greet(name):\n    return f'Привет, {name}!'\n\n# Вызов функции\nmessage = greet('Анна')\nprint(message)  # Привет, Анна!\n\n## Параметры и аргументы:\n# Позиционные параметры\ndef add(a, b):\n    return a + b\n\nresult = add(5, 3)  # 8\n\n# Именованные аргументы\ndef create_user(name, age, email):\n    return {'name': name, 'age': age, 'email': email}\n\nuser = create_user(age=25, email='test@mail.com', name='Иван')\n\n# Параметры по умолчанию\ndef greet(name, greeting='Привет'):\n    return f'{greeting}, {name}!'\n\nprint(greet('Мария'))  # Привет, Мария!\nprint(greet('Петр', 'Добрый день'))  # Добрый день, Петр!\n\n# Произвольное количество аргументов\ndef sum_all(*args):\n    return sum(args)\n\nprint(sum_all(1, 2, 3, 4, 5))  # 15\n\ndef print_info(**kwargs):\n    for key, value in kwargs.items():\n        print(f'{key}: {value}')\n\nprint_info(name='Анна', age=25, city='Москва')\n\n## Возвращаемые значения:\n# Возврат одного значения\ndef square(x):\n    return x * x\n\n# Возврат нескольких значений (кортеж)\ndef min_max(numbers):\n    return min(numbers), max(numbers)\n\nminimum, maximum = min_max([5, 2, 8, 1, 9])\nprint(f'Min: {minimum}, Max: {maximum}')\n\n## Лямбда-функции:\n# Анонимная функция в одну строку\nsquare = lambda x: x * x\nprint(square(5))  # 25\n\n# Использование с map\nnumbers = [1, 2, 3, 4, 5]\nsquares = list(map(lambda x: x * x, numbers))  # [1, 4, 9, 16, 25]\n\n# Использование с filter\nevens = list(filter(lambda x: x % 2 == 0, numbers))  # [2, 4]",
                "questions": [
                    {
                        "text": "Какой ключевое слово используется для определения функции?",
                        "options": ["function", "def", "func", "define"],
                        "correct": 1,
                        "explanation": "Функции определяются с помощью ключевого слова def."
                    },
                    {
                        "text": "Что вернет функция без return?",
                        "options": ["0", "None", "Пустую строку", "Ошибку"],
                        "correct": 1,
                        "explanation": "Если функция не возвращает значение явно, она возвращает None."
                    },
                    {
                        "text": "Что такое лямбда-функция?",
                        "options": ["Большая функция", "Анонимная функция в одну строку", "Функция для математики", "Импортированная функция"],
                        "correct": 1,
                        "explanation": "Лямбда-функция - это анонимная функция, определяемая в одну строку."
                    }
                ],
                "specializations": {
                    "data_science": "В Data Science функции обрабатывают данные, вычисляют метрики, визуализируют результаты. Часто используются с библиотеками NumPy и Pandas.",
                    "web_dev": "В веб-разработке функции обрабатывают запросы, валидируют данные, работают с базой данных, генерируют HTML.",
                    "bioinformatics": "В биоинформатике функции анализируют последовательности ДНК, обрабатывают данные экспериментов, вычисляют статистические показатели."
                }
            },
            "decorators": {
                "level": "advanced",
                "name": "Декораторы функций",
                "content": "# Декораторы функций\n\n## Что такое декоратор?\nДекоратор - это функция, которая принимает другую функцию и расширяет её поведение без изменения её кода.\n\n## Простой декоратор:\ndef my_decorator(func):\n    def wrapper():\n        print('Что-то происходит перед вызовом функции')\n        func()\n        print('Что-то происходит после вызова функции')\n    return wrapper\n\n@my_decorator\ndef say_hello():\n    print('Привет!')\n\nsay_hello()\n# Вывод:\n# Что-то происходит перед вызовом функции\n# Привет!\n# Что-то происходит после вызова функции\n\n## Декоратор с аргументами:\ndef repeat(num_times):\n    def decorator_repeat(func):\n        def wrapper(*args, **kwargs):\n            for _ in range(num_times):\n                result = func(*args, **kwargs)\n            return result\n        return wrapper\n    return decorator_repeat\n\n@repeat(num_times=3)\ndef greet(name):\n    print(f'Привет, {name}')\n\ngreet('Анна')\n# Вывод:\n# Привет, Анна\n# Привет, Анна\n# Привет, Анна\n\n## Полезные декораторы:\n# Декоратор для измерения времени выполнения\nimport time\n\ndef timer(func):\n    def wrapper(*args, **kwargs):\n        start = time.time()\n        result = func(*args, **kwargs)\n        end = time.time()\n        print(f'Функция {func.__name__} выполнилась за {end-start:.2f} секунд')\n        return result\n    return wrapper\n\n@timer\ndef slow_function():\n    time.sleep(1)\n    return 'Готово'\n\nslow_function()\n\n# Декоратор для логирования\ndef logger(func):\n    def wrapper(*args, **kwargs):\n        print(f'Вызов функции {func.__name__} с аргументами: {args}, {kwargs}')\n        result = func(*args, **kwargs)\n        print(f'Функция {func.__name__} вернула: {result}')\n        return result\n    return wrapper\n\n## Несколько декораторов:\n@timer\n@logger\ndef add(a, b):\n    return a + b\n\nresult = add(5, 3)\n# Вывод:\n# Вызов функции add с аргументами: (5, 3), {}\n# Функция add вернула: 8\n# Функция wrapper выполнилась за 0.00 секунд",
                "questions": [
                    {
                        "text": "Что такое декоратор?",
                        "options": ["Функция, которая изменяет поведение другой функции", "Тип данных", "Способ создания классов", "Модуль Python"],
                        "correct": 0,
                        "explanation": "Декоратор - это функция, которая принимает другую функцию и расширяет её поведение."
                    },
                    {
                        "text": "Какой символ используется для применения декоратора?",
                        "options": ["@", "#", "$", "%"],
                        "correct": 0,
                        "explanation": "Декоратор применяется с помощью символа @ перед определением функции."
                    },
                    {
                        "text": "Можно ли применять несколько декораторов к одной функции?",
                        "options": ["Да", "Нет", "Только 2", "Только если они разные"],
                        "correct": 0,
                        "explanation": "Да, можно применять несколько декораторов, они выполняются сверху вниз."
                    }
                ],
                "specializations": {
                    "data_science": "В Data Science декораторы используются для кэширования результатов вычислений, логирования, измерения производительности алгоритмов.",
                    "web_dev": "В веб-разработке декораторы контролируют доступ к роутам, проверяют авторизацию, логируют запросы (Flask, Django).",
                    "bioinformatics": "В биоинформатике декораторы валидируют входные данные, логируют этапы анализа, измеряют время выполнения сложных вычислений."
                }
            }
        }
    },
    "oop": {
        "topic": "Объектно-ориентированное программирование",
        "subtopics": {
            "classes": {
                "level": "intermediate",
                "name": "Классы и объекты",
                "content": "# Классы и объекты в Python\n\n## Определение класса:\nclass Student:\n    def __init__(self, name, age, major):\n        self.name = name      # атрибут экземпляра\n        self.age = age        # атрибут экземпляра\n        self.major = major    # атрибут экземпляра\n        self.grades = []      # атрибут экземпляра\n    \n    # Метод экземпляра\n    def add_grade(self, grade):\n        self.grades.append(grade)\n    \n    # Метод экземпляра\n    def get_average(self):\n        if not self.grades:\n            return 0\n        return sum(self.grades) / len(self.grades)\n    \n    # Магический метод для строкового представления\n    def __str__(self):\n        return f'Студент {self.name}, {self.age} лет, специальность: {self.major}'\n\n# Создание объектов (экземпляров класса)\nstudent1 = Student('Анна', 20, 'Информатика')\nstudent2 = Student('Иван', 22, 'Математика')\n\n# Использование методов\nstudent1.add_grade(4.5)\nstudent1.add_grade(5.0)\nstudent1.add_grade(4.0)\n\nprint(student1)  # Студент Анна, 20 лет, специальность: Информатика\nprint(f'Средний балл: {student1.get_average():.2f}')  # Средний балл: 4.50\n\n## Наследование:\nclass Person:\n    def __init__(self, name, age):\n        self.name = name\n        self.age = age\n    \n    def introduce(self):\n        return f'Меня зовут {self.name}, мне {self.age} лет'\n\n# Класс Student наследует от Person\nclass Student(Person):\n    def __init__(self, name, age, student_id):\n        super().__init__(name, age)  # вызов конструктора родителя\n        self.student_id = student_id\n    \n    def introduce(self):\n        # Переопределение метода\n        base_intro = super().introduce()\n        return f'{base_intro}. Мой студенческий билет: {self.student_id}'\n\n# Класс Teacher наследует от Person\nclass Teacher(Person):\n    def __init__(self, name, age, subject):\n        super().__init__(name, age)\n        self.subject = subject\n    \n    def introduce(self):\n        base_intro = super().introduce()\n        return f'{base_intro}. Я преподаю {self.subject}'\n\n# Использование\nstudent = Student('Мария', 20, 'S12345')\nteacher = Teacher('Алексей', 45, 'Математика')\n\nprint(student.introduce())  # Меня зовут Мария, мне 20 лет. Мой студенческий билет: S12345\nprint(teacher.introduce())  # Меня зовут Алексей, мне 45 лет. Я преподаю Математика\n\n## Инкапсуляция:\nclass BankAccount:\n    def __init__(self, owner, balance=0):\n        self.owner = owner\n        self.__balance = balance  # приватный атрибут\n    \n    def deposit(self, amount):\n        if amount > 0:\n            self.__balance += amount\n            print(f'Внесено: {amount}. Новый баланс: {self.__balance}')\n        else:\n            print('Сумма должна быть положительной')\n    \n    def withdraw(self, amount):\n        if 0 < amount <= self.__balance:\n            self.__balance -= amount\n            print(f'Снято: {amount}. Новый баланс: {self.__balance}')\n        else:\n            print('Недостаточно средств или неверная сумма')\n    \n    def get_balance(self):  # публичный метод для доступа к балансу\n        return self.__balance\n\naccount = BankAccount('Иван', 1000)\naccount.deposit(500)    # Внесено: 500. Новый баланс: 1500\naccount.withdraw(200)   # Снято: 200. Новый баланс: 1300\nprint(f'Баланс: {account.get_balance()}')  # Баланс: 1300",
                "questions": [
                    {
                        "text": "Что такое self в методах класса?",
                        "options": ["Имя класса", "Ссылка на экземпляр класса", "Ключевое слово Python", "Тип данных"],
                        "correct": 1,
                        "explanation": "self - это ссылка на текущий экземпляр класса, используется для доступа к атрибутам и методам."
                    },
                    {
                        "text": "Что делает super().__init__()?",
                        "options": ["Удаляет объект", "Вызывает конструктор родительского класса", "Создает новый класс", "Импортирует модуль"],
                        "correct": 1,
                        "explanation": "super().__init__() вызывает конструктор родительского класса для инициализации унаследованных атрибутов."
                    },
                    {
                        "text": "Как обозначается приватный атрибут в Python?",
                        "options": ["Одним подчеркиванием _attr", "Двумя подчеркиваниями __attr", "Словом private", "Ключевым словом private"],
                        "correct": 1,
                        "explanation": "Два подчеркивания перед именем атрибута (__attr) делают его приватным (name mangling)."
                    }
                ],
                "specializations": {
                    "data_science": "В Data Science классы создают модели машинного обучения, обработчики данных, конвейеры обработки. Scikit-learn полностью основан на ООП.",
                    "web_dev": "В веб-разработке классы представляют модели данных (Django Models), обработчики запросов, формы, представления.",
                    "bioinformatics": "В биоинформатике классы моделируют биологические объекты (гены, белки), инструменты анализа, алгоритмы поиска последовательностей."
                }
            },
            "inheritance": {
                "level": "advanced",
                "name": "Наследование и полиморфизм",
                "content": "# Наследование и полиморфизм\n\n## Множественное наследование:\nclass Animal:\n    def __init__(self, name):\n        self.name = name\n    \n    def speak(self):\n        return 'Звук животного'\n\nclass Flyable:\n    def fly(self):\n        return f'{self.name} летит'\n\nclass Swimmable:\n    def swim(self):\n        return f'{self.name} плывет'\n\nclass Duck(Animal, Flyable, Swimmable):\n    def speak(self):\n        return 'Кря-кря!'\n\nduck = Duck('Утка')\nprint(duck.speak())  # Кря-кря!\nprint(duck.fly())    # Утка летит\nprint(duck.swim())   # Утка плывет\n\n## Абстрактные классы:\nfrom abc import ABC, abstractmethod\n\nclass Shape(ABC):  # Абстрактный базовый класс\n    @abstractmethod\n    def area(self):\n        pass\n    \n    @abstractmethod\n    def perimeter(self):\n        pass\n\nclass Rectangle(Shape):\n    def __init__(self, width, height):\n        self.width = width\n        self.height = height\n    \n    def area(self):\n        return self.width * self.height\n    \n    def perimeter(self):\n        return 2 * (self.width + self.height)\n\nclass Circle(Shape):\n    def __init__(self, radius):\n        self.radius = radius\n    \n    def area(self):\n        import math\n        return math.pi * self.radius ** 2\n    \n    def perimeter(self):\n        import math\n        return 2 * math.pi * self.radius\n\n# Полиморфизм\nshapes = [Rectangle(5, 10), Circle(7)]\nfor shape in shapes:\n    print(f'Площадь: {shape.area():.2f}, Периметр: {shape.perimeter():.2f}')\n\n## Миксины (Mixins):\nclass JSONMixin:\n    def to_json(self):\n        import json\n        return json.dumps(self.__dict__)\n\nclass XMLMixin:\n    def to_xml(self):\n        attrs = ''.join(f' {k}=\"{v}\"' for k, v in self.__dict__.items())\n        return f'<{self.__class__.__name__}{attrs} />'\n\nclass Product(JSONMixin, XMLMixin):\n    def __init__(self, name, price):\n        self.name = name\n        self.price = price\n\nproduct = Product('Ноутбук', 50000)\nprint(product.to_json())  # {'name': 'Ноутбук', 'price': 50000}\nprint(product.to_xml())   # <Product name=\"Ноутбук\" price=\"50000\" />\n\n## Магические методы (dunder methods):\nclass Vector:\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y\n    \n    def __add__(self, other):\n        return Vector(self.x + other.x, self.y + other.y)\n    \n    def __sub__(self, other):\n        return Vector(self.x - other.x, self.y - other.y)\n    \n    def __mul__(self, scalar):\n        return Vector(self.x * scalar, self.y * scalar)\n    \n    def __str__(self):\n        return f'Vector({self.x}, {self.y})'\n    \n    def __eq__(self, other):\n        return self.x == other.x and self.y == other.y\n\nv1 = Vector(2, 3)\nv2 = Vector(4, 5)\nprint(v1 + v2)  # Vector(6, 8)\nprint(v2 - v1)  # Vector(2, 2)\nprint(v1 * 3)   # Vector(6, 9)\nprint(v1 == Vector(2, 3))  # True",
                "questions": [
                    {
                        "text": "Что такое полиморфизм?",
                        "options": ["Способность объектов разных классов использовать одинаковый интерфейс", "Создание новых классов", "Скрытие данных", "Наследование от одного класса"],
                        "correct": 0,
                        "explanation": "Полиморфизм - это способность объектов разных классов использовать одинаковый интерфейс."
                    },
                    {
                        "text": "Что такое миксин (Mixin)?",
                        "options": ["Класс, который добавляет определенную функциональность другим классам", "Основной класс", "Абстрактный класс", "Финальный класс"],
                        "correct": 0,
                        "explanation": "Миксин - это класс, который добавляет определенную функциональность другим классам через множественное наследование."
                    },
                    {
                        "text": "Какой метод вызывается при сложении объектов?",
                        "options": ["__add__", "__sum__", "__plus__", "__concat__"],
                        "correct": 0,
                        "explanation": "Метод __add__ определяет поведение при сложении объектов с помощью оператора +."
                    }
                ],
                "specializations": {
                    "data_science": "В Data Science наследование используется для создания иерархий моделей, миксины добавляют функциональность обработки данных, полиморфизм позволяет работать с разными типами данных через единый интерфейс.",
                    "web_dev": "В веб-разработке наследование создает иерархии контроллеров и моделей, миксины добавляют аутентификацию, полиморфизм используется в обработчиках запросов.",
                    "bioinformatics": "В биоинформатике наследование моделирует биологические иерархии (организмы → органы → клетки), миксины добавляют функциональность анализа, полиморфизм обрабатывает разные типы биологических данных."
                }
            }
        }
    },
    "data_structures": {
        "topic": "Структуры данных",
        "subtopics": {
            "stacks_queues": {
                "level": "intermediate",
                "name": "Стеки и очереди",
                "content": "# Стеки и очереди\n\n## Стек (LIFO - Last In, First Out):\n# Реализация стека на списке\nclass Stack:\n    def __init__(self):\n        self.items = []\n    \n    def push(self, item):\n        self.items.append(item)\n    \n    def pop(self):\n        if not self.is_empty():\n            return self.items.pop()\n        return None\n    \n    def peek(self):\n        if not self.is_empty():\n            return self.items[-1]\n        return None\n    \n    def is_empty(self):\n        return len(self.items) == 0\n    \n    def size(self):\n        return len(self.items)\n\n# Использование стека\nstack = Stack()\nstack.push(1)\nstack.push(2)\nstack.push(3)\nprint(stack.pop())  # 3 (последний добавленный)\nprint(stack.peek()) # 2\n\n## Очередь (FIFO - First In, First Out):\n# Реализация очереди на списке\nclass Queue:\n    def __init__(self):\n        self.items = []\n    \n    def enqueue(self, item):\n        self.items.append(item)\n    \n    def dequeue(self):\n        if not self.is_empty():\n            return self.items.pop(0)\n        return None\n    \n    def front(self):\n        if not self.is_empty():\n            return self.items[0]\n        return None\n    \n    def is_empty(self):\n        return len(self.items) == 0\n    \n    def size(self):\n        return len(self.items)\n\n# Использование очереди\nqueue = Queue()\nqueue.enqueue('Анна')\nqueue.enqueue('Борис')\nqueue.enqueue('Виктор')\nprint(queue.dequeue())  # Анна (первый добавленный)\nprint(queue.front())    # Борис\n\n## Двусторонняя очередь (deque):\nfrom collections import deque\n\nd = deque(['b', 'c', 'd'])\nd.append('e')          # добавление в конец\nd.appendleft('a')      # добавление в начало\nprint(d)               # deque(['a', 'b', 'c', 'd', 'e'])\n\nprint(d.pop())         # 'e' (удаление с конца)\nprint(d.popleft())     # 'a' (удаление с начала)\nprint(d)               # deque(['b', 'c', 'd'])\n\n## Применение стека - проверка скобок:\ndef is_balanced(expression):\n    stack = []\n    pairs = {')': '(', ']': '[', '}': '{'}\n    \n    for char in expression:\n        if char in '([{':\n            stack.append(char)\n        elif char in ')]}':\n            if not stack or stack[-1] != pairs[char]:\n                return False\n            stack.pop()\n    \n    return len(stack) == 0\n\nprint(is_balanced('({[]})'))  # True\nprint(is_balanced('({[})'))   # False\n\n## Применение очереди - обработка задач:\nclass TaskQueue:\n    def __init__(self):\n        self.queue = deque()\n    \n    def add_task(self, task):\n        self.queue.append(task)\n        print(f'Добавлена задача: {task}')\n    \n    def process_next(self):\n        if self.queue:\n            task = self.queue.popleft()\n            print(f'Обрабатывается: {task}')\n            return task\n        return None\n    \n    def show_queue(self):\n        return list(self.queue)\n\n# Пример использования\ntask_queue = TaskQueue()\ntask_queue.add_task('Отправить email')\ntask_queue.add_task('Создать отчет')\ntask_queue.add_task('Проверить код')\nprint(f'Очередь задач: {task_queue.show_queue()}')\ntask_queue.process_next()  # Обрабатывается: Отправить email",
                "questions": [
                    {
                        "text": "Какой принцип у стека?",
                        "options": ["FIFO", "LIFO", "FILO", "LILO"],
                        "correct": 1,
                        "explanation": "Стек работает по принципу LIFO (Last In, First Out) - последний пришел, первый ушел."
                    },
                    {
                        "text": "Какой метод добавляет элемент в очередь?",
                        "options": ["push()", "enqueue()", "add()", "append()"],
                        "correct": 1,
                        "explanation": "В очереди используется метод enqueue() для добавления элементов."
                    },
                    {
                        "text": "Для чего используется deque из collections?",
                        "options": ["Только для стеков", "Только для очередей", "Для двусторонних очередей", "Для деревьев"],
                        "correct": 2,
                        "explanation": "deque - двусторонняя очередь, позволяет добавлять и удалять элементы с обоих концов."
                    }
                ],
                "specializations": {
                    "data_science": "В Data Science стеки используются для обхода графов (DFS), очереди - для поиска в ширину (BFS), deque - для скользящих окон в анализе временных рядов.",
                    "web_dev": "В веб-разработке стеки хранят историю навигации, очереди обрабатывают асинхронные задачи (Celery), deque используется для кэширования.",
                    "bioinformatics": "В биоинформатике стеки и очереди используются в алгоритмах поиска по графам генетических связей, обработке последовательностей ДНК."
                }
            }
        }
    }
}

SPECIALIZATIONS = {
    "data_science": "Data Science и анализ данных",
    "web_dev": "Веб-разработка",
    "bioinformatics": "Биоинформатика и генетика"
}

# Количество вопросов в начальном тесте по каждой теме
INITIAL_TEST_QUESTIONS = {
    "beginner": 2,
    "intermediate": 1,
    "advanced": 0
}