You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[UX] Initial installation defaults to English regardless of browser language preference

# [UX] Initial installation defaults to English regardless of browser language preference

## Description

When a user installs hermes-webui for the first time, the interface always defaults to English regardless of the user's browser language preference or system locale settings. This is very unfriendly for non-English speakers who must manually change the language setting after every fresh installation.

## Current Behavior

- Fresh installation always loads the UI in English
- No detection of browser language (`Accept-Language` header) or system locale
- Users must navigate to settings to change the language manually
- For users deploying in multi-language environments (e.g., Chinese, Japanese, Spanish), this creates unnecessary friction

## Expected Behavior

The initial language should be detected from the user's browser preferences:

1. **Read `Accept-Language` header**: On first load, check the browser's preferred language from the HTTP request header
2. **Match available locales**: If the browser's preferred language matches an available translation, load that language by default
3. **Fallback to English**: If no match is found, fall back to English as the default
4. **Persist user choice**: Once the user explicitly selects a language, remember that choice (cookie/localStorage) and do not override it on subsequent visits
5. **No server-side change needed**: This can be implemented entirely client-side by reading `navigator.language` or `navigator.languages` on first visit

## Technical Details

### Client-side approach (preferred):
```javascript
// On first visit (no saved language preference)
const browserLang = navigator.language || navigator.userLanguage; // e.g. "zh-CN", "ja", "es"
const savedLang = localStorage.getItem('hermes-lang'); // user's explicit choice

if (!savedLang) {
    const preferredLang = browserLang.split('-')[0]; // e.g. "zh" from "zh-CN"
    // Check if translation exists for this language
    if (availableLocales.includes(preferredLang)) {
        setLanguage(preferredLang);
    }
}
```

### Server-side approach (if needed):
- Parse `Accept-Language` header in the Express/Nginx middleware
- Set the default language before rendering the page
- More reliable for SEO and initial page load, but requires server config changes

## Affected Files
- `static/index.html` (initial language setup)
- `static/js/` (language initialization logic)
- Any language detection/persistence mechanism

## Proposed Fix

1. On first load, check `localStorage.getItem('hermes-lang')` for a previously saved preference
2. If no saved preference exists, read `navigator.language` or `navigator.languages[0]`
3. Match the browser language against available locale files
4. If match found, load that locale; otherwise, default to English
5. When the user manually changes the language, save the choice to `localStorage`
6. Optionally, also check the `Accept-Language` header on the server side for the initial HTML render

## Related Issues
- #7582 (i18n: several elements not wired through data-i18n) — related internationalization cleanup

---

## 中文描述

## 问题描述

用户首次安装 hermes-webui 后，界面始终默认显示英文，无论用户的浏览器语言偏好或系统区域设置如何。这对非英语用户非常不友好——每次全新安装后都必须手动更改语言设置。

## 当前行为

- 全新安装后界面始终以英文加载
- 不检测浏览器语言（`Accept-Language` 请求头）或系统区域设置
- 用户必须手动导航到设置中更改语言
- 对于部署在多语言环境中的用户（例如中文、日文、西班牙文），这造成了不必要的摩擦

## 期望行为

首次安装时应根据用户的浏览器偏好自动检测语言：

1. **读取 `Accept-Language` 请求头**：首次加载时，检查 HTTP 请求中的浏览器首选语言
2. **匹配可用语言包**：如果浏览器首选语言匹配可用的翻译文件，则默认加载该语言
3. **回退到英文**：如果无匹配，则回退到英文作为默认值
4. **持久化用户选择**：用户明确选择语言后，记住该选择（通过 cookie/localStorage），后续访问不再覆盖
5. **无需服务端改动**：可完全通过客户端实现，读取 `navigator.language` 或 `navigator.languages`

## 技术细节

### 客户端方案（推荐）：
```javascript
// 首次访问时（无已保存的语言偏好）
const browserLang = navigator.language || navigator.userLanguage; // e.g. "zh-CN", "ja", "es"
const savedLang = localStorage.getItem('hermes-lang'); // 用户明确选择的语言

if (!savedLang) {
    const preferredLang = browserLang.split('-')[0]; // e.g. "zh" from "zh-CN"
    // 检查是否有该语言的翻译文件
    if (availableLocales.includes(preferredLang)) {
        setLanguage(preferredLang);
    }
}
```

### 服务端方案（如需）：
- 在 Express/Nginx 中间件中解析 `Accept-Language` 请求头
- 在渲染页面前设置默认语言
- 对 SEO 和初始页面加载更可靠，但需要服务端配置改动

## 影响文件
- `static/index.html`（初始语言设置）
- `static/js/`（语言初始化逻辑）
- 任何语言检测/持久化机制

## 建议修复

1. 首次加载时，检查 `localStorage.getItem('hermes-lang')` 是否有已保存的偏好
2. 如果无保存偏好，读取 `navigator.language` 或 `navigator.languages[0]`
3. 将浏览器语言与可用语言文件匹配
4. 如果匹配成功，加载该语言包；否则默认英文
5. 用户手动更改语言时，将选择保存到 `localStorage`
6. 可选：也在服务端检查 `Accept-Language` 请求头用于初始 HTML 渲染

## 相关 Issue
- #7582 (i18n: several elements not wired through data-i18n) — 相关的国际化清理工作
