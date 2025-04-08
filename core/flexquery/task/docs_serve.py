
from flexquery.utils.docs_browser import DocsGenerator
from flexquery.task.base import Task
from flexquery.config.exceptions import TaskExecutionError
from flexquery.config.logging_config import get_logger
import webbrowser
import os
from pathlib import Path

logger = get_logger(__name__)


class Browser:
    """Opens files and URLs in Microsoft Edge (on Windows) or default browser."""
    
    def __init__(self):
        pass


    def open(self, path_or_url):
        """Open a file or URL in  default browser."""

        path_or_url = str(path_or_url)
        
        # Convert file path to URL if needed
        if os.path.isfile(path_or_url):
            path_or_url = Path(path_or_url).absolute().as_uri()
            logger.debug(f"URI: {path_or_url}")
            try:
                result = webbrowser.open(path_or_url)
                if result:
                    return True
            except Exception as e:
                raise TaskExecutionError(f"webbrowser.open() failed: {e}")


class DocsServeTask(Task):
    """Task for opening documentation in the browser."""
    
    def __init__(self, docs_path=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.docs_path = docs_path
        self._browser = None
        self._docs_generator = None
        
    def validate(self):
        """Validate the browser task."""
        return True

    def setup(self):
        """Setup the browser task."""
        self._browser = Browser()
        self._generator = DocsGenerator()
        return True
        
    def _execute(self):
        """Execute the browser task."""
        docs_path = self.docs_path or self._generator.generate_docs()
        success = self._browser.open(docs_path)
        return success
    
    def cleanup(self):
        """Cleanup the browser task."""
        pass