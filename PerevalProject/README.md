# Виртуальная стажировка. Проект Pereval

# 1. Создание виртуального окружения:
python -m venv venv_pereval
# 2. Активировать виртуальное окружение:
source venv_pereval/bin/activate
# 3. Установка django:
pip install django
# 4. Создание проекта PerevalProject:
django-admin startproject PervalProject
# 5. Создание приложения pereval:
cd PerevalProject
python3 manage.py startapp pereval
# 6. Создание базы данных postgresql в терминале:
**Используемая СУБД - PostgreSQL**

Командная строка postgresql:
**sudo -i -u postgres**

Создать БД:
**createdb pereval_db**

Консоль суперпользователя:
**psql**

Установить пароль суперпользователя:
**ALTER USER postgres WITH PASSWORD 'мой стандартный пароль';**

Создать нового пользователя:
**CREATE USER makbutenko WITH PASSWORD 'мой стандартный пароль';**

Дал права суперпользователя новому пользователю:
**ALTER USER makbutenko WITH SUPERUSER;**

Команды: 
**\q** выход с консоли суперюзера;
**\l** просмотр существующих БД;
**\du** просмотр списка пользователей;
**exit** выход с консоли postgresql/

# 7. Описание моделей:

Данные, являющиеся константами, практически не изменяющиеся, выведены за пределы моделей в списки кортежей, такие как:

1) Активность - способ прохождения локации, вывел в список кортежей

`ACTIVITIES = [
    ('foot', 'пеший'),
    ('bike', 'велосипед'),
    ('car', 'автомобиль'),
    ('motorbike', 'мотоцикл'),
]`

2) Вид локации, вывел в список кортежей

`BEAUTYTITLE = [
    ('poss', 'перевал'),
    ('mountain_peak', 'горная вершина'),
    ('gorge', 'ущелье'),
    ('plateau', 'плато'),
]`

3) статус добавленной записи пользователя, списком кортежей
`STATUS = [
    ('new', 'новый'),
    ('pending', 'на модерации'),
    ('accepted', 'принят'),
    ('rejected', 'не принят'),
]`

4) Уровень сложности прохождения локации, списком кортежей
`LEVELS = [
    ('', 'не указано'),
    ('1A', '1a'),
    ('1B', '1б'),
    ('2А', '2а'),
    ('2В', '2б'),
    ('3А', '3а'),
    ('3В', '3б'),
    ]`

*Модель PerevalAdded - основные данные добавленные туристом:*

`class PerevalAdded(models.Model):
    status = models.CharField(choices=STATUS, max_length=25, default='new') #статус нового сообщения, по умолчанию Новое
    beautyTitle = models.CharField('тип', choices=BEAUTYTITLE, max_length=50)#тип локации - перевал, ущелье и т.д. списком
    title = models.CharField('название', max_length=50, blank=True)# название локации
    other_titles = models.CharField('иные названия', max_length=50)# описание локации
    connect = models.CharField('соединение', max_length=250)# какие локации соединяет (применимо к перевалу)
    add_time = models.DateTimeField(default=timezone.now, editable=False)#дата/время создания записи (не понял пользователь вручную создает или автоматическое поле при добавлении в БД)
    coord_id = models.OneToOneField(Coords, on_delete=models.CASCADE)# ссылка на объект с координатами локации. Зачем если связь один к одному?
    user = models.ForeignKey(Users, on_delete=models.CASCADE)# автор статьи - ссылка на объект пользователей
    levels = models.OneToOneField(Levels, on_delete=models.CASCADE)# ссылка на объект с уровнем сожности прохождения локации`

*Модель User - основные данные о туристе:*

`class Users(models.Model):
    mail = models.EmailField('почта', unique=True)# поле электронной почты, оно уникально, по нему проверяю уникальность пользователей
    phone = models.CharField('телефон', max_length=15)
    name = models.CharField('имя', max_length=30)
    surname = models.CharField('фамилия', max_length=30)
    otch = models.CharField('отчество', max_length=30)

    def __str__(self):
        return f'{self.surname}'`

*Модель Coords - Координаты локации, переданные туристом*

`class Coords(models.Model):
    latitude = models.FloatField('широта', max_length=9, blank=True)
    longitude = models.FloatField('долгота', max_length=9, blank=True)
    height = models.IntegerField('высота', blank=True)`

*класс Images фотографии добавленные пользователем*

