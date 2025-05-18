# -*- coding: utf-8 -*-

"""
This library extracts metadata such as project name, description, and URL
from HTML pages of Claude Projects and ChatGPT Projects.

It was developed to support power users who manage a large number of AI projects
and need an efficient way to search, organize, and launch them. The extracted data
can be used with Alfred workflows (e.g., afwf_fts_anything), browser bookmarks,
or curated project catalogs to improve navigation and productivity.
"""

import typing as T
import json
import shutil
import dataclasses
from pathlib import Path

from bs4 import BeautifulSoup

dir_home = Path.home()
dir_afwf_fts = dir_home / ".alfred-afwf" / "afwf_fts_anything"
dir_here = Path(__file__).absolute().parent


@dataclasses.dataclass
class Base:
    def to_dict(self) -> dict[str, T.Any]:
        return dataclasses.asdict(self)


T_Base = T.TypeVar("T_Base", bound=Base)


@dataclasses.dataclass
class ClaudeProject(Base):
    """Represents a Claude Project with URL, name, and description."""

    url: str
    name: str
    description: str


@dataclasses.dataclass
class ChatGPTProject(Base):
    """Represents a ChatGPT Project with URL and name."""

    url: str
    name: str


def parse_claude_project_html(html: str) -> T.List[ClaudeProject]:
    """
    Parse Claude project HTML content and extract metadata.

    :param html: Raw HTML string from the Claude project page.

    :return: A list of :class:`ClaudeProject`
    """
    projects = list()
    soup = BeautifulSoup(html, features="html.parser")
    for a in soup.find_all("a"):
        if "href" not in a.attrs:
            continue
        href = a.attrs["href"]
        if href.startswith("/project/"):
            url = f"https://claude.ai{href}"
            # look for:
            # <div class="truncate">Claude Project Name Here </div>
            div = a.find("div", class_="truncate")
            name = div.text
            # look for:
            # <div class="text-text-300 mt-1 line-clamp-3 text-sm flex-grow">Claude Project Description Here</div>
            div = a.find("div", class_="text-text-300")
            description = div.text
            print(f"---------- {name = }")
            print(f"{description[:120] = }")
            print(f"{url = }")
            claude_project = ClaudeProject(name=name, description=description, url=url)
            projects.append(claude_project)
    return projects


def parse_chatgpt_project_html(html: str) -> T.List[ChatGPTProject]:
    """
    Parse ChatGPT project HTML content and extract metadata.

    :param html: Raw HTML string from the ChatGPT project page.

    :return: A list of :class:`ChatGPTProject`
    """
    projects = list()
    soup = BeautifulSoup(html, features="html.parser")
    for a in soup.find_all("a"):
        if "href" not in a.attrs:
            continue
        href = a.attrs["href"]
        if href.startswith("/g/g-p"):
            name = a.attrs["title"]
            # Convert to unique url (without project name slug)
            prefix = "-".join(href.split("-")[:3])
            url = f"https://chatgpt.com{prefix}/project"
            print(f"---------- {name = }")
            print(f"{url = }")
            project = ChatGPTProject(name=name, url=url)
            projects.append(project)
    return projects


def get_base_fts_settings() -> dict:
    """
    Define base full-text search settings used by
    `afwf_fts_anything <https://github.com/MacHu-GWU/afwf_fts_anything-project>`_.
    """
    return {
        "fields": [
            {
                "name": "name",
                "type_is_store": True,
                "type_is_ngram_words": True,
                "ngram_maxsize": 10,
                "ngram_minsize": 2,
                "weight": 5.0,
            },
            {
                "name": "url",
                "type_is_store": True,
            },
        ],
        "title_field": "{name}",
        "arg_field": "{url}",
        "autocomplete_field": "{name}",
    }


claude_project_fts_settings = get_base_fts_settings()
claude_project_fts_settings["fields"].append(
    {
        "name": "description",
        "type_is_store": True,
        "type_is_phrase": True,
        "weight": 1.0,
    },
)
claude_project_fts_settings["subtitle_field"] = "{description}"

chatgpt_project_fts_settings = get_base_fts_settings()
claude_project_fts_settings["subtitle_field"] = "{url}"


def setup_afwf_fts_anything(
    fts_data: list[dict],
    fts_settings: dict[str, T.Any],
    path_icon: Path,
    dataset_name: str,
):
    """
    Install full-text search data and settings into Alfred’s
    `afwf_fts_anything <https://github.com/MacHu-GWU/afwf_fts_anything-project>`_
    plugin.

    This function writes the FTS data and settings to the Alfred plugin directory,
    copies the icon, and resets the search index and cache so that the dataset
    is immediately searchable in Alfred.
    """
    fts_settings["icon_field"] = path_icon.name

    # write {dataset_name}-data.json
    path_data = dir_afwf_fts.joinpath(f"{dataset_name}-data.json")
    path_data.write_text(json.dumps(fts_data, indent=4))
    # write {dataset_name}-setting.json
    path_settings = dir_afwf_fts.joinpath(f"{dataset_name}-setting.json")
    path_settings.write_text(json.dumps(fts_settings, indent=4))
    # create {dataset_name}-icon.json
    dir_icon = dir_afwf_fts.joinpath(f"{dataset_name}-icon")
    dir_icon.mkdir(parents=True, exist_ok=True)
    path_icon_dst = dir_icon.joinpath(path_icon.name)
    path_icon_dst.write_bytes(path_icon.read_bytes())
    # reset index and cache
    dir_index = dir_afwf_fts.joinpath(f"{dataset_name}-whoosh_index")
    shutil.rmtree(dir_index, ignore_errors=True)
    dir_cache = dir_afwf_fts.joinpath(".cache")
    shutil.rmtree(dir_cache, ignore_errors=True)
