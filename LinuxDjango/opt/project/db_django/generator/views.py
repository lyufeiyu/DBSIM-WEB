from django.shortcuts import render

# Create your views here.
import os
import shutil
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.conf import settings

@csrf_exempt
def file_upload(request):
    if request.method == 'POST' and request.FILES.get('myfile'):
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()    # 请注意，我们使用了 FileSystemStorage 类来保存上传的文件。该类会将文件保存在由 MEDIA_ROOT 设置定义的位置。
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)

        # 这里可以调用你的数据处理函数，比如:
        # process_file(os.path.join(settings.MEDIA_ROOT, filename))

        return JsonResponse({'status': 'success', 'uploaded_file_url': uploaded_file_url})

    return JsonResponse({'status': 'error', 'message': 'No file uploaded'})

def list_history_files(request):
    history_files_path = os.path.join(settings.MEDIA_ROOT, 'history')
    files = [
        {
            'name': filename,
            'download_url': settings.MEDIA_URL + 'history/' + filename
        }
        for filename in os.listdir(history_files_path)
        if os.path.isfile(os.path.join(history_files_path, filename))
    ]
    return JsonResponse(files, safe=False)

import subprocess
import logging

# Django视图函数示例
@csrf_exempt
def generate_data(request):
    if request.method == 'POST':
        # 获取参数
        dataset_name = request.POST.get('dataset_name')
        scale_factor = request.POST.get('scale_factor')
        coeffi = request.POST.get('coeffi')
        privacy_budget = request.POST.get('privacy_budget')
        cluster_per_col = request.POST.get('cluster_per_col')

        # 创建目录
        new_directory_path = f'/opt/project/db_django/media/create/dataset/{dataset_name}'
        new_directory_output_path = f'/opt/project/db_django/media/create/dataset/{dataset_name}/output'
        if not os.path.exists(new_directory_path):
            os.makedirs(new_directory_path)
        if not os.path.exists(new_directory_output_path):
            os.makedirs(new_directory_output_path)
        
        # 处理所有上传的文件
        for file_key in request.FILES.keys():
            # 这里的request.FILES是一个MultiValueDict，可以包含多个文件
            for file in request.FILES.getlist(file_key):
                # 这里你可以处理文件，例如保存它们
                with open(f'{new_directory_path}/' + file.name, 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)


        # 写入run.sh文件
        run_sh_path = '/opt/project/db_django/media/create/sh/run2.sh'
        with open(run_sh_path, 'w') as file:  # w是覆盖，a是追加。另外，如果对于open，如果文件不存在则会创建它
            file.write(f'\n\n#!/bin/bash\n')
            file.write(f'# 这里可以写入你的shell脚本内容\n')
            # file.write('set -e\n')  # 当任何一行命令执行失败时，退出脚本   SPN_experiment.py在错误情况下不返回非零状态码，那么set -e将不会有效，因为它只在命令返回非零退出状态时才会退出脚本。
            # file.write(f'echo "Param1 is: {dataset_name}"\n')
            # file.write(f'echo "Param2 is: {dataset_name}"\n')
            file.write(f'cd /opt/project/db_django/media/create/;\n')
            file.write(f'python SPN_experiment.py --dataset {dataset_name} --coeffi {coeffi} --privacy_budget {privacy_budget} --cluster_per_col {cluster_per_col}  --gen_dir dataset/{dataset_name}/output --in_dir ./dataset/{dataset_name}/ --scale_factor {scale_factor} --sche_file ./dataset/{dataset_name}/schema.txt;\n')
            file.write('set -e\n') 
            file.write(f'if [ ! -d "{new_directory_output_path}" ] || [ -z "$(ls -A {new_directory_output_path})" ]; then\n     echo "Output directory does not exist or is empty. Exiting with error."\n     exit 1\nfi\n')
            file.write(f'cd /opt/project/db_django/media/create/dataset/{dataset_name}/output/;\n')
            # file.write(f'echo "1111"\n')
            file.write(f'zip -r {dataset_name}_generate_data.zip *;\n')
            # file.write(f'echo "3333"\n')
            file.write(f'mv {dataset_name}_generate_data.zip ../../../../history;\n')
            # file.write(f'echo "4444"\n')
            file.write(f'cd ..;\n')
            # file.write(f'echo "5555"\n')
            # file.write(f'rm -rf output;\n')
            # file.write(f'echo "6666"\n')

        # 打印参数
        # print('Param 1:', param1)
        # print('Param 2:', param2)
        # logging.info('Param 1: %s, Param 2: %s', param1, param2)

        # 更改文件权限以确保脚本可执行
        os.chmod(run_sh_path, 0o755)

        # 调用run.sh脚本
        # subprocess.run(run_sh_path,shell=True)
    
        # 运行run.sh脚本
        try:
            subprocess.run(run_sh_path, shell=True, check=True)
            return JsonResponse({'message': 1})
        except subprocess.CalledProcessError as e:
            return JsonResponse({'message': 2})
    else:
        return JsonResponse({'message': '无效的请求方法'}, status=405)

@csrf_exempt
def generate_sql(request):
    if request.method == 'POST' and request.FILES['sql_file']:
        # 获取上传的 CSV 文件
        csv_file = request.FILES['sql_file']
        fs = FileSystemStorage()

        # 保存 CSV 文件
        filename = fs.save(csv_file.name, csv_file)
        uploaded_file_url = fs.url(filename)

        # 提取不包括后缀的文件名
        basename = os.path.splitext(filename)[0]

        # 定义 SQL 文件的源路径和历史记录路径
        source_sql_path = os.path.join('/opt/project/db_django/media/sql/sqls', basename + '.sql')
        history_path = os.path.join(settings.MEDIA_ROOT, 'history', basename + '.sql')

        # 如果同名的 SQL 文件存在，则复制到历史记录路径
        if os.path.exists(source_sql_path):
            shutil.copy2(source_sql_path, history_path)
            return JsonResponse({'status': 'success', 'url': uploaded_file_url})
        else:
            return JsonResponse({'status': 'error', 'message': 'Matching SQL file not found'})

    return JsonResponse({'status': 'error', 'message': 'No CSV file uploaded'})