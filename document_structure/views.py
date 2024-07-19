from django.shortcuts import render
from .models import Folder, Document
from rest_framework.generics import GenericAPIView
from datetime import datetime, timezone
from .serializers import ListFolderSerializer, ListDocumentSerializer, InputFolderSerializer, InputDocumentSerializer
from rest_framework import status
from rest_framework.response import Response
import json

# Create your views here.
class FoldersListView(GenericAPIView):
    """
    """

    def get(self, request):
        '''
        Handles GET request for returning
        '''
        folder_filter = request.GET.get('folder_filter')
        folder_filter = json.loads(folder_filter) if folder_filter else {}

        doc_folder_filter = request.GET.get('doc_folder_filter')
        doc_folder_filter = json.loads(doc_folder_filter) if doc_folder_filter else {}

        folders = Folder.objects.filter(parent=None, is_delete=False, **folder_filter)
        documents = Document.objects.filter(library_folder=None, is_delete=False, **doc_folder_filter)

        folder_serializer = ListFolderSerializer(folders, many=True)
        document_serializer = ListDocumentSerializer(documents, many=True)

        return Response(
            data={
                'folders':folder_serializer.data,
                'documents': document_serializer.data
            },
            status=status.HTTP_200_OK
        )


class CreateFolderView(GenericAPIView):
    """ 
    """
    # authentication_classes = [UserTokenAuthentication]
    serializer_class = InputFolderSerializer

    def post(self, request):
        '''
        Handles POST request for creating Library Folder:

        Args: 
            request: The request object.

        Returns:
            Response: JSON response with details of folder created.
        '''

        serializer = self.InputFolderSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                data={
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': serializer.errors,
                    'data': {}
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer.validated_data['created_by'] = request.user
        serializer.save()
        folder = Folder.objects.get(id=serializer.data['id'])
        serializer = ListFolderSerializer(folder)

        return Response(
            data={
                'status': status.HTTP_201_CREATED,
                'message': serializer.errors,
                'data': {}
            },
            status=status.HTTP_201_CREATED
        )