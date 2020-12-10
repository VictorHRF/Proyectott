from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import EcuacionSerializer
from .models import Ecuacion
from django.http import Http404

import numpy as np
from skimage.filters import threshold_otsu
import cv2
from time import time

def otsu( img, T, alto, ancho ):
    res = np.zeros( (alto, ancho), dtype = np.int32 )
    for i in range (alto):
        for j in range (ancho):
            if img[i][j] > T:
                res[i][j] = 255
            else:
                res[i][j] = 0
    return res

def findEquation(img,id):
    tiempo_inicial = time()
    imagen = cv2.imread(img[1:])#le quita un caracter / al inicio para que reconozca la url
    img_arr = np.asarray(imagen)
    alto = img_arr.shape[0]
    ancho = img_arr.shape[1]
    img_gris = np.ndarray(shape=(alto, ancho), dtype=int)
    for i in range(alto):
        for j in range(ancho):
            img_gris[i][j] = int(0.2126 * float(img_arr[i][j][0]) + 0.7152 * float(img_arr[i][j][1]) + 0.0722 * float(img_arr[i][j][2]))
    resf = otsu(img_gris, threshold_otsu(img_gris), alto, ancho)
    tiempo_final = time()
    tiempo_ejecucion = tiempo_final - tiempo_inicial
    print('El tiempo de ejecucion fue:', tiempo_ejecucion)
    cv2.imwrite("media/ecuaciones/Res"+str(id)+".jpg", resf)

class EcuacionList(APIView):
    parser_class = (FileUploadParser,)

    def post(self,request):
        ecuacion_serializer = EcuacionSerializer(data=request.data)
        if ecuacion_serializer.is_valid():
            ecuacion_serializer.save()
            dataImg = ecuacion_serializer.data
            print("img: ", dataImg['imagen'],"id: ",dataImg['id'])
            findEquation(dataImg['imagen'],dataImg['id'])
            return Response(ecuacion_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(ecuacion_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EcuacionDetail(APIView):
    parser_class = (FileUploadParser,)
    def get_object(self, pk):
        try:
            return Ecuacion.objects.filter(pk=pk)
        except Ecuacion.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        ecuacion = self.get_object(pk)
        ecuacion_serializer = EcuacionSerializer(ecuacion, many=True)
        return Response(ecuacion_serializer.data)