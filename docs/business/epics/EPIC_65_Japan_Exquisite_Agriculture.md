# 史诗 65：日本式“精致农业”与小农合规管理 (Japan-style Exquisite Farming & Compliance)
*目标：适配日本农业高龄化、小规模、高附加值及高度合规的特点，提供适老化、精细化与轻量化的解决方案。*

---

## 1. 用户故事 (User Stories)

1. **[US-65-01] 极致适老化移动端界面 (AgriNote style UI)**：✅ 已完成 (2026-01-27)
    - **描述**：作为一名 65 岁以上的农户，我希望移动端界面具备超大字体、高对比度图标，以便在老龄化背景下轻松记录。
    - **验收条件**：
        - **(UX)** 在 `accessibility.settings` 中提供“Japanese Elder Mode”预设，全局字号自动适配至 1.5 倍。
        - **(Voice)** 集成语音首选（Voice-First Entry）录入配置。

2. **[US-65-02] 匠人级加工工艺 IoT 监控 (Artisan Processing Monitor)**：✅ 已完成 (2026-01-27)
    - **描述**：作为“市田柿”加工户，我希望实时监控干燥房内的水分，由系统自动判断最佳出货时机。
    - **验收条件**：
        - **(IOT)** 在 `farm.processing.production` 中实现实时水分（Moisture）监控。
        - **(Algorithm)** 当水分降至 `target_moisture_content` 以下时，自动标记为 `Ready for Collection` 并推送通知。

3. **[US-65-03] 农业专用簿记与青色申告 (Japanese Agri-Bookkeeping)**：💡 待规划
    - **描述**：作为兼业农户，我希望系统预置日本农业专用科目（如种苗费、农机折旧费），并能一键生成用于报税的青色申告资料。

4. **[US-65-04] 轻量化“生产履历”合规报告 (Simplified Traceability)**：💡 待规划
    - **描述**：作为农户，我希望通过简单的农事拍照自动生成符合政府审计要求的“生产履历”，以获取农业补贴。