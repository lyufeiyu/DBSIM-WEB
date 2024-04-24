from enum import Enum
import csv
from sklearn.cluster import MiniBatchKMeans
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import silhouette_score
import numpy as np
from networkx import from_numpy_matrix, connected_components
import random
import radar
from scipy.spatial import KDTree
import itertools
from scipy.stats import rankdata
import pandas as pd
import math

MIN_VAL = int(-2**64)
MAX_VAL = int(2**64)

logging = None
row_split_threshold = None
sum_node_max_depth = None
col_effi = None
coeffi_type = None

tab_name = None
col_names = None                                                              
refer_node = None                                                               
refered_node = None
idx_dict = None
jk_max_len = None
dataset = None
is_scale = True
scale_factor = None
pk_domain_diff = None
is_tab_refer_scale = None
enable_eval = None
verbose = False
n_buckets = None
null_tag_dict = None
repeat_threshold = None
repeat_join_threshold = None
privacy_budget = None
col_epsilon = None

sc_diff_list = []
sc_weight_list = []
cc_diff_list = []
cc_weight_list = []
KL_div_list = []
kl_weight_list = []
cipher_dict = None
noise_dict_hist = {}
noise_keys_hist = None
noise_dict_clus = {}
noise_keys_clus = None
noise_dict_join = {}
noise_keys_join = None

def calibrate_idxs(data, idxs, isCol: bool):
    if (isCol):
        data = list(map(list, zip(*data))) #zip(*)求转置，map将元组转回list
        data = sorted(data, key = lambda x : idxs[get_index(data, x)])  #对每个元素都用其下标去索引col_idxs，得到其排序的位置
        data = list(map(list, zip(*data)))
    else:
        data = sorted(data, key = lambda x : idxs[get_index(data, x)])
    idxs.sort()
    return data, idxs

def get_index(lst, element):
    for i, e in enumerate(lst):
        if e is element:
            return i
    return -1

def transpose(in_list):
    return list(map(list, zip(*in_list)))

def verify_sample_shapes(s1, s2, k):
    # Expects [N, D]
    assert(len(s1.shape) == len(s2.shape) == 2)
    # Check dimensionality of sample is identical
    assert(s1.shape[1] == s2.shape[1])

def scipy_estimator(s1, s2, k=1):
    """KL-Divergence estimator using scipy's KDTree
    s1: (N_1,D) Sample drawn from distribution P
    s2: (N_2,D) Sample drawn from distribution Q
    k: Number of neighbours considered (default 1)
    return: estimated D(P|Q)
    """
    verify_sample_shapes(s1, s2, k)

    n, m = len(s1), len(s2)
    d = float(s1.shape[1])
    D = np.log(m / (n - 1))

    nu_d, _ = KDTree(s2).query(s1, k)
    rho_d, _ = KDTree(s1).query(s1, k + 1)

    # KTree.query returns different shape in k==1 vs k > 1
    if k > 1:
        D += (d / n) * np.sum(np.log(nu_d[::, -1] / rho_d[::, -1]))
    else:
        D += (d / n) * np.sum(np.log(nu_d / rho_d[::, -1]))
    return D

def rdc(x, y, f=np.sin, k=20, s=1/6., n=1):
    """
    Computes the Randomized Dependence Coefficient
    x,y: numpy arrays 1-D or 2-D
         If 1-D, size (samples,)
         If 2-D, size (samples, variables)
    f:   function to use for random projection
    k:   number of random projections to use
    s:   scale parameter
    n:   number of times to compute the RDC and
         return the median (for stability)
    According to the paper, the coefficient should be relatively insensitive to
    the settings of the f, k, and s parameters.
    """
    if n > 1:
        values = []
        for i in range(n):
            try:
                values.append(rdc(x, y, f, k, s, 1))
            except np.linalg.linalg.LinAlgError: pass
        return np.median(values)

    if len(x.shape) == 1: x = x.reshape((-1, 1))
    if len(y.shape) == 1: y = y.reshape((-1, 1))

    # Copula Transformation
    cx = np.column_stack([rankdata(xc, method='ordinal') for xc in x.T])/float(x.size)
    cy = np.column_stack([rankdata(yc, method='ordinal') for yc in y.T])/float(y.size)

    # Add a vector of ones so that w.x + b is just a dot product
    O = np.ones(cx.shape[0])
    X = np.column_stack([cx, O])
    Y = np.column_stack([cy, O])

    # Random linear projections
    Rx = (s/X.shape[1])*np.random.randn(X.shape[1], k)
    Ry = (s/Y.shape[1])*np.random.randn(Y.shape[1], k)
    X = np.dot(X, Rx)
    Y = np.dot(Y, Ry)

    # Apply non-linear function to random projections
    fX = f(X)
    fY = f(Y)

    # Compute full covariance matrix
    C = np.cov(np.hstack([fX, fY]).T)

    # Due to numerical issues, if k is too large,
    # then rank(fX) < k or rank(fY) < k, so we need
    # to find the largest k such that the eigenvalues
    # (canonical correlations) are real-valued
    k0 = k
    lb = 1
    ub = k
    while True:

        # Compute canonical correlations
        Cxx = C[:k, :k]
        Cyy = C[k0:k0+k, k0:k0+k]
        Cxy = C[:k, k0:k0+k]
        Cyx = C[k0:k0+k, :k]

        eigs = np.linalg.eigvals(np.dot(np.dot(np.linalg.pinv(Cxx), Cxy),
                                        np.dot(np.linalg.pinv(Cyy), Cyx)))

        # Binary search if k is too large
        if not (np.all(np.isreal(eigs)) and
                0 <= np.min(eigs) and
                np.max(eigs) <= 1):
            if ub == 1:
                break
            ub -= 1
            k = (ub + lb) // 2
            continue
        if lb == ub: break
        lb = k
        if ub == lb + 1:
            k = ub
        else:
            k = (ub + lb) // 2

    return np.sqrt(np.max(eigs))

def make_multicol_name(col_names, col_idx):
    key = ''
    for idx in col_idx:
        key += col_names[idx] + ','
    key = key[:-1]
    return key

def cul_unionkey_freq(leaf_data):
    data = leaf_data
    if (len(leaf_data[0]) > 2):
        data = transpose(leaf_data)
        data = [data[0].copy(), data[1].copy()]
        data = transpose(data)
        data.sort()
    freq = []
    f = 0
    last_val = data[0][0]
    for vals in data:
        if (vals[0] == last_val):
            f += 1
        else:
            freq.append(f)
            f = 0
            last_val = vals[0]
    return freq

def splitcol_by_rmcol(col_idxs, left_cols):
    for col in left_cols:
        col_idxs.remove(col)

def get_val_col(col_idxs, idx_dict):
    val_col_cur_idx = []
    for i in col_idxs:
        if i not in idx_dict['all_keys']:
            val_col_cur_idx.append(col_idxs.index(i))
    return val_col_cur_idx

def binary_search(arr, target):
    """
    在有序数组arr中搜索目标值target
    如果找到则返回其下标，否则返回-1
    """
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return True
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return False

