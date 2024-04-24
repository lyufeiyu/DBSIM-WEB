############################################################
# v6.6版本更新日志
# · buckets repeat值优化（skew data）
# · null值处理
# · 新增相关系数类型 rdc
# · queries mutation demo
############################################################

from cmath import nan
from random import random, sample, randint
import os
import sys

from matplotlib import axes
sys.path.append('../../') 
import csv
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import networkx as nx
from pyope.ope import OPE, ValueRange
from networkx.drawing.nx_agraph import write_dot, graphviz_layout
import time
import re
from queue import Queue
import logging
from datetime import datetime
import json
import warnings
warnings.filterwarnings("ignore")

from options import opt
import data_gen_SPN_v6 as SPN_test
# from read_job_queries import parse_queries_csv
# from utils import range_query

IMDB_COLS_DICT = {'title': ['id', 'production_year', 'kind_id'], 
                    'movie_keyword': ['movie_id', 'keyword_id'],
                    'movie_info_idx': ['movie_id', 'info_type_id'],
                    'movie_info': ['movie_id', 'info_type_id'],
                    'movie_companies': ['movie_id', 'company_type_id', 'company_id'],
                    'cast_info': ['movie_id', 'role_id', 'person_id']}

# logging.basicConfig(level=logging.INFO if not opt.verbose else logging.DEBUG)
logger = logging.getLogger('DBsi')
logger.setLevel(logging.INFO if not opt.verbose else logging.WARNING)

class MyFormatter(logging.Formatter):
    def format(self, record):
        levelname = record.levelname
        if levelname == "DEBUG":
            levelname_color = "\033[1;34m"  # 蓝色
        elif levelname == "INFO":
            levelname_color = "\033[1;32m"  # 绿色
        elif levelname == "WARNING":
            levelname_color = "\033[1;33m"  # 黄色
        elif levelname == "ERROR":
            levelname_color = "\033[1;31m"  # 红色
        elif levelname == "CRITICAL":
            levelname_color = "\033[1;35m"  # 洋红色
        else:
            levelname_color = "\x1b[0m"  # 默认颜色
        record.levelname = levelname_color + levelname + "\033[0m"
        return super().format(record)


console_handler = logging.StreamHandler()
console_handler.setFormatter(MyFormatter("[%(levelname)s] %(message)s"))

file_handler = logging.FileHandler(filename='../../log/DBsi_{}.log'.format(datetime.now().strftime("%d%m%y_%H%M")), encoding='utf8')
file_handler.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))
if not logger.handlers:
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

SPN_test.logging = logger
SPN_test.verbose = opt.verbose

class Table:
    def __init__(self, name, cols):
        self.name = name
        self.cols = cols
        self.data = None
        self.isVis = False
        self.pk_idx = []
        self.str_col_idx = None
        self.date_col_idx = None
        self.cate_col_idx = None
        self.null_tag_dict = None

        # 被引用的信息，格式：{被引用列名 : [(引用该列的表名, 引用该列的列名)]} 
        self.refered = {}

        # 引用信息，格式：[引用的表名]
        self.refer = []

        # 引用节点列表，格式：{引用他表某列的列名 : node_list}
        self.refer_node = {}

        # 被引用节点列表，格式：{被引用的列名 : node_list}
        self.refered_node = None

        # 联合被引用的列，格式：二维列表
        self.join_refered_idx = []

        # 联合外键（引用他表），格式：二维列表
        self.join_fk = []
        
        # 是否scale
        self.is_scale = True

        # 引用的表是否scale，格式：{本表的列名which引用他表：他表是否scale(True or False)} 
        self.is_tab_refer_scale = {}

        
    def __repr__(self) -> str:
        return f"Table {{ {self.name} }}'s reference info: {self.refered} ; refers {self.refer}."

def draw_plot(data, offset,edge_color, fill_color):
    pos = np.arange(data.shape[1])+offset 
    bp = axes.boxplot(data, positions= pos, widths=0.3, patch_artist=True)
    for element in ['boxes', 'whiskers', 'fliers', 'medians', 'caps']:
        plt.setp(bp[element], color=edge_color)
    for patch in bp['boxes']:
        patch.set(facecolor=fill_color)

# class RangeQuery:
#     def __init__(self, col_left, col_right):
#         self.col_left = col_left
#         self.col_right = col_right

