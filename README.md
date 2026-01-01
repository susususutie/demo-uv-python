## UV

### 安装

安装前打开代理的TUN模式，以启用命令行代理

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# downloading uv 0.9.18 aarch64-apple-darwin
# no checksums to verify
# installing to /Users/sutie/.local/bin
#   uv
#   uvx
# everything's installed!
```

### 检查安装是否成功

```bash
uv --version
# uv 0.9.10 (44f5a14f4 2025-11-17)
uvx --version
# uvx 0.9.10 (44f5a14f4 2025-11-17)
```

### 卸载

```bash
# 清理 uv 存储的数据
uv cache clean  
# Clearing cache at: /Users/sutie/.cache/uv
# Removed 11378 files (233.8MiB)
rm -r "$(uv python dir)"
rm -r "$(uv tool dir)"
rm ~/.local/bin/uv ~/.local/bin/uvx
```

### 更新

更新时需要使用 [GitHub](https://github.com/settings/tokens) 访问 token

```bash
uv self update
uv self update --token <github-token>
# info: Checking for updates...
# success: Upgraded uv from v0.9.18 to v0.9.21! https://github.com/astral-sh/uv/releases/tag/0.9.21
# 若不携带 token：
# error: GitHub API rate limit exceeded. Please provide a GitHub token via the `--token` option.
```

### 使用

```bash
uv init project-name
```

### 新增依赖

```bash
uv add pkg
```

### 删除依赖

```bash
uv remove pkg
```

### python 版本管理

```bash
# 安装指定 Python 版本。
uv python install 3.12
# 查看可用的 Python 版本。
uv python list
# 查找已安装的 Python 版本。
uv python find
# 为当前项目指定使用的 Python 版本。
uv python pin
# 卸载 Python 版本
uv python uninstall
```

### 链接

- [UV 官方文档](https://docs.astral.sh/uv/)