# 命令笔记
~~~
su      切换用户
mkdir   创建文件夹
cd      切换目录
touch   创建普通文件
cat     查看文本内容
vim     文本编辑器
ls      查看文件夹内容
ll      等于 ls   -l 
ps -ef   查看linux的进程
top     linux的任务管理器
find    查找linux文件的
grep    过滤字符串信息的
pwd     打印当前工作目录的绝对路径
mv      移动文件 ，重命名
rm      删除文件  rm -rf    -r  递归删除文件夹  -f  强制不提醒就删除
yum     linux安装软件的命令，如同pip
head    从文本前*行开始看，默认前10行
tail    从文本后面10行看      tail  -f  filename   实时监控文件内容
more    翻页显示文件内容
less    翻页显示文件内容
echo    相当于print打印
kill 进程id   杀死进程的命令
df -h      显示磁盘空间

/       在路径的最前面是根目录，在路径中间是，路径分隔符
-  		上一次的工作目录
~	    当前登录用户的家目录
.		当前目录 
..		上一级工作目录  
./		当前目录 
>       重定向输出符，覆盖写入。。。
>>		重定向输出符，追加写入 
<		重定向输入符，覆盖写入
<<  	重定向输入符，追加写入

linux的变量赋值不得有空格，有空格就识别为参数了
wget    在线下载url资源
alias   linux的别名命令    
		alias  rm="echo 你别使用rm了，你这个笨蛋"
scp     linux之间网络传输文件的
chattr +a filename      加锁，让文件不得删除
chattr -a filename      减锁
lsattr filname        显示文件是否有锁
~~~

# 相关常识
~~~
1、
[root@localhost home]# id kun
uid=1002(kun) gid=1002(kun) groups=1002(kun)
uid     用户id号码
gid     group id  用户组 id
groups  组id号码

系统超级用户：uid  默认是 0
系统常用服务的用户：系统默认会创建mysql用户，去执行mysql这个软件，他的id是从1-999之间
root创建的普通用户，默认id是从1000开始的

用户组，一组同样身份信息的用户
用户，普通用户

root可以随意更改别人的密码，普通用户不行
root可以随意切换普通用户
普通用户切换，必须想要登录用户的输入密码


2、
临时提权的命令sudo 
修改sudoers配置文件，把你想提权的用户写进去，编辑配置文件 
    vim  /etc/sudoers
写入如下信息，定位到那一行
	## Allow root to run any commands anywhere 
	root    ALL=(ALL)       ALL
	kun    ALL=(ALL)       ALL   #允许kun在任何地方，执行任何命令   
使用sudo命令
sudo 你想执行的命令

删除用户
userdel -r  用户名  #删除用户信息，和家目录（home）

linux的文件权限
文件拥有者分三类
	属主
	属组
	其他人
文件的读写执行，命令是？
	cat  读
	vim   echo追加写
	./文件    直接运行可执行文件 ，以绝对路径和相对路径
	sh shell脚本  #用shell解释器去读脚本

	文件夹的读写执行？
	ls  读
	touch  允许进入文件夹，写文本
	cd   允许进入文件夹，可执行

	linux文件的分类
	-  普通文本
	d  文件夹 
	l  软连接

	文件/文件夹权限
	r    read可读，可以用cat等命令查看
	w    write写入，可以编辑或者删除这个文件
	x    executable    可以执行

更改文件权限
chmod  权限   文件/文件夹权限 
-rw-r--rw-. 1 root root 79 May  5 09:58 你好.txt
-rw-r--rw-  
- 普通文本 
rw-     指的是root用户 可读可写不可执行     users     u  
r--     指的是root组里的成员，只读          group     g
rw-     指的是其他人  可读可写，不可执行     others    o  

#让你好.txt没有任何的权限
chmod u-r,u-w,u-x  你好.txt 
chmod g-r,g-w,g-x  你好.txt 
chmod o-r,o-w,o-x  你好.txt 

#让你好.txt 所有角色都有所有的权限
-rwxrwxrwx. 1 root root 79 May  5 09:58 你好.txt
chmod 777  你好.txt  #赋予文本最高的权限
权限分为
r 4 
w 2 
x 1  
权限计算最高是 4+2+1 =7  最低是 0


3、
更改文件的属主，属组
chown  用户名  要操作的文件 #更改文件属主
chgrp  组名   要操作的文件 #更改文件属组

软连接语法
ln   -s   目标文件  快捷方式绝对路径

