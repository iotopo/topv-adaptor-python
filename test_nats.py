#!/usr/bin/env python3
"""
NATS 连接测试脚本
"""

import asyncio
import logging
from nats_service import NatsPushService
from models import ValueItem
from datetime import datetime

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_nats_connection():
    """测试 NATS 连接"""
    try:
        logger.info("Testing NATS connection...")
        
        # 创建 NATS 服务
        nats_service = NatsPushService()
        
        # 尝试连接
        await nats_service.connect()
        logger.info("NATS connection successful!")
        
        # 测试推送一条数据
        test_item = ValueItem("test.tag", datetime.now(), 123.45, 1)
        await nats_service.push_realtime_value(test_item)
        logger.info("Test data pushed successfully!")
        
        # 关闭连接
        await nats_service.close()
        logger.info("NATS connection closed.")
        
    except Exception as e:
        logger.error(f"NATS test failed: {e}")
        logger.info("Make sure NATS server is running on nats://127.0.0.1:4222")


async def main():
    """主函数"""
    await test_nats_connection()


if __name__ == "__main__":
    asyncio.run(main()) 