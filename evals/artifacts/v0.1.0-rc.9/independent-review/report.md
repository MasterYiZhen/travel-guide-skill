# rc.9 独立审核报告（工作分支 `codex/travel-guide-rc9` 相对 `origin/main` ac6cdf6）

审核日期：2026-09-13。审核者：未参与本轮实现的独立 Reviewer（Claude Fable 5.1 子 Agent）。只读，未修改仓库任何文件；本报告写在 scratchpad。未联网。

审核对象说明：分支 HEAD 仍为 `ac6cdf6`（等于 origin/main），本轮全部差量均为**未提交的工作区改动**（7 个已跟踪文件修改／删除 + 3 个未跟踪文件／目录：两个 rc.9 ZIP、`evals/results-v0.1.0-rc.9.md`、`evals/artifacts/`）。因此“新 checkout 可复现”只能以工作区为对象验证，提交后应再核一次。

---

## 一、实际执行的检查清单

| # | 检查 | 方法 | 结果 |
|---|---|---|---|
| 1 | 差量总览 | `git diff origin/main --stat`；`git status --short` | 7 文件 +208/−102；另 3 项未跟踪；`git diff --check origin/main` 无输出（exit 0） |
| 2 | 逐文件 diff 阅读 | SKILL.md、README.md、docs/chatgpt-cloud-installation.md、evals/evals.md、evals/results-v0.1.0-rc.7.md、dist/build/SKILL.md | 全部通读；见第二、三节 |
| 3 | 新增记录阅读 | evals/results-v0.1.0-rc.9.md、evals/artifacts/v0.1.0-rc.9/README.md、behavior/operations.md、T1／T5 响应全文、T4 关键段、T1b／T3 数值抽查、T6-report.md、visual-fixtures 首审＋复审、rc8-real-review 首审＋复审、travel-trial-review review-01／02／03 与 delivery-and-selfcheck.md、maker-key.md、manifest.json、change-scope.md、fixture.py、render.py 头部、extract-rc8-materials.sh、package-checks.json、handoff.json（两份）、requests.log、SHA256SUMS.txt、files-sha256.txt、page-manifest-03.json | 见第三节发现表 |
| 4 | 被测运行时一致性 | `diff runtime-under-test.txt SKILL.md` | 逐字节相同（但见发现 F-01） |
| 5 | 源码／build 一致 | `diff SKILL.md dist/build/.../SKILL.md`；`diff agents/openai.yaml dist/build/.../agents/openai.yaml` | 均相同；openai.yaml 为 `policy:\n  allow_implicit_invocation: false` |
| 6 | quick_validate | `/Users/yizhen/.codex/skills/.system/skill-creator/scripts/quick_validate.py` 对根目录与 `dist/build/travel-guide-skill` | 两者均 `Skill is valid!` |
| 7 | ZIP 检查 | python zipfile：testzip、namelist、条目字节 vs 源码；`unzip -Z1`、`unzip -t`；release vs upload；upload 目录列表 | testzip=None；条目精确为 `travel-guide-skill/SKILL.md`、`travel-guide-skill/agents/openai.yaml`；两条目字节与根目录源码相同；release==upload（7,196 B，SHA-256 `4146dca6…caf5f4c`，与 results／package-checks 记录一致）；upload 目录仅一个文件 |
| 8 | 历史包 | `git show origin/main:dist/releases/…rc.N.zip | cmp` N=1…7 | 七个均与 origin/main 逐字节相同；rc.7 ZIP 从 upload 删除但 releases 中原件仍在 |
| 9 | 版本残留 | grep `rc.7|rc.8|rc.10` 于 README、SKILL、docs、evals.md、results-rc.9、artifacts README | 所有命中均为有意的历史／下一版引用，无误指当前版本的残留；SKILL.md 无任何 rc.7/rc.8 字样 |
| 10 | 运行时数值 | grep 数字于 SKILL.md | 仅 1080／1440／3:4、版本号、步骤序号；无测试数值（50／30／65 分钟、页码等）进入运行时 |
| 11 | 链接 | package-checks.json 56 条（去重 52 条）全部 `exists: true`；抽查 results-rc.9 与 artifacts README 所有链接指向的文件实际 `ls`/打开 | 全部可定位；但 results 正文写“42 个”与 JSON 计数不一致（发现 F-06） |
| 12 | extract 脚本复现 | 在 scratchpad `git clone` 仓库后运行 `extract-rc8-materials.sh` 到新目录，输出哈希与 `rc8-materials-sha256.txt` diff | exit 0；24 个文件哈希**完全一致** |
| 13 | fixture 复现 | scratchpad venv（reportlab 5.0.1）运行 `fixture.py create <新目录> 18798`、`serve`，curl 三个入口 | `/current.pdf` 200 且逐字节等于 v1；`/candidate-v2.pdf` 200 且等于 v2；`/materials.zip` 503；requests.log 写入正常。生成 PDF 与归档 run-01 哈希不同（reportlab 时间戳），行为等价 |
| 14 | 证据哈希核对 | run-01 两版 PDF vs agent-out fetched 文件；travel-trial delivery PDF vs files-sha256／handoff；candidate-02／03 PNG vs review-02／03 记录哈希 | 全部一致 |
| 15 | 历史材料声明核对 | `git show 77ff55c:…/fixture-review/review.md`、`…/travel-trial/self-check.md`、`page-manifest.json` | rc.8 首审确将陶器站图标缺失判为“不单凭此判 FAIL”，与 results §4.2 描述一致；rc.8 self-check.md（14 行）未提及四处字形错误，与 results §4.3 描述一致；rc.8 清单 `formal_review: pending_budget_limit` 属实 |
| 16 | 模型响应抽核 | T1（11 页、四件对象各整页、四观察点、声明未生成图片）；T1b（8 页）；T3（23:00／07:00／08:00–08:30／08:30／09:15；15:40／16:30／17:00；15:25）；T4（限定范围、集中询问一次、第 15 页不修、不扩大为整套 PASS）；T5（D／E／F 三判定） | 与 results §2 表述一致 |

