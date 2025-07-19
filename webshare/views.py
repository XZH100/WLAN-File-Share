import os
import shutil
from datetime import timedelta

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from .models import SharedFile
from .forms import UploadForm

# 登录页面
@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        if username:
            request.session['username'] = username
            return redirect('file_list')
    return render(request, 'login.html')


# 上传 & 列表视图
def file_list(request):
    username = request.session.get('username')
    if not username:
        return redirect('login')

    # 清理过期文件（超过 48 小时）
    cutoff = timezone.now() - timedelta(hours=48)
    expired = SharedFile.objects.filter(uploaded_at__lt=cutoff)
    for f in expired:
        # 删除物理文件
        if os.path.isfile(f.file.path):
            os.remove(f.file.path)
    expired.delete()

    # 处理上传
    if request.method == "POST":
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            sf = form.save(commit=False)
            sf.username = username
            sf.save()
            return HttpResponseRedirect(reverse('file_list'))
    else:
        form = UploadForm()

    # 当前用户文件列表
    files = SharedFile.objects.filter(username=username).order_by('-uploaded_at')
    return render(request, 'files.html', {
        'username': username,
        'form': form,
        'files': files,
    })


# 下载视图
def download_file(request, file_id):
    username = request.session.get('username')
    if not username:
        return redirect('login')

    try:
        sf = SharedFile.objects.get(id=file_id, username=username)
    except SharedFile.DoesNotExist:
        return HttpResponse("文件不存在或无权限", status=404)

    response = FileResponse(open(sf.file.path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename="{os.path.basename(sf.file.name)}"'
    return response


# 注销
def logout_view(request):
    request.session.flush()
    return redirect('login')
