from rest_framework import serializers
from .models import *



class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('mail', 'phone', 'name', 'surname', 'otch')
    # при сохранении пользователя, проверяем по емайлу его наличие в БД, если есть то возвращаем уже сохраненного, инача сохраняем нового
    def save(self, **kwargs):
        self.is_valid()
        print('тест сохранения')
        user = Users.objects.filter(mail=self.validated_data.get('mail'))
        print('test', self.validated_data.get('mail'))
        if user.exists():
            return user.first()
        else:
            new_user = Users.objects.create(
                surname=self.validated_data.get('surname'),
                name=self.validated_data.get('name'),
                otch=self.validated_data.get('otch'),
                phone=self.validated_data.get('phone'),
                mail=self.validated_data.get('mail'),
            )
            return new_user


class ImagesSerializer(serializers.ModelSerializer):
    photos = serializers.CharField()
    class Meta:
        model = Images
        fields = ('name', 'photos', 'pereval')


class CoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coords
        fields = ('latitude', 'longitude', 'height')

# сериализатор вложенной модели уровней сложности перевала
class LevelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Levels
        fields = [
            'winter',
            'summer',
            'autumn',
            'spring',
        ]


class PerevalAddedSerializer(serializers.ModelSerializer):
    user = UsersSerializer(required=False)
    coord_id = CoordsSerializer(required=False)
    images = ImagesSerializer(required=False, many=True)
    levels = LevelsSerializer(required=False)
    class Meta:
        model = PerevalAdded
        fields = ('status', 'beautyTitle', 'title', 'other_titles', 'connect', 'add_time', 'coord_id',
                  'levels', 'user', 'images')

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

    def update(self, instance, validated_data):
        # разбиваем словарь validated_data на таблицы
        user_data = validated_data.pop('user')
        coords_data = validated_data.pop('coord_id')
        images_data = validated_data.pop('images')
        levels_data = validated_data.pop('levels')
        print('test update', validated_data)
        print('test', instance)
        # получаю объекты связанных с текущим объектом таблиц
        user = instance.user
        coords = instance.coord_id
        levels = instance.levels
        # вношу изменения в поля основной таблицы
        instance.beautyTitle = validated_data.get('beautyTitle', instance.beautyTitle)
        instance.title = validated_data.get('title', instance.title)
        instance.other_titles = validated_data.get('other_titles', instance.other_titles)
        instance.connect = validated_data.get('connect', instance.connect)
        instance.save()
        # вношу изменения в таблицу координат
        coords.latitude = coords_data.get('latitude', coords.latitude)
        coords.longitude = coords_data.get('longitude', coords.longitude)
        coords.height = coords_data.get('height', coords.height)
        coords.save()
        # вношу изменения в таблицу уровней
        levels.winter = levels_data.get('winter', levels.winter)
        levels.summer = levels_data.get('summer', levels.summer)
        levels.autumn = levels_data.get('autumn', levels.autumn)
        levels.spring = levels_data.get('spring', levels.spring)
        levels.save()
        # получаю объекты модели Images, связанные с текущим объектом модели PerevalAdded (а надо ли? удалить и вписать новые или к старым добавить новые?)
        images = Images.objects.filter(pereval=instance)
        # удаляю старые объекты
        images.delete()
        # записываю новые объекты изображения
        if images_data:
            for imag in images_data:
                name = imag.pop('name')
                photos = imag.pop('photos')
                Images.objects.create(pereval=instance, name=name, photos=photos)

        return instance

    def validate(self, data):
        if self.instance is not None:
            instance_user = self.instance.user
            data_user = data.get('user')
            user_fields_for_validation = [
                instance_user.surname != data_user['surname'],
                instance_user.name != data_user['name'],
                instance_user.otch != data_user['otch'],
                instance_user.phone != data_user['phone'],
                instance_user.mail != data_user['mail'],
            ]
            if data_user is not None and any(user_fields_for_validation):
                raise serializers.ValidationError(
                    {
                        'Отказано': 'Данные пользователя не могут быть изменены',
                    }
                )
        return data
