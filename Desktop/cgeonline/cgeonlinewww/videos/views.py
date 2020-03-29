from django.shortcuts import render,get_object_or_404
from .models import Video_Tube,Video_Tag,Video_Type,WatchNumber
from django.core.paginator import Paginator

# Create your views here

def video_list(request):
    #取得所有影片
    videos_all_list=Video_Tube.objects.all()
    #9個影片分成1頁
    paginator=Paginator(videos_all_list,9)
    #獲取頁碼參數，沒有獲取的話 預設為1
    page_num=request.GET.get('page',1)
    #將此參數傳給GET_PAGE 內容屬性有object_list 可以取出所有影片
    page_of_videos=paginator.get_page(page_num)
    #獲取當前頁面
    current_page_num=page_of_videos.number
    #為了不將所有分頁列出來 將用者個顯示前後兩頁
    page_range = list(range(max(current_page_num - 2, 1), current_page_num)) + \
                 list(range(current_page_num, min(current_page_num + 2, paginator.num_pages) + 1))
    # 審略標記符號
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 首頁跟尾頁
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)


    context={}
    # context['videos']=Video_Tube.objects.all()
    context['videos']=page_of_videos.object_list
    context['page_of_videos']=page_of_videos
    context['page_range']=page_range
    context['blog_types']=Video_Type.objects.all()
    return render(request,'videos/video_list.html',context)

def video_detail(request,video_id):
    # ,Video_Tube_pk
    video=get_object_or_404(Video_Tube,video_id=video_id)
    # # ,pk=Video_Tube_pk
    # # if not request.COOKIES.get('video_%s_watch_number' % Video_Tube_pk):
    # #     video.watch_number +=1
    # #     video.save()

         
    context={}
    context['video']=video
    # response= render(request,'videos/video_detail.html',context)
    # response.set_cookie('video_%s_watch_number' % Video_Tube_pk, 'true' ,)
    return render(request,'videos/video_detail.html',context)


def videos_with_type(request,video_type_pk):
    
    context={}
    video_type=get_object_or_404(Video_Type,pk=video_type_pk)
    context['video_type']=video_type
    context['videos']=Video_Tube.objects.filter(video_type=video_type)
    context['video_types']=Video_Type.objects.all()
    return render(request,'videos/video_with_type.html',context)