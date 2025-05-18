AI Project Launcher
==============================================================================
.. image:: ./img/cover.png


AI Project Launcher is a productivity tool for power users who manage numerous Claude and ChatGPT projects. It extracts project metadata from HTML and integrates with Alfred's workflow capabilities to provide lightning-fast, keyboard-driven access to all your AI assistants. With just a few keystrokes, instantly search across hundreds of projects using powerful full-text search—bypassing the slow, imprecise browser-based navigation.

The implementation requires minimal setup: extract HTML from your project pages, run the Python script to build the search index, and configure the Alfred workflow. Maintenance is straightforward, requiring just a minute to refresh your project catalog whenever you create new AI assistants. The codebase is clean, well-documented, and handles both Claude and ChatGPT projects.

For a comprehensive step-by-step guide on setting up your own AI Project Launcher, visit our [detailed blog post on EasyScaleCloud](./blog.md). The blog covers the complete workflow, screenshots of the setup process, and explains how this tool transforms the way you interact with specialized AI assistants.


Installation
------------------------------------------------------------------------------
.. code-block:: bash

    git clone https://github.com/easyscalecloud/ai-project-launcher.git
    cd ai-project-launcher
    pip install -r requirements.txt


Usage
------------------------------------------------------------------------------
1. Copy the HTML from your Claude or ChatGPT projects page and save it to the ``html/`` directory
2. Run ``python setup_afwf_fts_anything.py`` to build your search index
3. Configure Alfred workflow following the instructions in the blog post
4. Start searching your projects with lightning speed!


Requirements
------------------------------------------------------------------------------
- macOS with Alfred installed (Alfred Powerpack required)
- Python 3.9+
- `afwf_fts_anything <https://github.com/MacHu-GWU/afwf_fts_anything-project>`_ workflow for Alfred
