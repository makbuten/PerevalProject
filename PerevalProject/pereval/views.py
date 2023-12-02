import django_filters
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import generics
from .serializers import *
from  rest_framework import viewsets, status

# сериализеры для работы с данными таблиц, просмотр, добавление, удаление
class PerevalAddedListAPIView(generics.ListCreateAPIView):# сериализер для работы с таблицей перевалов, просмотр, добавление
    queryset = PerevalAdded.objects.all()
    serializer_class = PerevalAddedSerializer

class PerevalAddedDetailAPIView(generics.RetrieveUpdateDestroyAPIView):# универсальный сериализер для работы с объектом перевалов, редактирование, удаление
    queryset = PerevalAdded.objects.all()
    serializer_class = PerevalAddedSerializer

class UsersListAPIView(generics.ListCreateAPIView):# универсальный сериализер для работы с таблицей пользователей, просмотр, добавление
    queryset = Users.objects.all()
    serializer_class = UsersSerializer

class UserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):# универсальный сериализер для работы с объектом пользователей, редактирование, удаление
    queryset = Users.objects.all()
    serializer_class = UsersSerializer


class ImagesListAPIView(generics.ListCreateAPIView):# сериализер для работы с таблицей фотографий, просмотр, добавление
    queryset = Images.objects.all()
    serializer_class = ImagesSerializer

class ImagesDetailAPIView(generics.RetrieveUpdateDestroyAPIView):# универсальный сериализер для работы с объектом фотографии, редактирование, удаление
    queryset = Images.objects.all()
    serializer_class = ImagesSerializer

class CoordsListAPIView(generics.ListCreateAPIView):# сериализер для работы с таблицей координат, просмотр, добавление
    queryset = Coords.objects.all()
    serializer_class = CoordsSerializer

class CoordsDetailAPIView(generics.RetrieveUpdateDestroyAPIView):# универсальный сериализер для работы с объектом координат, редактирование, удаление
    queryset = Coords.objects.all()
    serializer_class = CoordsSerializer

# Классы для реализации submitData, так же универсальные, можно добавлять, редактировать, удалять, просматривать, доступны по адресу api/v2/
class PerevalAddedViewSet(viewsets.ModelViewSet):
    queryset = PerevalAdded.objects.all()
    serializer_class = PerevalAddedSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ('user__mail',)
    http_method_names = ['get', 'post', 'head', 'patch', 'options']

    def retrieve(self, request, pk=None):
        queryset = self.queryset
        pereval = get_object_or_404(queryset, pk=pk)
        images_obj = Images.objects.filter(pereval=pereval)
        images_ser = ImagesSerializer(images_obj, many=True).data
        return Response({'pereval': self.serializer_class(pereval).data, 'images': images_ser})


    #переопределяю метод, для вывода сообщения о результатах сохранения данных
    def create(self, request, *args, **kwargs):
        serializer = PerevalAddedSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'status': status.HTTP_200_OK,
                    'message': 'Выполнено',
                    'id': serializer.data[id]
                }
            )
        if status.HTTP_400_BAD_REQUEST:
            return Response(
                {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'не выполнено',
                    'id': None
                }
            )
        if status.HTTP_500_INTERNAL_SERVER_ERROR:
            return Response(
                {
                    'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'message': 'Ошибка при выполнении операции',
                    'id': None
                }
            )


    # даем возможность частично изменять перевал
    def partial_update(self, request, pk=None, *args, **kwargs):
        print('тест вьюшки')
        pereval_new = self.get_object()
        if pereval_new.status == 'new':
            serializer = PerevalAddedSerializer(pereval_new, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        'state': '1',
                        'message': 'Изменения успешно внесены'
                    }
                )
            else:
                return Response(
                    {
                        'state': '0',
                        'message': serializer.errors
                    }
                )
        else:
            return Response(
                {
                    'state': '0',
                    'message': f'Текущий статус: {pereval_new.get_status_display()}, данные не могут быть изменены!'
                }
            )
# Меняем кверисет под фильтрацию по электронной почте автора
    def get_queryset(self):
        queryset = PerevalAdded.objects.all()
        user = self.request.query_params.get('user__email', None)
        if user is not None:
           queryset = queryset.filter(user__mail=user)
        return queryset

class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer

class ImagesViewSet(viewsets.ModelViewSet):
    queryset = Images.objects.all()
    serializer_class = ImagesSerializer


class CoordViewSet(viewsets.ModelViewSet):
    queryset = Coords.objects.all()
    serializer_class = CoordsSerializer

class LevelsViewSet(viewsets.ModelViewSet):
    queryset = Levels.objects.all()
    serializer_class = LevelsSerializer


