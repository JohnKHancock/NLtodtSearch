## The Natural Language to dtSearch Application

## Overview
The goal of this project is to create a simple application called NL-to-dtSearch that takes in a natural language query or statement and transforms it into a dtSearch query. This app can be used to search document corpuses that have been indexed by a dtSearch indexing application. The app will not
run the search itself. Rather, it serves in an advisory capacity by suggesting formatting and queries. 

## Project Specifications

1. Users log into the app using the Gradio auth mechanism.
2. After a successful sign in, they are greeted with flash message welcoming the user by name to the NL-to-dtSearch.
3. The welcoming message should give the user the option of a quick tour of the interface.
4. The UI should be in three columns. 
5. The left column is a list of historical chat sessions which can be retrived .
6. The center column is where the user interacts with the LLM/agent, submit queries, download history, load history, and upload documents.
7. The right column should consist of the following:
        - The dtSearch query itself (formatted, easy to copy)
        - A brief explanation of what the query does
        - Alternative queries (e.g., fuzzy, wildcard, phrase variants)
        - A confidence indicator
8. The user can upload a document (e.g. a subpoena) and the LLM/agent can review it and provide a list of suggested search terms.
9. The LLM's response appears word-by-word (or chunk-by-chunk) in real time as it's generated.  
10. The document-upload flow should be integrated into the main chat

## Technology Stack
1. For this demo, use Gradio for the UI. The next iteration will be web based.
2. Use Anthropic Claude API
3. The session history should be stored in a SQLite database
4. See the CODE_REVIEW.md in the .\pre-planning folder for additional technical specifications
