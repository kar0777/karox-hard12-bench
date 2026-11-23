You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Redis binary message parsing loses payload and headers with Unicode header values

### Description

The default Redis binary message format loses the payload and headers when a header contains a non-ASCII value. For an ASCII key such as `city` with value `Z\u00fcrich`, encoding succeeds, but parsing returns the entire binary envelope as the body and an empty headers dictionary.

This can break typed consumers and removes content-type and correlation metadata from otherwise valid messages. I assess the functional impact as medium; this is not a maintainer-assigned severity.

### Reproduction

```python
import asyncio
from faststream.redis.parser import BinaryMessageFormatV1

async def main():
    raw = await BinaryMessageFormatV1.encode(
        message="hello",
        headers={"city": "Z\u00fcrich"},
        correlation_id="id",
        reply_to=None,
    )
    print(BinaryMessageFormatV1.parse(raw))

asyncio.run(main())
```

Expected: body `b'hello'` and headers containing correlation_id `id`, content-type `text/plain`, and city `Z\u00fcrich`.

Actual: the body contains the binary envelope and headers are `{}`. Reproduced on main at `4047adcc2d40605d4ddb458094c9b89e79ae4da1`.

`BinaryWriter.write_string` prefixes the Unicode character count but writes UTF-8 bytes. The reader interprets that prefix as a byte count. Encoding before measuring the length resolves the mismatch. CJK and emoji values reproduce it too; ASCII values work.

AI assistance: OpenAI Codex (GPT-6) assisted investigation, implementation, and testing. A fix with regression tests is being prepared.

