import bpy

# Store the initial positions of markers
initial_marker_positions = {}


# Function to rename markers based on their frame number
def rename_markers():
    for marker in bpy.context.scene.timeline_markers:
        # Check if the marker name is in the format "F=X"
        if marker.name.startswith("F_") and marker.name[2:].isdigit():
            # Rename the marker to its current frame number
            marker.name = f"F_{marker.frame}"
        elif not marker.name.startswith("F_"):
            # If the marker has a user-defined name, do not rename it
            continue

# Function to check if markers have moved
def check_marker_movement():
    global initial_marker_positions
    moved = False

    for marker in bpy.context.scene.timeline_markers:
        # Check if the marker's frame has changed
        if marker.name not in initial_marker_positions:
            initial_marker_positions[marker.name] = marker.frame
        elif initial_marker_positions[marker.name] != marker.frame:
            moved = True
            initial_marker_positions[marker.name] = marker.frame  # Update the position

    return moved

# Function to update marker names
def update_markers():
    if check_marker_movement():
        # Rename markers if they have moved
        rename_markers()

# Function to add marker with automatic naming
def add_marker(frame):
    marker_name = f"F_{frame}"
    bpy.context.scene.timeline_markers.new(name=marker_name, frame=frame)
    initial_marker_positions[marker_name] = frame  # Initialize the position

# Timer function to periodically check for marker movement
def marker_movement_timer():
    update_markers()
    return 0.05  # Check every 0.05 seconds

# Register the frame change handler
bpy.app.handlers.frame_change_pre.append(lambda scene: update_markers())
# Register the timer
bpy.app.timers.register(marker_movement_timer)
