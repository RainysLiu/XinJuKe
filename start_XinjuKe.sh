#!/bin/sh
/usr/local/nginx/sbin/nginx > /dev/null
echo '开启nginx服务成功！'
nohup redis-server &
echo '开启redis服务成功！'
nohup uwsgi --ini /home/XinJuKe/uwsgi.ini > /home/XinJuKe.log &
echo '开启uwsgi服务成功！项目部署成功！！！'