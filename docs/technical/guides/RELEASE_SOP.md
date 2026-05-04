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
3.  **何时停止 cherry-pick**：
    *   **正常停止**：当所有从 `19.0` 之后在 `dev` 分支上的非文档提交都已同步完成时。
    *   **异常停止**：如果在 cherry-pick 过程中出现大量冲突或重复提交，应立即停止当前操作：
        ```bash
        # 停止当前的 cherry-pick 操作
        git cherry-pick --abort
        # 或者如果是在脚本中，可以检查 git status 确认是否在 cherry-pick 过程中
        if git status | grep -q "cherry-pick"; then
            git cherry-pick --abort
        fi
        ```
    *   **检查重复提交**：在开始 cherry-pick 前，检查目标分支是否已有相同的提交：
        ```bash
        # 检查提交是否已经存在
        if ! git log --oneline --max-count=50 19.0 | grep "$commit"; then
            # 只有当提交未在目标分支上存在时才 cherry-pick
            git cherry-pick $commit
        else
            echo "Skipping duplicate commit: $commit"
        fi
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

2. **自动化同步脚本**：
为确保 19.0 发布分支的同步一致性，使用提供的自动化脚本。为避免切换分支后脚本无法访问的问题，脚本应放置在Git仓库外部：

```bash
# 1. 确保分支最新
git checkout dev  # 在 dev 分支上运行脚本
git pull origin dev

# 2. 复制脚本到临时位置（避免分支切换后无法访问）
cp scripts/sync_to_19.sh /tmp/sync_to_19.sh

# 3. 运行同步脚本（脚本会自动切换到 19.0 分支进行操作）
/tmp/sync_to_19.sh

# 4. 验证同步结果
git checkout 19.0  # 切换到 19.0 查看结果
git status
git log --oneline -10  # 检查最近的同步提交
```

或者，使用独立的外部脚本创建方法：

```bash
# 创建独立的同步脚本（在仓库外，永久解决访问问题）
cat > /tmp/sync_to_19.sh << 'EOF'
#!/bin/bash

# Odoo Farm 自动化同步脚本 - 从 dev 分支同步非文档提交到 19.0 分支
# 此脚本将保持原始提交的作者和时间戳信息

set -e  # 遇到错误立即退出

echo "开始同步 dev 分支到 19.0 分支..."

# 确保在主目录
cd /Users/jeffery/odoo-farm-dev

# 检查当前分支状态并保存
CURRENT_BRANCH=$(git branch --show-current)
echo "当前分支: $CURRENT_BRANCH"