def exponential_mechanism(values, sensitivity, epsilon):
    """
    values: 一个列表，包含了所有可能的输出值
    sensitivity: 敏感性，即在数据集中添加或删除一个元素可能导致的最大输出变化
    epsilon: 隐私预算
    """
    # 计算每个值的概率
    probabilities = [math.exp(epsilon * value / (2 * sensitivity)) for value in values]
    
    # 归一化概率
    probabilities = [p / sum(probabilities) for p in probabilities]
    
    # 从values中按照probabilities的概率选择一个值
    chosen_value = np.random.choice(values, p=probabilities)
    
    return chosen_value


class NextOP(Enum):
    CREATE_LEAF = 1
    SPLIT_COLS = 2
    SPLIT_ROWS = 3

class DataType(Enum):
    STRING = 1
    INTEGER = 2
    DECIMAL = 3
    DATE = 4
    CATEGORY = 5

class NodeScope:
    def __init__(self, row_idxs, col_idxs):
        self.row_idxs = row_idxs
        self.col_idxs = col_idxs

    def n_rows(self):
        return len(self.row_idxs)

    def n_cols(self):
        return len(self.col_idxs)

    def __repr__(self):
        return f'NodeScope{{rows:[{self.row_idxs}), cols:{self.col_idxs}}}'

    @staticmethod
    def full_scope(dataset):
        assert(len(dataset) > 0) # cannot be empty
        row_idxs = [i for i in range(0, len(dataset))]
        col_idxs = [i for i in range(0, len(dataset[0]))]
        return NodeScope(row_idxs, col_idxs)

