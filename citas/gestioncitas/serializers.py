from rest_framework import serializers
from .models import Cliente, Vendedor, Vehiculo, Cita, Usuario


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'


class VehiculoSerializer(serializers.ModelSerializer):
    vendedores = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Vehiculo
        fields = '__all__'


class VendedorSerializer(serializers.ModelSerializer):
    vehiculos = VehiculoSerializer(many=True, read_only=True)

    class Meta:
        model = Vendedor
        fields = '__all__'


class CitaSerializer(serializers.ModelSerializer):
    cliente = ClienteSerializer(read_only=True)  # Incluye detalles del cliente
    vendedor = VendedorSerializer(read_only=True)  # Incluye detalles del vendedor
    vehiculo = VehiculoSerializer(read_only=True)  # Incluye detalles del vehículo
    cliente_id = serializers.PrimaryKeyRelatedField(queryset=Cliente.objects.all(), source='cliente', write_only=True)
    vendedor_id = serializers.PrimaryKeyRelatedField(queryset=Vendedor.objects.all(), source='vendedor', write_only=True)
    vehiculo_id = serializers.PrimaryKeyRelatedField(queryset=Vehiculo.objects.all(), source='vehiculo', write_only=True)

    class Meta:
        model = Cita
        fields = '__all__'


class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = '__all__'

    def validate(self, data):
        # Agregar validaciones personalizadas
        if 'email' not in data:
            raise serializers.ValidationError("El email es obligatorio.")
        return data

    def create(self, validated_data):
        # Creación de usuario con contraseña encriptada
        user = Usuario(
            email=validated_data['email'],
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
