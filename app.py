import asyncio
import json
import logging
import signal
import sys
import threading
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from api_handler import find_last, set_value, query_history, query_points, query_devices
from nats_service import NatsPushService

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# NATS 服务实例
nats_service = None
nats_task = None


class TopVRequestHandler(BaseHTTPRequestHandler):
    """自定义 HTTP 请求处理器"""
    
    def _set_response(self, status_code=200, content_type='application/json'):
        """设置响应头"""
        self.send_response(status_code)
        self.send_header('Content-Type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def _read_request_body(self):
        """读取请求体"""
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length > 0:
            return self.rfile.read(content_length).decode('utf-8')
        return None
    
    def _send_json_response(self, data, status_code=200):
        """发送 JSON 响应"""
        self._set_response(status_code)
        response = json.dumps(data, ensure_ascii=False)
        self.wfile.write(response.encode('utf-8'))
    
    def do_OPTIONS(self):
        """处理 OPTIONS 请求（CORS 预检）"""
        self._set_response()
    
    def do_POST(self):
        """处理 POST 请求"""
        try:
            parsed_url = urlparse(self.path)
            path = parsed_url.path
            
            # 读取请求体
            body = self._read_request_body()
            request_data = json.loads(body) if body else {}
            
            # 根据路径分发到不同的处理器
            if path == '/api/set_value':
                response = set_value(request_data)
            elif path == '/api/query_history':
                response = query_history(request_data)
            else:
                self._send_json_response({"error": "Not found"}, 404)
                return
            
            self._send_json_response(response)
            
        except json.JSONDecodeError:
            self._send_json_response({"error": "Invalid JSON"}, 400)
        except Exception as e:
            logger.error(f"Error handling POST request: {e}")
            self._send_json_response({"error": "Internal server error"}, 500)
    
    def do_GET(self):
        """处理 GET 请求"""
        try:
            parsed_url = urlparse(self.path)
            path = parsed_url.path
            
            if path == '/health':
                self._send_json_response({"status": "healthy", "service": "topv-adaptor-python"})
                return
            
            # 读取请求体（GET 请求也可能包含 body）
            body = self._read_request_body()
            request_data = json.loads(body) if body else {}
            
            # 根据路径分发到不同的处理器
            if path == '/api/find_last':
                response = find_last(request_data)
            elif path == '/api/query_points':
                response = query_points(request_data)
            elif path == '/api/query_devices':
                response = query_devices(request_data)
            else:
                self._send_json_response({"error": "Not found"}, 404)
                return
            
            self._send_json_response(response)
            
        except json.JSONDecodeError:
            self._send_json_response({"error": "Invalid JSON"}, 400)
        except Exception as e:
            logger.error(f"Error handling GET request: {e}")
            self._send_json_response({"error": "Internal server error"}, 500)
    

    
    def log_message(self, format, *args):
        """重写日志方法，使用我们的 logger"""
        logger.info(f"{self.address_string()} - {format % args}")


async def start_nats_service():
    """启动 NATS 服务"""
    global nats_service, nats_task
    try:
        nats_service = NatsPushService()
        await nats_service.connect()
        await nats_service.start_realtime_push()
        logger.info("NATS service started successfully")
    except Exception as e:
        logger.error(f"Failed to start NATS service: {e}")


async def stop_nats_service():
    """停止 NATS 服务"""
    global nats_service
    if nats_service:
        await nats_service.close()
        logger.info("NATS service stopped")


def signal_handler(signum, frame):
    """信号处理器"""
    logger.info(f"Received signal {signum}, shutting down...")
    if nats_task and not nats_task.done():
        nats_task.cancel()
    sys.exit(0)


def run_nats_service():
    """在新线程中运行 NATS 服务"""
    global nats_task
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    nats_task = loop.create_task(start_nats_service())
    loop.run_forever()


def main():
    """主函数"""
    # 设置信号处理器
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # 启动 NATS 服务
    nats_thread = threading.Thread(target=run_nats_service, daemon=True)
    nats_thread.start()
    
    # 启动 HTTP 服务器
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, TopVRequestHandler)
    
    logger.info("Starting HTTP server on port 8080")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("Shutting down server...")
        httpd.shutdown()


if __name__ == '__main__':
    main() 