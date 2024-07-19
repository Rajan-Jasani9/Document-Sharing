from rest_framework import serializers
from . models import Folder, Document


class InputFolderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Folder
        fields = ['id', 'name', 'parent']

class ListFolderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Folder
        fields = ['id', 'name', 'parent', 'created_by', 'created_at']

class InputDocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Document
        fields = ['id', 'name', 'library_folder', 'document']

class ListDocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Document
        fields = ['id', 'name', 'library_folder', 'created_by', 'created_at']