---

## 二、对 A—G 的逐项结论

**A. 产品目标** — 成立。主要定义位置：SKILL“产品目标与适用范围”＋“内容与视觉标准”的“讲解深度”“规格”条目；第 1 步“准备重点对象的知识依据、实物参考与现场观察点”、第 3 步自检落实。高清竖向、预约／行程／交通衔接／识别理解观察、详尽讲解五要素（身份、时代背景、用途工艺、重要性、造型纹饰铭文结构）、简略收敛、1080×1440／3:4／合格原生输出、用户明确尺寸优先均有清楚表述。唯一弱点：提示词要求“图片数量服从信息充分、手机可读、整套协调、现场实用”，运行时只写“图片数量与内容拆分均由任务决定”“篇幅由对象及信息量决定”，四个判断依据未作为图片数量的准绳明写（建议 F-09）。

**B. 图文融合与认可维度** — 成立。“图文融合”“参考与认可维度”两条与标准末段“成品质量以实际高清页面、必要局部和整套关系的检查为依据。知识稿正确、文本提取成功、工具返回完成或历史 PASS，均不能替代实际成品检查”是清楚的单一定义位置；第 3 步自检、第 4 步 Reviewer 查看方式、第 6 步引用。E20、E21 场景与之对应。

**C. 研究与时间** — 成立。第 1 步合并为“对象核实”“路线”“起居”“时间预算”“服务”五段，rc.7 三处重叠的时间／用餐规则已去重；一致起终点、完整计入、同一时段只计一次、沿用用户有效预算、变更走第 2 步确认、早餐窗口与晨间准备、简洁偏好与实际依赖条件并存（默认偏好段）均有落点；具名对象首次制作前取得参考在第 3 步。测试数值未进运行时（检查 10）。

**D. 反馈范围、审核与验收** — 成立。八步齐全（package-checks 亦核）；“有效确认后直接制作”（第 2 步末句＋第 3 步首句）；默认一名全新 Reviewer、首审全量、复审新 Reviewer 查实际影响＋完整候选、无实质问题即进入第 5 步、限定范围修复与范围外说明、范围内修复≠整套 PASS、带保留通过／接受当前版本／停止修订分别判断、进度询问保持阶段边界（流程总段）均有清楚位置。evals E07 A／B／C、E10 D／E／F 对应。

**E. 获取端交付与结束** — 成立。第 7 步三段分别覆盖“入口所指对象的内容页数顺序显示”“图片／PDF／存档／长期保存分别核对报告；本地正确／渠道可获取／用户下载是不同证据；长期保存仅承诺时纳入”“渲染字体导出压缩发布渠道限制由工具承担；受阻说明并继续授权补救”；第 5 步“用户明确通过后直接进入第 7、8 步”；第 8 步区分执行遗漏／Skill 表达机制问题／证据不足，最后说明结束状态与限制，建议不自动触发修改。E22 对应。

