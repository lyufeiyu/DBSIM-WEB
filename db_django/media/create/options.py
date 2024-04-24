import argparse
from enum import Enum

class CoeffiType(Enum):
    RDC = 0
    PCC = 1

class Dataset(Enum):
    IMDB = 0
    TPCH = 1
    CENSUS = 2
    DMV = 3


parser = argparse.ArgumentParser()

parser.add_argument('--coeffi', type=float, default=0.05, help='threshold of correlation coefficient for columns splitting')   #列分割的相关系数阈值
parser.add_argument('--cluster_per_col', type=int, default=9, help='the number of cluster per column')   #每列的簇数 簇是指具有相似特征或行为的数据点的集合
parser.add_argument('--n_buckets', type=int, default=20, help='number of buckets for a histogram')    #直方图的桶数
parser.add_argument('--muta_dist', type=int, default=200, help='distance for query generation')    #查询生成的距离
# parser.add_argument('--eval', action='store_true', help='perform evaluation or not')
parser.add_argument('--eval', type=bool, default=False, help='perform evaluation or not')  #是否执行评估
parser.add_argument('--scale_factor', type=int, default=1, help='factor for scaling up')  #扩大规模的因素
# parser.add_argument('--type_coeffi', choices=[x.name.upper() for x in CoeffiType], default='RDC', help='choose a coefficient between random dependency coefficient and pearson correlation coefficient')
parser.add_argument('--type_coeffi', choices=[x.name.upper() for x in CoeffiType], default='PCC', help='choose a coefficient between random dependency coefficient and pearson correlation coefficient')
                                                                                    #选择一个在随机依赖系数和Pearson相关系数之间的系数。
parser.add_argument('--dataset', default='CENSUS', help='choose a dataset')  #选择一个数据集 TODO
# parser.add_argument('--verbose', action='store_true', help='increase output verbosity')


parser.add_argument('--verbose', type=bool, default=False, help='increase output verbosity')  #增加输出详细程度
parser.add_argument('--gen_dir', type=str, default='../output',help='the name of the directory in which data generated will be stored') #数据生成后存储的目录名称 TODO

# parser.add_argument('--in_dir', type=str, default='../../samples/', help='the directory of input dataset')
parser.add_argument('--in_dir', type=str, default='./dataset', help='the directory of input dataset') #输入数据集的目录。 TODO

# parser.add_argument('--sche_file', type=str, default='./schema_census.txt', help='the schema file')
parser.add_argument('--sche_file', type=str, default='./dataset', help='the schema file') #模式文件  TODO


# 下面没加入网页参数
# parser.add_argument('--query_file', type=str, default='../../queries/mscn_400.csv', help='csv file of queries')
parser.add_argument('--query_file', type=str, default='./dataset/', help='csv file of queries') #查询的 CSV 文件 TODO
parser.add_argument('--repeat_join_threshold', type=int, default=0, help='frequency threshold to record the exact join key') #记录确切连接键的频率阈值
parser.add_argument('--repeat_threshold', type=int, default=3, help='frequency threshold to record the exact value') #记录确切值的频率阈值。
parser.add_argument('--privacy_budget', type=float, default=10, help='privacy budget for adding noise') #添加噪音的隐私预算。


opt = parser.parse_args()

# print("coeffi:", opt.coeffi)
# print("cluster_per_col:", opt.cluster_per_col)
# print("type_coeffi:", opt.type_coeffi)
# print("dataset:", opt.dataset)
# print("verbose:", opt.verbose)
# print("gen_dir:", opt.gen_dir)