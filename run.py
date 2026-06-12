import anyio.to_thread
import asyncio

# 修正 Python 3.14 與 anyio 的相容性問題 (解決載入 js 時發生的 TypeError)
async def _run_sync(func, *args, **kwargs):
    return await asyncio.to_thread(func, *args)

anyio.to_thread.run_sync = _run_sync

import sys
from streamlit.web.cli import main

if __name__ == '__main__':
    if len(sys.argv) > 1:
        sys.argv = ["streamlit", "run", "src/main.py"] + sys.argv[1:]
    else:
        sys.argv = ["streamlit", "run", "src/main.py"]
    main()
