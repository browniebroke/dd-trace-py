from ....utils.importlib import require_modules

required_modules = ['django']

with require_modules(required_modules) as missing_modules:
    if not missing_modules:
        from .middleware import TraceMiddleware, TraceExceptionMiddleware
        from .patch import patch
        __all__ = ['TraceMiddleware', 'TraceExceptionMiddleware', 'patch']

