from django.shortcuts import render
from django.contrib.auth.models import User
from .serializers import UserSerializer,FriendRequestSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes,throttle_classes
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from .models import FriendRequest
from .throttles import FriendRequestThrottle
# Create your views here.

class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class  = UserSerializer
    permission_classes = [AllowAny]
    
class UserLoginView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
    def post(self,request,*args,**kwargs):
        email = request.data.get('email').lower()
        password = request.data.get('password')
        user = User.objects.filter(email__iexact=email).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access':str(refresh.access_token)
            })
        return Response({'details':'Invalid Credentials'},status=status.HTTP_401_UNAUTHORIZED)
    
class UserSearchView(generics.ListAPIView):
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        query = self.request.query_params.get('query','')
        if '@' in query:
            return User.objects.filter(email__iexact=query)
        return User.objects.filter(Q(username__icontains=query) | Q(email__icontains=query))
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@throttle_classes([FriendRequestThrottle])
def sendFriendRequest(request):
    to_user_id = request.data.get('to_user_id')
    to_user = User.objects.get(id=to_user_id)
    friend_request, created = FriendRequest.objects.get_or_create(from_user=request.user, to_user=to_user)
    if created:
        return Response({'status': 'friend request sent'})
    return Response({'status': 'friend request already sent'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def respondToFriendRequest(request, pk, action):
    friend_request = FriendRequest.objects.get(pk=pk, to_user=request.user)
    if action == 'accept':
        friend_request.is_accepted = True
        friend_request.save()
        return Response({'status': 'friend request accepted'})
    elif action == 'reject':
        friend_request.delete()
        return Response({'status': 'friend request rejected'})
    return Response({'status': 'invalid action'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listFriends(request):
    friends = User.objects.filter(
        Q(sent_requests__to_user=request.user, sent_requests__is_accepted=True) |
        Q(received_reqests__from_user=request.user, received_reqests__is_accepted=True)
    ).distinct()
    serializer = UserSerializer(friends, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_pending_requests(request):
    pending_requests = FriendRequest.objects.filter(to_user=request.user, is_accepted=False)
    serializer = FriendRequestSerializer(pending_requests, many=True)
    return Response(serializer.data)