class LeafNode:
    def __init__(self, d_type, scope, check_constraints, leaf_data, hist, freq_dict, not_found_vals_list, repeat_join_dict = None):
        self.id = None
        self.d_type = d_type
        self.scope = scope
        self.col_idx = scope.col_idxs
        self.sel = None
        self.leaf_data = leaf_data
        self.check_c = check_constraints
        self.hist = hist  
        self.freq_dict = freq_dict
        self.not_found_vals_list = not_found_vals_list
        self.repeat_join_dict = repeat_join_dict
        self.data_sam = None
        self.mi = None
        self.ma = None

        if verbose:
            print("constructing LEAT_NODE completed...")

    @staticmethod
    def construct_leafnode_multicol(scope):
        
        col_idxs = scope.col_idxs
        leaf_data = []
        for row_idx in scope.row_idxs:
            rows = []
            for col_idx in scope.col_idxs:
                rows.append(dataset[row_idx][col_idx])
            leaf_data.append(rows)
        
        leaf_data.sort()

        if col_idxs[0] in idx_dict['date_col_idx'] and col_idxs[1] in idx_dict['date_col_idx']:
            d_type = DataType.DATE
        elif type(leaf_data[0][0]) == int and type(leaf_data[0][1]) == int:
            d_type = DataType.INTEGER            
        elif type(leaf_data[0][0]) == float and type(leaf_data[0][1]) == float:
            d_type = DataType.DECIMAL            
        elif type(leaf_data[0][0]) == str:
            d_type = DataType.STRING
        
        assert(d_type == DataType.INTEGER or d_type == DataType.DECIMAL)
        
        is_singrefered = False
        is_singrefer = False
        is_pk = False
        is_join_refered = False
        is_join_fk = False

        if idx_dict['pk_idx'] == col_idxs:
            is_pk = True

        if set(idx_dict['refer_singcols']).issubset(set(col_idxs)):
            is_singrefer = True

        if set(idx_dict['refered_singcols']).issubset(set(col_idxs)):
            is_singrefered= True

        if idx_dict['join_fk'] == col_idxs:
            is_join_fk = True

        if idx_dict['join_refered_idx'] == col_idxs:
            is_join_refered = True

        freq_dict = {}
        
        # 多列外键但并非复合外键，即每一列外键各自进行引用，每一列各自计算fanout即可
        if not is_join_fk and is_singrefer:
            leaf_data = transpose(leaf_data)
            for i, col in enumerate(col_idxs):
                if col in idx_dict['refer_singcols']:
                    freq_dict[col] = {}
                    col_data = leaf_data[i].copy()
                    col_data.sort()
                    LeafNode.cul_fanout_tpch(col_data, refer_node, col_names[col], freq_dict[col])
            leaf_data = transpose(leaf_data)

        # 复合外键，直接看作整体计算fanout
        elif is_join_fk:
            col_name = make_multicol_name(col_names, col_idxs)
            LeafNode.cul_fanout_tpch(leaf_data, refer_node, col_name, freq_dict)

        # 除了复合外键，所有多列作为key的情况，计算组合频率 （弃用）
        # unikey_freq = None
        # if (not is_join_fk):
        #     unikey_freq = cul_unionkey_freq(leaf_data)

        hist = None
            
        check_constraints = {'is_singrefered':is_singrefered, 'is_singrefer':is_singrefer, 'is_pk':is_pk,
                            'is_join_refered':is_join_refered, 'is_join_fk':is_join_fk}
        leafnode = LeafNode(d_type, scope, check_constraints, None, hist, freq_dict, None)
        
        if is_singrefered:
            leafnode.leaf_data = leaf_data

            # 被引用的node用list装起来，这里有必要吗，多列键有可能被单引用吗
        
            for col in col_idxs:
                if (col in idx_dict['refered_singcols']):
                    refered_node[col_names[col]].append(leafnode)
        if is_join_refered:
            leafnode.leaf_data = leaf_data
            key = make_multicol_name(col_names, col_idxs)
            refered_node[key].append(leafnode)
        return leafnode 

    @staticmethod
    def construct_leafnode(scope):
        
        if scope.n_rows() == 1 and dataset[scope.row_idxs[0]][1] == np.nan:
            a = 1

        col_idx = scope.col_idxs[0]
        leaf_data = []
        for row_idx in scope.row_idxs:
            leaf_data.append(dataset[row_idx][col_idx])

        if col_idx in idx_dict['date_col_idx']:
            d_type = DataType.DATE
            leaf_data.sort()
        elif col_idx in idx_dict['cate_col_idx']:
            d_type = DataType.CATEGORY
        elif type(leaf_data[0]) == int:
            d_type = DataType.INTEGER
            leaf_data.sort()
        elif type(leaf_data[0]) == float:
            d_type = DataType.DECIMAL
            leaf_data.sort()
        elif type(leaf_data[0]) == str:
            d_type = DataType.STRING
        
        is_singrefered = False
        for col in idx_dict['refered_singcols']:
            if col == col_idx:
                is_singrefered = True
                break
        is_singrefer = False
        for col in idx_dict['refer_singcols']:
            if col == col_idx:
                is_singrefer = True
                
                if col_idx in null_tag_dict:
                    tag = null_tag_dict[col_idx]
                    for i in range(len(leaf_data)):
                        if leaf_data[i] == tag:
                            leaf_data[i] = np.nan
                        elif type(leaf_data[i]) == float:
                            leaf_data[i] = int(leaf_data[i])

                elif type(leaf_data[0]) == float:
                    leaf_data = [int(x) for x in leaf_data]
                
        is_pk = False
        if col_idx in idx_dict['pk_idx']:
            is_pk = True
               
        freq_dict = {}
        repeat_join_dict = {}
        hist = None     
        not_found_vals_list = None

        if is_singrefer:
            not_found_vals_list = LeafNode.cul_fanout(leaf_data, refer_node, col_names[col_idx], freq_dict, repeat_join_dict)
            perturb_dict(repeat_join_dict, noise_keys=noise_keys_join, noise_dict=noise_dict_join)
        elif not is_pk:
            if d_type == DataType.DECIMAL or d_type == DataType.INTEGER or d_type == DataType.DATE:
                if col_idx in null_tag_dict:
                    if d_type == DataType.DECIMAL:
                        hist = Histogram(leaf_data, n_buckets, null_tag_dict[col_idx][0], cipher_dict[tab_name][col_names[col_idx]][1]) # n_buckets is a very important parameter.
                    else:
                        hist = Histogram(leaf_data, n_buckets, null_tag_dict[col_idx][0], None) # n_buckets is a very important parameter.

                else:
                    if d_type == DataType.DECIMAL:
                        hist = Histogram(leaf_data, n_buckets, None, cipher_dict[tab_name][col_names[col_idx]][1])
                    else:
                        hist = Histogram(leaf_data, n_buckets, None, None)
        check_constraints = {'is_singrefered':is_singrefered, 'is_singrefer':is_singrefer, 'is_pk':is_pk,
                            'is_join_refered':None, 'is_join_fk':None}
          
        leafnode = LeafNode(d_type, scope, check_constraints, None, hist, freq_dict, not_found_vals_list, repeat_join_dict)
        if d_type == DataType.STRING:
            leafnode.leaf_data = leaf_data
        if d_type == DataType.CATEGORY:
            hist = {}
            for item in leaf_data:
                if item not in hist:
                    hist[item] = 1
                else:
                    hist[item] += 1
            perturb_dict(hist, noise_keys=noise_keys_hist, noise_dict=noise_dict_hist)
            leafnode.hist = hist
        if is_singrefered:
            leafnode.leaf_data = leaf_data
            leafnode.mi = leaf_data[0]
            leafnode.ma = leaf_data[-1]
            refered_node[col_names[col_idx]].append(leafnode)
        if is_pk:
            leafnode.leaf_data = leaf_data
        return leafnode         


    # leaf_data 当前叶子节点数据
    # refer_node 当前列引用的列的所有节点，以指针列表给出
    # col_name 当前列的名字
    # freq_dict 所要计算的fanout，类型为字典，例如：{1 : [2, 3]} 表示引用了第1个节点的2个值，重复频率分别为2和3
    @staticmethod
    def cul_fanout(leaf_data, refer_node, col_name, freq_dict, repeat_join_dict):
        refer_col_node = refer_node[col_name][0]
        last_val = None
        last_bucket = None
        last_node = None
        not_found_vals_list = []
        for val in leaf_data:
            # 遍历每个值，由于已升序排列，故重复值直接数量+1
            if val == last_val:
                last_bucket[-1] += 1
                continue
            elif last_bucket:
                if last_bucket[-1] > repeat_join_threshold: 
                    repeat_join_dict[last_val] = last_bucket[-1]
                    del last_bucket[-1]
            if last_node:
                if binary_search(last_node.leaf_data, val):
                    last_bucket.append(1)
                    last_val = val                   
                    continue
            is_found = False
            for i in range(len(refer_col_node)):

                if val > refer_col_node[i].ma or val < refer_col_node[i].mi:
                    continue

                # 查找每个node的每个值
                if binary_search(refer_col_node[i].leaf_data, val):

                    # 若找到，则在该node的fanout频率+1，并记录最新的freq bucket
                    is_found = True
                    if (i not in freq_dict):
                        freq_dict[i] = []
                    freq_dict[i].append(1)
                    last_val = val
                    last_bucket = freq_dict[i]
                    last_node = refer_col_node[i]
                    break   
            if not is_found:
                not_found_vals_list.append(val)
        if len(not_found_vals_list) == 0:
            not_found_vals_list = None
        return not_found_vals_list

    @staticmethod
    def cul_fanout_tpch(leaf_data, refer_node, col_name, freq_dict):
        refer_col_node = refer_node[col_name][0]
        last_val = None
        last_bucket = None
        last_node = None
        not_found_vals_list = []
        for val in leaf_data:
            # 遍历每个值，由于已升序排列，故重复值直接数量+1
            if val == last_val:
                last_bucket[-1] += 1
                continue
            elif last_node:
                if binary_search(last_node.leaf_data, val):
                    last_bucket.append(1)
                    last_val = val                   
                    continue
            is_found = False
            for i in range(len(refer_col_node)):

                # 查找每个node的每个值
                if binary_search(refer_col_node[i].leaf_data, val):

                    # 若找到，则在该node的fanout频率+1，并记录最新的freq bucket
                    is_found = True
                    if (i not in freq_dict):
                        freq_dict[i] = []
                    freq_dict[i].append(1)
                    last_val = val
                    last_bucket = freq_dict[i]
                    last_node = refer_col_node[i]
                    break   
            if not is_found:
                not_found_vals_list.append(val)
        if len(not_found_vals_list) == 0:
            not_found_vals_list = None
        return not_found_vals_list

    def assign_id(self, id, G):
        self.id = id
        return id

    def assign_id_postorder(self, id, G, label_dict):
        self.id = id
        label_dict[id] = str(round(self.sel, 2))
        G.add_node(id)
        return id

    def debug_print(self, prefix, indent):
        print('%sLeafNode: %s, %s' % (prefix, self.scope, self.hist))
    
    # def debug_print(self, prefix, indent):
    #     print('%sLeafNode: ' % (prefix))

    def estimate(self, range_query, sel_list):
        left, right = range_query.column_range(col_names, MIN_VAL, MAX_VAL)
        row_cnt = self.hist.between_row_count(left, right)
        sel = float(row_cnt) / float(self.scope.n_rows())
        sel_list.append(sel)
        self.sel = sel
        return sel, sel_list

    def gen_data(self, refer_cols_node):
        data = []
        col_idxs = []
        row_idxs = []
        if len(self.col_idx) > 1:

            if self.check_c['is_join_fk']:
                refer_col_node = refer_cols_node[make_multicol_name(col_names, self.col_idx)][0]
                
                for i in self.freq_dict:
                    freq_list = self.freq_dict[i]
                    freq_list *= scale_factor               
                    sam_list = random.sample(refer_col_node[i].data_sam, len(freq_list))
                    for j in range(len(freq_list)):
                        data.extend([sam_list[j].copy() for _ in range(freq_list[j])])
                random.shuffle(data)
                                                                                
            elif self.check_c['is_singrefer']:
                data_0 = []
                data_1 = []
                if self.col_idx == idx_dict['refer_singcols']:
                    ref_col_node_0 = refer_cols_node[col_names[self.col_idx[0]]][0]
                    ref_col_node_1 = refer_cols_node[col_names[self.col_idx[1]]][0]
                    
                    for i in self.freq_dict[self.col_idx[0]]:
                        freq_list = self.freq_dict[self.col_idx[0]][i]  
                        freq_list *= scale_factor             
                        sam_list = random.sample(ref_col_node_0[i].data_sam, len(freq_list))
                        for j in range(len(freq_list)):
                            data_0.extend([sam_list[j].copy() for _ in range(freq_list[j])])

                    
                    for i in self.freq_dict[self.col_idx[1]]:
                        freq_list = self.freq_dict[self.col_idx[1]][i]  
                        freq_list *= scale_factor              
                        sam_list = random.sample(ref_col_node_1[i].data_sam, len(freq_list))
                        for j in range(len(freq_list)):
                            data_1.extend([[sam_list[j][0], freq_list[j]]])
                    j = 0
                    last_val = None
                    data_left = []
                    data_0.append([None])
                    for i in range(len(data_0)):
                        if data_0[i][0] == last_val:
                            continue
                        else:
                            if (i - j) <= len(data_1):
                                sam_list = random.sample(data_1, i - j)
                                for sam in sam_list:
                                    data_0[j].append(sam[0])
                                    sam[1] -= 1
                                    if sam[1] == 1:
                                        data_left.append(sam[0])
                                        data_1.remove(sam)
                                    j += 1                                
                            else:
                                if len(data_1) != 0:
                                    k = len(data_1)                               
                                    sam_list = random.sample(data_left, i - j - k)
                                    for item in data_1:
                                        sam_list.append(item[0])
                                        item[1] -= 1
                                        data_left.append(item[0])
                                        if item[1] == 0:                                            
                                            data_1.remove(item)
                                else:
                                    sam_list = random.sample(data_left, i - j)

                                for sam in sam_list:
                                    data_0[j].append(sam)
                                    data_left.remove(sam)
                                    j += 1
                            
                            last_val = data_0[i][0]
                    data_0.pop(len(data_0) - 1)
                    data = data_0

                else:
                    if self.col_idx[0] in idx_dict['refer_singcols']:
                        idx_0 = self.col_idx.index(self.col_idx[0])                        
                    else:
                        idx_0 = self.col_idx.index(self.col_idx[1])                       
                        self.col_idx = [self.col_idx[1], self.col_idx[0]]
                    
                    ref_col_node_0 = refer_cols_node[col_names[idx_0]][0]
                    for i in self.freq_dict[idx_0]:
                        freq_list = self.freq_dict[idx_0][i]  
                        freq_list *= scale_factor             
                        sam_list = random.sample(ref_col_node_0[i].data_sam, len(freq_list))
                        for j in range(len(freq_list)):
                            data_0.extend([sam_list[j][0] for _ in range(freq_list[j])])

                    data_1 = []
                    last_val = None
                    last_count = 0
                    data_0.append(None)
                    for val in data_0:
                        if val == last_val:
                            last_count += 1
                        else:
                            last_val = val                           
                            for i in range(last_count):
                                data_1.append(i)
                            last_count = 1
                    data_0.pop(len(data_0) - 1)
                    data.append(data_0)
                    data.append(data_1)
                    data = transpose(data)

            if self.check_c['is_join_refered']:
                self.data_sam = [x.copy() for x in data]

        else:
            if self.check_c['is_singrefer']:
            
                refer_col_node = refer_cols_node[col_names[self.col_idx[0]]]

                if len(self.repeat_join_dict) != 0:
                    if is_tab_refer_scale[col_names[self.col_idx[0]]]:
                        for i in range(scale_factor):
                            if i == 0:
                                for k, v in self.repeat_join_dict.items():
                                    data.extend([k] * v)
                            else:
                                diff = refer_col_node[1]
                                for k, v in self.repeat_join_dict.items():
                                    data.extend([k + i * diff] * v)
                    else:
                        for k, v in self.repeat_join_dict.items():
                            data.extend([k] * v * scale_factor) 

                data = transpose([data])                                                      

                if is_tab_refer_scale[col_names[self.col_idx[0]]]:               
                    for i in self.freq_dict:
                        freq_list = self.freq_dict[i]
                        freq_list *= scale_factor                
                        sam_list = random.sample(refer_col_node[0][i].data_sam, len(freq_list))
                        for j in range(len(freq_list)):
                            data.extend([sam_list[j].copy() for _ in range(freq_list[j])])
                else:
                    for _ in range(scale_factor):
                        for i in self.freq_dict:
                            freq_list = self.freq_dict[i]                                     
                            sam_list = random.sample(refer_col_node[0][i].data_sam, len(freq_list))
                            for j in range(len(freq_list)):
                                data.extend([sam_list[j].copy() for _ in range(freq_list[j])])

                if self.not_found_vals_list:
                    diff = refer_col_node[1]
                    not_found_vals = np.array(self.not_found_vals_list)
                    for i in range(scale_factor):
                        if i != 0:
                            not_found_vals += diff
                        data.extend([[d] for d in not_found_vals])

                if self.check_c['is_singrefered']:
                    self.data_sam = [x.copy() for x in data]

            elif self.check_c['is_singrefered'] or self.check_c['is_pk']:
                diff = pk_domain_diff
                leaf_data = np.array(self.leaf_data)
                for i in range(scale_factor):
                    if i != 0:
                        leaf_data += diff
                    data.extend([[d] for d in leaf_data])
                self.data_sam = [x.copy() for x in data]
             
            else:
                if self.d_type == DataType.STRING:
                    for s in self.leaf_data:                       
                        # for _ in range(scale_factor):
                        #     new_str_list = []
                        #     for _ in range(len(s)):
                        #         new_str_list.append(chr(random.randint(49, 122)))
                            # data.append([''.join(new_str_list)])
                        data.append([s])

                elif self.d_type == DataType.CATEGORY:
                    # cipher = cipher_dict[tab_name]
                    # cipher_int = cipher[col_names[self.col_idx[0]]][0]
                    # transform_dict = cipher[col_names[self.col_idx[0]]][1]
                    for item in self.hist:
                        if type(item) == float:
                            data.extend([''] * (self.hist[item] * scale_factor))
                            continue
                        # new_str_list = []
                        # for s in item:
                        #     new_ascii = ord(s) + cipher_int
                        #     while new_ascii > 90 :
                        #         new_ascii = new_ascii - 26
                        #     while new_ascii < 65:
                        #         new_ascii = new_ascii + 26
                        #     new_str_list.append(chr(new_ascii))
                        # new_str = ''.join(new_str_list)  
                        # transform_dict[item] = new_str                  
                        data.extend([item]*(self.hist[item] * scale_factor))
                    random.shuffle(data)
                    data = transpose([data])

                elif self.d_type == DataType.DECIMAL:
                    # cipher = cipher_dict[tab_name]
                    # digits = 10 ** cipher[col_names[self.col_idx[0]]][1]
                    # cipher = cipher[col_names[self.col_idx[0]]][0]
                    if self.hist.null_count != None:
                        data.extend([''] * (self.hist.null_count * scale_factor))
                    
                    for val, freq in self.hist.repeat_dict.items():
                        # val = cipher.encrypt(int(val * digits)) / digits
                        data.extend([val] * (freq * scale_factor))
                    
                    for i in range(len(self.hist.buckets)):

                        lower = self.hist.buckets[i].lower_bound
                        upper = self.hist.buckets[i].upper_bound
                        # lower = cipher.encrypt(lower)
                        # upper = cipher.encrypt(upper)

                        for _ in range(self.hist.buckets[i].row_count * scale_factor):                            
                            data.append(random.uniform(lower, upper))
                    data = transpose([data])
                
                elif self.d_type == DataType.INTEGER:
                    # cipher = cipher_dict[tab_name]
                    # cipher = cipher[col_names[self.col_idx[0]]][0]
                    if self.hist.null_count != None:
                        data.extend([''] * (self.hist.null_count * scale_factor))
                    
                    for val, freq in self.hist.repeat_dict.items():
                        
                        # val = cipher.encrypt(val)
                        data.extend([val] * (freq * scale_factor))

                    for i in range(len(self.hist.buckets)):
                        # if i == 0:
                        #     count = self.hist.buckets[i].row_count  
                        # else:
                        #     count = self.hist.buckets[i].row_count - self.hist.buckets[i - 1].row_count

                        lower = self.hist.buckets[i].lower_bound
                        upper = self.hist.buckets[i].upper_bound
                        # lower = cipher.encrypt(lower)
                        # upper = cipher.encrypt(upper)

                        for _ in range(self.hist.buckets[i].row_count * scale_factor):
                            data.append(random.randint(lower, upper))
                    data = transpose([data])
                
                elif self.d_type == DataType.DATE:
                    if self.hist.null_count != None:
                        data.extend([''] * (self.hist.null_count * scale_factor))
                    
                    for val, freq in self.hist.repeat_dict.items():                       
                        data.extend([val.strftime('%Y-%m-%d')] * (freq * scale_factor))

                    for i in range(len(self.hist.buckets)):
                
                        for _ in range(self.hist.buckets[i].row_count * scale_factor): 
                            data.append(radar.random_date(self.hist.buckets[i].lower_bound, self.hist.buckets[i].upper_bound).strftime('%Y-%m-%d'))
                            # data.append([str(np.datetime64(radar.random_date(self.hist.buckets[i].lower_bound, self.hist.buckets[i].upper_bound)))])
                    data = transpose([data])
        random.shuffle(data)
        col_idxs.extend(self.col_idx)
        row_idxs.extend(self.scope.row_idxs * scale_factor) 
        assert len(row_idxs) == len(data)
        return data, col_idxs, row_idxs, [1, 1, 1]   

