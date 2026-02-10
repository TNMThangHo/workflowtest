# Walkthrough - Advanced Engine Upgrades (v2)

## 1. Problem

The previous engine version missed critical "Action-based" tests for complex UI components.

- **Tables**: Missed Sort/Filter/Pagination/Actions.
- **Trees**: Missed CRUD/Search/Drag&Drop.
- **Uploads**: Missed specific file types and versioning.

## 2. Solution: `extra_props` Architecture

We upgraded the `FieldType` model to support a flexible `extra_props` dictionary.
This allows the Architect (AI) to specify granular capabilities.

### New Schema Example

```json
{
  "type": "tree_view",
  "extra_props": {
    "can_create_folder": true,
    "has_search": true,
    "can_drag_drop": true
  }
}
```

### Engine Logic Updates

- **`_expand_table`**: Now generates TCs for Columns, Sort (Default/Name), Pagination (Next/Large Data), Filters, and Row Actions.
- **`_expand_tree_view`**: Now generates TCs for Expand/Collapse, Search (Name/Code), Filter, CRUD (Folder/Doc), and Drag & Drop.
- **`_expand_file_upload`**: Now generates TCs for specific Extensions (PDF/DOC/IMG), Security (Shell/Double Ext), and Features (OCR/Version).
- **`_expand_permission_matrix`**: Now generates TCs for Role Capabilities (Enforce/Restrict).

## 3. Verification Results

We ran a test with `schema_input.json` containing these new props.

**Result File**: `output/tc4_advanced.md`
**Total TCs**: 133 (High granularity)

### Key Improvements

| Component              | Old Engine    | New Engine                                     |
| :--------------------- | :------------ | :--------------------------------------------- |
| **Project List Table** | 3 Generic TCs | **10 Detailed TCs** (Sort, Filter, Actions)    |
| **Document Tree**      | 5 Generic TCs | **14 Detailed TCs** (CRUD, Drag&Drop)          |
| **File Upload**        | 4 Generic TCs | **11 Detailed TCs** (Malware, OCR, Versioning) |

## 4. Next Steps

- The engine is now fully capable.
- Future runs of `/testcase` will automatically leverage this logic as long as the AI Architect fills in `extra_props` (Prompts already updated).
