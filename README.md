# TOOLs


一些自用的便捷脚本

目前可用的应该主要有：
- linux系统上的批量解压文件（主要解决unzip、unrar不能应对其他格式，而7z解压时不会自动创建文件夹的问题）
- 音视频与图片的处理（by ffmpeg）：
  - 一键限制图片到指定的分辨率（往往能同时大幅缩小图片体积，对于福利姬图片，通常压缩率为2~10x）
  - 
- 垃圾文件去重（比如很多资源下载之后会有一些宣称他们网站的文件，而对于同一个渠道，这些文件内容是一样的，所以我考虑记录常见文件的hash，存一个json库。然后运行去重程序一键删除已识别的。然后没识别出来的垃圾可以运行一遍检测程序，添加到库）
- 文件名的规范化
- 对于使用cookie的网站自动签到（需要自行写linux service unit）


其他功能待定

文件结构整理待定

可用性说明（帮助）待定

-----
btw，其实还有个videoZip的库，考虑的是自动压缩一些想存着，但是不是很常播放的视频。
那个我写的是比较完善的，能实际使用，而且压缩效果我也自己调试过一阵子。

但是我转换完之后，采用nas/smb/nfs等远程手段播放时，发现h265的格式虽然存储空间小，
但是解码速度太慢，所以我没有对我的视频全部应用。
（不过如果你的视频是本地存储，那解码基本不会有影响，完全可以考虑跑一遍）

之后想想 如果适合的话，把那个库也整理到这个项目里