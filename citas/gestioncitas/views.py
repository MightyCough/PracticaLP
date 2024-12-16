from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.utils import timezone
from rest_framework.decorators import action
from .models import *
from .serializers import *
# Create your views here.

# ViewSet para Cliente
class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

    @action(detail=False, methods=['get'])
    def recientes(self, request):
        # Devuelve los clientes registrados en los últimos 7 días
        recientes = Cliente.objects.filter(fecha_registro__gte=timezone.now() - timezone.timedelta(days=7))
        serializer = self.get_serializer(recientes, many=True)
        return Response(serializer.data)

# ViewSet para Vendedor
class VendedorViewSet(viewsets.ModelViewSet):
    queryset = Vendedor.objects.all()
    serializer_class = VendedorSerializer

    def create(self, request, *args, **kwargs):
        # verifica que se envíe al menos un vehículo
        if 'vehiculos' not in request.data or not request.data['vehiculos']:
            return Response({"error": "Debes asignar al menos un vehículo al vendedor."}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

# ViewSet para Vehiculo
class VehiculoViewSet(viewsets.ModelViewSet):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer

    @action(detail=False, methods=['get'])
    def disponibles(self, request):
        # Devuelve vehículos disponibles
        disponibles = Vehiculo.objects.filter(disponible=True)
        serializer = self.get_serializer(disponibles, many=True)
        return Response(serializer.data)

class CitaViewSet(viewsets.ModelViewSet):
    queryset = Cita.objects.all()
    serializer_class = CitaSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data['fecha_cita'] < timezone.now():
            return Response({'error': 'La fecha de la cita no puede ser en el pasado.'}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    


# ViewSet para Usuario
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    
    
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username
        })