class SumNode:

    depth = 0

    def __init__(self, scope, lchild, rchild, silhou_coeffi, dataset):
        self.id = None
        self.scope = scope
        self.lchild = lchild
        self.rchild = rchild
        self.silhou_coeffi = silhou_coeffi if enable_eval else None 
        self.dataset = dataset if enable_eval else None
        if verbose:
            print("constructing SUM_NODE completed...")

    def assign_id(self, id, G):
        self.id = id
        G.add_node(id)
        id = self.lchild.assign_id(id + 1, G)
        G.add_edge(self.id, self.id + 1)
        id = self.rchild.assign_id(id + 1, G)
        G.add_edge(self.id, self.rchild.id)
        return id

    def assign_id_postorder(self, id, G, label_dict):
        id = self.lchild.assign_id_postorder(id, G, label_dict)
        id = self.rchild.assign_id_postorder(id + 1, G, label_dict)
        self.id = id + 1
        label_dict[self.id] = '+'
        G.add_node(self.id)
        G.add_edge(self.id, self.lchild.id)
        G.add_edge(self.id, self.rchild.id)
        return id + 1

    def debug_print(self, prefix, indent):
        print('%sSumNode: %s' % (prefix, self.scope))
        self.lchild.debug_print(prefix+indent, indent)
        self.rchild.debug_print(prefix+indent, indent)

    def estimate(self, range_query, sel_list):
        l_sel, sel_list = self.lchild.estimate(range_query, sel_list)
        r_sel, sel_list = self.rchild.estimate(range_query, sel_list)
        l_rows = self.lchild.scope.n_rows()
        r_rows = self.rchild.scope.n_rows()
        l_weight = float(l_rows) / float(l_rows + r_rows)
        r_weight = float(r_rows) / float(l_rows + r_rows)
        res = l_sel*l_weight + r_sel*r_weight
        sel_list.append(res)
        return res, sel_list 

    def gen_data(self, refer_cols_node):
        ldata, col_idxs, left_row_idxs, weight_list_l = self.lchild.gen_data(refer_cols_node)
        rdata, _, right_row_idxs, weight_list_r= self.rchild.gen_data(refer_cols_node)

        kl_weight = weight_list_l[2] if weight_list_l[2] >= weight_list_r[2] else weight_list_r[2]
        cc_weight = weight_list_l[1] if weight_list_l[1] >= weight_list_r[1] else weight_list_r[1]
        sc_weight = weight_list_l[0] if weight_list_l[0] >= weight_list_r[0] else weight_list_r[0]

        assert(len(col_idxs) == len(ldata[0]) and len(_) == len(rdata[0]))

        label = [0]*len(ldata)
        ldata.extend(rdata)

        if enable_eval:
            
            label.extend([1]*len(rdata)) 
        
            val_col_cur_idx = get_val_col(col_idxs, idx_dict)
            
            # data_array = [x.copy() for x in ldata]
            # data_array = transpose(data_array)
            # for i in reversed(rm_col):
            #     data_array.pop(i)
            # data_array = transpose(data_array)

            data_array = np.array(ldata)
            data_array = data_array[:, val_col_cur_idx]
            data_array = np.where(data_array == '', 0, data_array).astype(float)
            
            data_array = MinMaxScaler().fit_transform(data_array)

            # silh_diff = silhouette_score(data_array, label) if data_array.shape[0] >= 2 else 1      
            # silh_diff = np.abs(silh_diff - self.silhou_coeffi)
            # sc_diff_list.append(silh_diff)
            
            # sc_weight += 2
            # sc_weight_list.append(sc_weight)

            if data_array.shape[0] > 10 and self.dataset.shape[0] > 10:
                KL_div = scipy_estimator(data_array, self.dataset, 1)
                if not np.isnan(KL_div) and not KL_div == float('inf'):
                    KL_div_list.append(np.abs(KL_div))
                    kl_weight += 2
                    kl_weight_list.append(kl_weight)

        left_row_idxs.extend(right_row_idxs)
        return ldata, col_idxs, left_row_idxs, [sc_weight, cc_weight, kl_weight]
        

