from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import jwt
import datetime
import json
from .serializers import UserSerializer, LoginSerializer, ChangePasswordSerializer, ForgotPasswordSerializer, FOBSerializer
from users.models import users
from bcrypt import hashpw, gensalt, checkpw

def generate_token(username):
    ist_timezone = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
    current_time_ist = datetime.datetime.now(ist_timezone)

    token = jwt.encode({
        'username': username,
        'exp': current_time_ist + datetime.timedelta(days=7)
    }, "app.config['SECRET_KEY']", algorithm='HS256')
    return token

class Register(APIView):

    def post(self, request):
        data = request.data
        print(data)
        data['password'] = hashpw(
            data.get('password').encode('utf-8'), gensalt()).decode('utf-8')
        
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Registered successfully", "isRegistered": True}, status=status.HTTP_201_CREATED)
        
        error_messages = []
        for field, errors in serializer.errors.items():
            for error in errors:
                error_messages.append(f"{field}: {error}")

        return Response(
            {
                "message": "Failed to Register",
                "isRegistered": False,
                "errors": error_messages,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

class LoginView(APIView):
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            try:
                user = users.objects.get(username=username)
            except users.DoesNotExist:
                return Response({'message': 'Username does not exists.','isLoggedIn':False}, status=status.HTTP_401_UNAUTHORIZED)

            try:
                if checkpw(password.encode('utf-8'),
                           user.password.encode('utf-8')):
                    return Response({'message': 'Authentication successful', 'isLoggedIn': True, 'token': generate_token(username)}, status=status.HTTP_200_OK)
            except:
                return Response({'message': 'Incorrect username or password', 'isLoggedIn': False}, status=status.HTTP_401_UNAUTHORIZED)

            else:
                return Response({'message': 'Incorrect username or password', 'isLoggedIn': False}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TokenAuthenticationView(APIView):
    def post(self, request):
        token_key = request.data.get('token')

        if token_key:
            try:
                jwt.decode(token_key, "app.config['SECRET_KEY']", algorithms=['HS256'])
                return Response({"message": "Authenticated successfully", "isAuthenticated": True}, status=status.HTTP_200_OK)
            except jwt.ExpiredSignatureError:
                return Response({"message": "Signature expired. Please log in again.", "isAuthenticated": False}, status=status.HTTP_400_BAD_REQUEST)
            
            except jwt.InvalidTokenError:
                return Response({"message": "Invalid token", "isAuthenticated": False},
                         status=status.HTTP_400_BAD_REQUEST)
        
        else:
            return Response({"message": "Token not provided", "isAuthenticated": False}, status=status.HTTP_400_BAD_REQUEST)

class ChangePassword(APIView):

    def post(self, request):

        
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():

            username = request.data.get('username')
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']

            try:
                user = users.objects.get(username=username)
            except users.DoesNotExist:
                return Response({'message': 'User does not exist','isChangedPassword':False}, status=status.HTTP_404_NOT_FOUND)

            if user.check_password(old_password):
                user.set_password(new_password)
                return Response({'message': 'Password changed successfully', 'isChangedPassword': True}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Incorrect old password', 'isChangedPassword': False}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ForgotPasswordView(APIView):
    
    def post(self,request):
        serializer = ForgotPasswordSerializer(data=request.data)

        if serializer.is_valid():

            new_password = serializer.validated_data['new_password']
            username = serializer.validated_data['username']

            try:
                user = users.objects.get(username=username)
            except users.DoesNotExist:
                return Response({'message': 'User does not exist','isChangedPassword':False}, status=status.HTTP_404_NOT_FOUND)
            user.set_password(new_password)
            return Response({'message': 'Password changed successfully', 'isChangedPassword': True}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FOBListView(APIView):

    def get(self, request, username, fieldName):
        user = users.objects.get(username=username)
        field_data = getattr(user, fieldName, None)
        if field_data is None:
            return Response(f"Field {fieldName} does not exist on user model", status=400)
        data = json.loads(str(field_data))
        return Response(data)

    def post(self, request, fieldName,username):
        user = users.objects.get(username=username)
        new_data = request.data.get(fieldName)
        if not new_data:
            return Response(f"Provided post data is incorrect.", status=500)
        field_data = getattr(user, fieldName, None)
        if field_data is None:
            return Response(f"Field {fieldName} does not exist on user model", status=400)

        data_list = json.loads(str(field_data))
        data_list.append(new_data)
        updated_data = json.dumps(data_list)

        serializer = FOBSerializer(
            user, data={fieldName: updated_data}, partial=True)
        try:
            if serializer.is_valid():
                setattr(user, fieldName, updated_data)
                user.save()
                return Response("Added data")
            else:
                return Response(f"Cannot add data,\n\n {serializer.errors}", status=400)
        except Exception as e:
            return Response(f"Cannot add {e}", status=500)

    def delete(self, request, username, fieldName):
        user = users.objects.get(username=username)

        index = request.data.get('index')

        if not index and index != 0:
            return Response(f"Provided post data is incorrect.", status=500)

        field_data = getattr(user, fieldName, None)
        if field_data is None:
            return Response(f"Field {fieldName} does not exist on user model", status=400)

        data_list = json.loads(str(field_data))
        if index < 0 or index >= len(data_list):
            return Response(f"Index {index} is out of bounds", status=400)
        data_list.pop(index)
        updated_data = json.dumps(data_list)

        serializer = FOBSerializer(
            user, data={fieldName: updated_data}, partial=True)
        try:
            if serializer.is_valid():
                setattr(user, fieldName, updated_data)
                user.save()
                return Response("Deleted Address")
            else:
                return Response(f"Cannot delete address,\n\n {serializer.errors}", status=400)
        except Exception as e:
            return Response(f"Cannot delete {e}", status=500)

    def patch(self, request, username, fieldName):
        try:
            user = users.objects.get(username=username)

            index = request.data.get('index')
            new_data = request.data.get('new')

            if not index and index != 0 or not new_data:
                return Response(f"Provided post data is incorrect.", status=500)

            if index is None or new_data is None:
                return Response("There is an issue with the index or new_data key provided.", status=400)

            field_data = getattr(user, fieldName, None)
            if field_data is None:
                return Response(f"Field {fieldName} does not exist on user model", status=400)

            data_list = json.loads(str(field_data))
            if index < 0 or index >= len(data_list):
                return Response(f"Index {index} is out of bounds", status=400)
            data_list[index] = new_data
            updated_data = json.dumps(data_list)

            serializer = FOBSerializer(
                user, data={fieldName: updated_data}, partial=True)
            try:
                if serializer.is_valid():
                    setattr(user, fieldName, updated_data)
                    user.save()
                    return Response("Updated data")
                else:
                    return Response(f"Cannot update data,\n\n {serializer.errors}", status=400)
            except Exception as e:
                return Response(f"Cannot update {e}", status=500)
        except Exception as e:
            return Response(f"Error occurred: {e}", status=500)
