# rc.9 验证证据索引

这些材料用于开发验证，不进入两文件运行时安装包。完整结论、边界与判断见[本版检查记录](../../results-v0.1.0-rc.9.md)。路径基准：本目录；相对链接指向留存副本。

执行环境：Claude Code 桌面端，主会话与全部子 Agent 均为 Claude Fable 5.1（`claude-fable-5-1`）。环境**没有**模型图片生成或编辑工具、没有 ChatGPT 云端安装渠道；可用的是网页读取、图片查看、独立子 Agent、Python（Pillow／pypdf／reportlab／numpy，安装在 scratchpad venv）、本地 HTTP 服务与 zip 工具。

| 材料 | 实际用途与边界 |
|---|---|
| [runtime-under-test.txt](runtime-under-test.txt)、[package-checks.json](package-checks.json) | 行为测试与各轮审核实际使用的被测 Skill 全文（测试后依自检建议与独立审核建议补入两句：第 3 步“局部修订另核对实际改动只落在目标范围、相邻文字与图形未受损”，产品范围“图片数量与内容拆分服从信息充分、手机可读、整套协调与现场实用”，最终文本见根目录 SKILL.md，差异可用 diff 查看）；结构、链接、调用策略、八步标题、源码／build／ZIP／upload 一致性与历史包字节检查结果。 |
| [behavior/operations.md](behavior/operations.md) | 行为测试 T1—T7 的输入、隔离方式、模型与实施者判断要点；各 `T*-response.md` 为被测 Agent 原始响应，`e19-materials.md` 为 E19 虚构资料。均为模型文字响应，不是图片效果证据。 |
| [delivery-fixture/fixture.py](delivery-fixture/fixture.py)、[run-01/](delivery-fixture/run-01/) | E22 获取端交付测试：可复现的本地故障服务（旧版入口、存档 503、长期保存失败为交接输入）、交接记录、请求日志、两版 PDF，以及被测 Agent 的实际核对报告 [T6-report.md](delivery-fixture/run-01/agent-out/T6-report.md)、下载对象、响应头与渲染图。复现方法见 fixture.py 文件头（create 拒绝写入已有产物的目录，须用新目录）；服务只读本目录，不连接生产系统。 |
| [visual-fixtures/](visual-fixtures/) | E21 程序渲染受控样例：`render.py` 生成 `pages/` 五页（对照页 + 四类缺陷页），`brief.md` 是 Reviewer 输入，`maker-key.md` 是制作者缺陷意图（未给 Reviewer）。[first-review/review.md](visual-fixtures/first-review/review.md) 为全新 Reviewer 首审；`pages/page-a-text-v2.png` 为局部修复版，[rereview/rereview.md](visual-fixtures/rereview/rereview.md) 为另一名全新 Reviewer 的复审。 |
| [rc8-real-review/](rc8-real-review/) | 旧 rc.8 内置 image_gen 真实生成的 sample-a／b／c（历史来源，用 [extract-rc8-materials.sh](extract-rc8-materials.sh) 从提交 77ff55c 提取，哈希见 [rc8-materials-sha256.txt](rc8-materials-sha256.txt)）在 rc.9 规则下的首审与复审报告及裁切。验证的是 rc.9 审核规则对真实生成图的判断，不是 rc.9 自行制作的效果。 |
| [travel-trial-review/](travel-trial-review/) | 旧 rc.8 五页天坛候选（历史来源，同上提取）的首次全量正式审核 [first-review/review-01.md](travel-trial-review/first-review/review-01.md)（系统 FAIL，4 处字形错误）；[repair/](travel-trial-review/repair/) 为本轮用 Pillow 做的栅格整行重绘修复脚本、区域记录与放大对照；[candidate-02/](travel-trial-review/candidate-02/) 为修复后的三张新版页面、清单与变更范围；[rereview/review-02.md](travel-trial-review/rereview/review-02.md) 为另一名全新 Reviewer 的正式复审（FAIL：修复引入 N-1）；[candidate-03/](travel-trial-review/candidate-03/) 与 [rereview-03/review-03.md](travel-trial-review/rereview-03/review-03.md) 为再修复后第三名全新 Reviewer 的正式复审（PASS，保留次要问题）；[delivery/](travel-trial-review/delivery/) 为模拟带保留通过后的实际导出（PDF、交接记录、两项交付物哈希；12 MB 图片 ZIP 未归档，条目清单见 images-zip-listing.txt）与被测 Agent 的第 7、8 步 [交付核对与流程自检](travel-trial-review/delivery/agent-out/delivery-and-selfcheck.md)。未改动的 02、03 页仍以 rc.8 提交中的文件为准，可用提取脚本取得。 |

被测执行者与 Reviewer 均未获得 evals.md 预期行为或缺陷答案；每轮审核使用新的 Agent。目录内报告保留执行时的 scratchpad 绝对路径，当前入口以本索引的相对链接为准。模拟用户确认与模拟验收单独标识，不代表任何真实用户接受成品；旧 rc.8 天坛候选的真实用户验收、云端下载和现场使用从未发生。
