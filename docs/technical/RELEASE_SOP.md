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
*   **最小逻辑单元**：每个提交只包含一个完整的逻辑功能单元，确保提交粒度足够细。
*   **严禁混合**：严禁在同一个 Commit 中同时修改代码和文档。
*   **无 Co-author**：严禁在提交中使用co-author标签。

---

## 3. 提交前准备（强制性）
在进行任何开发提交前，开发者必须执行以下步骤确保代码和文档分离：

### 3.1 验证当前工作区状态
```bash
git status
# 确认待提交的文件类型和内容
```

### 3.2 按类型分离文件
在添加文件到暂存区之前，需要将代码文件和文档文件分离：

```bash
# 1. 暂存代码相关文件
git add farm_sustainability/models/*.py farm_sustainability/views/*.xml farm_sustainability/security/*.csv farm_sustainability/__manifest__.py

# 2. 单独提交代码变更
git commit -m "feat: brief description of the feature in English"

# 3. 暂存文档相关文件
git add docs/**/*.md

# 4. 单独提交文档变更
git commit -m "docs: brief description of the documentation in English"
```

---

## 4. 发布与同步流程

### 场景 A：从 dev 持续同步到 19.0
当 `dev` 分支有新的代码提交需要发布时，使用以下逻辑进行同步：

1.  **切换到发布分支**：
    ```bash
    git checkout 19.0
    ```
2.  **筛选并同步 (Cherry-pick)**：
    使用脚本或手动筛选 `19.0..dev` 之间的提交。**必须严格按照时间先后顺序（从最早到最新）**进行 cherry-pick，仅 cherry-pick 那些不包含 `.md` 或 `docs/` 的 commit。`git rev-list --reverse` 命令确保了按时间顺序获取提交。
    ```bash
    # 推荐的自动化同步脚本逻辑
    NEW_COMMITS=$(git rev-list --reverse 19.0..dev)
    for commit in $NEW_COMMITS; do
        has_doc=$(git diff-tree --no-commit-id --name-only -r $commit | grep -E "^docs/|\.md$" | wc -l)
        if [ "$has_doc" -eq 0 ]; then
            echo "Syncing code commit: $commit"
            git cherry-pick $commit
        else
            echo "Skipping doc commit: $commit"
        fi
    done
    ```

    **保持原始提交信息（可选）**：
    如需在发布分支上保持与原始提交相同的时间戳、作者信息，并在提交信息中包含原始提交的hash ID，使用以下命令替代标准的 cherry-pick：
    ```bash
    # 手动进行 cherry-pick 并保留原始提交信息
    git cherry-pick --strategy=recursive -X theirs <commit-hash>
    # 或在 cherry-pick 后修改提交信息以包含原始hash
    git cherry-pick --no-commit <commit-hash>
    # 解决可能的冲突后
    git commit --author="$(git show --format="%an <%ae>" --no-patch <commit-hash>)" --date="$(git show --format="%ad" --no-patch <commit-hash>)" -m "$(git show --format="%s%n%n[From commit: <commit-hash>]" --no-patch <commit-hash>)"
    ```

    **验证同步结果**：
    ```bash
    # 检查最近同步的提交
    git log --oneline -10
    # 验证没有文档文件被包含
    git show --name-only HEAD | grep -E "\.md$|docs/"
    # 如果没有输出，说明同步成功
    ```

### 场景 B：混合提交的处理
如果在 dev 分支上意外创建了混合提交，应按以下步骤处理：

1. **立即修正（推荐）**：在提交后立即修正，使用 `git reset --soft HEAD~1`，然后按类型分离文件重新提交。

2. **分离既有混合提交**：如果混合提交已经存在，使用以下步骤分离：
    ```bash
    # 1. 重置到混合提交之前的状态
    git reset --hard <混合提交的前一个提交哈希>

    # 2. 提取混合提交的补丁
    git show <混合提交哈希> --name-only > /tmp/commit_files.txt

    # 3. 分别提取代码和文档更改
    git diff <前一个提交> <混合提交> -- 'farm_*/**' > /tmp/code_changes.patch
    git diff <前一个提交> <混合提交> -- 'docs/**' > /tmp/doc_changes.patch

    # 4. 应用代码更改并提交
    patch -p1 < /tmp/code_changes.patch
    git add .
    git commit -m "feat: description of the feature"

    # 5. 应用文档更改并提交
    patch -p1 < /tmp/doc_changes.patch
    git add .
    git commit -m "docs: description of the documentation"
    ```

