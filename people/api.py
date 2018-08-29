import json
from django.http import Http404
from rest_framework import permissions, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request

from people.models import Person, Group, Circle, Membership, PersonMeta
from people.serializers import PersonSerializer, GroupSerializer, \
    GroupListSerializer, CircleSerializer, PersonMetaGetSerializer, \
    PersonMetaPostSerializer
from fitness_connector.activity import PersonActivity


# HELPER METHODS
def get_person(user_id):
    # type: (str) -> Person
    try:
        return Person.objects.get(user__id=user_id)
    except Person.DoesNotExist:
        print("person not found")
        raise Http404

def get_group(person):
    # type: (Person) -> Group
    try:
        return Group.objects.get(members=person)
    except Group.DoesNotExist:
        print("group not found")
        raise Http404

def get_person_meta(person):
    # type: (Person) -> Optional(PersonMeta)
    try:
        return PersonMeta.objects.filter(person=person).first()
    except PersonMeta.DoesNotExist:
        raise Http404

def get_circle(person, circle_id):
    # type: (Person, int) -> Circle
    try:
        return Circle.objects.get(members=person, id=circle_id)
    except Circle.DoesNotExist:
        raise Http404


# CLASSES
class UserInfo(APIView):
    """
    Retrieve current User's detailed information
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        person = get_person(request.user.id)
        serializer = PersonSerializer(person)
        return Response(serializer.data)


class UserGroupInfo(APIView):
    """
    Retrieve the Group's detailed information in which the logged User
    belongs to
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        person = get_person(request.user.id)
        group = get_group(person)
        serializer = GroupSerializer(group)
        return Response(serializer.data)


class UserCircleInfo(APIView):
    """
    Retrieve a Circle's detailed information in which the logged User
    belongs to
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, circle_id, format=None):
        person = get_person(request.user.id)
        circle = get_circle(person, circle_id)
        serializer = CircleSerializer(circle)
        return Response(serializer.data)


class PersonProfileInfo(APIView):
    """
    GET request returns the Person's profile.
    POST request sets the Person's profile.
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, person_id, format=None):
        logged_person = get_person(request.user.id)
        group = get_group(logged_person)

        if Membership.is_member(group, person_id) is False:
            output = {"message": "Not authorized"}
            return Response(output, status=status.HTTP_400_BAD_REQUEST)
        else:
            person = Membership.get_member(group, person_id)
            person_meta = person.get_meta()
            serializer = PersonMetaGetSerializer(person_meta)
            return Response(serializer.data)

    def post(self, request, person_id, format=None):
        logged_person = get_person(request.user.id)
        group = get_group(logged_person)
        validator = PersonMetaPostSerializer(data=request.data) # type: PersonMetaPostSerializer
        if Membership.is_member(group, person_id) is False:
            output = {"message": "Can't update this person's metadata"}
            return Response(output, status=status.HTTP_400_BAD_REQUEST)
        elif validator.is_valid():
            validated_data = validator.validated_data  # type: dict
            person = Membership.get_member(group, person_id)
            person.set_meta_profile(json.dumps(validated_data['profile_json']))
            return Response(validated_data, status.HTTP_200_OK)
        else:
            errors = validator.errors
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


# CLASSES FOR ADMIN VIEWS (CURRENTLY NOT USED)
class PersonList(generics.ListAPIView):
    """
    List all Persons
    """
    permission_classes = (permissions.IsAdminUser,)
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class PersonInfo(APIView):
    """
    Retrieve a Person's detailed information
    """
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request, person_id, format=None):
        person = get_person(person_id)
        person_activity = PersonActivity(person_id)
        response = {
            'person': {
                'person_id': person_id,
                'name': person.name,
                'last_pull_time': person_activity.account.last_pull_time
            }
        }
        return Response(response)


class GroupList(generics.ListAPIView):
    """
    List all Families
    """
    permission_classes = (permissions.IsAdminUser,)
    queryset = Group.objects.all()
    serializer_class = GroupListSerializer


class GroupInfo(APIView):
    """
    Retrieve a Group's detailed information
    """
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request, group_id, format=None):
        group = get_person(group_id)
        serializer = GroupSerializer(group)
        return Response(serializer.data)
