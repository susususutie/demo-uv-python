# UV 包管理器

UV 是一个 Rust 写的 Python 包管理和项目工具，超快。

## 安装

安装前打开代理的 TUN 模式，以启用命令行代理。

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# downloading uv 0.9.18 aarch64-apple-darwin
# no checksums to verify
# installing to /Users/sutie/.local/bin
#   uv
#   uvx
# everything's installed!
```

验证安装：

```bash
uv --version
# uv 0.9.10 (44f5a14f4 2025-11-17)
uvx --version
# uvx 0.9.10 (44f5a14f4 2025-11-17)
```

## 基本使用

创建新项目：

```bash
uv init project-name
```

管理依赖：

```bash
uv add pkg          # 添加依赖
uv remove pkg       # 删除依赖
```

## Python 版本管理

```bash
uv python install 3.12    # 安装 Python 3.12
uv python list            # 查看可用版本
uv python find            # 查找已安装版本
uv python pin             # 为项目指定 Python 版本
uv python uninstall       # 卸载 Python 版本
```

## 更新与卸载

更新 UV：

```bash
uv self update
# error: GitHub API rate limit exceeded. Please provide a GitHub token via the `--token` option.
# 如遇 API 限制，使用 GitHub Token 更新
uv self update --token <github-token>
# success: Upgraded uv from v0.9.18 to v0.9.21! https://github.com/astral-sh/uv/releases/tag/0.9.21
```

卸载 UV：

```bash
uv cache clean                    # 清理缓存
rm -r "$(uv python dir)"           # 删除 Python 安装目录
rm -r "$(uv tool dir)"            # 删除工具目录
rm ~/.local/bin/uv ~/.local/bin/uvx  # 删除可执行文件
```

## 资源链接

- [UV 官方文档](https://docs.astral.sh/uv/)
- [生成 Github 访问 token](https://github.com/settings/tokens)
