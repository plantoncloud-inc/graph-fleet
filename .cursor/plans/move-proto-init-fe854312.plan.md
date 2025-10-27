<!-- fe854312-9306-4ed2-a426-a11d66635707 3c3f8551-9dfa-4966-a3e0-4c3c1fd7d20e -->
# Move Proto Schema Initialization to Application Startup

## Problem

Currently, proto schema files are fetched via Git clone on the first user request (when LLM calls `initialize_proto_schema` tool), causing significant delays. The user sees a "hang" when typing their first message.

## Solution

Move the initialization logic to **module-level code** that executes when the LangGraph server imports the graph module at