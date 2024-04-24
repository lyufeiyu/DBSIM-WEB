import matplotlib.pyplot as plt
from matplotlib import rcParams

# 设置中文字体
rcParams['font.family'] = 'SimHei'  # 设置字体为黑体
rcParams['axes.unicode_minus'] = False  # 正确显示负号

# Data from the user's table
percentiles = ["50%", "75%", "90%", "95%", "99%", "Max"]
MySQL = [0.670527458, 0.679473877, 0.691999435, 0.702765226, 0.747113943,0.94086051]
PostgreSQL = [0.104152203, 0.107404947, 0.110346079, 0.113426208, 0.119466066, 0.124714851]
Oracle = [0.496387482, 0.855882645, 0.868923187, 0.864046097, 0.89657196, 0.911599731]
Yashan = [0.400792238, 0.804966132, 0.850654642, 0.852628832, 0.853394547,0.855648985]
#IMDB
# MySQL = [2.042259455, 2.970974445, 3.861322403, 4.302089453, 4.963717937, 6.718556881]
# PostgreSQL = [0.065427303, 0.17878437, 0.339290619, 0.433474779, 0.593530655, 0.633081913]
# Oracle = [0.30652732, 1.50784437, 2.50329061, 3.00434777, 3.50553065, 4.50808191]
# Yashan = [0.301487465, 1.501321849, 2.501238998, 2.909846228, 3.482974984, 4.482664896]

# Create the plot
plt.figure(figsize=(10,6))

plt.plot(percentiles, MySQL, marker='o', label='MySQL', linestyle='--', markersize=10)
plt.plot(percentiles, PostgreSQL, marker='s', label='PostgreSQL', linestyle='--', markersize=10)
plt.plot(percentiles, Oracle, marker='^', label='Oracle', linestyle='--', markersize=10)
plt.plot(percentiles, Yashan, marker='D', label='Yashan', linestyle='--', markersize=10)

plt.xlabel('前百分比')
plt.ylabel('响应时间')
plt.title('数据库性能比较')
plt.legend()
plt.grid(True)

# Save the figure
# plt.savefig('/mnt/data/database_performance_comparison_large_markers_v2.png')

plt.show()