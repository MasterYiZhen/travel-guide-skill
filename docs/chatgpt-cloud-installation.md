# ChatGPT Cloud / Work 安装与更新

## 支持边界

本仓库是 Travel Guide Skill 的唯一源码。ChatGPT Cloud / Work 使用通过 ChatGPT 网页上传的云端 Skill；仓库中的变更不会自动同步到已上传版本，更新后必须重新生成 ZIP 并在技能管理界面重新上传。

当前已验证的网页入口是：**ChatGPT 网页端 → 插件 → 技能 → `+` → 上传技能文件**。上传界面当前支持 `.zip`、`.skill` 和 `SKILL.md`。该路径记录的是当前可用界面，不承诺所有账号、客户端或未来版本的界面名称及位置不变。

ChatGPT Desktop 当前没有发现技能上传入口；上传在 ChatGPT 网页端完成，上传后的云端 Skill 可以被 Cloud Work 正常调用。因此，当前正式运行环境是“网页上传的云端 Skill + Cloud Work”。

## 最小上传包

上传包固定只包含当前运行时需要的两个文件：

```text
travel-guide-skill/
├── SKILL.md
└── agents/
    └── openai.yaml
```

上传 ZIP，而不是单独上传 `SKILL.md`，因为本 Skill 还需要 `agents/openai.yaml` 中的调用策略。包中不得包含 `docs/`、`evals/`、`.git/`、`.DS_Store`、README、`.gitignore`、历史证据、测试材料或其他开发文件。

`dist/` 是可随时从 Git 工作树重建的派生产物，不提交到 Git：这样可以维持唯一源码，避免 ZIP 的二进制 diff、重复事实源以及上传包与源码漂移。

## 首次安装

1. 确认 Git 工作树中的 Skill 源码已经完成修改和验证。
2. 按下方“生成与验证”重建最小上传包。
3. 确认 ZIP 中只包含上方列出的运行时文件。
4. 在 ChatGPT 网页端进入“插件”→“技能”→ `+` →“上传技能文件”。
5. 上传 `dist/travel-guide-skill-v0.1.0-rc.1.zip`。
6. 在新的 Cloud Work 中显式选择 `Travel Guide Skill`。
7. 使用一个轻量请求确认云端 Skill 能正常加载。
8. 将正式旅行任务放在独立旅行项目或干净 Work 中，不放进 `travel-guide-skill 迭代` 项目。

## 后续更新

1. 在 Git 仓库中修改 `SKILL.md`、`agents/openai.yaml` 或必要的 Eval 和研发文档。
2. 完成静态检查。
3. commit 源码和文档变更。
4. 从最新 Git 工作树重新生成并验证最小云端上传 ZIP。
5. 在 ChatGPT 网页端的技能管理界面更新或重新上传云端 Skill；具体按钮名称以当时实际界面为准。
6. 新建干净 Cloud Work 做必要的轻量验证。
7. 确认没有实际运行问题后，再用于真实旅行项目。

> Git 源码发生变化后，已经上传到 ChatGPT 的云端 Skill 不会因为 Git 更新而自动同步；需要重新生成上传包并在网页端更新。

## 生成与验证

在仓库根目录执行以下最小操作；它们只重建 `dist/` 下的派生产物，不改变运行时源码：

```bash
rm -rf dist/travel-guide-skill
rm -f dist/travel-guide-skill-v0.1.0-rc.1.zip
mkdir -p dist/travel-guide-skill/agents
cp SKILL.md dist/travel-guide-skill/SKILL.md
cp agents/openai.yaml dist/travel-guide-skill/agents/openai.yaml
(cd dist && zip -X -r travel-guide-skill-v0.1.0-rc.1.zip \
  travel-guide-skill/SKILL.md \
  travel-guide-skill/agents/openai.yaml)
```

发布前至少确认：

- ZIP 解压后的根目录是 `travel-guide-skill/`，且文件清单与上方树形结构完全一致；
- 包内文件与当前 Git 工作树中的源文件逐字节一致；
- `SKILL.md` frontmatter 中存在 `name: travel-guide-skill` 和非空 `description`；
- `agents/openai.yaml` 中存在 `allow_implicit_invocation: false`；
- 包目录仍能通过仓库已有的 `quick_validate.py`；
- `git status` 没有把 `dist/` 识别为待提交源码。
