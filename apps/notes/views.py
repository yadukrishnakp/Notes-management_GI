from rest_framework import generics, status
from apps.notes.serializers import CreateOrUpdateAboutUsSerializer, DestroyNotesSerializer
from apps.notes.models import NoteManagement
from apps.notes.schemas import GetNotesResponseSchemas
from .response import ResponseInfo
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, render


# create or update APIs.
class CreateOrUpdateNotesAPIView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(CreateOrUpdateNotesAPIView, self).__init__(**kwargs)
        
    serializer_class = CreateOrUpdateAboutUsSerializer
    
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data,context={'request':request})
            if not serializer.is_valid():
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["status"]      = False
                self.response_format["errors"]      = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
            
            instance = serializer.validated_data.get('instance', None)
            serializer = self.serializer_class(instance, data=request.data, context={'request': request})
            if not serializer.is_valid():
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["status"]      = False
                self.response_format["errors"]      = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            self.response_format['status_code'] = status.HTTP_201_CREATED
            self.response_format["message"]     = "Successfully Completed"
            self.response_format["status"]      = True
            return Response(self.response_format, status=status.HTTP_201_CREATED)

        except Exception as e:
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status']      = False
            self.response_format['message']     = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, id):
        try:
            note_instance = get_object_or_404(NoteManagement, pk=id)
            serializer = self.serializer_class(note_instance, data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                self.response_format['status_code'] = status.HTTP_200_OK
                self.response_format["message"] = "Note updated successfully"
                self.response_format["status"] = True
                return Response(self.response_format, status=status.HTTP_200_OK)
            else:
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["status"] = False
                self.response_format["errors"] = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# fetch all data and individual data.
class GetAllNotesAPIView(generics.ListAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetAllNotesAPIView, self).__init__(**kwargs)

    queryset         = NoteManagement.objects.filter().order_by('-id')
    serializer_class = GetNotesResponseSchemas
    search_fields    = ['title', 'body',]
    def get(self, request, *args, **kwargs):
        queryset    = self.filter_queryset(self.get_queryset())

        instance_id = request.GET.get('id', None)
        if instance_id:
            queryset = queryset.filter(pk=instance_id)
        serializer = self.serializer_class(queryset, many=True)
        
        self.response_format['status'] = True
        self.response_format['data']   = serializer.data
        self.response_format['status_code'] = status.HTTP_200_OK
        return Response(self.response_format, status=status.HTTP_200_OK)


# Destroy APIs.
class DestroyNotesApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(DestroyNotesApiView, self).__init__(**kwargs)
    
    serializer_class = DestroyNotesSerializer
    
    def delete(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():

                ids = serializer.validated_data['instance_id']
                NoteManagement.objects.filter(id__in=ids).delete()

                self.response_format['status_code'] = status.HTTP_200_OK
                self.response_format["message"]     = "Successfully Completed"
                self.response_format["status"]      = True
                return Response(self.response_format, status=status.HTTP_200_OK)
            else:
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["status"]      = False
                self.response_format["errors"]      = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status']      = False
            self.response_format['message']     = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




# Web side for rendering templates
def notes_view(request):

    return render(request, 'notes/notes.html')  
