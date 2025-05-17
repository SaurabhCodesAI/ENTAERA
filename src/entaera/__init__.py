"""
ENTAERA: Kata-driven AI research agent package
"""

__version__ = "0.1.0"
__author__ = "ENTAERA Team"
__email__ = "team@entaera.com"

# Package metadata
__title__ = "entaera"
__description__ = "A kata-driven AI research agent with intelligent provider routing"
__url__ = "https://github.com/yourusername/ENTAERA-Kata"
__license__ = "MIT"

# Version info
__version_info__ = tuple(map(int, __version__.split(".")))

# Public API exports
# Import core functionality if available
__all__ = [
    "__version__",
    "__version_info__",
]

# Conditionally import core modules
try:
    from entaera.core.config import get_settings
    __all__.append("get_settings")
except ImportError:
    pass

try:
    from entaera.core.logger import get_logger
    __all__.append("get_logger")
except ImportError:
    pass
