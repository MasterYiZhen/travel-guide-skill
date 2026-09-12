# rc.8 验证证据索引

这些材料用于开发验证，不进入两文件运行时安装包。完整结论及边界见[本版检查记录](../../results-v0.1.0-rc.8.md)。

| 材料 | 实际用途与边界 |
|---|---|
| [runtime-under-test.txt](runtime-under-test.txt)、[package-checks.json](package-checks.json) | 冻结的被测 Skill，以及源码、build、ZIP、调用策略和历史包字节检查。 |
| [behavior/operations.md](behavior/operations.md) | 独立 Agent 的原始测试输入、响应与工具过程。A—D、F、G 是模型响应；E 实际读取受控 HTTP 入口及本地文件。 |
| [behavior/E-response-and-self-check.md](behavior/E-response-and-self-check.md)、[追加入口结果](behavior/E-second-entry-report.md) | 旧 PDF、存档 503、新版入口与分项交付状态。长期保存失败来自测试输入，真实云端和用户下载未验证。 |
| [delivery-fixture/server.py](delivery-fixture/server.py)、[交接输入](delivery-fixture/handoff.json) | 可复现的本地故障服务与两版 PDF；不连接生产系统。 |
| [visual-fixtures/brief.md](visual-fixtures/brief.md) | 虚构教学页的正确资料与目标，是独立 Reviewer 的输入。 |
| [A 对照图](visual-fixtures/sample-a.png)、[B 缺陷图](visual-fixtures/sample-b.png)、[C 修复图](visual-fixtures/sample-c.png) | 内置 image_gen 的实际生成、编辑与修复图；均保留原生尺寸。 |
| [首审](fixture-review/review.md)、[全新 Reviewer 复审](fixture-rereview/review.md) | 实际完整图片与局部的判断，含发现、修复核验及确定程度。 |
| [visual-fixtures/maker-key.md](visual-fixtures/maker-key.md) | 制作者的缺陷意图，仅供事后比对；未给独立 Reviewer，不把预设缺陷等同于实际缺陷。 |
| [travel-trial/user-and-responses.md](travel-trial/user-and-responses.md)、[候选清单](travel-trial/page-manifest.json) | 普通天坛半日游需求、模拟行程确认及五张实际高清攻略。资料、实物参考、原图和修订、提示、工具结果均随目录保留。 |

目录内的原始操作日志保留执行时的 `/private/tmp/` 路径及代理名称。以上相对链接对应留存副本；复制文件不改变图像或原始证据。模拟用户确认与验收单独标识，不代表本次用户接受旅行成品。西安历史会话的原图、PDF 和审核附件未取得，本目录没有声称回放这些原始材料。
