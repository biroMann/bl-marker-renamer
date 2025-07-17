# Blender Marker Renamer

## Overview

The Blender Marker Renamer is a Python script designed for Blender users who want to automatically rename timeline markers based on their frame positions. This tool enhances the workflow by providing real-time updates to marker names as they are moved in the timeline, ensuring a more organized and efficient animation process.

## Features

- Automatically renames markers in the format `F_X`, where `X` is the current frame number.
- Provides real-time updates as markers are moved in the timeline.
- If markers are renamed with a custom name, they will not be automatically renamed.
- Easy to integrate into your Blender projects.

## Installation

1. Open Blender.
2. Go to the Scripting workspace.
3. Create a new text file and copy the script code into it.
4. Run the script to activate the marker renaming functionality.
5. **Optional**: If you want the script to work automatically every time Blender starts, enable the "Register" option in the Scripting layout under the "Text" dropdown menu.

## Usage

- Add markers to your timeline; Blender by default will add them with names starting with `F_` (e.g., `F_1`, `F_2`).
- Move the markers in the timeline to see their names update automatically to reflect their current frame positions.
- **Note**: Manually renamed markers will not be renamed by the script, except in the case where the marker is renamed to the default naming of Blender `F_` (e.g., `F_1`, `F_2`).

## Code

```python
import bpy

# Store the initial positions of markers
initial_marker_positions = {}

# Function to rename markers based on their frame number
def rename_markers():
    for marker in bpy.context.scene.timeline_markers:
        if marker.name.startswith("F_") and marker.name[2:].isdigit():
            marker.name = f"F_{marker.frame}"
        elif not marker.name.startswith("F_"):
            continue

# Function to check if markers have moved
def check_marker_movement():
    global initial_marker_positions
    moved = False

    for marker in bpy.context.scene.timeline_markers:
        if marker.name not in initial_marker_positions:
            initial_marker_positions[marker.name] = marker.frame
        elif initial_marker_positions[marker.name] != marker.frame:
            moved = True
            initial_marker_positions[marker.name] = marker.frame

    return moved

# Function to update marker names
def update_markers():
    if check_marker_movement():
        rename_markers()

# Function to add marker with automatic naming
def add_marker(frame):
    marker_name = f"F_{frame}"
    bpy.context.scene.timeline_markers.new(name=marker_name, frame=frame)
    initial_marker_positions[marker_name] = frame

# Timer function to periodically check for marker movement
def marker_movement_timer():
    update_markers()
    return 0.1  # Check every 0.1 seconds

# Register the frame change handler
bpy.app.handlers.frame_change_pre.append(lambda scene: update_markers())
# Register the timer
bpy.app.timers.register(marker_movement_timer)
```

