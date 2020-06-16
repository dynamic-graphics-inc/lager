# -*- coding: utf-8 -*-

import atexit

import asyncio
import httpx


class HttpxSink(object):


    def __init__(self, url, *args, **kwargs):
        self.url = url
        self.client = httpx.AsyncClient(*args, **kwargs)


    async def __call__(self, msg):
        await self.client.post(self.url, data=msg)


    async def await_delete_channels(self):
        await self.client.aclose()


    @atexit.register
    def shutdown(self):
        print("Shutting down")
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.await_delete_channels())
