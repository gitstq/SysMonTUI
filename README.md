<div align="center">

# 🖥️ SysMonTUI

**轻量级跨平台系统监控 TUI 工具**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey)](https://github.com/gitstq/SysMonTUI)
[![PyPI](https://img.shields.io/badge/PyPI-Install-orange)](https://pypi.org/project/sysmontui/)

[English](#english) | [简体中文](#简体中文) | [繁體中文](#繁體中文)

</div>

---

<a name="简体中文"></a>
## 🎉 项目介绍

**SysMonTUI** 是一款轻量级、跨平台的系统资源监控 TUI（终端用户界面）工具，提供实时、美观、交互式的系统性能监控界面。

### 💡 灵感来源

本项目灵感来源于 [syswatch](https://github.com/matthart1983/syswatch)（Rust 实现），但我们使用 Python 完全重新开发，增加了更多可视化功能和更好的跨平台支持，让系统监控变得更加简单和美观。

### ✨ 核心特性

- 🚀 **实时监控**: CPU、内存、磁盘、网络实时数据更新
- 🎨 **精美界面**: 基于 Rich 库的高颜值 TUI 界面
- 🖥️ **跨平台**: 支持 Linux、macOS、Windows
- ⌨️ **交互操作**: 支持键盘快捷键切换视图
- 📊 **可视化图表**: 实时折线图、进度条、颜色编码
- 🔄 **历史记录**: 自动记录历史数据，支持趋势分析
- 🔧 **零依赖**: 仅依赖 psutil 和 rich，安装简单
- 🌐 **多语言**: 原生支持中文界面

---

## 🚀 快速开始

### 环境要求

- **Python**: 3.8 或更高版本
- **操作系统**: Linux / macOS / Windows

### 安装

```bash
# 使用 pip 安装
pip install sysmontui

# 或者从源码安装
git clone https://github.com/gitstq/SysMonTUI.git
cd SysMonTUI
pip install -e .
```

### 启动

```bash
# 启动交互式监控界面
sysmontui

# 或使用简写
smt

# 指定刷新率（秒）
sysmontui -r 0.5

# 显示一次并退出
sysmontui --once
```

---

## 📖 详细使用指南

### 键盘快捷键

| 按键 | 功能 |
|------|------|
| `0` | 概览模式（所有面板） |
| `1` | CPU 详细视图 |
| `2` | 内存详细视图 |
| `3` | 磁盘详细视图 |
| `4` | 网络详细视图 |
| `5` | 进程详细视图 |
| `q` | 退出程序 |
| `h` / `?` | 显示帮助 |

### 监控功能

#### 🧠 CPU 监控
- 总体使用率实时显示
- 每个核心的独立监控
- CPU 频率和温度（如可用）
- 系统负载平均值（Unix）
- CPU 时间统计

#### 💾 内存监控
- 物理内存使用详情
- Swap 交换分区监控
- 缓存和缓冲区统计
- 可视化进度条

#### 💿 磁盘监控
- 各分区使用情况
- 磁盘 I/O 统计
- 读写速度监控
- 挂载点信息

#### 🌐 网络监控
- 网络接口状态
- 上传/下载流量统计
- 数据包收发计数
- 连接状态监控

#### ⚙️ 进程监控
- Top 进程列表
- CPU/内存占用排序
- 进程状态显示
- 线程数统计

---

## 💡 设计思路与迭代规划

### 技术选型原因

- **Python**: 跨平台、生态丰富、开发效率高
- **Rich**: 提供现代化的终端 UI 组件，支持表格、进度条、布局等
- **psutil**: 跨平台的系统信息获取库，功能完善

### 后续功能迭代计划

- [ ] 数据导出功能（JSON/CSV）
- [ ] 告警阈值设置
- [ ] 远程监控支持
- [ ] 插件系统
- [ ] 自定义主题
- [ ] Docker 容器监控

### 社区贡献方向

- 提交 Bug 报告和功能建议
- 完善多语言支持
- 优化性能和资源占用
- 增加更多监控指标

---

## 📦 打包与部署指南

### 从源码运行

```bash
git clone https://github.com/gitstq/SysMonTUI.git
cd SysMonTUI
pip install -r requirements.txt
python -m sysmontui
```

### 打包发布

```bash
# 构建分发包
python -m build

# 上传到 PyPI
python -m twine upload dist/*
```

### Docker 运行

```bash
# 构建镜像
docker build -t sysmontui .

# 运行容器
docker run --rm -it --pid=host sysmontui
```

---

## 🤝 贡献指南

欢迎提交 Pull Request 和 Issue！

### 提交规范

- 使用 [Conventional Commits](https://conventionalcommits.org/) 规范
- 代码风格遵循 PEP 8
- 提交前运行测试：`pytest tests/`

### Issue 反馈

- 描述问题时请提供系统环境和复现步骤
- 功能建议请说明使用场景

---

## 📄 开源协议

本项目采用 [MIT License](LICENSE) 开源协议。

---

<a name="繁體中文"></a>
## 🎉 專案介紹

**SysMonTUI** 是一款輕量級、跨平台的系統資源監控 TUI（終端使用者介面）工具，提供即時、美觀、互動式的系統效能監控介面。

### ✨ 核心特性

- 🚀 **即時監控**: CPU、記憶體、磁碟、網路即時資料更新
- 🎨 **精美介面**: 基於 Rich 函式庫的高顏值 TUI 介面
- 🖥️ **跨平台**: 支援 Linux、macOS、Windows
- ⌨️ **互動操作**: 支援鍵盤快捷鍵切換視圖
- 📊 **視覺化圖表**: 即時折線圖、進度條、顏色編碼
- 🔄 **歷史記錄**: 自動記錄歷史資料，支援趨勢分析

### 🚀 快速開始

```bash
# 安裝
pip install sysmontui

# 啟動
sysmontui
```

### 鍵盤快捷鍵

| 按鍵 | 功能 |
|------|------|
| `0` | 概覽模式 |
| `1-5` | 切換視圖 |
| `q` | 退出 |

---

<a name="english"></a>
## 🎉 Introduction

**SysMonTUI** is a lightweight, cross-platform system resource monitoring TUI (Terminal User Interface) tool that provides real-time, beautiful, and interactive system performance monitoring.

### ✨ Key Features

- 🚀 **Real-time Monitoring**: Live updates for CPU, Memory, Disk, and Network
- 🎨 **Beautiful UI**: Modern TUI built with Rich library
- 🖥️ **Cross-Platform**: Supports Linux, macOS, and Windows
- ⌨️ **Interactive**: Keyboard shortcuts for view switching
- 📊 **Visual Charts**: Real-time line charts, progress bars, color coding
- 🔄 **History Tracking**: Automatic history recording for trend analysis

### 🚀 Quick Start

```bash
# Install
pip install sysmontui

# Run
sysmontui
```

### Keyboard Shortcuts

| Key | Function |
|-----|----------|
| `0` | Overview mode |
| `1-5` | Switch views |
| `q` | Quit |

---

<div align="center">

Made with ❤️ by [gitstq](https://github.com/gitstq)

</div>
