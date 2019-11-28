import os
import shutil

from django.shortcuts import render
from django.conf import settings

from utils.repository import GitRepository
from utils.ssh import SSHProxy


def code_transceiver(request):

    if request.method == "GET":

        return render(request,"code_page.html")

    else:

        repo = request.POST.get("repo")
        filename = request.POST.get("filename")

        code_path = os.path.join(settings.CODE_ZIP_PATH,filename)
        print(code_path)
        git = GitRepository(code_path,repo)

        abs_file_path = shutil.make_archive(
            base_name=os.path.join(settings.FILE_ZIP_PATH,filename),  # 压缩包文件路劲
            format='zip',  # “zip”, “tar”
            root_dir=code_path  # 被压缩的文件目录
        )

        with SSHProxy('192.168.16.130', 22, 'root', settings.ID_RSA) as proxy:
            proxy.upload(abs_file_path, f"/data/{filename}.zip")


        return render(request,'code_page.html')
