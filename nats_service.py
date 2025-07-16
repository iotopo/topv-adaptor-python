import asyncio
import json
import random
import logging
from datetime import datetime
from typing import Optional
import nats
from nats.aio.client import Client as NATS
from models import ValueItem

logger = logging.getLogger(__name__)


class NatsPushService:
    def __init__(self, nats_url: str = "nats://127.0.0.1:4222"):
        self.nats_url = nats_url
        self.nc: Optional[NATS] = None
        self.random = random.Random()
        self.push_task: Optional[asyncio.Task] = None

    async def connect(self):
        """连接到 NATS 服务器"""
        try:
            self.nc = await nats.connect(self.nats_url)
            logger.info("Connected to NATS server")
        except Exception as e:
            logger.error(f"Failed to connect to NATS: {e}")
            raise



    async def push_realtime_value(self, item: ValueItem):
        """推送实时数据到 NATS"""
        if self.nc:
            try:
                payload = item.to_json().encode('utf-8')
                subject = f"rtdb.iotopo.{item.tag}"
                await self.nc.publish(subject, payload)
            except Exception as e:
                logger.error(f"Error publishing to NATS: {e}")

    async def start_realtime_push(self):
        """开始实时数据推送"""
        if self.push_task and not self.push_task.done():
            return

        self.push_task = asyncio.create_task(self._push_loop())
        logger.info("Started realtime data push")

    async def stop_realtime_push(self):
        """停止实时数据推送"""
        if self.push_task and not self.push_task.done():
            self.push_task.cancel()
            try:
                await self.push_task
            except asyncio.CancelledError:
                pass
            logger.info("Stopped realtime data push")

    async def _push_loop(self):
        """推送循环"""
        while True:
            try:
                now = datetime.now()
                for i in range(3):
                    for j in range(10):
                        # 生成1-100之间的随机数
                        value = self.random.uniform(1, 100)
                        tag = f"group{i+1}.dev{j+1}.a"
                        
                        item = ValueItem(tag, now, value, 1)
                        await self.push_realtime_value(item)
                
                # 每秒推送一次
                await asyncio.sleep(1)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in push loop: {e}")
                await asyncio.sleep(1)

    async def close(self):
        """关闭 NATS 连接"""
        await self.stop_realtime_push()
        if self.nc:
            await self.nc.close()
            logger.info("NATS connection closed") 