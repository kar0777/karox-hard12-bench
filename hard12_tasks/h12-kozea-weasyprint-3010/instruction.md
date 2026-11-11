You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Crop marks are covered by elements in the page margin

## Expected Behavior

Crop marks should be visible, even when artwork bleeds into the page margin.

## Actual Behavior

You cannot see the crop marks because the artwork is layered on top of them.

## Suggested Fix

Move the crop marks out of the [`draw_background()` function](https://github.com/Kozea/WeasyPrint/blob/main/weasyprint/draw/__init__.py#L285). Do it as the last draw of the page, so that the marks are on top of any artwork.

## Example Document

Save the file below as `example.html`, then run `weasyprint example.html example.pdf`.

**example.html**

```html
<style>
    @page {
        bleed: 0.125in;
        margin: 0.5in;
        size: 8.5in 5.5in;
        marks: crop;

        @top-center {
            background: #ccc;
            content: element(header);
            margin-top: -0.125in;
            width: calc(8.5in + 0.25in);
        }

        @bottom-center {
            background: #999;
            content: element(footer);
            margin-bottom: -0.125in;
            width: calc(8.5in + 0.25in);
        }
    }

    header {
        position: running(header);
        text-align: center;
    }

    footer {
        position: running(footer);
        text-align: center;
    }
</style>
<div class="page">
    <header>HEADER</header>
    <main>
        Hello, world!
    </main>
    <footer>FOOTER</footer>
</div>
```

**[example.pdf](https://github.com/user-attachments/files/34338012/example.pdf)**

<img width="1297" height="993" alt="Image" src="https://github.com/user-attachments/assets/54e2a322-68ab-4c2f-940c-f1002cce7b81" />
