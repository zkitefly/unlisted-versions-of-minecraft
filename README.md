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
+ https://vip.123pan.cn/1821946486/unlisted-versions-of-minecraft
```

格式与 [version_manifest.json](https://zh.minecraft.wiki/w/Version_manifest.json) 保持一致

## 安装

### 安装器

使用 [Releases](https://github.com/zkitefly/unlisted-versions-of-minecraft/releases) 的安装器快速安装。

### 手动安装

前往 `files` 目录中，找到你想下载的版本，下载该版本的 json 文件

打开游戏目录，进入 `versions` 目录，新建一个文件夹，命名为该 json 文件的名称，再将 json 文件放入其中

回到启动器刷新版本列表即可找到该版本，启动游戏即可！

## 关于本仓库对旧版本的支持

本仓库不会添加任何修复补丁，如果你想获得比较良好的体验，可使用 [NeRdTheNed/RetroWrapper](https://github.com/NeRdTheNed/RetroWrapper) 的补丁，以修复并正常运行旧版本。
