# ChatGPT Cloud / Work 安装与更新

## 当前版本与验证范围

当前候选为 **v0.1.0-rc.8**，推荐安装文件为 [当前 ZIP](../dist/upload/travel-guide-skill-v0.1.0-rc.8.zip)。实现与安装包检查结果见 [rc.8 检查记录](../evals/results-v0.1.0-rc.8.md)。

本版明确默认详尽讲解、图文融合与实际成品质量，补清反馈范围、带保留验收、获取端交付和流程自检。验证方法、证据和实际结果以 rc.8 检查记录为准，分别报告文本场景、独立模型响应、实际制作与审核、工具及渠道检查、模拟或真实用户验收。测试使用本地故障服务时，不推导云端下载和长期保存能力；现场效果以实际使用反馈为依据。

## 安装入口与调用

仓库此前记录的可用入口为：**ChatGPT 网页端 → 插件 → 技能 → `+` → 上传技能文件**。这是旧版安装记录，本版没有重新验证当前账号或客户端界面；安装时以实际技能管理界面为准。仓库此前采用网页上传的云端 Skill 和 Cloud Work，本版没有新增 Desktop 安装能力声明。

1. checkout 需要安装的提交，使用 `dist/upload/` 中唯一 ZIP；已有发布包无需重新构建。
2. 在网页技能管理界面上传完整 ZIP，更新或替换旧版本。包内保留 `agents/openai.yaml` 的显式调用策略。
3. 在新的、干净的旅行任务中显式选择 Travel Guide Skill，检查能否正常加载；记录实际客户端和安装结果。
4. 通过完整旅行任务验证真实图片、审核修复和用户验收流程，分别记录实际执行到的环节及尚未验证部分。

Git 更新不会自动同步到已上传的云端 Skill，需要在技能管理界面更新。提交、远端 push、GitHub Release 和云端替换是分别执行的动作，应按当前授权范围进行。本版本地实现与安装 ZIP 的检查结果见本版记录；Git 提交、推送、GitHub Release 和云端替换按明确授权执行，分别报告实际状态。推送成功时核对本地 HEAD、跟踪分支和远端分支提交号一致。

## 运行时源码与发布目录

根目录的 `SKILL.md` 和 `agents/openai.yaml` 是唯一可编辑的运行时源码。ZIP 顶层目录为 `travel-guide-skill/`，文件条目严格为：

```text
travel-guide-skill/SKILL.md
travel-guide-skill/agents/openai.yaml
```

开发文档、评测、README、历史证据、`.git/`、`.DS_Store` 等不进入安装包。

| 目录 | 用途与一致性要求 |
|---|---|
| `dist/build/travel-guide-skill/` | 当前源码的展开包，两文件逐字节一致；由源码重建，不独立编辑。 |
| `dist/releases/` | 版本化安装归档，已有 ZIP 保留且不覆盖；rc.1—rc.7 仅供历史追溯或回退。 |
| `dist/upload/` | 唯一推荐安装 ZIP，与 releases 中同版本文件逐字节一致。 |

源码、展开包、新 release、唯一 upload、必要文档和评测结果随同一个 Git 提交保存，使 checkout 后可直接获得对应安装包。

## 版本与更新步骤

运行时变化时选择递增版本号；目标版本已存在则改用新版本，不重写历史 ZIP。仅修改开发文档、安装包内容未变时，不强制新增 ZIP。下一候选可使用 `v0.1.0-rc.9`，执行前检查是否被占用。

1. 修改根目录运行时，同步当前文档及行为场景，清理失效引用。
2. 完成结构、规则一致性、要求覆盖和行为场景检查，记录实际方法与范围。
3. 从源码重建 build，新增版本化 release，将 upload 切换为新版本。
4. 验证源码、build、ZIP 内容和 release/upload 一致性。
5. 审核差量，获 Git 提交授权后将相应文件一起提交，报告提交号、安装位置和验证状态；未提交时明确说明。
6. 需要发布或安装时执行相应动作，并更新实际结果。真实旅行任务验证状态独立记录。