#     def column_range(self, col_name, min_val, max_val):
#         if col_name not in self.col_left:
#             return min_val, max_val
#         return self.col_left[col_name], self.col_right[col_name]

def draw_query_heat_map(G, label_dict, sel_list, save_file):
    write_dot(G, save_file + '.dot')
    pos = graphviz_layout(G, prog='dot')
    plt.figure(dpi=300, figsize=[12.8, 9.6])
    nx.draw_networkx(G, pos=pos, node_size=400, node_color=sel_list, with_labels=False, cmap=plt.cm.Reds, vmin=-0.1, vmax=1.0)
    nx.draw_networkx_labels(G, pos=pos, labels=label_dict)
    sm = plt.cm.ScalarMappable(cmap=plt.cm.Reds, norm=plt.Normalize(vmin=-0.1, vmax=1.0))
    sm.set_array([])
    cbar = plt.colorbar(sm)
    cbar.ax.invert_yaxis()
    plt.savefig('./' + save_file + '.png')
    plt.close()

def check_min_max(min, max, x):
    if (x < min): 
        return min
    elif (x > max): 
        return max
    else:
        return x

def gen(root, refer_node):
    data, _, row_idxs, _ = root.gen_data(refer_node)
    # data, row_idxs = SPN_test.calibrate_idxs(data, row_idxs, False)
    return data

def find_refer_freq(data_ref):
    freq_dict = {}
    for val in data_ref:   
        if (val in freq_dict):
            freq_dict[val] += 1
        else:
            freq_dict[val] = 1
    return freq_dict

def transpose(in_list):
    return list(map(list, zip(*in_list)))    

def is_category(dataset, i):
    if len(dataset) > 1000:
        length = 1000
    else:
        length = len(dataset)

    occur_freq = {}
    for j in range(length):
        item = dataset[j][i]
        if item not in occur_freq:
            occur_freq[item] = 1

    return len(occur_freq) / length < 0.5

def is_date(dataset, i):
    if len(dataset) > 20:
        length = 20
    else:
        length = len(dataset) 

    occur = 0
    for j in range(length):
        if type(dataset[j][i]) == str:        
            try:
                pd.to_datetime(dataset[j][i])
                occur += 1
            except ValueError:
                pass

    return occur > 10 

def is_str(dataset, i):
    if len(dataset) > 20:
        length = 20
    else:
        length = len(dataset) 

    occur = 0
    for j in range(length):
        if type(dataset[j][i]) == str:
            occur += 1
    
    return occur / length > 0.5
    
def get_new_domain(datacol, mi, ma):
    d_type = float
    
    for i in range(len(datacol)):
        if type(datacol[i]) == int:
            d_type = int
            break
        elif type(datacol[i]) == str:
            d_type = str
            break

    if d_type == int:
        if not mi:
            mi = min(datacol)
            ma = max(datacol)
        diff = ma - mi
        transfer = int(np.sqrt(diff)) * randint(1000, 5000)
        new_mi = mi + transfer
        new_ma = ma + transfer
        new_ma += diff * 100
        return mi, ma, new_mi, new_ma, None
    elif d_type == float:
        digits = 0
        for j in range(10):
            if len(str(datacol[j]).split('.')[1]) > digits:
                digits = len(str(datacol[j]).split('.')[1])
        mi = int(min(datacol) * 10**digits)
        ma = int(max(datacol) * 10**digits)
        diff = ma - mi
        transfer = int(np.sqrt(diff)) * randint(100, 500)
        new_mi = mi + transfer
        new_ma = ma + transfer
        new_ma += diff * 100
        return mi, ma, new_mi, new_ma, digits
    else:
        return None, None, None, None, None

def special_cols_idx(dataset):
    str_col_idx = []
    date_col_idx = []
    cate_col_idx = []

    for i in range(len(dataset[0])):
        d_type = None
        for j in range(len(dataset)):
            if type(dataset[j][i]) == str:
                d_type = str
                break
            elif type(dataset[j][i]) == bool:
                d_type = str
                dataset = transpose(dataset)
                dataset[i] = [str(x) for x in dataset[i]]
                dataset = transpose(dataset)

        if d_type == str:

            if is_date(dataset, i):
                date_col_idx.append(i)
                dataset = transpose(dataset)
                dataset[i] = pd.to_datetime(pd.DataFrame(dataset[i])[0], errors='coerce',
                                            infer_datetime_format=True,
                                            cache=True).tolist()
                dataset = transpose(dataset)
            elif is_category(dataset, i):
                cate_col_idx.append(i)
            elif is_str(dataset, i):
                str_col_idx.append(i)
        


    return dataset, [str_col_idx, date_col_idx, cate_col_idx]

