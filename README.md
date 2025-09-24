# TopV Adaptor Python

这是 TopV Adaptor 的 Python 实现版本，使用 Python 内置的 `http.server` 模块，无需外部 Web 框架。

## 接口实现

1. 推送接口

   **基于 NATS 推送实时数据** - 自动推送模拟数据到 NATS

2. 实时数据接口

	HTTP 接口实现 - `GET /api/find_last`

3. 历史数据接口

	HTTP 接口实现 - `POST /api/query_history`

4. 标签接口

   * 查询设备标签  - `GET /api/query_devices`

   * 查询测点标签  - `GET /api/query_points`


5. 反写接口

	HTTP 接口实现 - `POST /api/set_value`

## 安装依赖

```bash
# Windows
install.bat

# Linux/Mac
chmod +x install.sh
./install.sh
```

**注意**: 如果不需要 NATS 功能，可以跳过安装依赖，直接运行服务。

## 启动服务

### Windows
```bash
start.bat
```

### Linux/Mac
```bash
chmod +x start.sh
./start.sh
```

### 手动启动
```bash
python app.py
```

## 测试 API

### Windows
```bash
test-api.bat
```

### Linux/Mac
```bash
chmod +x test-api.sh
./test-api.sh
```

## API 接口说明

### 1. 查询实时数据
- **URL:** `POST /api/find_last`
- **请求体:**
```json
{
  "projectID": "test",
  "tag": "group1.dev1.a",
  "device": false
}
```

### 2. 设置值
- **URL:** `POST /api/set_value`
- **请求体:**
```json
{
  "projectID": "test",
  "tag": "group1.dev1.a",
  "value": "25.5",
  "time": 1640995200000
}
```

### 3. 查询历史数据
- **URL:** `POST /api/query_history`
- **请求体:**
```json
{
  "projectID": "test",
  "tag": ["group1.dev1.a"],
  "start": "2022-01-01T00:00:00Z",
  "end": "2022-01-02T00:00:00Z"
}
```

### 4. 查询测点标签
- **URL:** `POST /api/query_points`
- **请求体:**
```json
{
  "projectID": "test",
  "parentTag": "group1.dev1"
}
```

### 5. 查询设备标签
- **URL:** `POST /api/query_devices`
- **请求体:**
```json
{
  "projectID": "test"
}
```

### 6. 健康检查
- **URL:** `GET /health`

## NATS 配置

默认连接到 `nats://127.0.0.1:4222`，可以通过修改 `NatsPushService` 的构造函数参数来更改。

## 项目结构

```
topv-adaptor-python/
├── app.py                    # 主应用（无框架版本）
├── models.py                 # 数据模型定义
├── api_handler.py            # API 处理器
├── nats_service.py           # NATS 推送服务
├── requirements.txt          # Python 依赖
├── start.bat                 # Windows 启动脚本
├── start.sh                  # Linux/Mac 启动脚本
├── test-api.bat              # Windows API 测试脚本
├── test-api.sh               # Linux/Mac API 测试脚本
├── test_nats.py              # NATS 连接测试脚本
├── test_models.py            # 模型测试脚本
├── install.bat               # Windows 安装脚本
├── install.sh                # Linux/Mac 安装脚本
└── README.md                 # 项目说明
```

## 注意事项

1. 确保 NATS 服务器正在运行（默认地址：`nats://127.0.0.1:4222`）
2. 服务默认运行在端口 8080
3. 所有 API 接口都使用 POST 方法（除了健康检查）
4. 实时数据推送每秒执行一次，生成 30 个测点的随机数据
5. 使用 Python 内置模块，无需安装外部 Web 框架

## 与其他版本对比

- **Go 版本**: 使用标准库 `net/http` 和 `nats.go`
- **Java 版本**: 使用 Vert.x 和 `nats.java`
- **Python 版本**: 使用 Python 内置 `http.server` 和 `nats-py` 