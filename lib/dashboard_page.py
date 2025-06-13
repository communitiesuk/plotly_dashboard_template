"""DashboardPage"""

from dataclasses import dataclass
from typing import Callable
from lib.url import selected_filters


@dataclass
class DashboardPage:
    """A class for storing information about each dashboard page
    Used for creating navbar links and displaying the page"""

    title: str
    pathname: str
    filters: list[str]
    function_to_call: Callable
    protective_marking: str = "OFFICIAL"
    hide_from_menu: bool = False

    def display_dashboard(self, query_string):
        """Return the dashboad using the given query string"""
        return self.function_to_call(**self.__dashboard_argument_values(query_string))

    def __dashboard_argument_values(self, url):
        """Assigns required arguments for each dashboard"""

        return {x: selected_filters(url).get(x) for x in self.filters}
