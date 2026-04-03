# 本地运行绘图脚本教程

本教程面向 Python 新手，指导你在 Windows 上使用 Jupyter Lab 运行本项目的绘图脚本。

---

## 第一步：检查 Python 是否安装

如果电脑上已经安装了 Jupyter Lab，通常意味着 Python 也已经安装好了。验证方法：按 `Win + R`，输入 `cmd`，回车打开命令提示符（或者用 PowerShell），输入：
```bash
python --version
```
如果显示 `Python 3.x.x` 说明安装成功。

---

## 第二步：下载本项目

在 GitHub 页面点击绿色 **Code** 按钮 → **Download ZIP**，解压到任意文件夹，例如 `C:\Users\XXX\XXX\hwang-plot`。

---

## 第三步：安装依赖库

按 `Win + R`，输入 `cmd`，回车打开命令提示符，先进入项目文件夹（路径替换为你实际的解压路径）：

```bash
cd C:\Users\XXX\XXX\hwang-plot
```

然后安装画图依赖库：

```bash
pip install -r requirements.txt
```

> **提示：** 如果下载很慢，可加国内镜像：
> ```bash
> pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
> ```

---

## 第四步：启动 Jupyter Lab

在命令提示符中（确保当前在项目根目录），运行：

```bash
jupyter lab
```

浏览器会自动打开 Jupyter Lab 界面，显示项目文件夹内容。

注：这其实有脱裤子放屁之嫌 —— 正常做法应该是在 CMD 或者 Powershell 中直接运行 Python 脚本 —— 但新手可能只用过 Jupyter。

---

## 第五步：运行绘图脚本

1. 在 Jupyter Lab 左侧文件浏览器中，双击进入对应的图表文件夹，例如 `figure5/`。
2. 在顶部菜单栏点击 **File** → **New** → **Terminal**，终端会自动在当前文件夹中打开。
3. 依次运行各绘图脚本：
   ```bash
   python plot1.py
   python plot2.py
   python plot3.py
   python plot4.py
   python plot5.py
   ```
4. 运行完成后，在左侧文件浏览器中进入 `figure5/figs/` 文件夹，即可看到生成的图片。

---

## 常见问题

**Q：`pip` 命令提示不是内部命令？**  
A：Python 安装时没有勾选 "Add Python to PATH"，重新安装并勾选该选项。

**Q：运行时提示 `ModuleNotFoundError`？**  
A：某个库未安装，重新执行第三步，或单独安装：`pip install 库名`。

**Q：提示找不到数据文件（`FileNotFoundError`）？**  
A：终端当前工作路径不在正确的 `figureN/` 文件夹中。`cd` 切换到正确的子文件夹再运行脚本，或者关闭当前终端，然后在正确子文件夹中新建一个终端。

**Q：图表中文字显示为方块？**  
A：字体缺失。在命令提示符中运行以下命令清除字体缓存后重试：
```bash
python -c "import matplotlib; import shutil; shutil.rmtree(matplotlib.get_cachedir())"
```
