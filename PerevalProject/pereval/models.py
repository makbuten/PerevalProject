from django.db import models
from django.utils import timezone

def get_image_path(instance, file): # прописываю путь сохранения изображений, у каждой записи PerevalAdded своя папка
    return f'photos/pereval-{PerevalAdded.objects.last().id}/{file}'

# Активность - способ прохождения локации, вывел в список кортежей
ACTIVITIES = [
    ('foot', 'пеший'),
    ('bike', 'велосипед'),
    ('car', 'автомобиль'),
    ('motorbike', 'мотоцикл'),
]

# Вид локации, вывел в список кортежей
BEAUTYTITLE = [
    ('poss', 'перевал'),
    ('mountain_peak', 'горная вершина'),
    ('gorge', 'ущелье'),
    ('plateau', 'плато'),
]

# статус добавленной записи пользователя, списком кортежей
STATUS = [
    ('new', 'новый'),
    ('pending', 'на модерации'),
    ('accepted', 'принят'),
    ('rejected', 'не принят'),
]

# Уровень сложности прохождения локации, списком кортежей
LEVELS = [
    ('', 'не указано'),
    ('1A', '1a'),
    ('1B', '1б'),
    ('2А', '2а'),
    ('2В', '2б'),
    ('3А', '3а'),
    ('3В', '3б'),
    ]

# Собственный класс, хранящий информацию о пользователях
class Users(models.Model):
    mail = models.EmailField('почта', unique=False)# поле электронной почты, оно уникально, по нему проверяю ункикальность пользователей
    phone = models.CharField('телефон', max_length=15)
    name = models.CharField('имя', max_length=30)
    surname = models.CharField('фамилия', max_length=30)
    otch = models.CharField('отчество', max_length=30)

    def __str__(self):
        return f'{self.surname}'

# Координаты локации хранятся в отдельной таблице
class Coords(models.Model):
    latitude = models.FloatField('широта', max_length=9, blank=True)
    longitude = models.FloatField('долгота', max_length=9, blank=True)
    height = models.IntegerField('высота', blank=True)

#отдельная таблица, содержащая уровни сложности прохождения локации в разные времена года
class Levels(models.Model):
    winter = models.CharField('зима', max_length=2, choices=LEVELS, default='')# уровень сложности прохождения локации зимой
    summer = models.CharField('лето', max_length=2, choices=LEVELS, default='')# уровень сложности прохождения локации летом
    autumn = models.CharField('осень', max_length=2, choices=LEVELS, default='')# уровень сложности прохождения локации осенью
    spring = models.CharField('весна', max_length=2, choices=LEVELS, default='')# уровень сложности прохождения локации весной

    def __str__(self):
        return f'зима: {self.winter}, лето: {self.summer}, осень: {self.autumn}, весна: {self.spring}'



# Класс, хранящий данные, переданные пользователем
class PerevalAdded(models.Model):
    status = models.CharField(choices=STATUS, max_length=25, default='new') #статус нового сообщения, по умолчанию Новое
    beautyTitle = models.CharField('тип', choices=BEAUTYTITLE, max_length=50)#тип локации - перевал, ущелье и т.д. списком
    title = models.CharField('название', max_length=50, blank=True)# название локации
    other_titles = models.CharField('иные названия', max_length=50)# описание локации
    connect = models.CharField('соединение', max_length=250)# какие локации соединяет (применимо к перевалу)
    add_time = models.DateTimeField(default=timezone.now, editable=False)#дата/время создания записи (не понял пользователь вручную создает или автоматическое поле при добавлении в БД)
    coord_id = models.OneToOneField(Coords, on_delete=models.CASCADE)# ссылка на объект с координатами локации. Зачем если связь один к одному?
    user = models.ForeignKey(Users, on_delete=models.CASCADE)# автор статьи - ссылка на объект пользователей
    levels = models.OneToOneField(Levels, on_delete=models.CASCADE)# ссылка на объект с уровнем сожности прохождения локации

# класс фотографии добавленные пользователем
class Images(models.Model):
    name = models.CharField(max_length=50)# название фотографии
    photos = models.ImageField('Фото', upload_to=get_image_path, blank=True, null=True)# объект фотографии
    pereval = models.ForeignKey(PerevalAdded, on_delete=models.CASCADE, related_name='images', default=0)# ссылка на объект с перевалом


