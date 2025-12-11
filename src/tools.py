from exa_py import Exa
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import os


class SearchInput(BaseModel):
    """Input for search tool."""
    query: str = Field(..., description="Search query")


class FindSimilarInput(BaseModel):
    """Input for find similar tool."""
    url: str = Field(..., description="URL to find similar pages")


class GetContentsInput(BaseModel):
    """Input for get contents tool."""
    ids: str = Field(..., description="List of IDs as string")


class SearchTool(BaseTool):
    name: str = "search"
    description: str = "Search for a webpage based on the query."
    args_schema: Type[BaseModel] = SearchInput

    def _run(self, query: str) -> str:
        exa = Exa(api_key=os.environ.get("EXA_API_KEY"))
        return exa.search(f"{query}", use_autoprompt=True, num_results=3)


class FindSimilarTool(BaseTool):
    name: str = "find_similar"
    description: str = "Search for webpages similar to a given URL. The url passed in should be a URL returned from search."
    args_schema: Type[BaseModel] = FindSimilarInput

    def _run(self, url: str) -> str:
        exa = Exa(api_key=os.environ.get("EXA_API_KEY"))
        return exa.find_similar(url, num_results=3)


class GetContentsTool(BaseTool):
    name: str = "get_contents"
    description: str = "Get the contents of a webpage. The ids must be passed in as a list, a list of ids returned from search."
    args_schema: Type[BaseModel] = GetContentsInput

    def _run(self, ids: str) -> str:
        exa = Exa(api_key=os.environ.get("EXA_API_KEY"))
        ids = eval(ids)
        contents = str(exa.get_contents(ids))
        contents = contents.split("URL:")
        contents = [content[:1000] for content in contents]
        return "\n\n".join(contents)


class ExaSearchToolset():
    @staticmethod
    def tools():
        return [
            SearchTool(),
            FindSimilarTool(),
            GetContentsTool()
        ]
    
    