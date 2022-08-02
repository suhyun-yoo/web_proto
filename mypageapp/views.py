from django.shortcuts import render
from searchapp.models import Request, SearchedData
# Create your views here.


def mypage(request):
    # 로그인 사용자의 요청목록 가져오기
    user_id = request.user.id
    try:
        request_list = Request.objects.all().order_by("-id").filter(request_user_id=user_id)
    except:
        request_list = []

    searched_list = []
    for req in request_list:
        searched_list.extend(SearchedData.objects.all().filter(request_id=req.id))
    return render(request, 'mypageapp/mypage.html', {'request_list': request_list, "searched_list": searched_list, })
