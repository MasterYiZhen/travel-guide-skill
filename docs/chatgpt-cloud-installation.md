# ChatGPT Cloud / Work 安装与更新

## 支持边界

本仓库是 Travel Guide Skill 的唯一源码。ChatGPT Cloud / Work 使用通过 ChatGPT 网页上传的云端 Skill；Git 变更不会自动同步到已经上传的云端版本，需要重新生成候选 ZIP 并在技能管理界面更新或重新上传。

当前已验证的网页入口是：**ChatGPT 网页端 → 插件 → 技能 → `+` → 上传技能文件**。上传界面当前支持 `.zip`、`.skill` 和 `SKILL.md`。该路径记录的是当前可用界面，不承诺所有账号、客户端或未来版本的界面名称及位置不变。

ChatGPT Desktop 当前没有发现技能上传入口；上传在 ChatGPT 网页端完成，上传后的云端 Skill 可以被 Cloud Work 正常调用。因此，当前正式运行环境是“网页上传的云端 Skill + Cloud Work”。

## 运行时包与发布目录

仓库根目录的 `SKILL.md` 和 `agents/openai.yaml` 是唯一可编辑的运行时源码。`dist/` 由这两份源码生成并随 Git commit 保存，不作为独立编辑源。上传完整 ZIP，而不是单独上传 `SKILL.md`，因为本 Skill 还需要 `agents/openai.yaml` 中的调用策略。ZIP 内固定只包含：

```text
travel-guide-skill/
├── SKILL.md
└── agents/
    └── openai.yaml
```

发布产物使用以下目录：

```text
dist/
├── build/
│   └── travel-guide-skill/
│       ├── SKILL.md
│       └── agents/
│           └── openai.yaml
├── releases/
│   └── travel-guide-skill-<version>.zip
└── upload/
    └── travel-guide-skill-<latest-version>.zip
```

- `dist/build/` 保存当前 commit 对应的展开运行包，必须与根目录运行时源码逐字节一致；准备新运行时版本时由根目录源码重建并在同一 commit 中更新。
- `dist/releases/` 保存仓库中的版本化发布产物历史；构建不得覆盖或删除其中的任何已有版本。
- `dist/upload/` 只保留一个当前推荐上传的最新版 ZIP；其中的 ZIP 必须与 `dist/releases/` 中同版本文件逐字节一致。发布新版本时删除这里的上一版本并复制新版本，但旧版本继续保留在 `releases/` 和 Git 历史中。

上传包不得包含 `docs/`、`evals/`、`.git/`、`.DS_Store`、README、`.gitignore`、历史证据、测试材料或其他开发文件。

## 版本规则

- 已经上传或发布的版本化 ZIP 不可重写或覆盖。
- `dist/releases/` 中的已有版本不可删除，也不得通过删除后重用同一版本号。
- 发布内容发生新变化时，先选择新的递增版本号；目标 ZIP 已存在时必须停止，改用新版本号。
- 当前已发布候选是 `v0.1.0-rc.1`；下一次候选实现应使用 `v0.1.0-rc.2`，不得继续覆盖 `rc.1`。
- 版本升级应与实际发布内容变化对应。仅修改文档且上传包中的运行时内容没有变化时，不强制生成新 ZIP；只有运行时内容发生变化或确实需要重新发布时，才创建新版本候选。
- 清理 `build/` 和 `upload/` 不得影响 `releases/`，也不得使用通配符清空历史发布档案。

## 提交一致性

同一个 Git commit 必须保存相互对应的根目录运行时源码、`dist/build/` 展开包、`dist/releases/` 版本化 ZIP 和 `dist/upload/` 当前候选。任何人 clone 或 checkout 该 commit 后，都能直接获得同一份可上传产物，无需重新构建当前发布包。

运行时版本发生变化时，在同一个 commit 中提交根目录源码修改、`dist/build/` 更新、`dist/releases/` 新版本 ZIP、`dist/upload/` 从上一版本切换到新版本，以及必要的 Eval 或文档变化。不得出现源码与 `dist/` 版本不一致、覆盖旧 release，或 `upload/` 同时存在多个候选的状态。

## 首次安装

1. clone 或 checkout 要使用的 Git commit。
2. 确认 `dist/upload/` 中只有一个经过验证的当前候选 ZIP。
3. 确认该 ZIP 与 `dist/releases/` 中同版本文件逐字节一致；当前发布包不需要重新构建。
4. 在 ChatGPT 网页端进入“插件”→“技能”→ `+` →“上传技能文件”。
5. 从 `dist/upload/` 选择当前最新 ZIP 上传。
6. 在新的 Cloud Work 中显式选择 `Travel Guide Skill`。
7. 使用一个轻量请求确认云端 Skill 能正常加载。
8. 将正式旅行任务放在独立旅行项目或干净 Work 中，不放进 `travel-guide-skill 迭代` 项目。

