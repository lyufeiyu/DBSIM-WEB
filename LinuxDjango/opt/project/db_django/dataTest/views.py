# /opt/project/db_django/dataTest/views.py

from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.db import connections
from django.views.decorators.csrf import csrf_exempt

import os
import time
from django.views.decorators.http import require_http_methods
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from django.db.utils import OperationalError
from collections import defaultdict
from django.conf import settings

def clean_data(df, table_name):
    """
    Clean the DataFrame `df` by ensuring that integer columns contain only integer values.
    
    Args:
    - df: pandas.DataFrame to clean
    - table_name: name of the table, used to tailor cleaning based on the table
    
    Returns:
    - cleaned pandas.DataFrame
    """
    if table_name == 'cast_info':
        # Ensure 'role_id' and 'person_id' are integers and 'movie_id' is not null
        df = df.dropna(subset=['movie_id'])  # Drop rows where 'movie_id' is null
        cols_to_check = ['role_id', 'person_id']
        
        for col in cols_to_check:
            df[col] = pd.to_numeric(df[col], errors='coerce')  # Coerce invalid values to NaN
        
        df = df.dropna(subset=cols_to_check)  # Drop rows with NaNs in the specified columns
        df[cols_to_check] = df[cols_to_check].astype(int)  # Convert columns to integer type
    elif table_name == 'title':
        # 假设 'id' 和 'production_year' 应该是整数类型
        int_columns = ['id', 'production_year','kind_id']  # 添加或删除列名以匹配您的数据结构
        for col in int_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')  # 将非整数值转换为NaN
                df = df.dropna(subset=[col])  # 删除含有NaN的行
                df[col] = df[col].astype(int)  # 转换列为整数类型
    # Implement additional cleaning logic for other tables if needed
    # ...
    
    return df

