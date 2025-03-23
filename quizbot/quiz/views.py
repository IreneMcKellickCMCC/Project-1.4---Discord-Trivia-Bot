from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.views import Response
from .models import Question
from .serializers import RandomQuestionSerializer

# Create your views here.
# Using APIView to utilize interface

class RandomQuestion(APIView):
    #Bot requests questions via get
    def get(self, request, formate=None, **kwargs):
        #Query, running a filter
        question = Question.objects.filter().order_by('?')[:1]
        #Running question through serializer and filtering out unwanted answers
        serializer = RandomQuestionSerializer(question, many=True)
        return Response(serializer.data)