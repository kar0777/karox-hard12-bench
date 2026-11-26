You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Enable override default type of selector to use on xpath method

## Summary

When calls `response.xpath` scrapy automatically chooses the "best parsing rules" but looking from the code of **parsel** it always try to parse using `html` parse even with xml documents. I would like that user could pass the type on method call, like: `response.xpath("xpath", type='xml')`

## Motivation

I have a response that **Content-Type** is `application/xhtml+xml;charset=iso-8859-1`, but body itself is a xml document, but scrapy consider `html` the best parsing rule type, because when i try to parse `CDATA` a get empty values.

## Describe alternatives you've considered

I using `seletor = Selector(text=response.text, type='xml')` to parse my data.

## Additional context

Here a proof-of-concept that i made:

```python
from parsel import Selector

xml_doc = """
<?xml version='1.0' encoding='iso-8859-1'?>
<rows>
    <page>1</page>
    <total>1</total>
    <records>1</records>
    <row id="1">
        <cell><![CDATA[Scrapy]]></cell>
        <cell><![CDATA[https://scrapy.org/]]></cell>
        <cell><![CDATA[Python]]></cell>
    </row>
</rows>
"""

seletor = Selector(text=xml_doc)

print(seletor.xpath("//cell[1]/text()").get())  # None

seletor = Selector(text=xml_doc, type='xml')

print(seletor.xpath("//cell[1]/text()").get())  # Scrapy
```
