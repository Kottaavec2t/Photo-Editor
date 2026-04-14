# Event Bus Documentation (AI GENERATED, MAY HAVE ERRORS)

## Published Events

### Top Bar (`top_bar.py`)
| Event | Publisher | Data Parameters | Description |
|-------|-----------|-----------------|-------------|
| `new_requested` | New button click | `None` | Requests creation of new blank image |
| `undo_requested` | Undo button click | `None` | Requests undo operation |
| `redo_requested` | Redo button click | `None` | Requests redo operation |
| `import_requested` | Import button click | `None` | Opens file dialog to import image |
| `save_requested` | Save button click | `None` | Saves current image |
| `zoom_changed` | Zoom buttons | `{'zoom_delta': float}` | Zoom change delta (0.1 or -0.1) |
| `search_requested` | Search submit | `{'query': str}` | Search query string |
| `show_message` | Command execution | `{'type': str, 'text': str}` | Message type (error/info) and text |
| `restart_requested` | /restart command | `{'args': list}` | Restarts application with optional arguments |

### Photo Viewer (`photo_viewer.py`)
| Event | Publisher | Data Parameters | Description |
|-------|-----------|-----------------|-------------|
| `zoom_changed` | Ctrl+MouseWheel | `{'zoom_delta': float}` | Zoom delta from mouse wheel |

### Edit Panel (`edit_panel.py`)
| Event | Publisher | Data Parameters | Description |
|-------|-----------|-----------------|-------------|
| `image_operation_applied` | Brightness slider/entry | `{'value': float, 'operation_type': 'brightness', 'save': bool}` | Brightness adjustment (0.0 - 2.0) |
| `image_operation_applied` | Rotation slider/entry | `{'angle': float, 'operation_type': 'rotation', 'save': bool}` | Rotation angle in degrees (-180 to 180) |
| `image_operation_applied` | Grayscale switch | `{'value': bool, 'operation_type': 'grayscale', 'save': bool}` | Toggle grayscale effect |

### Image Controller (`image_controller.py`)
| Event | Publisher | Data Parameters | Description |
|-------|-----------|-----------------|-------------|
| `image_loaded` | New/Import handler | `{'image': Image.Image}` | Successfully loaded PIL Image |
| `image_modified` | Operation/undo/redo handler | `{'image': Image.Image}` | Modified PIL Image |
| `undo_available` | Undo/Redo/Operation handler | `{'available': bool}` | Undo operation is available |
| `redo_available` | Undo/Redo/Operation handler | `{'available': bool}` | Redo operation is available |
| `history_updated` | Operation/undo/redo handler | `{'undo_stack': list, 'redo_stack': list}` | Updated command history stacks |
| `info_notification` | Info notification | `{'corpse': str}` | Info message to display |
| `error_notification` | Error notification | `{'corpse': str}` | Error message to display |
| `warning_notification` | Warning notification | `{'corpse': str}` | Warning message to display |

### Workspace (`workspace.py`)
| Event | Publisher | Data Parameters | Description |
|-------|-----------|-----------------|-------------|
| `panel_configuration_changed` | Panel manager | `{'panels': dict}` | Panel configuration settings |

---

## Subscribed Events

### Top Bar (`top_bar.py`)
| Event | Handler | Data Used | Action |
|-------|---------|-----------|--------|
| `image_loaded` | `_on_image_loaded()` | `data` (dict) | Enables save/zoom buttons |
| `image_modified` | `_on_image_modified()` | `data` (dict) | Reacts to image modification |
| `undo_available` | `_update_undo_button()` | `data['available']` (bool) | Enables/disables undo button |
| `redo_available` | `_update_redo_button()` | `data['available']` (bool) | Enables/disables redo button |

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

### History Panel (`history_panel.py`)
| Event | Handler | Data Used | Action |
|-------|---------|-----------|--------|
| `history_updated` | `_update_history()` | `data['undo_stack']`, `data['redo_stack']` (list) | Updates displayed command history |

### Image Controller (`image_controller.py`)
| Event | Handler | Data Used | Action |
|-------|---------|-----------|--------|
| `new_requested` | `_handle_new()` | `None` | Creates new blank image, publishes `image_loaded` and `history_updated` |
| `import_requested` | `_handle_import()` | `None` | Opens file dialog, loads image, publishes `image_loaded` and `history_updated` |
| `save_requested` | `_handle_save()` | `None` | Saves current image to file |
| `undo_requested` | `_handle_undo()` | `None` | Reverts to previous state, publishes `image_modified`, `undo_available`, `redo_available`, `history_updated` |
| `redo_requested` | `_handle_redo()` | `None` | Reapplies undone state, publishes `image_modified`, `undo_available`, `redo_available`, `history_updated` |
| `image_operation_applied` | `_handle_operation()` | `data['operation_type']`, `data['value']`/`data['angle']`, `data['save']` | Applies image operation, publishes `image_modified`, `undo_available`, `redo_available`, `history_updated` |

### Notifications Controller (`notifications_controller.py`)
| Event | Handler | Data Used | Action |
|-------|---------|-----------|--------|
| `info_notification` | `_info_notification()` | `data['title']`, `data['corpse']` | Displays info message dialog |
| `error_notification` | `_error_notification()` | `data['title']`, `data['corpse']` | Displays error message dialog |
| `warning_notification` | `_warning_notification()` | `data['title']`, `data['corpse']` | Displays warning message dialog |

---

## Placeholder/Unimplemented Events

These events are defined in code but may not have full handlers yet:
- `show_message` - Used for command feedback, may need enhanced message system
- `search_requested` - Search functionality is published but may need implementation
