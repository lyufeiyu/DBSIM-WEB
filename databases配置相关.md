# 安装 PostgreSQL 数据库

## 在 Linux（CentOS） 上安装 PostgreSQL (django只支持版本12及以上)
```sh
sudo yum install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-7-x86_64/pgdg-redhat-repo-latest.noarch.rpm

sudo yum install -y postgresql12-server postgresql12
```
这将安装 PostgreSQL 服务器及其附加组件。

## 初始化数据库
安装完成后，你需要初始化数据库并启动 PostgreSQL 服务。执行以下命令：
```sh
sudo /usr/pgsql-12/bin/postgresql-12-setup initdb
sudo systemctl start postgresql-12.service
sudo systemctl enable postgresql-12.service
```
可以使用 sudo systemctl enable  postgresql-12.service 命令来设置 PostgreSQL 开机启动。

## 配置 PostgreSQL 服务
编辑 PostgreSQL 配置文件 /var/lib/pgsql/data/postgresql.conf，找到并修改 listen_addresses 参数，将其设置为 '*'，以允许远程连接：

### 创建一个新的数据库用户: (首先，你需要切换到postgres用户。各版本都适用)
```sh
sudo -u postgres createuser --interactive
```
~~~
sudo
sudo命令允许你以另一个用户的安全权限，通常是超级用户（root），来运行命令。这在需要执行需要更高权限的命令时非常有用。
-u postgres
-u选项后跟的是用户名，这里是postgres。这告诉sudo命令以postgres用户的身份执行后面的命令。postgres是PostgreSQL安装后默认创建的超级用户，拥有创建新用户和数据库的权限。
createuser
createuser是一个PostgreSQL的工具，用于创建一个新的数据库用户。它是postgresql-client包的一部分。
--interactive
--interactive或-i选项使createuser命令以交互模式运行，它会提示你输入新用户的名称，并询问你是否要让新用户成为超级用户等。
~~~

### 创建一个新数据库
你可以使用createdb命令创建一个新数据库。比如，创建一个数据库的命令如下：
```sh
createdb -U username mynewdb
```
将username替换为你的用户名，mynewdb替换为你想要的数据库名称。

### 设置密码
为新用户设置密码可以通过psql命令行接口完成。首先，登录到psql：(退出使用\q)
```sh
psql -U username -d mynewdb
```
然后，使用SQL命令设置密码：
```sql
ALTER USER username WITH PASSWORD 'newpassword';
```
将username替换为你的用户名，newpassword替换为你的新密码。

## 补充内容
命令 sudo find / -name "pg_hba.conf" 用于在整个文件系统中搜索 pg_hba.conf 文件，但由于某些目录可能有权限限制，你会看到“权限不够”的信息。
我们可以修改命令来忽略这些“权限不够”的错误消息，只输出我们有权限访问的目录中的 pg_hba.conf 文件的位置：
```sh
sudo find / -name "pg_hba.conf" 2>/dev/null
```
找到文件后，将ident改为 md5 或 scram-sha-256 来允许密码验证。

一旦确认修改正确，不要忘记重新启动 PostgreSQL 服务来应用更改：
```sh
sudo systemctl restart postgresql-12.service
```





# 在 Django 中配置 PostgreSQL

## 安装 psycopg2
在 Django 中连接 PostgreSQL，你需要安装 psycopg2 包。可以通过 pip 安装：
```sh
pip install psycopg2
```

## 配置 Django 设置文件
在 Django 项目的设置文件 (settings.py) 中，修改数据库配置为连接到 PostgreSQL 数据库：
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydatabase',
        'USER': 'myuser',
        'PASSWORD': 'mypassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```
请确保将 'NAME'、'USER' 和 'PASSWORD' 等参数替换为你的 PostgreSQL 数据库的实际值。
配置完成后记得进行迁移：
```sh
python manage.py migrate
```


# 安装 MariaDB 数据库

## 更新包索引
在安装任何软件之前，建议先更新系统的软件包索引：
```sh
sudo yum update
```

## 安装 MariaDB
使用 yum 包管理器安装 MariaDB：
```sh
sudo yum install mariadb-server mariadb
```
这将安装 MariaDB 服务器和 MariaDB 客户端工具。

## 配置 MariaDB
启动 MariaDB并设置开机启动：
```sh
sudo systemctl start mariadb
sudo systemctl enable mariadb
```
MariaDB 提供了一个安全性脚本，可以帮助你更改默认的安全设置并设置 root 密码等。运行以下命令：
```sh
sudo mysql_secure_installation
```
登录 MariaDB:
```sh
sudo mysql -u root -p
```

## 创建数据库和用户（可选）：
在 MariaDB 控制台中，你可以创建新的数据库和用户，并为用户授予适当的权限。例如：
```sql
CREATE DATABASE mydatabase;
CREATE USER 'myuser'@'localhost' IDENTIFIED BY 'mypassword';
GRANT ALL PRIVILEGES ON mydatabase.* TO 'myuser'@'localhost';
FLUSH PRIVILEGES;
```
这些命令将创建一个名为 mydatabase 的数据库，创建一个名为 myuser 的用户，并为该用户授予在 mydatabase 数据库上的所有权限。

安装和配置 MariaDB 完成后，你可以通过以下命令来检查 MariaDB 服务的状态：
```sh
sudo systemctl status mariadb
```