## 构建示例

以下在仓库根目录执行，仅在运行时变化或确需重新发布时使用。示例采用下一候选版本；当前 rc.8 可直接安装。

```bash
VERSION=v0.1.0-rc.9 python3 - <<'PY'
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import os
import re
import shutil

root = Path.cwd()
version = os.environ['VERSION']
if not re.fullmatch(r'v\d+\.\d+\.\d+(?:-rc\.\d+)?', version):
    raise SystemExit('Invalid version')
sources = ['SKILL.md', 'agents/openai.yaml']
for name in sources:
    if not (root / name).is_file():
        raise SystemExit('Run from the repository root with both runtime files')
release = root / 'dist/releases' / f'travel-guide-skill-{version}.zip'
if release.exists():
    raise SystemExit('Version already exists; choose a new version')
build = root / 'dist/build'
upload = root / 'dist/upload'
if build.exists():
    shutil.rmtree(build)
package = build / 'travel-guide-skill'
for name in sources:
    target = package / name
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(root / name, target)
release.parent.mkdir(parents=True, exist_ok=True)
with ZipFile(release, 'x', compression=ZIP_DEFLATED) as archive:
    for name in sources:
        archive.write(package / name, 'travel-guide-skill/' + name)
with ZipFile(release) as archive:
    assert archive.testzip() is None
    assert archive.namelist() == ['travel-guide-skill/' + n for n in sources]
    for name in sources:
        assert archive.read('travel-guide-skill/' + name) == (root / name).read_bytes()
if upload.exists():
    shutil.rmtree(upload)
upload.mkdir(parents=True)
target = upload / release.name
shutil.copyfile(release, target)
assert release.read_bytes() == target.read_bytes()
print(release.relative_to(root))
print(target.relative_to(root))
PY
```

示例只重建 build 和 upload，保留已有 releases。使用新版本前同步运行时标题及当前版本说明；脚本失败后先检查实际文件状态，再选取后续处理，不覆盖已产生的同名 release。

## 检查方法与交付状态

- 运行 skill-creator 提供的 `quick_validate.py <仓库路径>`，并检查非空名称和描述、`allow_implicit_invocation: false`。验证器位于执行环境，仓库不新增运行时依赖。
- 对照本版确认要求审核规则与覆盖关系；用搜索定位失效规则和断链，用 `git diff --check` 检查差量格式。
- 按 [行为场景](../evals/evals.md) 选择与差量风险相称的检查并记录实际方法；E01—E18 为既有及扩展场景，E19—E22 覆盖默认深度、认可维度、实际图片审核与获取端交付。文本推演不计作模型、图片或工具实测。
- 对根目录和 build 两文件使用 `cmp`；对 release 使用 `unzip -t`、`unzip -Z1`，检查精确两文件清单，并将 ZIP 内实际字节与根目录源码比较。
- 使用 `cmp` 比较 release 与 upload，检查 upload 只有一个推荐安装 ZIP，历史 release 未被修改。

实施报告分别展示：

| 状态层 | 可报告的结果 |
|---|---|
| 规则与文本场景 | 记录要求覆盖、文本推演和回归结果，仅证明规则与场景预期一致。 |
| 实际工具执行 | 记录实际结构、策略、链接、格式、构建和包一致性检查；仅证明执行过的检查，不推导旅行研究、制图或 Reviewer 已运行。 |
| 实际制作与旅行效果 | 用完整候选检查默认讲解、图文融合、实际字形、对象及局部对应、内部动线、修复范围和获取端交付；独立 Reviewer 的输入、检查结果与修复证据分别记录。明确测试使用模拟用户还是实际用户；未发生的修复、真实验收、云端获取或现场使用保留未验证状态。 |

文件与安装包准备完成、Git 提交、推送、GitHub Release 和云端加载另外记录各自实际状态。

真实旅行任务结束后，如发现有证据支持的 Skill 问题，按运行时流程提出改进方案供后续实施。
