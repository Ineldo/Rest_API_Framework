# from django.http import JsonResponse, HttpResponse
import json
from products.models import Products
from django.forms.models import model_to_dict
from rest_framework.response import Response
from rest_framework.decorators import api_view
from products.serializer  import ProductsSerializers


#this request used here it has nothing to do with 
# python requests but  its a http request instace from django
@api_view(["POST"])
def api_home(request, *args, **kwargs):

    data=request.data
    # instance = Products.objects.all().order_by("?").first()
    # data={}
    # if instance:
    #     #data = model_to_dict(instace, fields=['id','title','price']) #convert into dictionary
    #     data= ProductsSerializers(instance).data
    serializer=ProductsSerializers(data=request.data)
    if serializer.is_valid(raise_exception=True):
       # instance=serializer.save()
        print(serializer.data)
        return Response(serializer.data)
    return Response({"invalid":"not so good data"}, status=400)
   

# Create your views here.

    # print(request.GET)#this will get url query params
    # body=request.body # byte string of json data
    # data={}
    # try:
    #     data=json.loads(body)
    # except:
    #     pass
    # print(data)
    # # data['headers'] = request.headers
    # data['params'] = request.GET
    # print(request.headers)
    # data['headers'] =  (dict(request.headers)) #convert into dictionary 
    # data['content_type'] = request.content_type


      # json_data_str= json.dumps(data) 
        # data['id']=model_data.id
        # data['title']=model_data.title
        # data['content']=model_data.content
        # data['price']=model_data.price
        #model_instance(model_data)
        #turn a python dict
        #return json to my client
        