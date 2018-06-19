from rest_framework import serializers
from people.models import Person, Group, Membership, Circle, CircleMembership
from fitness_connector.models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('user_id', 'last_pull_time', 'device_version')


class PersonSerializer(serializers.ModelSerializer):
    #account = AccountSerializer(read_only=True)
    account = serializers.SerializerMethodField()

    class Meta:
        model = Person
        fields = ('id', 'name', 'account')

    def get_account(self, obj):
        account = Account.objects.filter(person__id=obj.id)

        if (account.exists()):
            serialized = AccountSerializer(account.first())
            return serialized.data
        else:
            return None;


class MembershipSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="person.id")
    name = serializers.ReadOnlyField(source="person.name")
    account = serializers.SerializerMethodField()

    class Meta:
        model = Membership
        fields = ('id', 'name', 'role', 'account')

    def get_account(self, obj):
        account = Account.objects.filter(person__id=obj.id)

        if (account.exists()):
            serialized = AccountSerializer(account.first())
            return serialized.data
        else:
            return None;


class CircleMembershipSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="person.id")
    name = serializers.ReadOnlyField(source="person.name")

    class Meta:
        model = CircleMembership
        fields = ('id', 'name')


class GroupListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name', 'members')


class GroupSerializer(serializers.ModelSerializer):
    members = MembershipSerializer(source="membership_set", many=True)

    class Meta:
        model = Group
        fields = ('id', 'name', 'members', )


class CircleSerializer(serializers.ModelSerializer):
    members = CircleMembershipSerializer(source="circlemembership_set", many=True)

    class Meta:
        model = Circle
        fields = ('id', 'name', 'members', )
        