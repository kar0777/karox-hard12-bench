You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

`SearchableToolset` cannot find a tool by a word from its snake_case name

### Describe the bug
`SearchableToolset`'s `search_tools` cannot find a tool by a word from its snake_case name. Searching `weather` returns nothing for a tool named `get_weather`, unless its description also contains `weather`. The tool's own instructions to the model ask for exactly that kind of keyword: "Space-separated words from tool names/descriptions (e.g. 'route weather search')" (`haystack/tools/searchable_toolset.py:275`, and again at line 283).

### Error message
No exception. `search_tools` returns "No tools found matching these keywords. Try different keywords."

### Expected behavior
`weather` finds `get_weather` and `email` finds `send_email`.

### Additional context
The index text is `f"{tool.name} {tool.description}"` (line 204). The default BM25 tokenizer counts `_` as a word character, so `get_weather` stays one token.

Not checked: camelCase and kebab-case names.

### To Reproduce

```python
from haystack.tools import Tool, SearchableToolset

def make(name, description):
    return Tool(name=name, description=description, parameters={"type": "object", "properties": {}}, function=lambda: "ok")

catalog = [
    make("get_weather", "Current conditions for a city."),
    make("send_email", "Deliver a message to a recipient."),
    make("book_flight", "Reserve an airline seat."),
]
toolset = SearchableToolset(catalog=catalog, search_threshold=2)
search_tools = next(iter(toolset))
for keywords in ["weather", "email", "get_weather", "city"]:
    print(f"{keywords!r}: {search_tools.invoke(tool_keywords=keywords)}")
```

```
$ python repro.py
'weather': No tools found matching these keywords. Try different keywords.
'email': No tools found matching these keywords. Try different keywords.
'get_weather': Found and loaded 1 tool(s): get_weather. Use them directly as tools.
'city': Found and loaded 1 tool(s): get_weather. Use them directly as tools.
```

### FAQ Check
- [x] Have you had a look at [our new FAQ page](https://docs.haystack.deepset.ai/docs/faq)?

### System:
- OS: macOS 26.7.2
- Haystack version: `main` at `0ad7474` (3.5.0-rc0), Python 3.12.12

Would you take a fix that also indexes the name split on `_`?

