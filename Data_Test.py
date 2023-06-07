import pytest
import asyncio

from main import cache
from main import greet
from main import get_cache

local_cache = cache


@pytest.mark.asyncio
async def test_greeting():
    res = await greet()
    assert {"Timur": 'Hello, I am aiming to become a great Junior Python Developer'} == res


@pytest.mark.asyncio
async def test_cache():
    res = await get_cache()
    assert cache == res
