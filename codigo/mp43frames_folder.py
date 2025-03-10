import cv2
import os

# set the folder name
parent_folder_name = "VIDEOS"

counter = 0

# read video files recursively in folder
for root, dirs, files in os.walk(parent_folder_name):
    for file in files:
        counter += 1
        if file.endswith(".MOV") or file.endswith(".MP4"):
            file_video_name = os.path.join(root, file)
            folder_name = file_video_name.split(".")[0]

            print(file_video_name)
            print(folder_name)
            # check if the video file exists
            if not os.path.exists(file_video_name):
                print("The video file does not exist.")
                exit()

            # create the folder
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)
                print(f"Folder {folder_name} created.")

            # capture the video
            cap = cv2.VideoCapture(file_video_name)
            # get the frame rate and frame count
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

            # loop through the video and save the frames
            for i in range(int(frame_count/fps)):
                arr_frame=[]
                arr_lap=[]
                for j in range(fps):
                    success, frame = cap.read()
                    # get Laplacian of the frame
                    laplacian = cv2.Laplacian(frame, cv2.CV_64F).var()

                    # if the Laplacian is greater than 5, save the frame
                    if laplacian > 5:
                        arr_lap.append(laplacian)
                        arr_frame.append(frame)

                # get the frame with the highest Laplacian
                if len(arr_lap) > 0:
                    selected_frame = arr_frame[arr_lap.index(max(arr_lap))]
                    # save the frame to folder_name applying left padding to the frame number
                    cv2.imwrite(f"{folder_name}/A_V_000{counter}_{str(i+1).zfill(4)}.jpg", selected_frame)
                    print(f"Frame '{str(i).zfill(4)}.jpg' saved to folder: {folder_name}.")
                else:
                    print(f"No frame saved to folder: {folder_name} for second {i}.")

