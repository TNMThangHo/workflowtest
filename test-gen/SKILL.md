---
name: test-gen
description: AI-powered Test Artifact Generator (Agent-Driven)
---

# Skill: test-gen

Skill này hỗ trợ Agent trong việc sinh artifact kiểm thử.

## Architecture

- **Logic**: Nằm hoàn toàn trong `Agent Context` (Prompt của bạn).
- **Formatter**: `format_output.py` (Chuyển đổi JSON -> Excel/Markdown).
- **Exporter**: `exporter.py` (Class hỗ trợ xuất file).

## Usage

1. **Agent** sinh nội dung ra file `output/raw_ai_output.json`.
2. **Agent** gọi lệnh:
   ```bash
   python test-gen/format_output.py --input output/raw_ai_output.json
   ```
