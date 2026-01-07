# 服务器和浏览器实现 CORS 原理

## 浏览器端 CORS 实现原理

### 1. **预检请求（Preflight Request）**
- 对于复杂请求（如 PUT、DELETE 或带自定义头的请求），浏览器先发送 OPTIONS 预检请求
- 检查服务器是否允许跨域请求
- 预检成功后才发送实际请求

### 2. **简单请求处理**
- 对于 GET、POST 等简单请求，浏览器直接发送请求
- 检查响应头中的 CORS 相关字段
- 检查不通过，浏览器会阻止前端代码访问响应内容

### 3. **CORS 头验证**
- 浏览器验证响应头中的 `Access-Control-Allow-Origin` 等字段
- 判断是否允许当前源的跨域访问

## 服务器端 CORS 实现原理

### 1. **响应头设置**
- `Access-Control-Allow-Origin`: 指定允许访问的源
- `Access-Control-Allow-Methods`: 允许的 HTTP 方法
- `Access-Control-Allow-Headers`: 允许的请求头
- `Access-Control-Max-Age`: 预检请求缓存时间

### 2. **预检请求处理**
- 对 OPTIONS 请求返回适当的 CORS 头
- 告知浏览器是否允许实际请求

## 结合代码配置理解

在您的 [CorsConfig](file:///Users/zbz/workspace/rusthing/robotech-rs/src/web/server/web_server_settings.rs#L37-L50) 配置中：

- [allowed_origins](file:///Users/zbz/workspace/rusthing/robotech-rs/src/web/server/web_server_settings.rs#L41-L41): 控制 `Access-Control-Allow-Origin` 响应头
- [allowed_methods](file:///Users/zbz/workspace/rusthing/robotech-rs/src/web/server/web_server_settings.rs#L43-L43): 控制 `Access-Control-Allow-Methods` 响应头
- [allowed_headers](file:///Users/zbz/workspace/rusthing/robotech-rs/src/web/server/web_server_settings.rs#L44-L44): 控制 `Access-Control-Allow-Headers` 响应头

## 关键区别

- **服务器端**: 主要负责设置响应头，告知浏览器允许的跨域策略
- **浏览器端**: 验证服务器返回的 CORS 头，执行安全策略
- **通信流程**: 浏览器作为中间人，验证服务器的 CORS 策略后才允许前端代码获取响应数据