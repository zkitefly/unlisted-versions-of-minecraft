# Unlisted versions of Minecraft

## 关于

本仓库整理在启动器中未列出的版本，并提供启动器接口提供下载

这些版本的数据来自 [PrismLauncher/meta](https://github.com/PrismLauncher/meta) 仓库和 [Minecraft Wiki](https://zh.minecraft.wiki/)。

**版权由 Mojang AB 所有。**

## API 接口

```
https://zkitefly.github.io/unlisted-versions-of-minecraft/version_manifest.json
```

如果要大陆加速，可以将链接前缀修改成：

```diff
- https://zkitefly.github.io/unlisted-versions-of-minecraft
+ https://gitee.com/bleaker/unlisted-versions-of-minecraft/raw/main
```

格式与 [version_manifest.json](https://zh.minecraft.wiki/w/Version_manifest.json) 保持一致

## 安装

### 安装器

使用 [Releases](https://github.com/zkitefly/unlisted-versions-of-minecraft/releases) 的安装器快速安装。

### 手动安装

前往 `files` 目录中，找到你想下载的版本，下载该版本的 json 文件

打开启动器的 `.minecraft` 目录

进入 `versions` 目录，新建一个文件夹，命名为该 json 的名称

回到启动器刷新版本列表即可找到该版本，启动游戏即可！

## 关于游戏内无声的问题

在确认设置中开启声音的情况下，游玩时不会听到任何声音

可能是由于版本过于老旧，一些版本无法下载到所需要的资源文件，导致游戏内无声音

可尝试在启动器的 Java 虚拟机参数中追加如下参数，并确保网络通畅，然后重新启动游戏

```
-Dhttp.proxyHost=betacraft.uk
```

###### 该参数来自 [Betacraft](https://github.com/betacraftuk)
