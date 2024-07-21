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
    

class CutCopyOperationPasteView(GenericAPIView):

    def post(self, request):
        '''
        Example Payload:
            {
                'source_folder/document_id': id,
                'destination_folder': id,
                'operation': 'cut'/'copy',
            }
        '''
        source_folders = request.data.get('source_folders', [])
        source_documents = request.data.get('source_documents', [])
        operation = request.data.get('operation',None)
        destination_folder = request.data.get('destination_folder', None)

        if not operation:
            return Response(
                data={
                    'message':'API Payload not accurate!!',
                    'status':status.HTTP_400_BAD_REQUEST,
                    'data': {}
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        destination_folder = Folder.objects.filter(id=destination_folder, is_delete=False).first() if destination_folder else None

        if operation == 'cut':
            for folder in source_folders:
                folder = Folder.objects.filter(id=folder, is_delete=False).first()
                folder.parent = destination_folder
                folder.save()

            for document in source_documents:
                document = Document.objects.filter(id=document, is_delete=False).first()
                document.library_folder = destination_folder 
                document.save()

        if operation == 'copy':
            # keeping pending till decision of database is decided for documents.
            pass

        return Response(
            data={
                'message': f'{operation.capitalize()} operation performed successfully',
                'status':status.HTTP_200_OK,
                'data': {}
            },
            status=status.HTTP_200_OK
        )



## Helper Functions section:

def copy_sub_folders(folder, new_folder):
    '''
    Recursive function to copy all subfolders:  
    '''
    sub_folders = Folder.objects.filter(parent=folder, is_delete=False)

    if sub_folders.count() == 0:
        return True

    for sub_folder in sub_folders:
        new_copied_folder = Folder.objects.create(parent=new_folder)
        copy_sub_folders(sub_folder, new_copied_folder)

    return True

def copy_sub_documents(folder, new_folder):

    documents=Document.objects.filter(library_folder=folder, is_delete=False)
    # keeping pending based on decision on where to set up database as code will differ accordingly!!
    pass