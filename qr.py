import cv2
import numpy as np
from pyapriltags import Detector
import time

# ==========================================
# CONFIGURATION
# ==========================================

# Size of your AprilTag in meters
TAG_SIZE = 0.081  # 5 cm


# Approximate camera parameters
# These MUST ideally be obtained through camera calibration.
CAMERA_MATRIX = np.array([[916.88082537, 0.,706.6202824 ],
 [  0.,907.83200628,504.31084818],
 [  0.,0.,1.]], dtype=np.float64)

DIST_COEFFS = np.array([[-1.20914806e-01,7.52312129e-01,2.04870239e-03,-7.32500653e-04,-1.58114493e+00]])



detector = Detector(
    families="tag36h11",
    nthreads=1,
    quad_decimate=1.0,
    quad_sigma=0.0,
    refine_edges=1,
    decode_sharpening=0.25
)


half = TAG_SIZE / 2

object_points = np.array([
    [-half,  half, 0],
    [ half,  half, 0],
    [ half, -half, 0],
    [-half, -half, 0]
], dtype=np.float64)


class camera():
    def __init__(self):
        self.cap=cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Cannot open webcam")
            exit()

    def get_frame(self):
        return self.cap.read()

cam=camera()
while True:

    ret,frame=cam.get_frame()

    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    results = detector.detect(gray)

    ds=time.time()
    for tag in results:

        image_points = np.array(
            tag.corners,
            dtype=np.float64
        )


       
        success, rvec, tvec = cv2.solvePnP(
            object_points,
            image_points,
            CAMERA_MATRIX,
            DIST_COEFFS,
            flags=cv2.SOLVEPNP_IPPE_SQUARE
        )

        if success:

           
            x = tvec[0][0]
            y = tvec[1][0]
            z = tvec[2][0]

            # Distance from camera to tag
            distance = np.sqrt(
                x*x + y*y + z*z
            )


            rotation_matrix, _ = cv2.Rodrigues(rvec)

            # Convert rotation matrix to Euler angles
            sy = np.sqrt(
                rotation_matrix[0, 0] ** 2 +
                rotation_matrix[1, 0] ** 2
            )

            singular = sy < 1e-6

            if not singular:

                roll = np.arctan2(
                    rotation_matrix[2, 1],
                    rotation_matrix[2, 2]
                )

                pitch = np.arctan2(
                    -rotation_matrix[2, 0],
                    sy
                )

                yaw = np.arctan2(
                    rotation_matrix[1, 0],
                    rotation_matrix[0, 0]
                )

            else:

                roll = np.arctan2(
                    -rotation_matrix[1, 2],
                    rotation_matrix[1, 1]
                )

                pitch = np.arctan2(
                    -rotation_matrix[2, 0],
                    sy
                )

                yaw = 0


            # Convert radians → degrees

            roll = np.degrees(roll)
            pitch = np.degrees(pitch)
            yaw = np.degrees(yaw)


            corners = tag.corners.astype(int)

            for i in range(4):

                p1 = tuple(corners[i])
                p2 = tuple(corners[(i + 1) % 4])

                cv2.line(
                    frame,
                    p1,
                    p2,
                    (0, 255, 0),
                    2
                )


            
            center = tuple(
                tag.center.astype(int)
            )

            cv2.putText(
                frame,
                f"ID: {tag.tag_id}",
                center,
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                f"Distance: {distance:.3f} m",
                (20, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (30, 30, 30),
                2
            )

            cv2.putText(
                frame,
                f"X: {x:.2f} Y: {y:.2f} Z: {z:.2f}",
                (20, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (30, 30, 30),
                2
            )

            cv2.putText(
                frame,
                f"Yaw: {yaw:.1f}  Pitch: {pitch:.1f}  Roll: {roll:.1f}",
                (20, 90),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (30, 30, 30),
                2
            )

    cv2.putText(
        frame,
        f"fps:{1/(time.time()-ds)}",
        (20, 120),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (30, 30, 30),
        2
    )
    cv2.imshow(
        "AprilTag Pose",
        frame
    )


    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()