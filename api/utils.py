# from rest_framework.response import Response
# from rest_framework import status

# def create_response(data=None, message=None, status_code=status.HTTP_200_OK, error=None):
#     response_data = {}

#     if error:
#         response_data['message'] = error
#         # response_data['message'] = message
#         response_data['status'] = status_code
#     else:
#         response_data['data'] = data
#         response_data['message'] = message
#         response_data['status'] = status_code
    
#     return Response(response_data, status=status_code)


from rest_framework.response import Response
from rest_framework import status

def create_response(data=None, message=None, status_code=status.HTTP_200_OK, error=None):
    response_data = {}

    if error:
        response_data['message'] = error
        response_data['status'] = status_code
    else:
        if data is not None:
            response_data['data'] = data
        response_data['message'] = message
        response_data['status'] = status_code

    return Response(response_data, status=status_code)
