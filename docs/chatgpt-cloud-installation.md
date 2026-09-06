# ChatGPT Cloud / Work 安装与更新

## 当前版本与验证范围

当前候选为 **v0.1.0-rc.3**，推荐安装文件为 [当前 ZIP](../dist/upload/travel-guide-skill-v0.1.0-rc.3.zip)。实现与安装包检查结果见 [rc.3 检查记录](../evals/results-v0.1.0-rc.3.md)。

本版实施完成结构、规则一致性、要求覆盖、行为场景文本推演和打包一致性检查。真实旅行任务验证尚未执行，待安装后通过完整旅行任务检查实际图片质量、系列一致性、独立审核修复和用户验收流程。文本推演、安装包完整性和云端加载是不同范围的检查，均不替代真实旅行任务结果。

## 安装入口与调用

仓库此前记录的可用入口为：**ChatGPT 网页端 → 插件 → 技能 → `+` → 上传技能文件**。这是旧版安装记录，本版没有重新验证当前账号或客户端界面；安装时以实际技能管理界面为准。仓库此前采用网页上传的云端 Skill 和 Cloud Work，本版没有新增 Desktop 安装能力声明。

1. checkout 需要安装的提交，使用 `dist/upload/` 中唯一 ZIP；已有发布包无需重新构建。
2. 在网页技能管理界面上传完整 ZIP，更新或替换旧版本。包内保留 `agents/openai.yaml` 的显式调用策略。
3. 在新的、干净的旅行任务中显式选择 Travel Guide Skill，检查能否正常加载；记录实际客户端和安装结果。
4. 通过完整旅行任务验证真实图片、审核修复和用户验收流程，分别记录实际执行到的环节及尚未验证部分。

Git 更新不会自动同步到已上传的云端 Skill，需要在技能管理界面更新。提交、远端 push、GitHub Release 和云端替换是分别执行的动作，应按当前授权范围进行。本版交付本地 Git 提交及安装 ZIP，不包含远端发布或云端替换。

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
| `dist/releases/` | 版本化安装归档，已有 ZIP 保留且不覆盖；rc.1、rc.2 仅供历史追溯或回退。 |
| `dist/upload/` | 唯一推荐安装 ZIP，与 releases 中同版本文件逐字节一致。 |

源码、展开包、新 release、唯一 upload、必要文档和评测结果随同一个 Git 提交保存，使 checkout 后可直接获得对应安装包。

## 版本与更新步骤

运行时变化时选择递增版本号；目标版本已存在则改用新版本，不重写历史 ZIP。仅修改开发文档、安装包内容未变时，不强制新增 ZIP。下一候选可使用 `v0.1.0-rc.4`，执行前检查是否被占用。

1. 修改根目录运行时，同步当前文档及行为场景，清理失效引用。
2. 完成结构、规则一致性、要求覆盖和行为场景检查，记录实际方法与范围。
3. 从源码重建 build，新增版本化 release，将 upload 切换为新版本。
4. 验证源码、build、ZIP 内容和 release/upload 一致性。
5. 审核差量，将相应文件一起提交，报告提交号、安装位置和验证状态。
6. 需要发布或安装时执行相应动作，并更新实际结果。真实旅行任务验证状态独立记录。

## 构建示例

以下在仓库根目录执行，仅在运行时变化或确需重新发布时使用。示例采用下一候选版本；当前 rc.3 可直接安装。

```bash
VERSION=v0.1.0-rc.4 python3 - <<'PY'
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
- 按 [行为场景](../evals/evals.md) 记录所用方法。本版方法为逐场景文本推演，记录下一动作、等待节点、角色及结束条件；不计作真实图片或 Agent 执行。
- 对根目录和 build 两文件使用 `cmp`；对 release 使用 `unzip -t`、`unzip -Z1`，检查精确两文件清单，并将 ZIP 内实际字节与根目录源码比较。
- 使用 `cmp` 比较 release 与 upload，检查 upload 只有一个文件，历史 release 未被修改。

实施报告分别展示：

| 状态层 | 可报告的结果 |
|---|---|
| 实现与安装包 | 文件已更新、规定检查完成并有记录、包与源码一致、Git 提交已保存后，可报告本轮实现与安装包交付完成。 |
| 真实旅行任务验证 | 列出实际执行和检查过的环节；未执行时明确写尚未执行、待安装后完整旅行任务验证。 |

真实旅行任务结束后，如发现有证据支持的 Skill 问题，按运行时流程提出改进方案供后续实施。