@csrf_exempt  # 如果没有使用CSRF token，可能需要禁用CSRF保护
@require_http_methods(["POST"])
def import_data_view(request):
    try:
        error_messages = []  # 收集报错信息
        new_database_name = request.POST.get('dataset_name')
        if not new_database_name:
            return JsonResponse({'error': '未提供数据库名称'}, status=400)
        
        db_username = 'root'
        db_password = '2002'
        db_host = 'localhost'
        db_port = '3306'
        db_name = f"db_{new_database_name}"

        db_uri_server = f"mysql+pymysql://{db_username}:{db_password}@{db_host}:{db_port}/"
        engine_server = create_engine(db_uri_server)

        try:
            with engine_server.connect() as conn:
                conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {db_name}"))
        except SQLAlchemyError as e:
            return JsonResponse({'error': f"创建{db_name}数据库时出错: {e}"}, status=500)

        db_uri_db = f"{db_uri_server}{db_name}"
        engine_db = create_engine(db_uri_db)

        dataset_path = f'/opt/project/db_django/media/sql/files/{new_database_name}'
        ignore_files = ['schema.txt']

        for csv_file in os.listdir(dataset_path):
            if csv_file.endswith('.csv') and csv_file not in ignore_files:
                file_path = os.path.join(dataset_path, csv_file)

                try:
                    # Read the CSV file
                    df = pd.read_csv(file_path)

                    # Clean the DataFrame
                    table_name = csv_file.replace('.csv', '')
                    df_cleaned = clean_data(df, table_name)

                    # Import the cleaned data to the database
                    df_cleaned.to_sql(name=table_name, con=engine_db, if_exists='replace', index=False)
                    print(f"表 {table_name} 导入成功！")
                except SQLAlchemyError as e:
                    error_messages.append(f"导入数据表 {table_name} 时出错：{e}")
                    print(f"导入数据表 {table_name} 时出错：{e}")

        # for csv_file in os.listdir(dataset_path):
        #     if csv_file.endswith('.csv') and csv_file not in ignore_files:
        #         file_path = os.path.join(dataset_path, csv_file)
        #         try:
        #             # 分批读取并导入数据
        #             for chunk in pd.read_csv(file_path, chunksize=10000):  # 调整chunksize以优化内存使用
        #                 chunk.to_sql(name=csv_file.replace('.csv', ''), con=engine_db, if_exists='append', index=False)
        #         except Exception as e:
        #             error = f"导入数据表 {csv_file} 时出错：{e}"
        #             error_messages.append(error)
        #             print(error)

        if error_messages:
            return JsonResponse({'errors': error_messages}, status=500)
        return JsonResponse({'message': '数据导入成功'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

    
    except Exception as e:
        # 在这里捕获所有的异常，并将错误信息返回给前端
        return JsonResponse({'error': str(e)}, status=500)
    
def import_to_postgres(csv_file_path, table_name, database_url):
    try:
        # 使用 SQLAlchemy 创建 Postgres 引擎
        engine = create_engine(database_url)
        # 使用 pandas 读取 csv 文件
        data_frame = pd.read_csv(csv_file_path, low_memory=False)

        df_cleaned = clean_data(data_frame, table_name)
        # 将数据导入 PostgreSQL
        df_cleaned.to_sql(table_name, engine, if_exists='replace', index=False)
        return True, f"表 {table_name} 导入成功！"
    except Exception as e:
        return False, str(e)

@csrf_exempt
@require_http_methods(["POST"])
def dispatcher_databases_view(request):
    print("456789")
    print(request.POST)  # 查看整个 POST 对象
    # print(request.FILES)
    database_type = request.POST.get('database_type')
    dataset_name = request.POST.get('dataset_name')
    # print("database_type是：",database_type)
    # print("dataset_name",dataset_name)
    if database_type == 'MySQL':
        return import_data_view(request)
    elif database_type == 'PostgreSQL':
        print("-----11------")
        db_config = settings.DATABASES['default1']
        database_url = f"postgresql://{db_config['USER']}:{db_config['PASSWORD']}@{db_config['HOST']}:{db_config['PORT']}/{db_config['NAME']}"
        csv_dir_path = f"/opt/project/db_django/media/sql/files/{dataset_name}"
        
         # 遍历目录下的所有csv文件，并导入
        for csv_file in os.listdir(csv_dir_path):
            if csv_file.endswith('.csv'):
                csv_file_path = os.path.join(csv_dir_path, csv_file)
                table_name = csv_file.replace('.csv', '')
                print(table_name)
                success, message = import_to_postgres(csv_file_path, table_name, database_url)
                if not success:
                    return JsonResponse({'error': message}, status=500)
        
        return JsonResponse({'message': '所有数据已成功导入PostgreSQL数据库'})
    else:
        return JsonResponse({'error': '不支持的数据库类型'}, status=400)
    
@csrf_exempt
def run_sql_query(request):
    print("77777777777")
    if request.method == 'POST':
        # 获取文件和数据库类型
        sql_file = request.FILES.get('sql_file')
        db_type = request.POST.get('db_type')
        print(sql_file)
        print(db_type)
        if not sql_file:
            return JsonResponse({'error': '未接收到SQL文件。'}, status=400)
        if not db_type or (db_type not in ['MySQL', 'PostgreSQL']):
            return JsonResponse({'error': '数据库类型不支持或未指定。'}, status=400)


        # 获取文件名并建立文件在服务器上的预期路径
        sql_filename = sql_file.name
        # print(sql_filename)
        expected_file_path = f"/opt/project/db_django/media/sql/sqls/{sql_filename}"
        # print(expected_file_path)

        # 检查文件是否存在
        if not os.path.isfile(expected_file_path):
            return JsonResponse({'error': '没有在服务器上找到同名的SQL文件。'}, status=404)
        
        response_times = []
        try:
            print(11111)
            # 连接到MySQL数据库
            db_who=""
            if db_type == 'MySQL':
                db_who="my_mysql_db_alias"
            elif db_type == 'PostgreSQL':
                db_who="default1"
            with connections[db_who].cursor() as cursor:
                with open(expected_file_path, 'r') as file:
                    sql_commands = file.readlines()
                print(333333)
                query_count = len(sql_commands)
                start_time = time.time()
                print(44444)
                for command in sql_commands:
                    command = command.strip()
                    if command:
                        try:
                            print(f"Executing command: {command}")
                            start_query_time = time.time()
                            print(555555)
                            cursor.execute(command + ';')
                            print(666666)
                            end_query_time = time.time()
                            print(f"Command executed successfully in {end_query_time - start_query_time} seconds")
                            response_times.append(end_query_time - start_query_time)
                        except Exception as e:
                            print(f"Error executing command: {e}")
                    # Handle exception or break/continue depending on your needs
                
                total_time = time.time() - start_time
                TPS = QPS = query_count / total_time  # Assuming each query is a transaction
    
                response_times.sort()
                percentiles = defaultdict(lambda: None, {
                    "50%": response_times[int(0.50 * query_count)],
                    "75%": response_times[int(0.75 * query_count)],
                    "90%": response_times[int(0.90 * query_count)],
                    "95%": response_times[int(0.95 * query_count)],
                    "99%": response_times[int(0.99 * query_count)],
                    "Max": response_times[-1],
                })
                print("total_time:", total_time)
                return JsonResponse({
                    'message': f'"{sql_filename}"执行成功，数据库已更新。',
                    'TPS': TPS,
                    'QPS': QPS,
                    'Response_Times_Percentiles': percentiles
                })
            
        except OperationalError as e:
            # 数据库操作错误处理
            return JsonResponse({'error': f'执行SQL文件时出错: {str(e)}'}, status=500)
        except Exception as e:
            # 其他错误处理
            return JsonResponse({'error': f'出现错误: {str(e)}'}, status=500)
    else:
        return JsonResponse({'error': '仅支持POST请求。'}, status=405)