# ChatGPT Cloud / Work 安装与更新

## 支持边界

本仓库是 Travel Guide Skill 的唯一源码。ChatGPT Cloud / Work 使用通过 ChatGPT 网页上传的云端 Skill；Git 变更不会自动同步到已经上传的云端版本，需要重新生成候选 ZIP 并在技能管理界面更新或重新上传。

当前已验证的网页入口是：**ChatGPT 网页端 → 插件 → 技能 → `+` → 上传技能文件**。上传界面当前支持 `.zip`、`.skill` 和 `SKILL.md`。该路径记录的是当前可用界面，不承诺所有账号、客户端或未来版本的界面名称及位置不变。

ChatGPT Desktop 当前没有发现技能上传入口；上传在 ChatGPT 网页端完成，上传后的云端 Skill 可以被 Cloud Work 正常调用。因此，当前正式运行环境是“网页上传的云端 Skill + Cloud Work”。

## 运行时包与发布目录

Git 工作树中的 `SKILL.md` 和 `agents/openai.yaml` 是唯一运行时源码。上传完整 ZIP，而不是单独上传 `SKILL.md`，因为本 Skill 还需要 `agents/openai.yaml` 中的调用策略。ZIP 内固定只包含：

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

- `dist/build/` 是从当前 Git 工作树组装的临时展开目录，每次构建前可以清理并重建。
- `dist/releases/` 保存带明确版本号的本机发布档案；构建不得自动删除其中的旧版本。
- `dist/upload/` 只保留一个当前待上传 ZIP，可在准备新版本时清理并重建；其中的 ZIP 必须与 `dist/releases/` 中同版本文件逐字节一致。

上传包不得包含 `docs/`、`evals/`、`.git/`、`.DS_Store`、README、`.gitignore`、历史证据、测试材料或其他开发文件。

## 版本规则

- 已经上传或发布的版本化 ZIP 不可重写或覆盖。
- 发布内容发生新变化时，先选择新的递增版本号；目标 ZIP 已存在时必须停止，改用新版本号。
- 当前已发布候选是 `v0.1.0-rc.1`；下一次候选实现应使用 `v0.1.0-rc.2`，不得继续覆盖 `rc.1`。
- 版本升级应与实际发布内容变化对应。仅修改文档且上传包中的运行时内容没有变化时，不强制生成新 ZIP；只有运行时内容发生变化或确实需要重新发布时，才创建新版本候选。
- 清理 `build/` 和 `upload/` 不得影响 `releases/`，也不得使用通配符清空历史发布档案。

## 首次安装

1. 确认 Git 工作树中的 Skill 源码已经完成修改和验证。
2. 确认 `dist/upload/` 中已有一个经过验证的当前候选 ZIP；如尚未准备候选，按下方“生成新版本候选”操作。
3. 确认该 ZIP 与 `dist/releases/` 中同版本文件逐字节一致。
4. 在 ChatGPT 网页端进入“插件”→“技能”→ `+` →“上传技能文件”。
5. 从 `dist/upload/` 选择当前最新 ZIP 上传。
6. 在新的 Cloud Work 中显式选择 `Travel Guide Skill`。
7. 使用一个轻量请求确认云端 Skill 能正常加载。
8. 将正式旅行任务放在独立旅行项目或干净 Work 中，不放进 `travel-guide-skill 迭代` 项目。

## 后续更新

1. Codex 修改 Git 中的运行时源码。
2. 完成静态检查。
3. 为新的候选选择递增版本号。
4. 从最新 Git 工作树生成临时展开目录。
5. 创建新的版本化 ZIP 到 `dist/releases/`。
6. 不覆盖任何已存在版本。
7. 清理并更新 `dist/upload/`，使其只包含新版本。
8. 验证发布 ZIP、源码和待上传副本。
9. commit 并 push 源码或文档变更。
10. 用户从 `dist/upload/` 将新 ZIP 上传到 ChatGPT 网页端。
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
  echo "Choose a new version instead of overwriting an existing release."
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

该示例只清理 `build/` 和 `upload/`，不清理 `releases/`。如果相同版本已存在，命令会在清理前停止；此时应提升版本号，而不是删除旧 ZIP。成功后，`upload/` 中的唯一 ZIP 与 `releases/` 中对应版本完全一致。

## 验证与保存边界

发布前至少确认：

- ZIP 可以正常解压，顶层目录是 `travel-guide-skill/`，且只包含两个运行时文件；
- 包内文件与当前 Git 工作树中的源码逐字节一致；
- `SKILL.md` frontmatter 中存在 `name: travel-guide-skill` 和非空 `description`；
- `agents/openai.yaml` 中存在 `allow_implicit_invocation: false`；
- `dist/build/travel-guide-skill/` 能通过仓库已有的 `quick_validate.py`；
- `dist/upload/` 只包含一个当前候选 ZIP，且与 `dist/releases/` 中同版本文件逐字节一致；
- `git status` 没有把 `dist/` 识别为待提交源码。

`dist/` 继续由 `.gitignore` 忽略。`build/`、`releases/` 和 `upload/` 都是从运行时源码生成的派生产物，不提交 Git，以避免二进制历史、双份源码和版本漂移。由于整个 `dist/` 被忽略，`dist/releases/` 只是当前电脑上的发布档案，不会随 `git clone` 自动恢复；正式稳定版本未来可以通过 GitHub Release 持久保存 ZIP，但本轮不创建 GitHub Release 或 Git tag。
