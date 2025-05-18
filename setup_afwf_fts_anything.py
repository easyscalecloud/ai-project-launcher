# -*- coding: utf-8 -*-

from ai_project_launcher import (
    dir_here,
    parse_claude_project_html,
    parse_chatgpt_project_html,
    claude_project_fts_settings,
    chatgpt_project_fts_settings,
    setup_afwf_fts_anything,
)

path_claude_icon = dir_here / "icon" / "claude-icon.png"
path_chatgpt_icon = dir_here / "icon" / "chatgpt-icon.png"

path_claude_project_sh = dir_here / "html" / "claude_project_sh.html"
path_claude_project_esc = dir_here / "html" / "claude_project_esc.html"
path_chatgpt_project_sh = dir_here / "html" / "chatgpt_project_sh.html"


def setup_claude_sh():
    """
    Personal Claude Account.
    """
    setup_afwf_fts_anything(
        fts_data=[
            project.to_dict()
            for project in parse_claude_project_html(path_claude_project_sh.read_text())
        ],
        fts_settings=claude_project_fts_settings,
        path_icon=path_claude_icon,
        dataset_name="ClaudeProjectSh",
    )


def setup_claude_esc():
    """
    EasyScaleCloud Work Claude Account.
    """
    setup_afwf_fts_anything(
        fts_data=[
            project.to_dict()
            for project in parse_claude_project_html(
                path_claude_project_esc.read_text()
            )
        ],
        fts_settings=claude_project_fts_settings,
        path_icon=path_claude_icon,
        dataset_name="ClaudeProjectEsc",
    )


def setup_chatgpt_sh():
    """
    Personal ChatGPT Account.
    """
    setup_afwf_fts_anything(
        fts_data=[
            project.to_dict()
            for project in parse_chatgpt_project_html(
                path_chatgpt_project_sh.read_text()
            )
        ],
        fts_settings=chatgpt_project_fts_settings,
        path_icon=path_chatgpt_icon,
        dataset_name="ChatGPTProjectSh",
    )


setup_claude_sh()  # personal claude
setup_claude_esc()  # esc work claude
setup_chatgpt_sh()  # personal chatgpt