def transform_nan(isnull_list, data, dataset):
    null_tag_dict = {}
    data = transpose(data)
    for i in range(len(isnull_list)):
        if dataset == 'IMDB':
            for j in range(len(data[i])):
                val = data[i][j]
                if type(val) == str:
                    try:
                        data[i][j] = int(val)
                    except:
                        data[i][j] = np.nan
                    continue
                if not np.isnan(val):
                    data[i][j] = int(val)

        if isnull_list[i]:
            can_continue = False
            for j in range(0, len(data[i])):
                if type(data[i][j]) == str:
                    can_continue = True
                    break
            if can_continue:
                continue
            if np.all(np.isnan(data[i])):
                continue
            ma = max(x for x in data[i] if not np.isnan(x))
            mi = min(x for x in data[i] if not np.isnan(x))
            d = ma - mi
            d *= 1000
            if mi - d > 0:
                null_tag = 0
            else:
                null_tag = ma + d
            for j in range(len(data[i])):
                val = data[i][j]
                if np.isnan(val):
                    data[i][j] = null_tag
                                        
            null_tag_dict[i] = [null_tag, mi, ma]
    data = transpose(data)
    return data, null_tag_dict

def read_csv(file_path, tab, dataset):
    logger.info('Reading file: ' + file_path)
    null_tag_dict = {}
    if dataset == 'TPCH':
        df = pd.read_csv(file_path, header=0, sep='|')
        data = df.values.tolist()
        
    elif dataset == 'IMDB':
        df = pd.read_csv(file_path, header=0, usecols=IMDB_COLS_DICT[tab])
        df = df[IMDB_COLS_DICT[tab]]
        isnull_list = df.isnull().any().values.tolist()       
        data = df.values.tolist()
        data, null_tag_dict = transform_nan(isnull_list, data, dataset)

    elif dataset == 'CENSUS':
        cols =[0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        df = pd.read_csv(file_path, usecols=cols, header=None)
        df = df[cols]
        isnull_list = df.isnull().any().values.tolist()
        data = df.values.tolist()
        data, null_tag_dict = transform_nan(isnull_list, data, dataset)
    elif dataset == 'DMV':
        cols = [
            'Record Type','Registration Class', 'State', 'County', 'Body Type',
            'Fuel Type', 'Reg Valid Date', 'Color', 'Scofflaw Indicator',
            'Suspension Indicator', 'Revocation Indicator'
        ]
        df = pd.read_csv(file_path, usecols=cols)
        isnull_list = df.isnull().any().values.tolist()
        data = df.values.tolist()
        data, null_tag_dict = transform_nan(isnull_list, data, dataset)
    elif dataset == 'Banking':
        df = pd.read_csv(file_path, header=0, sep=';')
        isnull_list = df.isnull().any().values.tolist()
        data = df.values.tolist()
        data, null_tag_dict = transform_nan(isnull_list, data, dataset)    
    else:
        df = pd.read_csv(file_path, header=0, sep=',')
        isnull_list = df.isnull().any().values.tolist()
        data = df.values.tolist()
        data, null_tag_dict = transform_nan(isnull_list, data, dataset)   
    # else:
    #     df = pd.read_csv(file_path, header=0)
    #     # df.fillna(0, inplace=True)
    #     data = df.values.tolist()

    cols = df.columns.tolist()

    special_cols_idx_list = []

    if dataset != 'IMDB':
        data, special_cols_idx_list = special_cols_idx(data)
    else:
        special_cols_idx_list = [[],[],[]]

    return data, cols, special_cols_idx_list, null_tag_dict

def read_schema_and_load(schema_file):

	# schema_property.txt文件第一行的读取
    logger.info("Reading schema through file: " + schema_file)
    f = open(schema_file)
    line = f.readline()
    tables = line[:-1].split(',')
    
    table_dict = {}
    if opt.dataset == 'IMDB':
        for tab in tables:
            table_dict[tab] = Table(name=tab, cols=IMDB_COLS_DICT[tab])
    else:
        for tab in tables:
            with open(opt.in_dir + tab + '.csv', 'r') as table_f:
                line = table_f.readline()   # csv文件的属性（字符串的形式，以逗号分隔）
            if opt.dataset == 'TPCH': 
                sep = '|'
            elif opt.dataset == 'Banking':
                sep = ';'
            else:
                sep = ','
            cols = line.split(sep=sep)
            table_dict[tab] = Table(name=tab, cols=cols)
   
    while(line != '[Foreign Key]\n'):
        line = f.readline()

    line = f.readline()
    while(line != '\n'):		#处理主外键引用关系
        
        line = line[:-1]
        ref_str = line.split('-')
        left_key = ref_str[0]
        right_key = ref_str[1]
        left_tab = left_key.split('.')
        right_tab = right_key.split('.')

        # left是被引用，tab[0]：表名，tab[1]：被引用的字段，
        # right是引用，tab[0]：表名，tab[1]：引用的字段，与外键类似


        # 2个以上的key联合，则添加相关信息
        if (len(left_tab[1].split(',')) > 1):
            table_dict[left_tab[0]].join_refered_idx.extend([table_dict[left_tab[0]].cols.index(i) for i in left_tab[1].split(',')])
            table_dict[right_tab[0]].join_fk.extend([table_dict[right_tab[0]].cols.index(i) for i in right_tab[1].split(',')])

        if (left_tab[1] not in table_dict[left_tab[0]].refered):
            # 首次被引用，初始化list，并添加引用信息
            table_dict[left_tab[0]].refered[left_tab[1]] = [(right_tab[0], right_tab[1])]
        else:
            # 非首次，append
            table_dict[left_tab[0]].refered[left_tab[1]].append((right_tab[0], right_tab[1]))

        # right引用别的表添加到right信息里边，确定生成顺序的队列要用到
        if (left_tab[0] not in table_dict[right_tab[0]].refer):
            table_dict[right_tab[0]].refer.append(left_tab[0])

        line = f.readline() 

    for tab in table_dict:
        table_dict[tab].refered_node = {key : [] for key in table_dict[tab].refered}

    while(f.readline() != '[Primary Key]\n'):
        pass

    line = f.readline()
    while(line != '\n'): 	# 处理主键
        line = line[:-1]    
        tab_pk = line.split('.')
        pk = tab_pk[1].split(',')
        table_dict[tab_pk[0]].pk_idx = [table_dict[tab_pk[0]].cols.index(i) for i in pk]
        line = f.readline()

    while(f.readline() != '[Tables do not scale]\n'):
        pass

    line = f.readline()
    line = line[:-1]
    if len(line) != 0:
        tab_not_scale = line.split(',')
        for tab in tab_not_scale:
            table_dict[tab].is_scale = False
                
    f.close()  

    for tab in list(table_dict.values()):    
        for info in list(tab.refered.values()):
            for tup in info:
                if not tab.is_scale:
                    table_dict[tup[0]].is_tab_refer_scale[tup[1]] = False
                else:
                    table_dict[tup[0]].is_tab_refer_scale[tup[1]] = True

    # print(f'table_dict是：{table_dict}')
    return table_dict

def laplace_noise(epsilon, t):
    tmp = np.exp(-epsilon / 2)
    return ((1 - tmp) / (1 + tmp)) * np.exp(-epsilon * np.abs(t) / 2)

def init_noise_dict(budget):
    a = 0
    noise_dict = {}
    for i in range(-100, 100, 1):
        a += laplace_noise(budget, i)
        noise_dict[a] = i
    noise_dict[1.0] = 100   
    noise_keys = list(noise_dict.keys())
    return noise_dict, noise_keys

if __name__  == '__main__':

    logger.info('######################## DB simulation config #############################')
    logger.info(f'coeffi: {opt.coeffi} | n_buckets: {opt.n_buckets} | muta_dist: {opt.muta_dist}')
    logger.info(f'scale_factor: {opt.scale_factor} | type_coeffi: {opt.type_coeffi} | cluster_per_col: {opt.cluster_per_col}')
    logger.info(f'dataset: {opt.dataset} | privacy budget: {opt.privacy_budget}')
    logger.info('###########################################################################')

    SPN_test.col_effi = opt.coeffi
    SPN_test.coeffi_type = opt.type_coeffi
    SPN_test.enable_eval = opt.eval
    SPN_test.cipher_dict = {}
    SPN_test.repeat_threshold = opt.repeat_threshold
    SPN_test.repeat_join_threshold = opt.repeat_join_threshold
    SPN_test.noise_dict_hist, SPN_test.noise_keys_hist = init_noise_dict(0.1 * opt.privacy_budget)
    SPN_test.noise_dict_clus, SPN_test.noise_keys_clus = init_noise_dict(0.09 * opt.privacy_budget / opt.cluster_per_col)
    SPN_test.col_epsilon = 0.01 * opt.privacy_budget
    SPN_test.noise_dict_join, SPN_test.noise_keys_join = init_noise_dict(0.8 * opt.privacy_budget)

    if not os.path.exists('../../result/' + opt.gen_dir + '/'):    # TODO
        os.mkdir('../../result/' + opt.gen_dir + '/')

    T_start = time.time()

    root_dict = {}

    table_dict = read_schema_and_load(opt.sche_file)  # 返回一个字典（记录着每张表的引用关系）
    # SPN_test.table_dict = table_dict

    # 依据各个表的依赖关系确定生成顺序 ################################################

    q = Queue(maxsize=10)
    for tab in table_dict:
        if len(table_dict[tab].refer) == 0:   # 没有引用关系的表
            q.put(table_dict[tab])

    while(not q.empty()):

        tab = q.get()

        tab.isVis = True

        tab.data, tab.cols, col_idx_list, tab.null_tag_dict = read_csv(opt.in_dir + tab.name + '.csv',                                                                
                                                                           tab=tab.name,
                                                                           dataset=opt.dataset)
        tab.str_col_idx = col_idx_list[0]
        tab.date_col_idx = col_idx_list[1]
        tab.cate_col_idx = col_idx_list[2]

        # 对于每个表，先看被引用的列
        for key in tab.refered:

            # 引用该列的表，ref_tab[0]为表名， ref_tab[1]为引用列
            for ref_tab in tab.refered[key]:
                
                wait = False

                # 看该表引用的表是否已经生成
                for ref in table_dict[ref_tab[0]].refer:
                    # 若有表尚未生成，则该表等待未生成的表生成
                    if (not table_dict[ref].isVis):
                        wait = True
                        break
                # 若引用的表已全部生成，则可进行该表的生成，加入待生成队列
                if (not wait and not table_dict[ref_tab[0]].isVis):
                    q.put(table_dict[ref_tab[0]])
                    table_dict[ref_tab[0]].isVis = True

    # 记录每个表的特殊类型列和带键的列 ###################################################

        # 传本表的引用他表的列索引以及被引用列索引
        refer_singcols = []
        for col in tab.refer_node:
            if (len(col.split(',')) > 1):
                continue
            refer_singcols.append(tab.cols.index(col))

        refered_singcols = []
        for col in tab.refered:
            if (len(col.split(',')) > 1):
                continue
            refered_singcols.append(tab.cols.index(col))

        idx_dict = {'refer_singcols':refer_singcols, 'refered_singcols':refered_singcols,
                    'str_col_idx':tab.str_col_idx, 'date_col_idx':tab.date_col_idx,
                    'pk_idx':tab.pk_idx, 'join_refered_idx':tab.join_refered_idx,
                    'join_fk':tab.join_fk, 'cate_col_idx':tab.cate_col_idx}
        
        jk_max_len = 0
        jk_all_idx = []
        all_keys = []

        for idx_list in ['pk_idx', 'join_refered_idx', 'join_fk']:
            if (len(idx_dict[idx_list]) > jk_max_len):
                jk_max_len = len(idx_dict[idx_list])
            jk_all_idx.extend(idx_dict[idx_list])
        
        for idx_list in ['refer_singcols', 'pk_idx', 'date_col_idx', 'cate_col_idx']:
            all_keys.extend(idx_dict[idx_list])
        all_keys = list(set(all_keys))
        jk_all_idx = list(set(jk_all_idx))
        
        idx_dict['all_keys'] = all_keys
        idx_dict['jk_all_idx'] = jk_all_idx


    # 初始化加密实例 ###########################################################################

        dataset = tab.data
        dataset = transpose(dataset)
        cipher_dict = {}
        key = OPE.generate_key()
        for i in range(len(dataset)):
            if i in tab.pk_idx:
                if len(tab.pk_idx) == 1:
                    SPN_test.pk_domain_diff = max(dataset[i]) - min(dataset[i]) + 1
                else:
                    SPN_test.pk_domain_diff = None
            elif i in tab.cate_col_idx:
                cipher_dict[tab.cols[i]] = [randint(0, 8), {}]
            elif i in tab.date_col_idx or i in idx_dict['all_keys']:
                continue
            else:
                if i in tab.null_tag_dict:
                    mi, ma, new_mi, new_ma, digits = get_new_domain(dataset[i],
                                                                    tab.null_tag_dict[i][1],
                                                                    tab.null_tag_dict[i][2])
                else:
                    mi, ma, new_mi, new_ma, digits = get_new_domain(dataset[i], None, None)
                if mi != None:
                    cipher = OPE(key, in_range=ValueRange(mi, ma), out_range=ValueRange(new_mi, new_ma))
                    cipher_dict[tab.cols[i]] = [cipher]
                if digits != None:
                    cipher_dict[tab.cols[i]].append(digits)

        SPN_test.cipher_dict[tab.name] = cipher_dict

    # 构建SPN ################################################################################# 

        logger.info("Start building SPN of table " + tab.name)
        T_build = time.time()

        SPN_test.row_split_threshold = len(tab.data) // 2**opt.cluster_per_col if (len(tab.data) // 2**opt.cluster_per_col > 0) else opt.cluster_per_col                                                            
        SPN_test.sum_node_max_depth = opt.cluster_per_col
        SPN_test.refer_node = tab.refer_node                                                               
        SPN_test.refered_node = tab.refered_node
        SPN_test.idx_dict = idx_dict
        SPN_test.jk_max_len = jk_max_len
        SPN_test.dataset = tab.data
        SPN_test.tab_name = tab.name
        SPN_test.col_names = tab.cols
        SPN_test.is_scale = tab.is_scale
        SPN_test.scale_factor = opt.scale_factor if tab.is_scale else 1
        SPN_test.is_tab_refer_scale = tab.is_tab_refer_scale
        SPN_test.n_buckets = opt.n_buckets
        SPN_test.null_tag_dict = tab.null_tag_dict

        col_idxs = [i for i in range(len(tab.data[0]))] 
        for col in reversed(col_idxs):                           
            if (col in idx_dict['all_keys'] or col in idx_dict['str_col_idx'] \
                or col in idx_dict['jk_all_idx']):
                col_idxs.remove(col)

        data_array = []
        for row in tab.data:
            val_row = []
            for i in col_idxs:
                val_row.append(row[i])
            data_array.append(val_row)
        
        data_array = np.array(data_array)
        if data_array.shape[1] != 0:
            data_array = MinMaxScaler().fit_transform(data_array)
        
        root_dict[tab.name] = SPN_test.SPN.construct_top_down(SPN_test.NodeScope.full_scope(tab.data), data_array)

    # 生成数据 #################################################################################

        # 将每个被引用的列的node_list传给引用该列的表
        for refered_key in tab.refered:
            refered_node = tab.refered_node[refered_key]
            for refer_tab in tab.refered[refered_key]:
                table_dict[refer_tab[0]].refer_node[refer_tab[1]] = [refered_node, SPN_test.pk_domain_diff]

        logger.info("Start generating data of table " + tab.name)
        gen_data = gen(root_dict[tab.name], tab.refer_node)
        gen_data = sorted(gen_data, key = lambda x : x[0])

        with open('../../result/' + opt.gen_dir + '/' + tab.name + '.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f, delimiter='|' if opt.dataset == 'TPCH' else ',')
            writer.writerow(tab.cols)
            writer.writerows(gen_data)

        # pd.DataFrame(gen_data).to_csv('../../result/tpch_10to20/' + tab.name + '_0.01_gen.csv', sep='|', header=tab.cols, encoding='UTF8', index=False)
        
    # 评估 ###################################################################################

        if opt.eval:
            sc_mean_diff = np.average(SPN_test.sc_diff_list, weights=SPN_test.sc_weight_list) if SPN_test.sc_weight_list else nan
            cc_mean_diff = np.average(SPN_test.cc_diff_list, weights=SPN_test.cc_weight_list) if SPN_test.cc_weight_list else nan
            KL_div = np.average(SPN_test.KL_div_list, weights=SPN_test.kl_weight_list) if SPN_test.kl_weight_list else nan

            logger.info(f"Mean error of silhouette coefficient is {{{round(sc_mean_diff, 3)}}}")
            logger.info(f"Mean error of correlation coefficient is {{{round(cc_mean_diff, 3)}}}")
            logger.info(f"Mean error of KL divergence is {{{round(KL_div, 3)}}}")
            SPN_test.sc_diff_list = []
            SPN_test.sc_weight_list = []
            SPN_test.cc_diff_list = []  
            SPN_test.cc_weight_list = []
            SPN_test.KL_div_list = []
            SPN_test.kl_weight_list = []
        logger.info(f"Duration of generating table {{{tab.name}}} is {{{round(time.time() - T_build, 2)}}} s\n")

    logger.info(f'Total duration is {round(time.time() - T_start, 2)} s')
    
    # query predicate value 映射 ########################

    # if opt.dataset == 'IMDB':
    #     for query_file in ['job-light-sub-query',
    #                     'job-light',
    #                     'mscn_400',
    #                     'mscn_sample_1000',
    #                     'mscn_full'                      
    #                     ]:
    #         logger.info("Start mapping predicate values of {}".format(query_file))
    #         parse_queries_csv('../../queries/{}.csv'.format(query_file), SPN_test.cipher_dict, query_file)
    # elif opt.dataset == 'CENSUS':
    #     with open('../../queries/census_test.txt', 'r') as f:
    #         query_and_card_list = json.load(f)
    #     query_list = query_and_card_list['query_list']
     
    #     cipher = SPN_test.cipher_dict['census']
    #     for query in query_list:           
    #         for i in range(len(query[0])):
    #             if type(cipher[query[0][i]][0]) == int:
    #                 query[2][i] = cipher[query[0][i]][1][query[2][i]]
    #             else:
    #                 query[2][i] = str(cipher[query[0][i]][0].encrypt(int(query[2][i])))
    #     with open('../../queries/census_test_cipher.txt', 'w') as f:
    #         f.write(json.dumps(query_and_card_list))
    # elif opt.dataset == 'DMV':
    #     with open('../../queries/dmv_test.txt', 'r') as f:
    #         query_and_card_list = json.load(f)
    #     query_list = query_and_card_list['query_list']
     
    #     cipher = SPN_test.cipher_dict['DMV']
    #     for query in query_list:           
    #         for i in range(len(query[0])):
    #             if query[0][i] not in cipher:
    #                 continue
    #             elif type(cipher[query[0][i]][0]) == int:
    #                 query[2][i] = cipher[query[0][i]][1][query[2][i]]
    #             else:
    #                 query[2][i] = str(cipher[query[0][i]][0].encrypt(int(query[2][i])))
    #     with open('../../queries/dmv_test_cipher.txt', 'w') as f:
    #         f.write(json.dumps(query_and_card_list))
    # logger.info("Done.")

    # 保存实验配置和结果 #######################################################################################
    # config_list = ['n_buckets','cluster_per_col','coeffi','type_coeffi','scale_factor',
    #                 'PS_SCME','PS_SCME_W','PS_CCME','PS_CCME_W','PS_KLDiv','PS_KLDiv_W',
    #                 'PS_GENTIME','O_SCME','O_SCME_W','O_CCME','O_CCME_W','O_KLDiv',
    #                 'O_KLDiv_W','O_GENTIME','L_SCME','L_SCME_W','L_CCME','L_CCME_W','L_KLDiv','L_KLDiv_W','L_GENTIME'
    #                 ]
    # with open('../../report/statistics_{}.csv'.format(datetime.now().strftime("%d%m")), 'a', encoding='UTF8', newline='') as f:                  
    #     writer = csv.writer(f, delimiter=',')
    #     writer.writerow(config_list)
    #     writer.writerows(res)  




