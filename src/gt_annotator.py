import dv_processing as dv
import cv2 as cv
import json
import os

# Global variables to store mouse click coordinates
mouse_coordinates = []

# Global variable to store annotation data
annotations = []

def on_mouse_click(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONUP:
        mouse_coordinates.append((x, y))
        if len(mouse_coordinates) == 2:
            cv.setMouseCallback("Preview", on_mouse_click)  # Set the callback again for the next frame

filename = "/file/path"
# Open any camera
reader = dv.io.MonoCameraRecording(filename)

# print(reader)

visualizer = dv.visualization.EventVisualizer(reader.getEventResolution())
visualizer.setBackgroundColor(dv.visualization.colors.white())
visualizer.setPositiveColor(dv.visualization.colors.iniBlue())
visualizer.setNegativeColor(dv.visualization.colors.darkGrey())
frame_count = 0

# Extract date and time information from the AEDAT4 filename
filename_without_extension = os.path.splitext(os.path.basename(filename))[0]
date_time_info = filename_without_extension.split("-")[0]
output_file = f"annotations_{date_time_info}.json"

# Initialize a preview window
cv.namedWindow("Preview", cv.WINDOW_NORMAL)

# Open the JSON file in append mode
while reader.isRunning():
    # Read batch of events
    events = reader.getNextEventBatch()

    if events is not None:
        skipped = False
        event_count = len(events)
        if event_count > 1000: #17000 > 
            frame_count += 1
            frame = visualizer.generateImage(events)
            frame = cv.rotate(frame, cv.ROTATE_90_CLOCKWISE)
            frame = cv.rotate(frame, cv.ROTATE_90_CLOCKWISE)
            print("frame no:", frame_count)
            # Show the image to the user
            cv.imshow("Preview", frame)
            # Set the mouse callback for the first time
            cv.setMouseCallback("Preview", on_mouse_click)

            # Check if the user has clicked twice to get center coordinates
            mouse_coordinates.clear()
            while len(mouse_coordinates) < 2:
                key = cv.waitKey(1) & 0xFF
                if key == ord('q'):  # Press 'q' to exit
                    break
                if key ==ord('s'):
                    print("skipping the frame", frame_count)
                    skipped = True
                    break
            if skipped == True:
                skipped = False
                continue
            if len(mouse_coordinates) == 2:
                center_coordinates = mouse_coordinates.pop(0)
                radius = 50  # Set the radius to 50
                color = (0, 255, 0)  # Green color in BGR
                thickness = 2
                frame = cv.circle(frame, center_coordinates, radius, color, thickness)

                cv.imshow("Preview", frame)

                # Log annotation data
                annotations.append({
                    "frame_number": frame_count,
                    "filename": date_time_info,
                    "center_x": center_coordinates[0],
                    "center_y": center_coordinates[1],
                    "radius": radius
                })

                # Append the annotation data to the JSON file after each frame
                with open(output_file, "a") as jsonfile:
                    json.dump({
                        "frame_number": frame_count,
                        "filename": date_time_info,
                        "center_x": center_coordinates[0],
                        "center_y": center_coordinates[1],
                        "radius": radius
                    }, jsonfile)
                    jsonfile.write('\n')  # Add a newline for better readability

            # Wait for a key press to move on to the next frame
            key = cv.waitKey(0) & 0xFF
            if key == ord('q'):  # Press 'q' to exit
                break

cv.destroyAllWindows()
print(f"Annotations have been saved to {output_file}")