class ProductNode:
    def __init__(self, scope, lchild, rchild, is_both_val, dataset):
        self.id = None
        self.scope = scope
        self.lchild = lchild
        self.rchild = rchild
        self.is_both_val = is_both_val
        self.dataset = dataset if enable_eval else None
        if verbose:
            print("constructing PROD_NODE completed...")
    
    def assign_id(self, id, G):
        self.id = id
        G.add_node(id)
        id = self.lchild.assign_id(id + 1, G)
        G.add_edge(self.id, self.id + 1)
        id = self.rchild.assign_id(id + 1, G)
        G.add_edge(self.id, self.rchild.id)
        return id

    def assign_id_postorder(self, id, G, label_dict):
        id = self.lchild.assign_id_postorder(id, G, label_dict)
        id = self.rchild.assign_id_postorder(id + 1, G, label_dict)
        self.id = id + 1
        label_dict[self.id] = '×'
        G.add_node(self.id)
        G.add_edge(self.id, self.lchild.id)
        G.add_edge(self.id, self.rchild.id)
        return id + 1

    def debug_print(self, prefix, indent):
        print('%sProductNode: %s' % (prefix, self.scope))
        self.lchild.debug_print(prefix+indent, indent)
        self.rchild.debug_print(prefix+indent, indent)

    def estimate(self, range_query, sel_list):
        l_sel, sel_list = self.lchild.estimate(range_query, sel_list)
        r_sel, sel_list = self.rchild.estimate(range_query, sel_list)
        res = l_sel * r_sel
        sel_list.append(res)
        return res, sel_list

    def gen_data(self, refer_cols_node):
        if self.scope.n_rows() == 1 and self.scope.row_idxs[0] == 26348:
            a = 1
        ldata, left_col_idxs, row_idxs, weight_list_l = self.lchild.gen_data(refer_cols_node)
        rdata, right_col_idxs, _, weight_list_r = self.rchild.gen_data(refer_cols_node)

        assert(len(left_col_idxs) == len(ldata[0]) and len(right_col_idxs) == len(rdata[0]))

        for i in range(len(ldata)):
            ldata[i].extend(rdata[i])

        left_col_idxs.extend(right_col_idxs)
        ldata, col_idxs = calibrate_idxs(ldata, left_col_idxs, True)

        
        kl_weight = weight_list_l[2] if weight_list_l[2] >= weight_list_r[2] else weight_list_r[2]
        cc_weight = weight_list_l[1] if weight_list_l[1] >= weight_list_r[1] else weight_list_r[1]
        sc_weight = weight_list_l[0] if weight_list_l[0] >= weight_list_r[0] else weight_list_r[0]

        if enable_eval:
            if self.is_both_val is not None:
                val_col_cur_idx = get_val_col(col_idxs, idx_dict)
                
                # data_array = [x.copy() for x in ldata]
                # data_array = transpose(data_array)
                # for i in reversed(rm_col):
                #     data_array.pop(i)

                data_array = np.array(ldata)               
                data_array = data_array[:, val_col_cur_idx].T
                data_array = np.where(data_array == '', 0, data_array).astype(float)
                               
                # coeffi_matrix = np.corrcoef(data_array)
                # coeffi_matrix = np.nan_to_num(coeffi_matrix)
                # coeffi_diff = np.mean(np.abs(coeffi_matrix - self.pearson_coeffi))
                # cc_diff_list.append(coeffi_diff)
                # cc_weight += 2
                # cc_weight_list.append(cc_weight)

                data_array = data_array.T
                data_array = MinMaxScaler().fit_transform(data_array)
                if data_array.shape[0] > 10 and self.dataset.shape[0] > 10:
                    KL_div = scipy_estimator(data_array, self.dataset, 1)
                    if not np.isnan(KL_div) and not KL_div == float('inf'):
                        KL_div_list.append(np.abs(KL_div))
                        kl_weight += 2
                        kl_weight_list.append(kl_weight) 
        return ldata, col_idxs, row_idxs, [sc_weight, cc_weight, kl_weight]
    
