# from config.django.base import SERVER_ENV
import logging
import os
from config.settings import BASE_DIR

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
    },
    "formatters": {
        "django.server": {
            "format": "[%(asctime)s] %(levelname)s [PID: %(process)d - %(processName)s] | [TID: %(thread)d - %(threadName)s] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        # "console": {
        #     "level": "DEBUG",
        #     "class": "logging.StreamHandler",
        #     "filters": ["require_debug_true"],
        #     "formatter": "django.server",
        # },
        "file": {
            "level": "INFO",
            "filters": ["require_debug_true"],
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(BASE_DIR, 'log', 'app.log'),
            "maxBytes": 1024 * 1024 * 10,  # 10 MB
            "backupCount": 5,
            "formatter": "django.server",
            "encoding": "utf-8",
        },
    },
}


# if SERVER_ENV == "config.django.local":
#     LOGGING["loggers"] = {
#         "django.db.backends": {
#             "handlers": ["console"],
#             "level": "DEBUG",
#             "propagate": False,
#         },
#     }
# else:
#     LOGGING["loggers"] = {
#         "django": {
#             "handlers": ["file"],
#             "level": "INFO",
#             "propagate": False,
#         },
#     }

LOGGING["loggers"] = {
    "django": {
        "handlers": ["file"],
        "level": "INFO",
        "propagate": False,
    },
}

logger = logging.getLogger("django")
