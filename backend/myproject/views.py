from django.http import JsonResponse
from myproject.settings import MONGO_DB

def test_mongo(request):
    # Insert a test document
    MONGO_DB['testcollection'].insert_one({"message": "Hello, MongoDB!"})
    # Fetch the document
    document = MONGO_DB['testcollection'].find_one()
    return JsonResponse({"data": str(document)})