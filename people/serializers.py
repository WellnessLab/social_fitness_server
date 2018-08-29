from django.db.models.query import QuerySet
import json
from rest_framework import serializers
from people.models import Person, Group, Membership, Circle, CircleMembership, PersonMeta
from fitness_connector.models import Account


# HELPER METHODS
def get_person_meta_profile_json(person):
    # type: (Person) -> object
    person_meta = PersonMeta.objects.filter(person=person)

    if person_meta.exists():
        return json.loads(person_meta.first().profile_json)
    else:
        return None


# CLASSES
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('user_id', 'last_pull_time', 'device_version')


class PersonMetaGetSerializer(serializers.ModelSerializer):
    profile_json = serializers.SerializerMethodField()

    class Meta:
        model = PersonMeta
        fields = ('profile_json', )

    def get_profile_json(self, obj):
        return json.loads(obj.profile_json)


class PersonMetaPostSerializer(serializers.ModelSerializer):
    profile_json = serializers.JSONField()

    class Meta:
        model = PersonMeta
        fields = ('profile_json', )


class PersonSerializer(serializers.ModelSerializer):
    account = serializers.SerializerMethodField()
    profile = serializers.SerializerMethodField()

    class Meta:
        model = Person
        fields = ('id', 'name', 'account', 'profile')

    def get_account(self, obj):
        account = Account.objects.filter(person=obj)

        if account.exists():
            serialized = AccountSerializer(account.first())
            return serialized.data
        else:
            return None

    def get_profile(self, obj):
        return get_person_meta_profile_json(obj)


class MembershipSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="person.id")
    name = serializers.ReadOnlyField(source="person.name")
    account = serializers.SerializerMethodField()
    profile = serializers.SerializerMethodField()

    class Meta:
        model = Membership
        fields = ('id', 'name', 'role', 'account', 'profile')

    def get_account(self, obj):
        account = Account.objects.filter(person__id=obj.id)

        if account.exists():
            serialized = AccountSerializer(account.first())
            return serialized.data
        else:
            return None

    def get_profile(self, obj):
        return get_person_meta_profile_json(obj.person)


class CircleMembershipSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="person.id")
    name = serializers.ReadOnlyField(source="person.name")
    profile = serializers.SerializerMethodField()

    class Meta:
        model = CircleMembership
        fields = ('id', 'name', 'profile')

    def get_profile(self, obj):
        return get_person_meta_profile_json(obj.person)


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