class SPN:
    col_effi_thres = None

    def __init__(self, root):
        self.root = root

    def debug_print(self, prefix, indent):
        self.root.debug_print(prefix, indent)
        pass    

    # >>> a = [1, 2, 3, 4, 5, 6, 7]
    # >>> for i in a:
    # ...     if i == 3 or i ==5 or i ==6:
    # ...             a.remove(i)
    # ... 
    # >>> a
    # [1, 2, 4, 6, 7]
    # 不能这样写，for里面直接remove当前指针，会导致接下来的元素指针-1

    @staticmethod
    def seperate_cols(scope, all_keys):
        rm_col = []
        col_idxs = scope.col_idxs.copy()            
        for col in col_idxs:                           
            if (col in all_keys):
                rm_col.append(col)
        for col in rm_col:
            col_idxs.remove(col) 

        return col_idxs, rm_col

    @staticmethod
    def construct_top_down(scope, data_array):

        split_col_failed = False
        split_col_force = False
        SPN.col_effi_thres = col_effi
        while True:
            NextOP, split_col_force = SPN.get_next_op(scope, split_col_failed)
            if NextOP == NextOP.SPLIT_ROWS:
                left_scope, right_scope, silh_coeffi, dataset_list = SPN.split_rows(scope, data_array)
                SumNode.depth += 1
                lchild = SPN.construct_top_down(left_scope, dataset_list[0])
                rchild = SPN.construct_top_down(right_scope, dataset_list[1])
                SumNode.depth -= 1
                return SumNode(scope, lchild, rchild, silh_coeffi, dataset_list[2])
            if NextOP == NextOP.SPLIT_COLS:
                left_scope, right_scope, coeffient_coeffi, dataset_list = SPN.split_cols(scope, data_array, split_col_force)
                if left_scope.n_cols() == 0 or right_scope.n_cols == 0:
                    split_col_failed = True
                    continue
                lchild = SPN.construct_top_down(left_scope, dataset_list[0])
                rchild = SPN.construct_top_down(right_scope, dataset_list[1])
                return ProductNode(scope, lchild, rchild, coeffient_coeffi, dataset_list[2])
            if NextOP == NextOP.CREATE_LEAF:
                if scope.n_cols() > 1:
                    return LeafNode.construct_leafnode_multicol(scope)
                else:
                    return LeafNode.construct_leafnode(scope)

    @staticmethod
    def split_rows(scope, data_array):
        # data_array, _, _ = SPN.construct_array_from_scope(dataset, scope, idx_dict['all_keys'])

        if data_array.shape[1] == 0:
            half_n_rows = scope.n_rows() // 2
            return NodeScope(scope.row_idxs[:half_n_rows], scope.col_idxs), \
                   NodeScope(scope.row_idxs[half_n_rows:], scope.col_idxs), \
                   1.0, [data_array[:half_n_rows], data_array[half_n_rows:], \
                         data_array if enable_eval else None]


        # data_array = MinMaxScaler().fit_transform(data_array)

        if scope.n_rows() <= 100:
            isSame = True
            for arr in data_array:
                if not np.array_equal(arr, data_array[0]):
                    isSame = False
                    break
            if isSame:
                half_n_rows = scope.n_rows() // 2
                return NodeScope(scope.row_idxs[:half_n_rows], scope.col_idxs), \
                       NodeScope(scope.row_idxs[half_n_rows:], scope.col_idxs), \
                       1.0, [data_array[:half_n_rows], data_array[half_n_rows:], \
                             data_array if enable_eval else None]
        
        
        kmeans = MiniBatchKMeans(n_clusters = 2,
                                 max_iter = 30, 
                                 max_no_improvement = 3,
                                 reassignment_ratio = 0.0001,
                                 batch_size = 50,
                                 n_init = 1,
                                 random_state=0).partial_fit(data_array)
        
        noise = noise_gen(noise_keys_clus, noise_dict_clus)
        while np.abs(noise) > scope.n_rows():
            noise = noise_gen(noise_keys_clus, noise_dict_clus)
        if noise < 0:
            noise = -noise

        l_rows, l_idxs = [], []
        r_rows, r_idxs = [], []

        for i, x in enumerate(kmeans.labels_):
            if x == 0:   
                
                l_idxs.append(i)
            else:
                
                r_idxs.append(i)
        
        if random.random() > 0.5:
            for _ in range(noise):
                if len(l_idxs) != 0:
                    tmp = random.choice(l_idxs)
                    l_idxs.remove(tmp)
                    r_idxs.append(tmp)
        else:
            for _ in range(noise):
                if len(r_idxs) != 0:
                    tmp = random.choice(r_idxs)
                    r_idxs.remove(tmp)
                    l_idxs.append(tmp)
        
        assert len(r_idxs) + len(l_idxs) == scope.n_rows()
        for i in l_idxs:
            l_rows.append(scope.row_idxs[i])
        for i in r_idxs:
            r_rows.append(scope.row_idxs[i])

        if len(r_rows) == 0 or len(l_rows) == 0:
            half_n_rows = int(scope.n_rows() / 2)
            return NodeScope(scope.row_idxs[:half_n_rows], scope.col_idxs), \
                   NodeScope(scope.row_idxs[half_n_rows:], scope.col_idxs), \
                   1.0, [data_array[:half_n_rows], data_array[half_n_rows:], \
                         data_array if enable_eval else None]        

        return NodeScope(l_rows, scope.col_idxs), \
               NodeScope(r_rows, scope.col_idxs), \
               None, [data_array[l_idxs], data_array[r_idxs], data_array if enable_eval else None]

    @staticmethod
    def split_cols(scope, data_array, split_col_force):
        assert (scope.n_cols() > 1)
        col_idxs = scope.col_idxs.copy()

        # string类型视为条件独立，
        for col in col_idxs:
            if col in idx_dict['str_col_idx']:
                col_idxs.remove(col)
                return NodeScope(scope.row_idxs, [col]), NodeScope(scope.row_idxs, col_idxs), \
                       None, [data_array, data_array, None]

            if col in idx_dict['jk_all_idx']:
                if col in idx_dict['pk_idx'] and len(idx_dict['pk_idx']) > 1:
                    splitcol_by_rmcol(col_idxs, idx_dict['pk_idx'])
                    return NodeScope(scope.row_idxs, idx_dict['pk_idx'].copy()), \
                           NodeScope(scope.row_idxs, col_idxs), None, \
                           [data_array, data_array, None]
                if col in idx_dict['join_fk']:
                    splitcol_by_rmcol(col_idxs, idx_dict['join_fk'])
                    return NodeScope(scope.row_idxs, idx_dict['join_fk'].copy()), \
                           NodeScope(scope.row_idxs, col_idxs), None, \
                           [data_array, data_array, None]
                if col in idx_dict['join_refered_idx']:
                    splitcol_by_rmcol(col_idxs, idx_dict['join_refered_idx'])
                    return NodeScope(scope.row_idxs, idx_dict['join_refered_idx'].copy()), \
                           NodeScope(scope.row_idxs, col_idxs), None, \
                           [data_array, data_array, None]

        # date/category类型，以及单列主键和外键，切分到最后再一列一列切分
        # np_array, col_idxs, rm_col = SPN.construct_array_from_scope(dataset, scope, idx_dict['all_keys'])
        col_idxs, rm_col = SPN.seperate_cols(scope, idx_dict['all_keys'])


        if len(col_idxs) == 1:
            if split_col_force == False:
                return NodeScope([], []), NodeScope([], []), None, [None, None, None]
            else:
                return NodeScope(scope.row_idxs, col_idxs), NodeScope(scope.row_idxs, rm_col), \
                       None, [data_array, None, None]
        elif len(col_idxs) == 0:
            if split_col_force == False:
                return NodeScope([], []), NodeScope([], []), None, [None, None, None]
            else:                
                return NodeScope(scope.row_idxs, rm_col[:-1]), NodeScope(scope.row_idxs, [rm_col[-1]]), \
                       None, [None, None, None]

        
        corr_matrix = None
        rdc_list = None

        if coeffi_type == 'PCC':
            
            corr_matrix = np.corrcoef(data_array.T)
            corr_matrix = np.nan_to_num(corr_matrix)
            corr_matrix = np.abs(corr_matrix)

        elif coeffi_type == 'RDC':
            if scope.n_rows() == 1:
                col_idxs.extend(rm_col)
                col_idxs.sort()
                return NodeScope(scope.row_idxs, col_idxs[:-1]), NodeScope(scope.row_idxs, [col_idxs[-1]]), \
                    None, [None, None, None]    
                                                       
            rdc_list = []
            cols = data_array.shape[1]
            for l in range(1, cols // 2 + 1):
                for combi in itertools.combinations([i for i in range(cols)], l):
                    arr_right = np.ones(cols, dtype=bool)
                    arr_right[list(combi)] = False
                    arr_right = data_array[:, arr_right]
                    arr_left = data_array[:, combi]
                    rdc_list.append((combi, rdc(arr_left, arr_right)))
            rdc_list = sorted(rdc_list, key = lambda x : x[1])

        

        while True:
            if coeffi_type == 'PCC':
                edge = corr_matrix.copy()
                edge[edge >= SPN.col_effi_thres] = True
                edge[edge < SPN.col_effi_thres] = False
                graph = from_numpy_matrix(edge)
                groups = sorted(connected_components(graph), key=len, reverse=True)
                if len(groups) == 1 and len(groups[0]) == len(edge[0]): 
                    # all nodes are connected so we cannot split a group of cols in this case
                    if split_col_force is True:
                        SPN.col_effi_thres *= 1.5
                        continue
                    else:
                        return NodeScope([], []), NodeScope([], []), None, [None, None, None]
                max_group = groups[0]

            elif coeffi_type == 'RDC':
                if rdc_list[0][1] > SPN.col_effi_thres:
                    if split_col_force is True:
                        SPN.col_effi_thres *= 1.5
                        continue
                    else:                    
                        return NodeScope([], []), NodeScope([], []), None, [None, None, None]
                else:
                    target_rdc = exponential_mechanism([-a[1] for a in rdc_list], 1, epsilon=col_epsilon)
                    for item in rdc_list:
                        if item[1] == -target_rdc:
                            combi = item[0]
                            break
                    if len(combi) >= data_array.shape[1] // 2 + 1:
                        max_group = combi
                    else:
                        max_group = []
                        for i in range(len(col_idxs)):
                            if i not in combi:
                                max_group.append(i)
            
            l_cols, l_idxs = [], []
            r_cols, r_idxs = [], []
            for i in range(len(col_idxs)):
                col = col_idxs[i]
                if i in max_group:
                    l_cols.append(col)
                    l_idxs.append(i)
                else:
                    r_cols.append(col)
                    r_idxs.append(i)

            l_cols.extend(rm_col)
            l_cols.sort()

            return NodeScope(scope.row_idxs, l_cols), NodeScope(scope.row_idxs, r_cols), \
                   True if enable_eval else None, [data_array[:, l_idxs], \
                                                          data_array[:, r_idxs], data_array \
                                                          if enable_eval else None]

    @staticmethod
    def get_next_op(scope, split_col_failed):

        if 1 < scope.n_cols() <= jk_max_len:
            for idx_list in idx_dict:
                if (len(idx_dict[idx_list]) == scope.n_cols()):
                    if (scope.col_idxs == idx_dict[idx_list]):
                        return NextOP.CREATE_LEAF, False
        if scope.n_cols() == 1:
            return NextOP.CREATE_LEAF, False
        
        if scope.n_cols() == 1:
            if (SumNode.depth > sum_node_max_depth or \
                scope.n_rows() <= row_split_threshold or \
                scope.col_idxs[0] in idx_dict['str_col_idx'] or \
                scope.col_idxs[0] in idx_dict['all_keys']):
                return NextOP.CREATE_LEAF, False
            else:
                return NextOP.SPLIT_ROWS, False
        if split_col_failed:
            if SumNode.depth <= sum_node_max_depth and scope.n_rows() > row_split_threshold:
                return NextOP.SPLIT_ROWS, False
            else:
                return NextOP.SPLIT_COLS, True
        return NextOP.SPLIT_COLS, False

        # if scope.n_cols() == 1:
        #     if (SumNode.depth > sum_node_max_depth or \
        #         scope.col_idxs[0] in idx_dict['str_col_idx'] or \
        #         scope.col_idxs[0] in idx_dict['all_keys']) and scope.n_rows() <= row_split_threshold:
        #         return NextOP.CREATE_LEAF, False
        #     else:
        #         return NextOP.SPLIT_ROWS, False
        
        # if SumNode.depth <= sum_node_max_depth and scope.n_rows() > row_split_threshold:
        #     return NextOP.SPLIT_ROWS, False
        # else:
        #     return NextOP.SPLIT_COLS, True



def noise_gen(noise_keys, noise_dict):
    rand = 0
    while rand < noise_keys[0]:
        rand = random.random()

    for i in range(1, len(noise_keys)):
        if rand >= noise_keys[i - 1] and rand < noise_keys[i]:
            noise = noise_dict[noise_keys[i]]

    return noise

def perturb_dict(d : dict, noise_keys, noise_dict):

    freq_keys = list(d.keys())
    freq_total = 0
    for v in d.values():
        freq_total += v

    for k in freq_keys:
        while True:
            noise = noise_gen(noise_keys, noise_dict)
            if (d[k] + noise) < 0:
                continue
            else:
                d[k] += noise
                break

    new_repeat_total = sum(list(d.values()))
    if new_repeat_total != freq_total:
        diff = new_repeat_total - freq_total
        if diff > 0:
            for _ in range(diff):
                while True:
                    k = random.choice(freq_keys)
                    if d[k] == 0:
                        continue
                    else:
                        d[k] -= 1
                        break
        else:
            for _ in range(-diff):
                k = random.choice(freq_keys)
                d[k] += 1
    
    assert sum(list(d.values())) == freq_total

class Histogram:
    def __init__(self, vals, n_buckets = 10, null_tag = None, digits = None):
        self.repeat_dict = {}       
        self.null_count = 0 if null_tag or null_tag == 0 else None
        

        if vals[0] == null_tag or vals[-1] == null_tag:
            for i in reversed(range(len(vals))):
                if vals[i] == null_tag or type(vals[i]) == pd._libs.tslibs.nattype.NaTType:
                    del vals[i]
                    self.null_count += 1

        length = len(vals)
        if length <= n_buckets:
            n_buckets = 1

        if length == 0:
            buckets = []
        else:
            mi = vals[0]
            ma = vals[-1]

            if mi == ma:
                buckets = [Bucket(len(vals), mi, ma)]
            else:
                if digits != None:
                    interval = round(round((ma - mi), digits) / n_buckets, digits)
                elif type(vals[0]) == int:
                    interval = (ma - mi) / n_buckets
                    interval = math.ceil(interval)
                elif type(vals[0] == pd.Timestamp):
                    interval = (ma - mi) / n_buckets
                else:
                    raise Exception('Unrecognized')
                        
                buckets = []
                lower_bound = mi

                bucket = Bucket(0, lower_bound, lower_bound + interval)
                repeat = 0
                last_val = vals[0]

                for val in vals:
            
                    if val == last_val:
                        repeat += 1
                        continue
                    elif val > bucket.upper_bound:
                        if repeat > 0:
                            if repeat < repeat_threshold:
                                bucket.row_count += repeat
                            else:
                                self.repeat_dict[last_val] = repeat
                        buckets.append(bucket)
                        lower_bound = bucket.upper_bound
                        bucket = Bucket(0, lower_bound, lower_bound + interval)

                    elif repeat >= repeat_threshold:
                        self.repeat_dict[last_val] = repeat   
                    else:
                        bucket.row_count += repeat
                    repeat = 1 
                    last_val = val
                
                if repeat > 0:
                    if repeat < repeat_threshold:
                        bucket.row_count += repeat
                        bucket.upper_bound = last_val
                        buckets.append(bucket)
                    elif bucket.row_count > 0:
                        buckets.append(bucket)
                        self.repeat_dict[last_val] = repeat
                    else:
                        self.repeat_dict[last_val] = repeat

            # keys = list(noise_dict.keys())
            for b in buckets:

                while True:
                    noise = noise_gen(noise_keys_hist, noise_dict_hist)
                    if (b.row_count + noise) < 0:
                        continue
                    else:
                        b.row_count = b.row_count + noise
                        break
            
            for v in self.repeat_dict.values():
                length -= v

            perturb_dict(self.repeat_dict, noise_keys=noise_keys_hist, noise_dict=noise_dict_hist)                
        
        new_total = sum(b.row_count for b in buckets)
        
        if new_total != length:
            diff = new_total - length
            if diff > 0:
                for _ in range(diff):
                    while True:
                        b = random.choice(buckets)
                        if b.row_count == 0:
                            continue
                        else:
                            b.row_count -= 1
                            break 
       
            elif diff < 0:
                for _ in range(-diff):
                    random.choice(buckets).row_count += 1
                  

        self.buckets = buckets
        test_count = 0
        for b in buckets:
            test_count += b.row_count

        assert test_count == length

    def __repr__(self):
        return f'Histogram{{{self.buckets}}}'
            
class Bucket:
    def __init__(self, row_count, lower_bound, upper_bound):
        self.row_count = row_count
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        
        
    def __repr__(self):
        return f'Bucket{{row_count:{self.row_count}, lower:{self.lower_bound}, upper:{self.upper_bound}, ' \
               



    
