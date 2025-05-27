from .auth import setup_auth_handlers
from .schedule import setup_schedule_handlers
from .grades import setup_grades_handlers
from .news import setup_news_handlers
from .feedback import setup_feedback_handlers
from .logout import setup_logout_handler

__all__ = [
    'setup_auth_handlers',
    'setup_schedule_handlers',
    'setup_grades_handlers',
    'setup_news_handlers',
    'setup_feedback_handlers',
    'setup_logout_handler'
]