**F. 实现原则** — 基本成立。显式调用、全新连续任务、两文件运行时保持；只改 SKILL.md；无页数、分包大小、视觉样式、修图手法（“不拉伸变形、裁掉有效内容或仅放大低清图片”为 rc.7 既有禁止句，非新增手法规定）。描述 88 字、窄触发。OpenAI 文章要点在 results 中有实际读取记录。发现两处术语不同步（F-04、F-05）。

**G. 验证与交付要求** — 大部分成立，有若干记录准确性问题。分层记录清楚，历史材料与新验证有来源标识，模拟验收全部标为模拟，rc.8 材料明确“不作为 rc.9 自行制作效果证据”；历史五页候选先核哈希再首次全量正式审核，修复后由新 Reviewer 复审（共三名不同 Reviewer）；缺陷覆盖以实际图片为准（maker-key 未给 Reviewer；visual-fixtures 首审命中全部预设项，rc8-real 首审一处漏检被如实记录）；fixture 生成器／服务／交接输入在同一目录且可复现；extract 脚本哈希可复现；build／ZIP／release／upload／历史包一致。问题：被测运行时冻结件标注不准（F-01）、部分归档产物缺失但报告与哈希清单仍列出（F-02、F-03）、链接计数不一致（F-06）、fixture 无覆盖保护（F-07）。

---

## 三、发现表

严重级别：实质问题＝影响运行时正确性或证据可信度且须处理；次要问题＝应修正但不影响结论；建议＝可选改进。

| 编号 | 文件:位置 | 问题描述 | 影响 | 级别 |
|---|---|---|---|---|
| F-01 | `evals/artifacts/v0.1.0-rc.9/README.md:9`（“冻结的被测 Skill 全文”）；`behavior/operations.md:3`（“内容与 ../runtime-under-test.txt 一致”）；对照 `evals/results-v0.1.0-rc.9.md:76` | results 明确说明第 3 步“局部修订另核对实际改动只落在目标范围、相邻文字与图形未受损”一句是在**全部行为测试与审核之后**加入的，且 7,157 B 的旧包已删除；而 `runtime-under-test.txt` 与最终 SKILL.md 逐字节相同，即它保存的是**最终文本**而非被测文本。artifacts README 将其称为“冻结的被测 Skill 全文”，operations.md 称被测 Agent 收到的 SKILL 与该文件一致，两处表述与 results §4.4 末段自相矛盾；被测文本（缺该句的版本）没有被归档。 | 证据标注不准确：无法从仓库取得测试时的真实运行时文本。差异仅一句、方向为收紧，对测试结论影响很小，但违反“记录被测版本”的要求。修正办法：把 runtime-under-test.txt 改为被测版本（可由 SKILL.md 删去该句重建并核对字节数），或改名并在两处说明“为最终文本，与被测文本差第 3 步一句”。 | 次要问题 |
| F-02 | `evals/artifacts/v0.1.0-rc.9/delivery-fixture/run-01/agent-out/`；`SHA256SUMS.txt:1`；`T6-report.md:30,45,101` | T6 报告与 SHA256SUMS.txt 均列出 `agent-out/delivery-candidate-v2.pdf`（“本地交付副本”“第二获取途径”），归档目录中**不存在该文件**（目录仅 SHA256SUMS.txt、T6-report.md、两组 headers、两份 fetched PDF、503 正文、render/）。 | 哈希清单指向不存在的文件；读者按报告找不到“交付副本”。内容与 candidate-v2.pdf 相同（哈希 94cf8539…），可能是去重删除，但未在 artifacts README 说明。 | 次要问题 |
| F-03 | `evals/artifacts/v0.1.0-rc.9/travel-trial-review/delivery/files-sha256.txt:1`；`handoff.json` `local_files`；`artifacts/README.md:14` | 交付测试的两项交付物中，`tiantan-candidate-03-images.zip`（12,318,824 B）未归档，只保留其 headers 与哈希；README 对 delivery/ 的描述为“实际导出（PDF、交接记录、哈希）”，未明确说明 ZIP 未归档及重建方式（candidate-03 三页＋extract 脚本取得的 02／03 页＋page-manifest-03.json，按 delivery 报告记录的条目顺序打包，但字节不会一致）。 | “PNG 图片承诺：渠道可获取”的一手对象无法从仓库直接取得，只能以报告与哈希为据。与 README 中对 02／03 页“可用提取脚本取得”的处理方式不一致。 | 次要问题 |
| F-04 | `evals/evals.md:62,73` | E04／E05 写“按 SKILL 第 4 节”。rc.9 SKILL 内部引用统一为“第 4 步”（第 3 步末、第 6 步），标题也是“### 4. 独立审核与修复”。 | 术语与运行时不同步，可能被误读为另有章节。 | 次要问题 |
| F-05 | `evals/evals.md:21,29,54,110,234`；对照 `SKILL.md:56`（“### 3. 制作完整候选”） | evals 仍多处使用“完整套图”“套图制作”，运行时第 3 步已改名“制作完整候选”并全文改用“候选”。 | 术语漂移，不影响判定，但与“合并替换减少重复、统一表达”原则不一致。 | 次要问题 |
| F-06 | `evals/results-v0.1.0-rc.9.md:40`；`evals/artifacts/v0.1.0-rc.9/package-checks.json` `links` | results 写“42 个 Markdown 本地链接全部存在”，package-checks.json 记录 56 条（去重后 52 条 file→target 对）。 | 数字与证据文件不一致；结论（全部存在）本身经我实际抽查成立。 | 次要问题 |
| F-07 | `evals/artifacts/v0.1.0-rc.9/delivery-fixture/fixture.py:22-24, 76-81` | 文件头声称“不覆盖既有归档证据”，但 `create()` 对传入目录 `mkdir(exist_ok=True)` 后直接写入 candidate-v1/v2.pdf 与 handoff.json，无任何“目录已存在则拒绝”的保护；若按文档以归档路径 `run-01` 复现，会覆盖归档 PDF 与 handoff。 | 复现操作有误伤归档的风险（我在 scratchpad 新目录运行，未触发）。建议在 create 中对已存在的 PDF／handoff 报错退出，或在 README 明示“须使用新目录”。 | 建议 |
| F-08 | `evals/results-v0.1.0-rc.7.md:64` | 同一目标 `../dist/releases/travel-guide-skill-v0.1.0-rc.7.zip` 出现两个链接文字（“rc.7 安装 ZIP（现位于 releases）”与“rc.7 release”）。 | 冗余；原因是 upload 链接改指 releases 后与旧链接重复。 | 建议 |
| F-09 | `SKILL.md:9`（“图片数量与内容拆分均由任务决定”）；`SKILL.md:16` | 提示词 A 要求“图片数量服从信息充分、手机可读、整套协调、现场实用”，运行时未把这四个依据写成图片数量的判断标准，只写“由任务决定”“篇幅由对象及信息量决定”。 | 对“该做多少页”的边界判断依据略弱；其他条目（规格、一致性、覆盖）间接覆盖。 | 建议 |
| F-10 | `README.md:16` | “验证分开记录……实际工具执行和云端交付”；本轮无云端渠道，results 只在“发布状态”一节说明云端安装未执行，并无“云端交付”记录层。 | 措辞略超出实际记录层次；README 同段随后已说明“没有云端安装渠道……保留未验证”。 | 建议 |
| F-11 | `evals/results-v0.1.0-rc.9.md:89` | “## 独立审核”为占位“【待补……】”。 | 属预期（待本报告结论回填），提交前须填写，不能以占位提交。 | 建议 |

