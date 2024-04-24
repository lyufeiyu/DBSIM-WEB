# 一、Oracle

## 1、添加用户和用户组
添加oracle用户，后续安装过程中需要使用oracle用户权限，来创建文件等操作，将其归为oinstall用户组，附加用户组为dba。
```sh
[lfy@handsome ~]# groupadd oinstall
[lfy@handsome ~]# groupadd dba
[lfy@handsome ~]# useradd -g oinstall -G dba oracle
```
后面使用`id oracle`查看创建的oracle用户信息。

注意：这些命令只是在系统中创建用户和用户组，不依赖于是否已经安装了Oracle数据库。这些命令会创建一个名为oracle的用户，将其添加到oinstall用户组，并将其附加到dba用户组中。这样，在安装Oracle数据库后，你可以使用这个oracle用户来执行数据库相关的操作。

## 2、下载oracle的安装包


## 3、相关命令
su
cd /oracle/
vim sh_python_property_oracle.py
python sh_python_property_oracle.py
lsnrctl status
lsnrctl start
find ./ listener
sqlplus / as sysdba
sqlplus sys/2002@172.31.178.221:1521/ORCLCDB as sysdba

ps -ef | grep ora_
echo $ORACLE_SID
echo $ORACLE_HOME
echo $ORACLE_BASE
tail -n 100  ORCLCDB_vktm_6588.trc

下载oracle预安装包
wget http://yum.oracle.com/repo/OracleLinux/OL7/latest/x86_64/getPackage/oracle-database-preinstall-19c-1.0-1.el7.x86_64.rpm

下载19c安装包
https://www.oracle.com/cn/database/technologies/oracle-database-software-downloads.html#19c

选择Linux rpm安装包

执行预安装
yum install -y oracle-database-preinstall-19c-1.0-1.el7.x86_64.rpm

安装oracle数据库
yum install oracle-database-ee-19c-1.0-1.x86_64.rpm

这一步需要一些时间，但是不需要手工干预，会自动安装完成。

数据库初始化
/etc/init.d/oracledb_ORCLCDB-19c configure

这个数据库初始化过程花的时间也会比较长，耐心等待。

修改oracle用户密码
在上面的过程中，oracle用户会被自动创建

passwd oracle

以上步骤都是在root账户下进行的，后续的步骤在oracle账户下进行

设置环境变量
su - oracle

## 4、在文件后面添加环境变量
vi .bash_profile
export  ORACLE_BASE=/opt/oracle
export  ORACLE_HOME=/opt/oracle/product/19c/dbhome_1
export  ORACLE_SID=ORCLCDB
export  ORACLE_PDB_SID=ORCLPDB1
export  PATH=$ORACLE_HOME/bin:$PATH:$HOME/.local/bin:$HOME/bin
export LD_LIBRARY_PATH=$ORACLE_HOME/lib:/usr/lib
export NLS_LANG=american_america.ZHS16GBK

保存退出

source .bash_profile

修改system密码
sqlplus / as sysdba




# 二、Yashan

## 1、关闭防火墙
~~~
systemctl stop firewalld
systemctl disable firewalld
~~~

## 2、关闭交换分区
~~~
# 最大限度使用物理内存
echo " vm.swappiness = 0" >> /etc/sysctl.conf  
~~~

## 3、调整自动分配本地端口范围
~~~
echo "net.ipv4.ip_local_port_range = 32768 60999" >> /etc/sysctl.conf
~~~

## 4、调整进程的VMA上限
~~~
#该参数作用是限制一个进程可以拥有的VMA（虚拟内存区域）的数量，调整是为了让数据库进程充分使用主机资源
echo "vm.max_map_count=2000000" >> /etc/sysctl.conf
~~~

## 5、使调整生效
~~~
sysctl -p
~~~

## 6、调整资源限制
~~~
# vi /etc/security/limits.conf

# 表示yashan用户可以打开的最大的文件描述符数量65536个
yashan soft nofile 65536
yashan hard nofile 65536
# 表示yashan用户可以打开的最大的进程数65536个
yashan soft nproc 65536 
yashan hard nproc 65536
# 表示yashan用户可以没有限制的使用常驻内存的大小
yashan soft rss unlimited 
yashan hard rss unlimited
# 表示yashan用户可以使用linux的默认栈空间大小是8192kb
yashan soft stack 8192 
yashan hard stack 8192
~~~

## 关闭透明大页
编辑/etc/default/grub，在 GRUB_CMDLINE_LINUX 中添加或修改参数 transparent_hugepage=never

# vi /etc/default/grub
GRUB_TIMEOUT=5
GRUB_DISTRIBUTOR="$(sed 's, release .*$,,g' /etc/system-release)"
GRUB_DEFAULT=saved
GRUB_DISABLE_SUBMENU=true
GRUB_TERMINAL_OUTPUT="console"
GRUB_CMDLINE_LINUX="crashkernel=auto rd.lvm.lv=rhel/root rd.lvm.lv=rhel/swap rhgb quiet transparent_hugepage=never"
GRUB_DISABLE_RECOVERY="true"

grub2-mkconfig -o /boot/grub2/grub.cfg