`class Images(models.Model):
    name = models.CharField(max_length=50)# название фотографии
    photos = models.ImageField('Фото', upload_to=get_image_path, blank=True, null=True)# объект фотографии
    pereval = models.ForeignKey(PerevalAdded, on_delete=models.CASCADE, related_name='images', default=0)# ссылка на объект с перевалом`

*класс Levels уровень сложности прохождения локации*

`class Levels(models.Model):
    winter = models.CharField('зима', max_length=2, choices=LEVELS, default='')# уровень сложности прохождения локации зимой
    summer = models.CharField('лето', max_length=2, choices=LEVELS, default='')# уровень сложности прохождения локации летом
    autumn = models.CharField('осень', max_length=2, choices=LEVELS, default='')# уровень сложности прохождения локации осенью
    spring = models.CharField('весна', max_length=2, choices=LEVELS, default='')# уровень сложности прохождения локации весной`

    def __str__(self):
        return f'зима: {self.winter}, лето: {self.summer}, осень: {self.autumn}, весна: {self.spring}'

# 8 Проектирование Views и Serializers

*установка Django Rest Framework:*
`pip install djangorestframework`

Для заполнения и тестирования работоспособности отдельных таблиц, создал 
классы для отдельных таблиц на основе generics.ListCreateAPIView и generics.RetrieveUpdateDestroyAPIView, 
доступные по запросу api/v1/название_модели - для просмотра списком или добавления, 
api/v1/название_модели/pk - для редактирования, удаления.

Для реализации метода submitData используются классы на основе viewsets.ModelViewSet,
доступные по запросу api/v2/submitData

Реализация метода submitData заключается в том, что турист (клиентское приложение)
отправляет POST запрос в формате JSON содержащий все необходимые данные.
Далее, полученный от туриста JSON на стадии валидации переводится в список словарей validated_data
который разделяется на блоки, содержащие данные отдельных таблиц,
например Users, Coords, Images

user = validated_data.pop('user')
coords = validated_data.pop('coord_id')
images = validated_data.pop('images')

Отдельные блоки данных сохраняются в побочные таблицы:

user = Users.objects.create(**user)
coords = Coords.objects.create(**coords)

затем в основную таблицу PerevalAdded добаляются оставшиеся данные и ссылки на побочные объекты таблиц

`pereval_new = PerevalAdded.objects.create(**validated_data, images=images, author=user, coord_id=coords)`

Данная процедура реализуется в методе create сериализатора PerevalAddedSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        # разбиваем словарь validated_data на таблицы
        user = validated_data.pop('user')
        coords = validated_data.pop('coord_id')
        images = validated_data.pop('images')
        levels = validated_data.pop('levels')
        # Создаем нового автора или возвращаем модель существующего
        current_user = Users.objects.filter(mail=user['mail'])
        if current_user.exists():
            user_serializers = UsersSerializer(data=user)
            user_serializers.is_valid(raise_exception=True)
            user = user_serializers.save()
        else:
            user = Users.objects.create(**user)

        coords = Coords.objects.create(**coords)

        levels = Levels.objects.create(**levels)

        pereval_new = PerevalAdded.objects.create(**validated_data, user=user, coord_id=coords, levels=levels)

        if images:
            for imag in images:
                name = imag.pop('name')
                photos = imag.pop('photos')
                Images.objects.create(pereval=pereval_new, name=name, photos=photos)

        return pereval_new

Получение списка загруженных данных по локациям осуществляется по GET запросу на адрес api/v2/submitData, по средствам
встроенного представления viewsets.ModelViewSet.

Получение конкретной записи по первичному ключу осуществляется по GET запросу на адрес api/v2/submitData/pk, путем 
переопределения метода retrieve() в классе PerevalAddedViewSet(viewsets.ModelViewSet)

    def retrieve(self, request, pk=None):
        queryset = self.queryset
        pereval = get_object_or_404(queryset, pk=pk)
        images_obj = Images.objects.filter(pereval=pereval)
        images_ser = ImagesSerializer(images_obj, many=True).data
        return Response({'pereval': self.serializer_class(pereval).data, 'images': images_ser})

т.е. получаю queryset содержащий все объекты модели PerevalAdded, далее получаем конкретный объект по переданному в метод первичному ключю
при помощи метода get_object_or_404(queryset, pk=pk). Фильтрую объекты модели Images по полю pereval, равному полученному объекту PerevalAdded
images_obj = Images.objects.filter(pereval=pereval), после чего провожу сериализацию images_ser = ImagesSerializer(images_obj, many=True).data.
Возвращаю сериализованные данные объекта PerevalAdded и полученные данные объекта Images, сформированные в формат JSON


