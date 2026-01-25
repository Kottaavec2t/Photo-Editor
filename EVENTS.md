# Event Bus Documentation

## Published Events

### Top Bar (`top_bar.py`)
| Event | Publisher | Data Parameters | Description |
|-------|-----------|-----------------|-------------|
| `menu_requested` | Menu button click | `None` | Opens main menu |
| `undo_requested` | Undo button click | `None` | Requests undo operation |
| `redo_requested` | Redo button click | `None` | Requests redo operation |
| `import_requested` | Import button click | `None` | Opens file dialog to import image |
| `save_requested` | Save button click | `None` | Saves current image |
| `zoom_changed` | Zoom buttons | `{'zoom_delta': float}` | Zoom change delta (0.1 or -0.1) |
| `edit_requested` | Edit button click | `None` | Opens edit popup |
| `crop_requested` | Crop button click | `None` | Opens crop popup |
| `search_requested` | Search submit | `{'query': str}` | Search query string |
| `show_message` | Command execution | `{'type': str, 'text': str}` | Message type (error/info) and text |
| `restart_requested` | /restart command | `None` | Restarts application |

### Photo Viewer (`photo_viewer.py`)
| Event | Publisher | Data Parameters | Description |
|-------|-----------|-----------------|-------------|
| `zoom_requested` | Ctrl+MouseWheel | `{'zoom_delta': float}` | Zoom delta from mouse wheel |

### Edit Panel (`edit_panel.py`)
| Event | Publisher | Data Parameters | Description |
|-------|-----------|-----------------|-------------|
| `edit_brightness_changed` | Brightness slider/entry | `{'value': float}` | Brightness factor (0.0 - 2.0) |
| `edit_rotation_changed` | Rotation slider/entry | `{'value': float}` | Rotation angle in degrees (-180 to 180) |

### Image Popups (`edit_popup.py`, `crop_popup.py`)
| Event | Publisher | Data Parameters | Description |
|-------|-----------|-----------------|-------------|
| `image_operation_applied` | Apply button in popup | `Image.Image` | Modified PIL Image object |

### Image Controller (`image_controller.py`)
| Event | Publisher | Data Parameters | Description |
|-------|-----------|-----------------|-------------|
| `image_loaded` | Import handler | `{'image': Image.Image}` | Successfully loaded PIL Image |
| `image_modified` | Operation handler | `{'image': Image.Image}` | Modified PIL Image |

### Workspace (`workspace.py`)
| Event | Publisher | Data Parameters | Description |
|-------|-----------|-----------------|-------------|
| `panel_configuration_changed` | Panel manager | `{'panels': dict}` | Panel configuration settings |

### Panel Container (`panel_container.py`)
| Event | Publisher | Data Parameters | Description |
|-------|-----------|-----------------|-------------|
| `panel_order_changed` | Panel reordering | `None` | Panel order has changed |

---

## Subscribed Events

### Top Bar (`top_bar.py`)
| Event | Handler | Data Used | Action |
|-------|---------|-----------|--------|
| `image_loaded` | `_on_image_loaded()` | `data` (dict) | Enables save/zoom/edit/crop buttons |
| `image_modified` | `_on_image_modified()` | `data` (dict) | Placeholder for image modification reactions |
| `undo_available` | `_update_undo_button()` | `available` (bool) | Enables/disables undo button |
| `redo_available` | `_update_redo_button()` | `available` (bool) | Enables/disables redo button |

### Photo Viewer (`photo_viewer.py`)
| Event | Handler | Data Used | Action |
|-------|---------|-----------|--------|
| `image_loaded` | `_on_image_update()` | `data['image']` (Image) | Displays loaded image |
| `image_modified` | `_on_image_update()` | `data['image']` (Image) | Updates display with modified image |
| `zoom_changed` | `_on_zoom_changed()` | `data['zoom_delta']` (float) | Applies zoom changes (0.1 - 10.0x) |

### Workspace (`workspace.py`)
| Event | Handler | Data Used | Action |
|-------|---------|-----------|--------|
| `panel_configuration_changed` | `_on_panel_configuration_changed()` | `data['panels']['position']` (str) | Reorganizes panels (left/right) |

### Panel Container (`panel_container.py`)
| Event | Handler | Data Used | Action |
|-------|---------|-----------|--------|
| `panel_order_changed` | `_on_panel_order_changed()` | `data` (dict) | Handles panel reordering |

### Image Controller (`image_controller.py`)
| Event | Handler | Data Used | Action |
|-------|---------|-----------|--------|
| `import_requested` | `_handle_import()` | `None` | Opens file dialog, loads image, publishes `image_loaded` |
| `save_requested` | `_handle_save()` | `None` | Saves current image to file |
| `undo_requested` | `_handle_undo()` | `None` | Reverts to previous state, publishes `image_modified` |
| `redo_requested` | `_handle_redo()` | `None` | Reapplies undone state, publishes `image_modified` |
| `image_operation_applied` | `_handle_operation()` | `modified_image` (Image) | Saves operation, publishes `image_modified` |

---

## Event Flow Examples

### Import Image Flow
```
User clicks Import → "import_requested" published
  ↓
ImageController receives "import_requested"
  ↓
Opens file dialog, loads image
  ↓
Publishes "image_loaded" with {'image': Image}
  ↓
PhotoViewer receives "image_loaded" → displays image
TopBar receives "image_loaded" → enables buttons
```

### Edit Image Flow
```
User modifies brightness in EditPanel → "edit_brightness_changed" published with {'value': 1.5}
  ↓
(Could be handled by controller, currently placeholder)
  ↓
User applies changes in popup → "image_operation_applied" published with Image
  ↓
ImageController receives "image_operation_applied"
  ↓
Publishes "image_modified" with {'image': Image}
  ↓
PhotoViewer receives "image_modified" → updates display
```

### Zoom Flow
```
User scrolls Ctrl+MouseWheel → "zoom_requested" published with {'zoom_delta': 0.1}
  ↓
PhotoViewer receives "zoom_requested"
  ↓
Applies zoom change (clamps to 0.1 - 10.0)
  ↓
Updates display at new zoom level
```

---

## Placeholder/Unimplemented Events

These events are published but have no subscribers (future features):
- `menu_requested` - Main menu functionality not yet implemented
- `undo_available` - Undo/redo state tracking not yet published
- `redo_available` - Undo/redo state tracking not yet published
- `restart_requested` - Restart functionality not yet implemented
- `show_message` - Message display system not yet implemented
- `panel_order_changed` - Panel reordering not yet implemented
