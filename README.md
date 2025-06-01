# FuckXZ

一个高效针对XZphotos的账号生成工具

## 特性

- 多线程并发注册（1-20个线程）
- 可自定义注册频率（0.3-60秒/次）
- 智能生成随机账号信息：
  - 用户名：20-25位字母数字组合
  - 邮箱：20-25位字母数字组合
  - 密码：32-40位包含特殊字符的强密码
- 实时显示注册进度和统计
- 支持优雅退出（Ctrl+C）
- 自动保存成功注册的账号信息

## 环境要求

- Python 3.6+
- requests库

## 安装

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/xz-photos-account-generator.git
cd xz-photos-account-generator
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

## 使用方法

### 基本用法

```bash
python fuckxz.py
```

### 命令行参数

- `--threads`: 并发线程数量（1-20，默认5）
- `--frequency`: 注册频率，单位秒（0.3-60，默认1.0）
- `--count`: 需要注册的总账号数量（默认10）

### 示例

1. 使用默认配置（5线程，1秒/次，注册10个账号）：
```bash
python fuckxz.py
```

2. 高速模式（10线程，0.3秒/次，注册100个账号）：
```bash
python fuckxz.py --threads 10 --frequency 0.3 --count 100
```

3. 稳定模式（3线程，2秒/次，注册50个账号）：
```bash
python fuckxz.py --threads 3 --frequency 2 --count 50
```

## 输出文件

成功注册的账号信息会自动保存在 `successful_accounts.txt` 文件中，格式如下：
```
账号: Abc123xyz789def456ghi, 邮箱: Xyz123abc456def789ghi@domain.com, 密码: Kj#9$mP2*nX5@qL7^vR4&wY8!zC3%tB6
```

## 开发注意事项

1. 账号生成规则
   - 用户名：20-25位字母数字组合，以字母开头
   - 邮箱前缀：20-25位字母数字组合，以字母开头
   - 密码：32-40位，包含大小写字母、数字和特殊字符

2. 性能优化
   - 每个线程使用独立的session以提高效率
   - 使用线程锁确保计数器和文件写入的线程安全
   - 实现了优雅退出机制，确保数据不丢失

3. 注意事项
   - 建议从低线程数开始测试
   - 当线程数超过10时会显示警告
   - 频率设置过快可能导致注册失败或IP被封
   - 建议使用代理IP轮换以避免IP被封

4. 错误处理
   - 所有网络请求都有超时处理
   - 失败的请求会被记录但不会中断程序
   - 可以通过Ctrl+C随时停止程序

## 自定义开发

### 修改账号生成规则

可以修改以下函数来自定义生成规则：
- `generate_username()`: 自定义用户名生成规则
- `generate_email_prefix()`: 自定义邮箱前缀生成规则
- `generate_password()`: 自定义密码生成规则

### 添加新功能

1. 添加代理支持：
```python
proxies = {
    'http': 'http://your-proxy:port',
    'https': 'https://your-proxy:port'
}
session.proxies = proxies
```

2. 添加验证码处理：
```python
# 在register_account函数中添加验证码处理逻辑
```

## 常见问题

1. 注册失败率高
   - 降低注册频率
   - 减少并发线程数
   - 检查网络连接
   - 考虑使用代理IP

2. IP被封
   - 降低注册频率
   - 减少并发线程数
   - 使用代理IP
   - 增加注册间隔时间

3. 程序异常退出
   - 检查网络连接
   - 查看错误日志
   - 确保有写入文件权限

## 贡献指南

1. Fork 项目
2. 创建新分支：`git checkout -b feature-name`
3. 提交更改：`git commit -am 'Add some feature'`
4. 推送分支：`git push origin feature-name`
5. 提交 Pull Request

## 免责声明

本工具仅供学习和研究使用，请勿用于非法用途。使用本工具所产生的任何后果由使用者自行承担。

## 许可证

MIT License 