## 7、数据库安装
7.1 创建yashan用户
~~~
useradd -d /home/yashan -m yashan
password yashan
~~~
7.2 软件目录创建
~~~
mkdir -p /yasdb
chown -R yashan:yashan /yasdb/
chmod -R 755 /yasdb/
~~~
7.3 安装包解压
~~~
[root@alldb yasdb]# su - yashan
[yashan@alldb ~]$ cd /yasdb/
[yashan@alldb yasdb]$ mkdir ~/install
[yashan@alldb yasdb]$ cd ~/install/
[yashan@alldb install]$ tar -xf /opt/yashandb-personal-23.1.1.100-linux-x86_64.tar.gz
~~~ 
7.4 配置文件编辑
~~~
[yashan@alldb install]$ cd scripts/
[yashan@alldb scripts]$ vi install.ini 

[install]
#软件目录
YASDB_HOME=/yasdb/yasdb_home
#数据目录
YASDB_DATA=/yasdb/yasdb_data
REDO_FILE_SIZE=100M
REDO_FILE_NUM=4
INSTALL_SIMPLE_SCHEMA_SALES=N
NLS_CHARACTERSET=UTF8
[instance]
LISTEN_ADDR=0.0.0.0:1688
DB_BLOCK_SIZE=8K
DATA_BUFFER_SIZE=256M
SHARE_POOL_SIZE=256M
WORK_AREA_POOL_SIZE=32M
LARGE_POOL_SIZE=32M
REDO_BUFFER_SIZE=8M
UNDO_RETENTION=300
OPEN_CURSORS=310
MAX_SESSIONS=1024
RUN_LOG_LEVEL=INFO
NODE_ID=1-1:1
~~~
7.5 软件安装
~~~
[yashan@alldb scripts]$ ./install.sh 
~~~
7.6 数据库初始化
~~~
[yashan@alldb scripts]$ ./initDB.sh 
process started!
Database open succeed !
[yashan@alldb scripts]$ 
~~~
7.7 生效环境变量
~~~
$ source ~/.bashrc
​ 至此，数据库安装完成了，非常的简单吧。
~~~
8.崖山数据库初体验
~~~
8.1 登陆数据库
$ yasql sys/yasdb_123
8.2 查看表空间及数据文件
SQL> select name,status from v$tablespace;
8.3 查看参数
SQL> show parameter 
8.4 查看线程信息
SQL> select name,status from v$process;
8.5 关闭数据库
$ yasql sys/yasdb_123
8.6 启动数据库
[yashan@alldb scripts]$ yasdb open &
[1] 17462
[yashan@alldb scripts]$ Starting instance open
Instance started
[yashan@alldb scripts]$ 
~~~

9.数据库卸载
~~~
$ yasql sys/yasdb_123

SQL> shutdown immediate;

$ rm - rf /home/yashan/yashandb/yasdb_home
$ rm - rf /home/yashan/yashandb/yasdb_data

vi ~/.bashrc

#删除以下两行
# User specific aliases and functions
[ -f /yasdb/yasdb_home/conf/yasdb.bashrc ] && source /yasdb/yasdb_home/conf/yasdb.bashrc
~~~



# 反复遇到的一个链接库的问题
~~~
(db_web) [root@lgh3 db_django]# gparted
======================
libparted : 3.1
======================
(db_web) [root@lgh3 db_django]# 
(db_web) [root@lgh3 db_django]# 
(db_web) [root@lgh3 db_django]# 
(db_web) [root@lgh3 db_django]# locate libcurl.so.4
/usr/lib/libcurl.so.4
/usr/lib64/libcurl.so.4
/usr/lib64/libcurl.so.4.3.0
/yasdb/install/lib/libcurl.so.4
/yasdb/install/lib/libcurl.so.4.8.0
/yasdb/yasdb_home/lib/libcurl.so.4
/yasdb/yasdb_home/lib/libcurl.so.4.8.0
(db_web) [root@lgh3 db_django]#  ldd /usr/lib64/python2.7/site-packages/pycurl.so 
	    linux-vdso.so.1 =>  (0x00007ffd487c1000)
        libcurl.so.4 => /usr/local/lib/libcurl.so.4 (0x00007f89c19e1000)(此处的问题)
        libpython2.7.so.1.0 => /lib64/libpython2.7.so.1.0 (0x00007f89c1615000)
        libpthread.so.0 => /lib64/libpthread.so.0 (0x00007f89c13f9000)
        libc.so.6 => /lib64/libc.so.6 (0x00007f89c102c000)
        libz.so.1 => /lib64/libz.so.1 (0x00007f89c0e16000)
        libdl.so.2 => /lib64/libdl.so.2 (0x00007f89c0c12000)
        libutil.so.1 => /lib64/libutil.so.1 (0x00007f89c0a0f000)
        libm.so.6 => /lib64/libm.so.6 (0x00007f89c070d000)
        /lib64/ld-linux-x86-64.so.2 (0x00007f89c1e44000)
(db_web) [root@lgh3 db_django]# 
(db_web) [root@lgh3 db_django]# 



libcurl.so.4 在哪里：
locate libcurl.so.4
ldd /usr/lib64/python2.7/site-packages/pycurl.so

# 删掉有问题的lib库
rm /usr/local/lib/libcurl.so.4

# 重新link
ln -s /usr/lib64/libcurl.so.4.3.0 /usr/lib/libcurl.so.4