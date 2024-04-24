# 首先服务器安装依赖包
```sh
pip install -r requirements.txt
```

# Nginx 相关内容

## Nginx 代码解释
```sh
server {
    listen 80;
    server_name your_domain.com;

    location / {
        root /path/to/your/vue/app/dist;
        try_files $uri $uri/ /index.html;
    }
}
```
- server：这个指令开始一个新的server块，用于定义一个虚拟主机和相关的配置。在一个Nginx配置文件中，你可以拥有多个server块，每个块配置不同的网站或应用。

- listen 80;：这行告诉Nginx监听80端口，这是HTTP协议的默认端口。这意味着对你的服务器发起的HTTP请求将由这个server块处理。

- server_name your_domain.com;：这里设置这个server块处理的域名。你应该将your_domain.com替换成你自己的域名。

- location / {：location指令用于决定Nginx如何响应不同的URL请求。这个例子中，/代表根URL，也就是说，这个块会应用到所有对这个服务器的请求。

- root /path/to/your/vue/app/dist;：指定请求的根目录。这里你需要将/path/to/your/vue/app/dist替换为你Vue应用构建（build）后的dist目录的路径。这意味着当Nginx接收到一个HTTP请求时，它会在这个目录下查找请求的文件。

- try_files $uri $uri/ /index.html;：这行告诉Nginx首先尝试按请求的URI去找文件，如果找不到文件，再尝试将请求视为一个目录处理，如果这也失败了，则最终返回index.html文件。这对于单页面应用（SPA）非常有用，因为大部分路由都是由前端JavaScript处理的，所以无论请求的路径是什么，最终都应该加载index.html文件并由前端框架处理路由。


## 如何配置 Nginx
- 首先，确保你的CentOS虚拟机上安装了Nginx。如果没有安装，可以通过CentOS的包管理器安装它。

- 找到Nginx的配置文件。Nginx的主配置文件通常位于/etc/nginx/nginx.conf，而具体的server配置通常放在/etc/nginx/conf.d/目录下的单独文件中，或者在/etc/nginx/sites-available/（并通过链接到/etc/nginx/sites-enabled/来启用）。

- 创建一个新的配置文件（如果你在conf.d目录下或sites-available），将上面的代码块复制进去，并按照你的实际情况修改server_name和root指令的值。

- 保存配置文件，并确保配置没有语法错误。可以通过运行sudo nginx -t来测试。

- 如果测试通过，重新加载Nginx配置使更改生效：sudo systemctl reload nginx。


## 为什么要使用 Nginx
- 性能：Nginx以其高性能、稳定性以及低资源消耗而闻名。
- 反向代理和负载均衡：Nginx可以作为反向代理服务器，帮助你将请求转发到后端的多个服务器，实现负载均衡。
- 静态文件托管：Nginx非常适合托管静态文件（如HTML、CSS、JavaScript文件），这使得它成为部署前端应用的理想选择。
- 安全：通过配置SSL/TLS，Nginx能够提供安全的HTTPS连接。
- 灵活的配置：Nginx的配置非常灵活，支持复杂的请求处理逻辑，满足不同的部署需求。



# 将前端构建的静态文件部署到 Web 服务器 and 配置Nginx来为这些文件提供服务

- 将前端文件传输到服务器：你需要将你的 Vue 应用构建出来的 dist 目录中的文件传输到你的 CentOS 服务器上。你可以使用 scp 命令，FTP 工具，或者任何其他你习惯的文件传输方法。
```sh
npm run build
```

- 配置 Nginx：根据你之前提供的 Nginx 配置，你应该指定一个实际的路径来替换占位符 /path/to/your/vue/app/dist，这个路径指向你传输到服务器上的 Vue 静态文件的位置。

- 服务器配置：如果你没有域名，你可以简单地修改你的 Nginx 配置文件中的 server_name 指令，使用服务器的 IP 地址或者 localhost（如果你打算在本地浏览）。
```sh
server_name localhost;  # 或者你服务器的公网IP地址
```

- 启动 Nginx 服务：确保 Nginx 正在运行，并且你的配置没有错误。在 CentOS 上，你可以使用以下命令：
```sh
sudo nginx -t    # 检查配置文件是否有误
sudo systemctl restart nginx  # 重启nginx服务
```

- 配置防火墙规则：如果你的CentOS服务器正在运行防火墙，你需要允许HTTP（端口80）和HTTPS（端口443，如果你使用SSL）的流量。可以使用以下命令：
```sh
sudo firewall-cmd --permanent --zone=public --add-service=http
sudo firewall-cmd --permanent --zone=public --add-service=https
sudo firewall-cmd --reload
```

- 测试前端应用：在浏览器中访问 http://your_server_ip 或者 http://localhost（取决于你使用的是什么），你应该能看到你的 Vue 应用的页面。

- 配置后端服务：确保你的 Django 后端服务也正在运行。通常你会在生产环境中使用一个应用服务器来运行 Django，比如 gunicorn。
```sh
gunicorn your_django_project.wsgi:application --bind 0.0.0.0:8000 --worker 3
```

- 配置 Nginx 作为反向代理：如果你还没有做，你需要配置 Nginx 来作为 Django应用的反向代理，以便于处理动态内容。这通常在 Nginx 配置文件中的一个新的 location 块中完成，如下所示：
```sh
location /api {
    proxy_pass http://localhost:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```
在实际应用中，/api 通常表示后端 API 的端点。这意味着，如果你的前端应用尝试访问像 `http://yourdomain.com/api/some_endpoint` 这样的地址，请求会被 Nginx 代理到运行在 localhost:8000 的 Django 应用。这是一种常见的前后端分离架构中的配置方式，允许 Nginx 处理静态文件和前端内容，同时也代理到后端应用以处理动态内容和 API 请求。

- 再次重载Nginx配置：每次修改Nginx配置后，你需要重载配置，或者重启Nginx服务。
```sh
sudo nginx -t
sudo systemctl reload nginx
```

- 确保所有服务开机自启：你可能想要确保Nginx和你的Django应用在服务器重启时能够自动启动。
```sh
sudo systemctl enable nginx
sudo systemctl enable gunicorn
```

# 后端运行命令
```sh
sudo iptables -I INPUT -p tcp --dport 8000 -j ACCEPT
sudo systemctl start nginx
gunicorn db_django.wsgi:application --bind 0.0.0.0:8000 --workers 3
gunicorn db_django.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 2000   # 超时时间设置为2000秒
```