linux的命令提示符
PS1变量
echo $PS1  #显示命令提示符
修改命令提示符
PS1="[\u@\h \w \t]\$"


4、
linux的打包，解压缩的命令
	tar命令

	-c  打包
	-x  解包
	-z  调用gzip命令去压缩文件，节省磁盘空间
	-v  显示打包过程

	语法：
	tar  -cvf  打包文件的名字   你要打包的内容

	#实例：
	#压缩当前的所有内容到alltmp.tar这个文件中，这里不节省磁盘 
	tar  -cvf  压缩文件的名字.tar   ./*
	#解压的方式
	tar  -xvf  压缩文件的名字.tar

	#打包文件，并且压缩文件大小的用法，节省磁盘
	tar  -zcvf  压缩文件的名字.tar.gz  ./*  
	#解压缩
	tar -zxvf  压缩文件的名字.tar.gz
~~~

# django相关
~~~
django程序跑起来，如何检测呢？
	1.去浏览器检测是否可以访问, 192.168.16.37:8000
	2.确认django的端口是否启动
	netstat -tunlp  | grep 8000
	3.确认django的进程是否存在 
	ps -ef |grep python


什么是dns（域名解析系统）,其实就是一个超大的网络电话簿  
	dns就是域名解析到ip的一个过程，
	大型公司，用的dns服务名叫做bind软件
	提供dns服务的公司有
	119.29.29.29  腾讯的
	223.5.5.5	阿里的
	223.6.6.6   阿里的 
	8.8.8.8		谷歌的
	114.114.114.114 	114公司的

	linux的dns配置文件如下
	vim /etc/resolv.conf 
	里面定义了dns服务器地址
	linux解析dns的命令
	nslookup  域名 
	
	

dns解析流程，当你在浏览器输入一个url，有了那些解析
pythonav.cn:80/index.html
解析流程：
1.浏览器首先在本地机器，操作系统dns缓存中查找是否有域名-ip的对应记录
2.去/etc/hosts文件中寻找是否写死了域名解析记录
3.如果hosts没写，就取 /etc/resolv.conf配置文件中寻找dns服务器地址
4.如果找到了对应的解析记录，就记录到本地dns缓存中
/etc/hosts 本地强制dns的文件
~~~


# Linux系统下升级Python版本
1.解决python3安装所需的依赖关系
```sh
yum install gcc patch libffi-devel python-devel  zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel -y
```

2.下载python3的源代码
```sh
wget https://www.python.org/ftp/python/3.9.6/Python-3.9.6.tar.xz
```

3.最终搞得到一个压缩包Python-3.9.6.tar.xz
xz -d  Python-3.9.6.tar.xz
tar -xvf  Python-3.9.6.tar

4.进入python3的源码目录
cd Python-3.9.6

5.开始编译安装三部曲
~~~
1.释放makefile，编译文件，并且指定安装路径
./configure --prefix=/opt/python36/

2.开始编译，调用gcc编译器
make 

3.开始安装，到/opt/python36目录下
make install  

4.安装完毕之后，python3的解释器就出现在了/opt/python36/bin目录下

5.配置PATH环境变量，写入如下变量到/etc/profile
PATH="/opt/python36/bin/:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/root/bin"

6.还得读取/etc/profile
source /etc/profile  #读取配置文件，让PATH生效
~~~
6、至于怎么在linux下切换默认python版本
google一下就知道了。


# Linux 中创建 Python 虚拟环境
1、安装 virtualenv:
如果你的系统中还没有安装 virtualenv，可以通过pip安装它：
```sh
pip3 install virtualenv
```
2、创建虚拟环境:
在你的项目文件夹中创建一个新的虚拟环境。替换 myenv 为你想要的虚拟环境名称：
```sh
virtualenv myenv
```
如果你的系统中有多个Python版本，你可以指定 virtualenv 使用特定的Python版本，通过-p选项。例如，使用Python 3.9：
```sh
virtualenv -p python3.9 myenv
```
3、激活虚拟环境:
创建好虚拟环境后，你需要激活它。在虚拟环境文件夹所在的目录中，运行以下命令：
```sh
source myenv/bin/activate
```
激活虚拟环境后，你的命令提示符应该会显示虚拟环境的名称，表明你现在在虚拟环境中工作。<br>

4、使用虚拟环境:
现在你可以在虚拟环境中安装包了，而不用担心影响到系统其他部分或其他项目。例如：
```sh
pip install django
```

5、退出虚拟环境:
当你完成工作，想要退出虚拟环境时，可以简单地输入
```sh
deactivate
```



