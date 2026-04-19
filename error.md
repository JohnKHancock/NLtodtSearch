## python application/app.py

(.venv) (base) PS C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch> python application/app.py
Running on local URL:  http://127.0.0.1:7860
ERROR:    Exception in ASGI application
Traceback (most recent call last):
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\uvicorn\protocols\http\h11_impl.py", line 415, in run_asgi
    result = await app(  # type: ignore[func-returns-value]
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\uvicorn\middleware\proxy_headers.py", line 60, in __call__
    return await self.app(scope, receive, send)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\fastapi\applications.py", line 1159, in __call__
    await super().__call__(scope, receive, send)
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\starlette\applications.py", line 90, in __call__
    await self.middleware_stack(scope, receive, send)
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\starlette\middleware\errors.py", line 186, in __call__
    raise exc
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\starlette\middleware\errors.py", line 164, in __call__
    await self.app(scope, receive, _send)
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\gradio\route_utils.py", line 761, in __call__
    await self.app(scope, receive, send)
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\starlette\middleware\exceptions.py", line 63, in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\starlette\_exception_handler.py", line 53, in wrapped_app
    raise exc
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\starlette\_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\fastapi\middleware\asyncexitstack.py", line 18, in __call__
    await self.app(scope, receive, send)
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\starlette\routing.py", line 660, in __call__
    await self.middleware_stack(scope, receive, send)
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\starlette\routing.py", line 680, in app
    await route.handle(scope, receive, send)
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\starlette\routing.py", line 276, in handle
    await self.app(scope, receive, send)
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\fastapi\routing.py", line 134, in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\starlette\_exception_handler.py", line 53, in wrapped_app
    raise exc
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\starlette\_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\fastapi\routing.py", line 120, in app
    response = await f(request)
               ^^^^^^^^^^^^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\fastapi\routing.py", line 674, in app
    raw_response = await run_endpoint_function(
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\fastapi\routing.py", line 330, in run_endpoint_function
    return await run_in_threadpool(dependant.call, **values)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\starlette\concurrency.py", line 32, in run_in_threadpool
    return await anyio.to_thread.run_sync(func)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\anyio\to_thread.py", line 63, in run_sync
    return await get_async_backend().run_sync_in_worker_thread(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\anyio\_backends\_asyncio.py", line 2518, in run_sync_in_worker_thread
    return await future
           ^^^^^^^^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\anyio\_backends\_asyncio.py", line 1002, in run
    result = context.run(func, *args)
             ^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\gradio\routes.py", line 432, in main
    return templates.TemplateResponse(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\starlette\templating.py", line 148, in TemplateResponse
    template = self.get_template(name)
               ^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\starlette\templating.py", line 115, in get_template
    return self.env.get_template(name)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\jinja2\environment.py", line 1016, in get_template
    return self._load_template(name, globals)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\jinja2\environment.py", line 964, in _load_template
    template = self.cache.get(cache_key)
               ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\jinja2\utils.py", line 477, in get
    return self[key]
           ~~~~^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\jinja2\utils.py", line 515, in __getitem__
    rv = self._mapping[key]
         ~~~~~~~~~~~~~^^^^^
TypeError: unhashable type: 'dict'
ERROR:    Exception in ASGI application
Traceback (most recent call last):
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\uvicorn\protocols\http\h11_impl.py", line 415, in run_asgi
    result = await app(  # type: ignore[func-returns-value]
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\uvicorn\middleware\proxy_headers.py", line 60, in __call__
    return await self.app(scope, receive, send)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\fastapi\applications.py", line 1159, in __call__
    await super().__call__(scope, receive, send)
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\starlette\applications.py", line 90, in __call__
    await self.middleware_stack(scope, receive, send)
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\starlette\middleware\errors.py", line 186, in __call__
    raise exc
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\starlette\middleware\errors.py", line 164, in __call__
    await self.app(scope, receive, _send)
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\gradio\route_utils.py", line 761, in __call__
    await self.app(scope, receive, send)
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\starlette\middleware\exceptions.py", line 63, in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\starlette\_exception_handler.py", line 53, in wrapped_app
    raise exc
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\starlette\_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\fastapi\middleware\asyncexitstack.py", line 18, in __call__
    await self.app(scope, receive, send)
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\starlette\routing.py", line 660, in __call__
    await self.middleware_stack(scope, receive, send)
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\starlette\routing.py", line 680, in app
    await route.handle(scope, receive, send)
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\starlette\routing.py", line 276, in handle
    await self.app(scope, receive, send)
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\fastapi\routing.py", line 134, in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\starlette\_exception_handler.py", line 53, in wrapped_app
    raise exc
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\starlette\_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\fastapi\routing.py", line 120, in app
    response = await f(request)
               ^^^^^^^^^^^^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\fastapi\routing.py", line 674, in app
    raw_response = await run_endpoint_function(
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\fastapi\routing.py", line 330, in run_endpoint_function
    return await run_in_threadpool(dependant.call, **values)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\starlette\concurrency.py", line 32, in run_in_threadpool
    return await anyio.to_thread.run_sync(func)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\anyio\to_thread.py", line 63, in run_sync
    return await get_async_backend().run_sync_in_worker_thread(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\anyio\_backends\_asyncio.py", line 2518, in run_sync_in_worker_thread
    return await future
           ^^^^^^^^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\anyio\_backends\_asyncio.py", line 1002, in run
    result = context.run(func, *args)
             ^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\gradio\routes.py", line 432, in main
    return templates.TemplateResponse(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\starlette\templating.py", line 148, in TemplateResponse
    template = self.get_template(name)
               ^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\starlette\templating.py", line 115, in get_template
    return self.env.get_template(name)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\jinja2\environment.py", line 1016, in get_template
    return self._load_template(name, globals)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\jinja2\environment.py", line 964, in _load_template
    template = self.cache.get(cache_key)
               ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\jinja2\utils.py", line 477, in get
    return self[key]
           ~~~~^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\jinja2\utils.py", line 515, in __getitem__
    rv = self._mapping[key]
         ~~~~~~~~~~~~~^^^^^
TypeError: unhashable type: 'dict'
ERROR:    Exception in ASGI application
Traceback (most recent call last):
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\uvicorn\protocols\http\h11_impl.py", line 415, in run_asgi
    result = await app(  # type: ignore[func-returns-value]
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\uvicorn\middleware\proxy_headers.py", line 60, in __call__
    return await self.app(scope, receive, send)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\fastapi\applications.py", line 1159, in __call__
    await super().__call__(scope, receive, send)
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\starlette\applications.py", line 90, in __call__
    await self.middleware_stack(scope, receive, send)
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\starlette\middleware\errors.py", line 186, in __call__
    raise exc
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\starlette\middleware\errors.py", line 164, in __call__
    await self.app(scope, receive, _send)
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\gradio\route_utils.py", line 761, in __call__
    await self.app(scope, receive, send)
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\starlette\middleware\exceptions.py", line 63, in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\starlette\_exception_handler.py", line 53, in wrapped_app
    raise exc
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\starlette\_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\fastapi\middleware\asyncexitstack.py", line 18, in __call__
    await self.app(scope, receive, send)
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\starlette\routing.py", line 660, in __call__
    await self.middleware_stack(scope, receive, send)
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\starlette\routing.py", line 680, in app
    await route.handle(scope, receive, send)
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\starlette\routing.py", line 276, in handle
    await self.app(scope, receive, send)
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\fastapi\routing.py", line 134, in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\starlette\_exception_handler.py", line 53, in wrapped_app
    raise exc
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\starlette\_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\fastapi\routing.py", line 120, in app
    response = await f(request)
               ^^^^^^^^^^^^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\fastapi\routing.py", line 674, in app
    raw_response = await run_endpoint_function(
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\fastapi\routing.py", line 330, in run_endpoint_function
    return await run_in_threadpool(dependant.call, **values)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\starlette\concurrency.py", line 32, in run_in_threadpool
    return await anyio.to_thread.run_sync(func)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\anyio\to_thread.py", line 63, in run_sync
    return await get_async_backend().run_sync_in_worker_thread(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\anyio\_backends\_asyncio.py", line 2518, in run_sync_in_worker_thread
    return await future
           ^^^^^^^^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\anyio\_backends\_asyncio.py", line 1002, in run
    result = context.run(func, *args)
             ^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\gradio\routes.py", line 432, in main
    return templates.TemplateResponse(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\starlette\templating.py", line 148, in TemplateResponse
    template = self.get_template(name)
               ^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\starlette\templating.py", line 115, in get_template
    return self.env.get_template(name)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\jinja2\environment.py", line 1016, in get_template
    return self._load_template(name, globals)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\jinja2\environment.py", line 964, in _load_template
    template = self.cache.get(cache_key)
               ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\jinja2\utils.py", line 477, in get
    return self[key]
           ~~~~^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\jinja2\utils.py", line 515, in __getitem__
    rv = self._mapping[key]
         ~~~~~~~~~~~~~^^^^^
TypeError: unhashable type: 'dict'
ERROR:    Exception in ASGI application
Traceback (most recent call last):
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\uvicorn\protocols\http\h11_impl.py", line 415, in run_asgi
    result = await app(  # type: ignore[func-returns-value]
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\uvicorn\middleware\proxy_headers.py", line 60, in __call__
    return await self.app(scope, receive, send)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\fastapi\applications.py", line 1159, in __call__
    await super().__call__(scope, receive, send)
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\starlette\applications.py", line 90, in __call__
    await self.middleware_stack(scope, receive, send)
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\starlette\middleware\errors.py", line 186, in __call__
    raise exc
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\starlette\middleware\errors.py", line 164, in __call__
    await self.app(scope, receive, _send)
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\gradio\route_utils.py", line 761, in __call__
    await self.app(scope, receive, send)
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\starlette\middleware\exceptions.py", line 63, in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\starlette\_exception_handler.py", line 53, in wrapped_app
    raise exc
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\starlette\_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\fastapi\middleware\asyncexitstack.py", line 18, in __call__
    await self.app(scope, receive, send)
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\starlette\routing.py", line 660, in __call__
    await self.middleware_stack(scope, receive, send)
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\starlette\routing.py", line 680, in app
    await route.handle(scope, receive, send)
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\starlette\routing.py", line 276, in handle
    await self.app(scope, receive, send)
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\fastapi\routing.py", line 134, in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\starlette\_exception_handler.py", line 53, in wrapped_app
    raise exc
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\starlette\_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\fastapi\routing.py", line 120, in app
    response = await f(request)
               ^^^^^^^^^^^^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\fastapi\routing.py", line 674, in app
    raw_response = await run_endpoint_function(
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\fastapi\routing.py", line 330, in run_endpoint_function
    return await run_in_threadpool(dependant.call, **values)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\starlette\concurrency.py", line 32, in run_in_threadpool
    return await anyio.to_thread.run_sync(func)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\anyio\to_thread.py", line 63, in run_sync
    return await get_async_backend().run_sync_in_worker_thread(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\anyio\_backends\_asyncio.py", line 2518, in run_sync_in_worker_thread
    return await future
           ^^^^^^^^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\anyio\_backends\_asyncio.py", line 1002, in run
    result = context.run(func, *args)
             ^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\gradio\routes.py", line 432, in main
    return templates.TemplateResponse(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\starlette\templating.py", line 148, in TemplateResponse
    template = self.get_template(name)
               ^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\starlette\templating.py", line 115, in get_template
    return self.env.get_template(name)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\jinja2\environment.py", line 1016, in get_template
    return self._load_template(name, globals)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\jinja2\environment.py", line 964, in _load_template
    template = self.cache.get(cache_key)
               ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\jinja2\utils.py", line 477, in get
    return self[key]
           ~~~~^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\jinja2\utils.py", line 515, in __getitem__
    rv = self._mapping[key]
         ~~~~~~~~~~~~~^^^^^
TypeError: unhashable type: 'dict'
ERROR:    Exception in ASGI application
Traceback (most recent call last):
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\uvicorn\protocols\http\h11_impl.py", line 415, in run_asgi
    result = await app(  # type: ignore[func-returns-value]
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\uvicorn\middleware\proxy_headers.py", line 60, in __call__
    return await self.app(scope, receive, send)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\fastapi\applications.py", line 1159, in __call__
    await super().__call__(scope, receive, send)
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\starlette\applications.py", line 90, in __call__
    await self.middleware_stack(scope, receive, send)
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\starlette\middleware\errors.py", line 186, in __call__
    raise exc
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\starlette\middleware\errors.py", line 164, in __call__
    await self.app(scope, receive, _send)
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\gradio\route_utils.py", line 761, in __call__
    await self.app(scope, receive, send)
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\starlette\middleware\exceptions.py", line 63, in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\starlette\_exception_handler.py", line 53, in wrapped_app
    raise exc
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\starlette\_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\fastapi\middleware\asyncexitstack.py", line 18, in __call__
    await self.app(scope, receive, send)
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\starlette\routing.py", line 660, in __call__
    await self.middleware_stack(scope, receive, send)
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\starlette\routing.py", line 680, in app
    await route.handle(scope, receive, send)
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\starlette\routing.py", line 276, in handle
    await self.app(scope, receive, send)
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\fastapi\routing.py", line 134, in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\starlette\_exception_handler.py", line 53, in wrapped_app
    raise exc
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\starlette\_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\fastapi\routing.py", line 120, in app
    response = await f(request)
               ^^^^^^^^^^^^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\fastapi\routing.py", line 674, in app
    raw_response = await run_endpoint_function(
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\fastapi\routing.py", line 330, in run_endpoint_function
    return await run_in_threadpool(dependant.call, **values)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\starlette\concurrency.py", line 32, in run_in_threadpool
    return await anyio.to_thread.run_sync(func)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\anyio\to_thread.py", line 63, in run_sync
    return await get_async_backend().run_sync_in_worker_thread(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\anyio\_backends\_asyncio.py", line 2518, in run_sync_in_worker_thread
    return await future
           ^^^^^^^^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\anyio\_backends\_asyncio.py", line 1002, in run
    result = context.run(func, *args)
             ^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\gradio\routes.py", line 432, in main
    return templates.TemplateResponse(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\starlette\templating.py", line 148, in TemplateResponse
    template = self.get_template(name)
               ^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\starlette\templating.py", line 115, in get_template
    return self.env.get_template(name)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\jinja2\environment.py", line 1016, in get_template
    return self._load_template(name, globals)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\jinja2\environment.py", line 964, in _load_template
    template = self.cache.get(cache_key)
               ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\jinja2\utils.py", line 477, in get
    return self[key]
           ~~~~^^^^^
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\jinja2\utils.py", line 515, in __getitem__
    rv = self._mapping[key]
         ~~~~~~~~~~~~~^^^^^
TypeError: unhashable type: 'dict'
Traceback (most recent call last):
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\application\app.py", line 599, in <module>
    demo.launch(
  File "C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch\.venv\Lib\site-packages\gradio\blocks.py", line 2465, in launch
    raise ValueError(
ValueError: When localhost is not accessible, a shareable link must be created. Please set share=True or check your proxy settings to allow access to localhost.
(.venv) (base) PS C:\Users\jkhan\Documents\Professional Development\AI Engineering and Implementation\PROJECTS\proj_NLtodtSearch>