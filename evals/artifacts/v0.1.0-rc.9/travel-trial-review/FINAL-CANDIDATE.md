# 天坛五页候选：最终版本、文件来源与结论索引

本文件是接手者的当前入口。三份审核报告、各轮清单（page-manifest-02.json、page-manifest-03.json）、变更范围与哈希记录保持其原始证据身份，不再改写；其中的 `file` 路径为执行时的 scratchpad 路径，`formal_review`／`status` 字段停留在各轮写成时的状态。

## 最终候选 tiantan-candidate-03（review-03 系统 PASS）

阅读顺序 01→05。哈希与 review-03 报告记录逐字一致。

| 页 | 版本 | 本目录内文件来源 | sha256 |
|---|---|---|---|
| 01 | v5 | [candidate-03/page-01-v5.png](candidate-03/page-01-v5.png)（本轮栅格重绘两处文字，见 repair/changes-03.json） | 69a3358785f5eddc3a27078f37a715e3596f9a518d28b15091e5e8a487da47c7 |
| 02 | v2 | 未改动，rc.8 历史图：`sh ../extract-rc8-materials.sh <目录>` 后取 `travel-trial/images/page-02-v2.png` | 52a7f0efe1f07d015302753680579a0374bdb2d2c79cb731298c812bcce9c6c3 |
| 03 | v1 | 未改动，同上取 `page-03-v1.png` | e2f1ae11709b01781120215fc3ea0b41abb7d1d1955ae29d648d2c30db33d057 |
| 04 | v3 | [candidate-02/page-04-v3.png](candidate-02/page-04-v3.png)（本轮重绘一行，见 repair/changes.json） | 8fa55054b978433626da9d2dcede0a21636ff95eb874a6e0df386e7d6612bcc0 |
| 05 | v4 | [candidate-02/page-05-v4.png](candidate-02/page-05-v4.png)（本轮重绘一行，见 repair/changes.json） | 6f2e4c454042dddea25427ca256e3792c4fa807a062ddbb6492ed100d3935c0a |

均为 1086 × 1448 px、3:4、RGB PNG。rc.8 历史原图的哈希见 [../rc8-materials-sha256.txt](../rc8-materials-sha256.txt)。

## 各轮文件的身份

- [candidate-02/page-manifest-02.json](candidate-02/page-manifest-02.json)：候选 02 提交 review-02 前的清单快照（P1 v4、P4 v3、P5 v4）；candidate-02/page-01-v4.png 已被 v5 取代，只作 review-02 N-1 的对照证据。
- [candidate-03/page-manifest-03.json](candidate-03/page-manifest-03.json)：候选 03 提交 review-03 **之前**的原始清单快照，`formal_review` 字段停留在 “awaiting review-03”，属于历史状态，不表示最终结论；最终结论以 review-03 与本文件为准。
- [candidate-03/change-scope-03.md](candidate-03/change-scope-03.md)、[candidate-02/change-scope-02.md](candidate-02/change-scope-02.md)：制作者向各轮 Reviewer 提供的变更范围。
- [repair/](repair/)：修复脚本 `repair.py`（最终形态只重做 page-01 → v5）、`changes.json`（候选 02 三页的区域记录）、`changes-03.json`（page-01-v5 区域记录）及放大对照图。

## 结论链

| 环节 | 结论 | 报告 |
|---|---|---|
| 首次全量正式审核（候选 01，rc.8 历史五页） | 系统 FAIL：4 处字形错误，7 项次要 | [first-review/review-01.md](first-review/review-01.md) |
| 修复后正式复审（候选 02） | 系统 FAIL：4 处错字已改，修复引入 N-1（切断相邻行、遮住图标） | [rereview/review-02.md](rereview/review-02.md) |
| 再修复后正式复审（候选 03） | **系统 PASS**；保留次要问题：四处重绘行字重偏细、两处填底矩形仅放大可检出、首审 7 项次要、清单路径字段 | [rereview-03/review-03.md](rereview-03/review-03.md) |
| 模拟用户验收 | 模拟用户“带保留通过，接受这个版本；字重偏细我知道了，先交付图片和 PDF”（非真实用户） | [delivery/handoff.json](delivery/handoff.json) |
| 第 7 步交付核对 | 图片 ZIP 与 PDF：本地正确、本地 HTTP 渠道可获取、用户实际下载未验证；导出 PDF 内嵌 JPEG 有损，判为次要并说明以 PNG 为原始像素 | [delivery/agent-out/delivery-and-selfcheck.md](delivery/agent-out/delivery-and-selfcheck.md) |
| 第 8 步流程自检 | 4 项执行遗漏、2 项 Skill 改进候选（其一已补入 rc.9 第 3 步）、4 项证据不足；流程结束 | 同上 |

交付物：[delivery/tiantan-candidate-03.pdf](delivery/tiantan-candidate-03.pdf)（已归档）；图片 ZIP 未归档，条目与 CRC 见 [delivery/images-zip-listing.txt](delivery/images-zip-listing.txt)，两项哈希见 [delivery/files-sha256.txt](delivery/files-sha256.txt)。

边界：五页图片由旧 rc.8 生成，本轮只执行审核、栅格修复、复审、模拟验收与交付核对；rc.9 从普通请求自行制作图片的效果、真实用户验收、云端下载与现场使用均未验证。
