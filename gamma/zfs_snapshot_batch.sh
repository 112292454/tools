#!/bin/bash

# 动态获取所有用户目录
users=$(zfs list -H -o name | grep "^gamma/home/" | cut -d'/' -f3)

# 遍历用户，执行快照和删除任务
for user in $users; do
    echo 'now updating snapshot for :'$user
    zfs snapshot gamma/home/$user@auto-$(date +%Y%m%d%H)
    zfs destroy -r gamma/home/$user@auto-$(date --date='24 hours ago' +%Y%m%d%H)
done
echo 'snapshot update finished'