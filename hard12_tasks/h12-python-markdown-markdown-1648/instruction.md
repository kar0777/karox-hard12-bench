You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

HTML comment inside inline raw HTML creates malformed output

Originally mis-filed against Zensical as zensical/zensical#981. @squidfunk [graciously deduced](https://github.com/zensical/zensical/issues/981#issuecomment-5865544666) this project as the root cause. The [repro repo](https://github.com/posita/zensical-picture-repro/) illustrates via Zensical, but let me know if I should provide a more compact version that doesn't rely on that as the vehicle.

### Context

Discovered while investigating zensical/zensical#975.

### Bug description

This (in `docs/symptom.md`) ...

```md
<picture>
  <!-- TODO(@posita): https://github.com/zensical/zensical/issues/975 - What the heck? 👉 -->
  <source media="(prefers-color-scheme: dark)" srcset="../images/example.svg">
  <img alt="Example" src="../images/example.svg">
</picture>
```

... renders as this (in `site/symptom/index.html`) ...

```html
<p><picture>
  <!-- TODO(@posita): https://github.com/zensical/zensical/issues/975 - What the heck? 👉 --></p>
<p><source media="(prefers-color-scheme: dark)" srcset="../images/example.svg">
  <img alt="Example" src="../../images/example.svg">
</picture></p>
```

Note the insertion of `</p> ... <p>` in the middle of the `<picture> ... </picture>` block immediately after the comment.

### Reproduction / Steps to reproduce

```sh
git clone https://github.com/posita/zensical-picture-repro.git
cd zensical-picture-repro
git checkout posita/0/comment-in-picture-destroys-picture  # branch pertaining to this issue
zensical build --clean
grep --after-context=4 '<picture>' site/symptom/index.html
```

### Environment

```
% uname -prism
Linux 7.1.5-76070105-generic x86_64 x86_64 x86_64
% python3 --version
Python 3.11.15
% zensical --version
0.0.65
```

### Related links

Repro: https://github.com/posita/zensical-picture-repro/tree/posita/0/comment-in-picture-destroys-picture
Zip file: https://github.com/posita/zensical-picture-repro/archive/refs/heads/posita/0/comment-in-picture-destroys-picture.zip
