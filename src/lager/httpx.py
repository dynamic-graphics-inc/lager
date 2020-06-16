# -*- coding: utf-8 -*-

import atexit

import asyncio
import httpx


class HttpxSink(object):


    def __init__(self, url, *args, **kwargs):
        self.url = url
        self.client = httpx.AsyncClient(*args, **kwargs)


    def __call__(self, msg):
        httpx.post(self.url, data={
            'msg': msg
            })


    async def handle(self, msg):
        await self.client.post(self.url, data=msg)


    async def await_delete_channels(self):
        await self.client.aclose()

# @atexit.register
# def shutdown():
#     print("Shutting down")
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(await_delete_channels())
