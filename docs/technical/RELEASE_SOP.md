# Odoo Farm 代码发布与同步操作规程 (SOP)

本文档旨在指导开发者如何管理 `19.0` 发布分支，确保从 `dev` 分支同步代码时排除所有开发文档，同时保留完整的提交历史。

## 1. 分支策略
*   **dev (开发分支)**：全量开发分支，包含源代码、开发规约（`.md`）和详细设计文档（`docs/`）。
*   **19.0 (发布分支)**：纯净代码分支，仅包含运行所需的源代码及必要许可证，历史提交中不含任何文档变更。

---

## 2. 核心规约：提交分离 (Commit Isolation)
在 `dev` 分支上工作时，必须严格遵守以下原子化提交原则：
*   **代码提交**：仅包含 `.py`, `.xml`, `.js`, `.csv`, `.css` 等功能代码。
*   **文档提交**：仅包含 `.md` 文件或 `docs/` 目录下的变更。
*   **严禁混合**：严禁在同一个 Commit 中同时修改代码和文档。

---

## 3. 发布与同步流程

### 场景 A：从 dev 持续同步到 19.0
当 `dev` 分支有新的代码提交需要发布时，使用以下逻辑进行同步：

1.  **切换到发布分支**：
    ```bash
    git checkout 19.0
    ```
2.  **筛选并同步 (Cherry-pick)**：
    使用脚本或手动筛选 `19.0..dev` 之间的提交。仅 cherry-pick 那些不包含 `.md` 或 `docs/` 的 commit。
    ```bash
    # 推荐的自动化同步脚本逻辑
    NEW_COMMITS=$(git rev-list --reverse 19.0..dev)
    for commit in $NEW_COMMITS; do
        has_doc=$(git diff-tree --no-commit-id --name-only -r $commit | grep -E "^docs/|\.md$" | wc -l)
        if [ "$has_doc" -eq 0 ]; then
            git cherry-pick $commit
        fi
    done
    ```

### 场景 B：误操作后的历史清洗
如果不慎将文档混入了 `19.0` 的历史，或需要重新基于 `dev` 生成发布版本，使用 `git filter-repo`：

1.  **基于 dev 创建临时分支**：
    ```bash
    git checkout dev
    git checkout -b 19.0-temp
    ```
2.  **执行净化操作**：
    ```bash
    git filter-repo --path docs/ --invert-paths --path-glob '*.md' --invert-paths --refs 19.0-temp --force
    ```
3.  **覆盖/替换 19.0 分支**：
    ```bash
    git branch -f 19.0 19.0-temp
    git branch -D 19.0-temp
    ```

---

## 4. 常见问题 (FAQ)
*   **问：为什么要物理删除历史中的文档？**
    答：为了减小发布包体积，保护内部设计细节不随代码流出，并符合特定的发布规范。
*   **问：混合提交了怎么办？**
    答：同步脚本会跳过混合提交。如果该提交包含关键修复，请在 `19.0` 分支手动执行 `git cherry-pick -n <hash>`，然后 `git reset HEAD docs/ *.md` 并手动提交代码部分。

---
**核准人**：Jeffery
**更新日期**：2026-01-16
