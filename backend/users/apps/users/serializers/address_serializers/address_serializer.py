from django.db import transaction

from rest_framework import serializers

from apps.users.models.address import Address


class AddressSerializer(serializers.ModelSerializer):
    # Obtener el nombre de la comuna y de la region para leerlo
    commune_name = serializers.CharField(source='commune.name', read_only=True)
    region_name = serializers.CharField(source='commune.region.name', read_only=True)

    class Meta:
        model = Address
        fields = [
            'id',
            'street',
            'number',
            'apartment',
            'commune',
            'commune_name',
            'region_name',
            'is_main',
            'is_active'
        ]
        read_only_fields = ['is_active']

    # Impedir que otra persona actualice una direccion del usuario, por ende validamos que
    # el usuarrio que haga el request sea el dueño de la direccón
    def validate(self, attrs):
        request = self.context.get('request')

        # si la instancia es distinta de None entonces estamos en update (si es None estamos en Create)
        if self.instance and request:
            if self.instance.user != request.user:
                raise serializers.ValidationError('No es posible modificar una dirección que no te pertenece')
        return attrs
    

    # Si vamos a crear una direccion asignada a un usuario debemos sobreescribir el metodo create
    def create(self, validated_data):
        # Para asignarlo al usuario, primero debemos encontrarlo. El usuario viene en el context
        # Usamos context['request'] con corchetes porque esto nos devuelve un error si es que el contexto no viene
        user = self.context['request'].user

        # Desmarcar otras direcciones si is_main=True. Para eso comprobamos la key is_main
        # Luego hacemos una query buscando la direccion perteneciente al usuario que tenga actualmente
        # is_main en True y le hacemos un update a false
        if validated_data.get('is_main', False):
            Address.objects.filter(user=user, is_main=True).update(is_main=False)
        
        # Ahora creamos la direccion asignale el usuario
        address = Address.objects.create(user=user, **validated_data)
        return address

    def update(self, instance, validated_data):
        # Traemos el usuario para hacer la query de las direcciones
        user = self.context['request'].user
        new_is_main = validated_data.get('is_main', instance.is_main)

        # Si el new_is_main es True y instance.is_main es falso, es decir que si se quiere cambiar de false a true,
        # entonces buscamos si hay una dirección que tenga is_main en true, obviamente que no sea la misma que estamos 
        # actualizando (por eso el exclude) y le actualizamos el is_main a False 
        with transaction.atomic():
            if new_is_main and not instance.is_main:
                main_address = Address.objects.filter(user=user, is_main=True).exclude(id=instance.id)
                if main_address.exists(): 
                    main_address.update(is_main=False)
            instance = super().update(instance, validated_data)
        return instance