**未发现的问题类别（明确说明）：** 运行时无 rc.7／rc.8 版本残留；无测试数值进入运行时；无与 evals 场景相矛盾的规则；八步标题与内部引用（第 2／3／4／5／7／8 步）互相一致；README／安装说明版本号、下一候选 rc.10、ZIP 链接均已同步；源码／build／ZIP／release／upload／历史包一致；模拟验收在 results、artifacts README、三份 review、delivery 报告中均明确标为模拟，未发现把模拟说成真实、把模型响应或历史材料说成 rc.9 制作效果的情况；rc8-real 首审漏检（sample-b 四足小图）被如实记录而非隐去。

---

## 四、总体结论

**不存在必须处理的实质问题。** 运行时 SKILL.md 对 A—G 各项要求都有清楚的主要定义位置和步骤落实，未引入不该有的具体数值或方法；安装产物（build／ZIP／release／upload／历史包）经实际工具检查全部一致，quick_validate 通过，`git diff --check` 干净；extract 脚本与 fixture 在新目录可复现。

需要在提交前处理的次要问题集中在**证据记录的准确性**：F-01（被测运行时冻结件实为最终文本，与两处“被测全文／一致”表述矛盾）、F-02／F-03（报告与哈希清单列出的产物未归档且未说明）、F-04／F-05（evals 术语未随运行时同步）、F-06（链接计数）。这些不改变任何验证结论，但按 G 项“清单与链接能从仓库定位真实材料、记录被测版本”的要求应当修正。另请注意本轮差量尚未提交（HEAD=origin/main），“新 checkout 可复现”待提交后复核；results §独立审核占位需回填。
