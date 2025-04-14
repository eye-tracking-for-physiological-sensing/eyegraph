import dv_processing as dv
import cv2 as cv
from datetime import timedelta
import numpy as np
import os

# Hardcoded VGA resolution
resolution = (346, 260)

directory = './userStudy_eyeTracking_Davis346'

# directory = os.fsencode(directory)

num_events = 0
frame_count = 0
    
for file in os.listdir(directory):
    # path_to_file = os.fsdecode(file)
    if file.endswith(".aedat4"): 
        # print(os.path.join(directory, filename))
        # continue
        path_to_file = os.path.join(directory, file)
        reader = dv.io.MonoCameraRecording(path_to_file)

        # Print file path and camera name
        print(f"Checking available streams in [{path_to_file}] for camera name [{reader.getCameraName()}]:")

        # Check if event stream is available
        if reader.isEventStreamAvailable():
            # Check the resolution of event stream
            resolution = reader.getEventResolution()

            # Print that the stream is present and its resolution
            print(f"  * Event stream with resolution [{resolution}]")

        # Check if frame stream is available
        if reader.isFrameStreamAvailable():
            # Check the resolution of frame stream
            resolution = reader.getFrameResolution()

            # Print that the stream is available and its resolution
            print(f"  * Frame stream with resolution [{resolution}]")

        # Check if IMU stream is available
        if reader.isImuStreamAvailable():
            # Print that the IMU stream is available
            print("  * IMU stream")

        # Check if trigger stream is available
        if reader.isTriggerStreamAvailable():
            # Print that the trigger stream is available
            print("  * Trigger stream")

        # Open any camera
        reader = dv.io.MonoCameraRecording(path_to_file)

        noise_1 = []
        noise_2 = []
        noise_3 = []

        # Run the loop while camera is still connected
        while reader.isRunning():
            # Read batch of events
            events = reader.getNextEventBatch()
            if events is not None:
                # Print received packet time range
                # print(f"{events}")

                event_count = len(events)
                num_events += event_count
                frame_count += 1

                # if event_count > 2000:

                # Initialize a background activity noise filter with 1-millisecond activity period
                filter = dv.noise.BackgroundActivityNoiseFilter(resolution, backgroundActivityDuration=timedelta(milliseconds=100))

                # Pass events to the filter
                filter.accept(events)

                # Call generate events to apply the noise filter
                filtered = filter.generateEvents()

                # Print out the reduction factor, which indicates the percentage of discarded events
                # print(f"Filter reduced number of events by a factor of {filter.getReductionFactor()}")

                noise_1.append(filter.getReductionFactor())

                # Use a visualizer instance to preview the events
                visualizer = dv.visualization.EventVisualizer(resolution)

                # Generate preview images of data input and output
                input = visualizer.generateImage(events)
                output = visualizer.generateImage(filtered)

                # Concatenate the images into a single image for preview
                preview = cv.hconcat([input, output])

                # Display the input and output images
                cv.namedWindow("preview", cv.WINDOW_NORMAL)
                cv.imshow("preview", preview)
                cv.waitKey()
            else:
                continue

path_to_file = './userStudy_eyeTracking_Davis346/3.aedat4'

print(np.mean(noise_1))
print(num_events)
print(frame_count)

reader = dv.io.MonoCameraRecording(path_to_file)

# Run the loop while camera is still connected
while reader.isRunning():
    # Read batch of events
    events = reader.getNextEventBatch()
    if events is not None:
        # Print received packet time range
        # print(f"{events}")

        filter = dv.noise.FastDecayNoiseFilter(resolution,
                                       halfLife=timedelta(milliseconds=100),
                                       subdivisionFactor=4,
                                       noiseThreshold=1.0)

        # Pass events to the filter
        filter.accept(events)

        # Call generate events to apply the noise filter
        filtered = filter.generateEvents()

        # the reduction factor, which indicates the percentage of discarded events
        noise_2.append(filter.getReductionFactor())

        # Use a visualizer instance to preview the events
        visualizer = dv.visualization.EventVisualizer(resolution)

        # Generate preview images of data input and output
        input = visualizer.generateImage(events)
        output = visualizer.generateImage(filtered)

        # Concatenate the images into a single image for preview
        preview = cv.hconcat([input, output])

        # Display the input and output images
        cv.namedWindow("preview", cv.WINDOW_NORMAL)
        cv.imshow("preview", preview)
        cv.waitKey()
print(np.mean(noise_2))

reader = dv.io.MonoCameraRecording(path_to_file)

# Run the loop while camera is still connected
while reader.isRunning():
    # Read batch of events
    events = reader.getNextEventBatch()
    if events is not None:
        # Print received packet time range
        # print(f"{events}")

        filter = dv.RefractoryPeriodFilter(resolution, timedelta(milliseconds=100))

        # Pass events to the filter
        filter.accept(events)

        # Call generate events to apply the filter
        filtered = filter.generateEvents()

        #the number of events after filtering
        noise_3.append(len(filtered)/len(events))

print(np.mean(noise_3))