Изменение конкретного объекта модели PerevalAdded осуществляется patch запросом на адрес api/v2/submitData/pk, реализуется встроенными методами инструмента 
WritableNestedModelSerializer из пакета drf-writable-nested

pip install drf-writable-nested

Получение записей конкретного автора, осуществляется по GET запросу, содержащему параметр 'user__mail' равный электронной почте автора, на адрес
api/v2/submitData/

api/v2/submitData/user__mail=User@gmail.com

реализуется в методе get_queryset(self) класса PerevalAddedViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        queryset = PerevalAdded.objects.all()
        user = self.request.query_params.get('user__email', None)
        if user is not None:
           queryset = queryset.filter(user__mail=user)
        return queryset

получаю queryset равный всем объектам модели PerevalAdded - queryset = PerevalAdded.objects.all() , получаю mail автора из переданного GET запросом параметра 'user__email'
user = self.request.query_params.get('user__email', None), если параметр в запросе существует, то
фильтрую полученный queryset по связанному полю user - queryset = queryset.filter(user__mail=user).
Передаю queryset.

# Комментарии:

Все требуемые в ТЗ функции выполняются в api/v2/submitData, все функции доступные по api/v1/

# Развертывание приложения на хостинге:

Опубликованное на хостинге приложение использует БД sqlite, рабочий проект использует postgerql 

Хостинг: [pythonanywhere.com](www.pythonanywhere.com)

Ссылка на проект: [makbutenko.pythonanywhere.com](makbutenko.pythonanywhere.com)

# Зависимости:

1. pip install django
2. pip install djangorestframework
3. pip install django-filter

# Примеры JSON:

1) Пример добавления новой записи POST запросом по адресу `api/v2/submitData `:

`{
    "status": "new",
    "beautyTitle": "poss",
    "title": "Тестовый перевал",
    "other_titles": "перевал",
    "connect": "соединяет две равнины",
    "coord_id": {
        "latitude": "63.256",
        "longitude": "85.596",
        "height": "1657"
    },
    "levels": {
        "winter": "1A",
        "summer": "",
        "autumn": "",
        "spring": ""
    },
    "user": {
        "mail": "User@example.com",
        "phone": "89104564645",
        "name": "Boris",
        "surname": "Vardanov",
        "otch": "Sergeevich"
    },
    "images": [{"photos":"/Users/MAX/Desktop/фото для перевала/42483f0d38b9408698e3396b0fa1dee2.max-1200x800.jpg", "name":"Седловина"}, {"photos":"/Users/MAX/Desktop/фото для перевала/42483f0d38b9408698e3396b0fa1dee2.max-1200x800.jpg", "name":"Седловина"}]
}`

2) Пример редактирования конкретной записи PATCH запросом по адресу `api/v2/submitData/<pk:int> `: 
Подается аналогичный добавлению новой записи JSON запрос
3) Пример JSON получения конкретной записи GET запросом по адресу `api/v2/submitData/<pk:int> `:

`{
    "pereval": {
        "status": "new",
        "beautyTitle": "poss",
        "title": "Третий Тестовый перевал",
        "other_titles": "изменил название",
        "connect": "изменил текст соединяет две равнины",
        "add_time": "2023-09-17T07:25:02.737496Z",
        "coord_id": {
            "latitude": 86.5531,
            "longitude": 27.5917,
            "height": 8848
        },
        "levels": {
            "winter": "1A",
            "summer": "1A",
            "autumn": "1A",
            "spring": ""
        },
        "user": {
            "mail": "makbutenko@mail.ru",
            "phone": "89105011701",
            "name": "Maksim",
            "surname": "Butenko",
            "otch": "Aleksandrovich"
        },
        "images": [
            {
                "name": "Седловина",
                "photos": "/Users/MAX/Desktop/фото для перевала/42483f0d38b9408698e3396b0fa1dee2.max-1200x800.jpg",
                "pereval": 30
            },
            {
                "name": "Седловина",
                "photos": "/Users/MAX/Desktop/фото для перевала/42483f0d38b9408698e3396b0fa1dee2.max-1200x800.jpg",
                "pereval": 30
            }
        ]
    }
}`