# 保存当前工作区状态
if ! git diff-index --quiet HEAD --; then
    echo "警告: 当前分支有未提交的更改，可能会在分支切换时丢失"
    echo "是否继续？(y/N)"
    read -r response
    if [[ ! "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        exit 1
    fi
fi

# 切换到 19.0 分支
echo "切换到 19.0 分支..."
git checkout 19.0

# 获取 dev 分支上从 19.0 分支分离点之后的所有提交（按时间顺序，从最早到最新）
echo "获取 dev 分支上的新提交..."
NEW_COMMITS=$(git rev-list --reverse 19.0..dev)

if [ -z "$NEW_COMMITS" ]; then
    echo "没有新的提交需要同步"
    # 切回原分支
    git checkout "$CURRENT_BRANCH"
    exit 0
fi

echo "发现 $(echo "$NEW_COMMITS" | wc -w) 个新提交需要处理"

# 逐个处理提交
for commit in $NEW_COMMITS; do
    echo "处理提交: $commit"

    # 检查这个提交是否包含文档文件
    has_doc=$(git diff-tree --no-commit-id --name-only -r $commit | grep -E "^docs/|\.md$" | wc -l)

    if [ "$has_doc" -gt 0 ]; then
        echo "  跳过文档提交: $commit"
        continue
    fi

    # 检查提交是否已经存在于 19.0 分支（防止重复）
    if git log --oneline --max-count=200 19.0 | grep -q "$(git show --format="%H" --no-patch $commit)"; then
        echo "  跳过已存在的提交: $commit"
        continue
    fi

    # 检查提交消息是否已经存在于最近的提交中（基于提交消息的相似性）
    commit_message=$(git show --format="%s" --no-patch $commit | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
    if git log --oneline --max-count=100 19.0 | grep -F -q "$commit_message"; then
        echo "  跳过可能重复的提交（基于消息）: $commit - $commit_message"
        continue
    fi

    echo "  同步代码提交: $commit (保持原始作者和时间戳)"

    # 获取原始提交的作者和日期
    ORIGINAL_AUTHOR=$(git show --format="%an <%ae>" --no-patch $commit)
    ORIGINAL_DATE=$(git show --format="%ad" --no-patch $commit)

    # 执行 cherry-pick 但不自动提交
    if ! git cherry-pick --no-commit $commit; then
        echo "错误：提交 $commit 产生冲突"
        echo "请手动解决冲突后执行: git cherry-pick --continue"
        echo "或跳过此提交: git cherry-pick --skip"
        echo "或中止操作并返回到 $CURRENT_BRANCH 分支: git cherry-pick --abort && git checkout $CURRENT_BRANCH"
        exit 1
    fi

    # 获取原始提交信息用于构建提交消息
    ORIGINAL_SUBJECT=$(git show --format="%s" --no-patch $commit)
    ORIGINAL_BODY=$(git show --format="%b" --no-patch $commit)

    # 构建包含原始提交链接的新提交消息
    if [ -n "$ORIGINAL_BODY" ]; then
        NEW_COMMIT_MSG="${ORIGINAL_SUBJECT}

[From dev commit: ${commit}]

${ORIGINAL_BODY}"
    else
        NEW_COMMIT_MSG="${ORIGINAL_SUBJECT}

[From dev commit: ${commit}]"
    fi

    # 手动提交，保持原始作者和时间戳，并添加原始提交链接
    GIT_AUTHOR_NAME="$(git show --format="%an" --no-patch $commit)" \
    GIT_AUTHOR_EMAIL="$(git show --format="%ae" --no-patch $commit)" \
    GIT_AUTHOR_DATE="$ORIGINAL_DATE" \
    git commit --no-verify --cleanup=whitespace -m "$NEW_COMMIT_MSG"

    echo "  成功同步: $commit (作者: $(git show --format="%an" --no-patch HEAD), 日期: $(git show --format="%ad" --no-patch HEAD), 新提交: $(git rev-parse --short HEAD))"
done

echo "同步完成！"
echo "当前 19.0 分支状态："
git log --oneline -5

# 切回原分支
echo "切回原分支: $CURRENT_BRANCH"
git checkout "$CURRENT_BRANCH"
EOF

chmod +x /tmp/sync_to_19.sh

# 然后运行
/tmp/sync_to_19.sh
```

此脚本将：
*   按时间顺序（从最早到最新）处理提交
*   跳过包含文档的提交（.md 文件或 docs/ 目录）
*   防止重复提交到目标分支
*   保持原始提交的作者和时间戳
*   在提交消息中包含原始提交的链接
*   自动在 dev 和 19.0 分支之间切换，完成同步后自动返回原分支
*   避免切换分支后脚本无法访问的问题（通过放置在仓库外部）

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

*   **问：如何避免重复的 cherry-pick 提交？**
    答：为避免重复提交，自动化同步脚本会：1) 检查提交的哈希值是否已存在于目标分支；2) 检查提交消息是否与最近的提交相似；3) 跳过任何已存在或潜在的重复提交。如需手动操作，可在执行 cherry-pick 前使用 `git log --oneline --max-count=50 19.0 | grep <commit-hash>` 验证提交是否已存在。

*   **问：何时应该停止 cherry-pick 操作？**
    答：正常情况下，当所有 dev 分支上新的非文档提交都已同步到 19.0 分支后停止。异常情况下，如果出现大量冲突、重复提交或其他问题，应立即使用 `git cherry-pick --abort` 停止当前操作，以防止造成更混乱的状态。

*   **问：如何保持原始提交的时间戳和作者信息？**
    答：使用提供的自动化同步脚本 (`./scripts/sync_to_19.sh`)，它会自动保持原始提交的作者、时间戳和提交消息。脚本通过设置 `GIT_AUTHOR_NAME`、`GIT_AUTHOR_EMAIL` 和 `GIT_AUTHOR_DATE` 环境变量来实现这一点。

*   **问：如何在新提交中保留与原始提交的链接？**
    答：自动化同步脚本会在每个同步的提交消息中添加 "[From dev commit: <hash>]" 信息，这样可以追踪到原始提交。这有助于维护提交历史的完整性。

## 7. 改进方案：使用临时目录管理脚本和SOP

为解决切换分支后无法访问脚本和SOP文档的问题，建议将脚本和SOP文档复制到临时目录：

### 7.1 创建临时管理脚本
```bash
# 创建临时目录
mkdir -p /tmp/odoo_farm_release

# 复制SOP文档到临时目录
cp docs/technical/RELEASE_SOP.md /tmp/odoo_farm_release/

# 复制同步脚本到临时目录
cp scripts/sync_to_19.sh /tmp/odoo_farm_release/

# 或者直接在临时目录创建脚本
cat > /tmp/odoo_farm_release/sync_to_19.sh << 'EOF'
#!/bin/bash

# Odoo Farm 自动化同步脚本 - 从 dev 分支同步非文档提交到 19.0 分支
# 此脚本将保持原始提交的作者和时间戳信息

set -e  # 遇到错误立即退出

echo "开始同步 dev 分支到 19.0 分支..."

# 确保在主目录
cd /Users/jeffery/odoo-farm-dev

# 检查当前分支状态并保存
CURRENT_BRANCH=$(git branch --show-current)
echo "当前分支: $CURRENT_BRANCH"

# 保存当前工作区状态
if ! git diff-index --quiet HEAD --; then
    echo "警告: 当前分支有未提交的更改，可能会在分支切换时丢失"
    echo "是否继续？(y/N)"
    read -r response
    if [[ ! "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        exit 1
    fi
fi

# 切换到 19.0 分支
echo "切换到 19.0 分支..."
git checkout 19.0

# 获取 dev 分支上从 19.0 分支分离点之后的所有提交（按时间顺序，从最早到最新）
echo "获取 dev 分支上的新提交..."
NEW_COMMITS=$(git rev-list --reverse 19.0..dev)

if [ -z "$NEW_COMMITS" ]; then
    echo "没有新的提交需要同步"
    # 切回原分支
    git checkout "$CURRENT_BRANCH"
    exit 0
fi

echo "发现 $(echo "$NEW_COMMITS" | wc -w) 个新提交需要处理"

# 逐个处理提交
for commit in $NEW_COMMITS; do
    echo "处理提交: $commit"

    # 检查这个提交是否包含文档文件
    has_doc=$(git diff-tree --no-commit-id --name-only -r $commit | grep -E "^docs/|\.md$" | wc -l)

    if [ "$has_doc" -gt 0 ]; then
        echo "  跳过文档提交: $commit"
        continue
    fi

    # 检查提交是否已经存在于 19.0 分支（防止重复）
    if git log --oneline --max-count=200 19.0 | grep -q "$(git show --format="%H" --no-patch $commit)"; then
        echo "  跳过已存在的提交: $commit"
        continue
    fi

    # 检查提交消息是否已经存在于最近的提交中（基于提交消息的相似性）
    commit_message=$(git show --format="%s" --no-patch $commit | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
    if git log --oneline --max-count=100 19.0 | grep -F -q "$commit_message"; then
        echo "  跳过可能重复的提交（基于消息）: $commit - $commit_message"
        continue
    fi

    echo "  同步代码提交: $commit (保持原始作者和时间戳)"

    # 获取原始提交的作者和日期
    ORIGINAL_AUTHOR=$(git show --format="%an <%ae>" --no-patch $commit)
    ORIGINAL_DATE=$(git show --format="%ad" --no-patch $commit)

    # 执行 cherry-pick 但不自动提交
    if ! git cherry-pick --no-commit $commit; then
        echo "错误：提交 $commit 产生冲突"
        echo "请手动解决冲突后执行: git cherry-pick --continue"
        echo "或跳过此提交: git cherry-pick --skip"
        echo "或中止操作并返回到 $CURRENT_BRANCH 分支: git cherry-pick --abort && git checkout $CURRENT_BRANCH"
        exit 1
    fi

    # 获取原始提交信息用于构建提交消息
    ORIGINAL_SUBJECT=$(git show --format="%s" --no-patch $commit)
    ORIGINAL_BODY=$(git show --format="%b" --no-patch $commit)

    # 构建包含原始提交链接的新提交消息
    if [ -n "$ORIGINAL_BODY" ]; then
        NEW_COMMIT_MSG="${ORIGINAL_SUBJECT}

[From dev commit: ${commit}]

${ORIGINAL_BODY}"
    else
        NEW_COMMIT_MSG="${ORIGINAL_SUBJECT}

[From dev commit: ${commit}]"
    fi

    # 手动提交，保持原始作者和时间戳，并添加原始提交链接
    GIT_AUTHOR_NAME="$(git show --format="%an" --no-patch $commit)" \
    GIT_AUTHOR_EMAIL="$(git show --format="%ae" --no-patch $commit)" \
    GIT_AUTHOR_DATE="$ORIGINAL_DATE" \
    git commit --no-verify --cleanup=whitespace -m "$NEW_COMMIT_MSG"

    echo "  成功同步: $commit (作者: $(git show --format="%an" --no-patch HEAD), 日期: $(git show --format="%ad" --no-patch HEAD), 新提交: $(git rev-parse --short HEAD))"
done

echo "同步完成！"
echo "当前 19.0 分支状态："
git log --oneline -5

# 切回原分支
echo "切回原分支: $CURRENT_BRANCH"
git checkout "$CURRENT_BRANCH"
EOF

chmod +x /tmp/odoo_farm_release/sync_to_19.sh

# 创建快速访问脚本
cat > /tmp/odoo_farm_release/sync.sh << 'EOF'
#!/bin/bash
# 快速同步脚本
echo "使用临时目录中的脚本进行同步..."
/tmp/odoo_farm_release/sync_to_19.sh
EOF

chmod +x /tmp/odoo_farm_release/sync.sh

echo "临时目录已创建: /tmp/odoo_farm_release"
echo "SOP文档已复制: /tmp/odoo_farm_release/RELEASE_SOP.md"
echo "同步脚本已复制: /tmp/odoo_farm_release/sync_to_19.sh"
echo "快速访问脚本: /tmp/odoo_farm_release/sync.sh"
```

### 7.2 使用临时目录进行同步
```bash
# 1. 确保分支最新
git checkout dev
git pull origin dev

# 2. 使用临时目录中的脚本进行同步
/tmp/odoo_farm_release/sync.sh

# 3. 验证同步结果
git checkout 19.0
git log --oneline -10
```

---

**核准人**：Jeffery
**更新日期**：2026-01-29