## 后续更新

1. 修改 Git 中的运行时源码。
2. 完成静态检查。
3. 选择递增的新版本号。
4. 从最新根目录源码更新 `dist/build/`。
5. 在 `dist/releases/` 新增新版本 ZIP，不覆盖任何已有版本。
6. 将 `dist/upload/` 切换为该新版本，使其只包含一个 ZIP。
7. 验证根目录源码、build、release ZIP 和 upload ZIP。
8. 将源码、`dist/` 及必要文档一起 commit。
9. push 当前 commit。
10. 从 `dist/upload/` 将唯一 ZIP 上传到 ChatGPT 网页端。
11. 在干净 Cloud Work 中做轻量验证，确认后再用于真实旅行项目。

> Git 源码发生变化后，已经上传到 ChatGPT 的云端 Skill 不会因为 Git 更新而自动同步；需要重新生成上传包并在网页端更新。

## 生成新版本候选

仅当运行时内容发生变化或确实需要重新发布时，在仓库根目录执行以下参数化示例。以 `v0.1.0-rc.2` 为下一候选示例；实际执行前应选择与发布内容对应的新版本号。

```bash
VERSION="v0.1.0-rc.2"

ROOT="$(pwd)"
BUILD_ROOT="$ROOT/dist/build"
PACKAGE_DIR="$BUILD_ROOT/travel-guide-skill"
RELEASE_DIR="$ROOT/dist/releases"
UPLOAD_DIR="$ROOT/dist/upload"
RELEASE_ZIP="$RELEASE_DIR/travel-guide-skill-$VERSION.zip"
UPLOAD_ZIP="$UPLOAD_DIR/travel-guide-skill-$VERSION.zip"

if [ -e "$RELEASE_ZIP" ]; then
  echo "Release already exists: $RELEASE_ZIP"
  echo "Choose a new version instead of overwriting it."
  exit 1
fi

rm -rf "$BUILD_ROOT"
rm -rf "$UPLOAD_DIR"

mkdir -p "$PACKAGE_DIR/agents"
mkdir -p "$RELEASE_DIR"
mkdir -p "$UPLOAD_DIR"

cp "$ROOT/SKILL.md" "$PACKAGE_DIR/SKILL.md"
cp "$ROOT/agents/openai.yaml" "$PACKAGE_DIR/agents/openai.yaml"

(
  cd "$BUILD_ROOT"
  zip -X -r "$RELEASE_ZIP" \
    travel-guide-skill/SKILL.md \
    travel-guide-skill/agents/openai.yaml
)

cp "$RELEASE_ZIP" "$UPLOAD_ZIP"
cmp "$RELEASE_ZIP" "$UPLOAD_ZIP"
```

该示例只清理 `build/` 和 `upload/`，不清理 `releases/`。如果相同版本已存在，命令会在清理前停止；此时应提升版本号，而不是删除旧 ZIP。成功后，`upload/` 中的唯一 ZIP 与 `releases/` 中对应版本完全一致。该命令会更新 Git 跟踪的 `dist/` 内容，执行后必须审查并与对应源码变更一起提交；不建立额外打包脚本。

## 验证与保存边界

发布前至少确认：

- ZIP 可以正常解压，顶层目录是 `travel-guide-skill/`，且只包含两个运行时文件；
- 包内文件与当前 Git 工作树中的源码逐字节一致；
- `SKILL.md` frontmatter 中存在 `name: travel-guide-skill` 和非空 `description`；
- `agents/openai.yaml` 中存在 `allow_implicit_invocation: false`；
- 根目录和 `dist/build/travel-guide-skill/` 均能通过仓库已有的 `quick_validate.py`；
- `dist/upload/` 只包含一个当前候选 ZIP，且与 `dist/releases/` 中同版本文件逐字节一致；
- `git diff` 同时包含运行时源码及其对应的 `dist/` 更新，并且没有意外的 `.DS_Store`、临时解压目录或其他文件。

`dist/build/`、`dist/releases/` 和 `dist/upload/` 都由普通 Git 正式跟踪。可编辑真值仍是仓库根目录的运行时源码；提交派生产物是为了让同一 commit 对应同一展开包、历史 release 和当前上传 ZIP，而不是建立第二套独立源码。