### 场景 C：改写既有提交以拆分代码和文档
如果需要对历史中的混合提交进行拆分，使用交互式变基（interactive rebase）：

1. **启动交互式变基**：
    ```bash
    # 对特定提交前的N个提交进行变基
    git rebase -i <目标提交~N的哈希>
    # 或者对最近10个提交进行变基（如果目标提交比较近）
    git rebase -i HEAD~10
    ```

2. **在变基编辑器中**：
    - 找到需要拆分的提交行
    - 将该行的 `pick` 改为 `edit`
    - 保存并退出编辑器

3. **分离提交内容**：
    ```bash
    # 当前处于需要拆分的提交，重置为暂存状态
    git reset HEAD^

    # 重新添加文件并分离提交
    # 先添加代码文件
    git add farm_sustainability/models/*.py farm_sustainability/views/*.xml farm_sustainability/security/*.csv
    git commit -m "feat: description of the feature in English"

    # 再添加文档文件
    git add docs/**/*.md
    git commit -m "docs: description of the documentation in English"

    # 继续变基过程
    git rebase --continue
    ```

4. **处理冲突**（如有）：
    - 如果出现冲突，解决后使用 `git add <文件>` 标记冲突已解决
    - 然后执行 `git rebase --continue`

**警告**：变基会改写历史，在共享分支上操作前请确认没有其他人在使用相关提交。

### 场景 D：误操作后的历史清洗
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

## 5. 预防机制
为了从源头防止混合提交，建议在项目中配置 pre-commit hook：

1. 创建 `.git/hooks/pre-commit` 文件：
```bash
#!/bin/bash
# 检查提交是否混合了代码和文档
CODE_FILES=$(git diff --cached --name-only | grep -E "\.(py|xml|js|csv|css|yml|yaml|json)$" | wc -l)
DOC_FILES=$(git diff --cached --name-only | grep -E "\.md$|^docs/" | wc -l)

if [ "$CODE_FILES" -gt 0 ] && [ "$DOC_FILES" -gt 0 ]; then
    echo "ERROR: Mixed code and documentation files detected in commit!"
    echo "Please separate code and documentation into different commits."
    echo "Code files: $(git diff --cached --name-only | grep -E '\.(py|xml|js|csv|css|yml|yaml|json)$')"
    echo "Documentation files: $(git diff --cached --name-only | grep -E '\.md$|^docs/')"
    exit 1
fi
```

2. 给脚本执行权限：
```bash
chmod +x .git/hooks/pre-commit
```

---

## 6. 常见问题 (FAQ)
*   **问：为什么要物理删除历史中的文档？**
    答：为了减小发布包体积，保护内部设计细节不随代码流出，并符合特定的发布规范。

*   **问：混合提交了怎么办？**
    答：同步脚本会跳过混合提交。如果该提交包含关键修复，请在 `19.0` 分支手动执行 `git cherry-pick -n <hash>`，然后 `git reset HEAD docs/ *.md` 并手动提交代码部分。更推荐在 dev 分支上立即修正混合提交。

*   **问：如何检查提交是否符合规范？**
    答：使用 `git show --name-only <commit-hash>` 检查提交包含的文件类型。一个合规的提交应只包含单一类型的文件（纯代码或纯文档）。

*   **问：发布分支的提交信息有什么要求？**
    答：发布分支上的提交信息必须使用英文，清晰描述功能变更，不包含文档说明或开发过程记录。

*   **问：cherry-pick 时提交顺序重要吗？**
    答：**非常重要！** 必须严格按照时间顺序进行 cherry-pick（从最早的提交到最新的提交），以确保提交之间的依赖关系得到正确处理，避免冲突。`git rev-list --reverse` 命令可以按时间顺序返回提交。

*   **问：是否可以保持原始提交的作者和时间戳信息？**
    答：可以。在发布分支上进行 cherry-pick 时，可以使用特定命令来保持原始提交的作者信息、时间戳，并在提交信息中包含原始提交的hash ID，以保持提交历史的完整性。

---

**核准人**：Jeffery
**更新日期**：2026-01-29