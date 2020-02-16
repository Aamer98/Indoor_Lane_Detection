
import cv2
import numpy as np

def make_points(frame, line):
    height, width, _ = frame.shape
    slope, intercept = line
    y1 = height  # bottom of the frame
    y2 = int(y1 * 1 / 2)  # make points from middle of the frame down

    # bound the coordinates within the frame
    x1 = max(-width, min(2 * width, int((y1 - intercept) / slope)))
    x2 = max(-width, min(2 * width, int((y2 - intercept) / slope)))
    return [[x1, y1, x2, y2]]

def main():
    camera = cv2.VideoCapture('lane22.mp4')
    camera.set(3,3840)
    camera.set(4,2160)

    while (camera.isOpened()):
        _, frame = camera.read()
        cv2.imshow('Original', frame)

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        cv2.imshow('HSV', hsv)
        lower_blue = np.array([60, 40, 40])
        upper_blue = np.array([150, 255, 255])
        mask = cv2.inRange(hsv, lower_blue, upper_blue)

        edges = cv2.Canny(mask, 200, 400)
        height, width = edges.shape
        mask = np.zeros_like(edges)

        # only focus bottom half of the screen
        polygon = np.array([[
            (0, height * 1 / 2),
            (width, height * 1 / 2),
            (width, height),
            (0, height),
        ]], np.int32)

        cv2.fillPoly(mask, polygon, 255)
        cropped_edges = cv2.bitwise_and(edges, mask)

        rho = 1  # distance precision in pixel, i.e. 1 pixel
        angle = np.pi / 180  # angular precision in radian, i.e. 1 degree
        min_threshold = 10  # minimal of votes
        line_segments = cv2.HoughLinesP(cropped_edges, rho, angle, min_threshold,
                                        np.array([]), minLineLength=8, maxLineGap=4)

        lane_lines = []

        height, width, _ = frame.shape
        left_fit = []
        right_fit = []

        boundary = 1 / 3
        left_region_boundary = width * (1 - boundary)  # left lane line segment should be on left 2/3 of the screen
        right_region_boundary = width * boundary  # right lane line segment should be on left 2/3 of the screen

        for line_segment in line_segments:
            for x1, y1, x2, y2 in line_segment:

                fit = np.polyfit((x1, x2), (y1, y2), 1)
                slope = fit[0]
                intercept = fit[1]
                if slope < 0:
                    if x1 < left_region_boundary and x2 < left_region_boundary:
                        left_fit.append((slope, intercept))
                else:
                    if x1 > right_region_boundary and x2 > right_region_boundary:
                        right_fit.append((slope, intercept))

        left_fit_average = np.average(left_fit, axis=0)
        if len(left_fit) > 0:
            height, width, _ = frame.shape
            slope, intercept = left_fit_average
            y1 = height  # bottom of the frame
            y2 = int(y1 * 1 / 2)  # make points from middle of the frame down

            # bound the coordinates within the frame
            x1 = max(-width, min(2 * width, int((y1 - intercept) / slope)))
            x2 = max(-width, min(2 * width, int((y2 - intercept) / slope)))
            lane_lines.append([x1, y1, x2, y2])

        right_fit_average = np.average(right_fit, axis=0)
        if len(right_fit) > 0:
            height, width, _ = frame.shape
            slope, intercept = right_fit_average
            y1 = height  # bottom of the frame
            y2 = int(y1 * 1 / 2)  # make points from middle of the frame down

            # bound the coordinates within the frame
            x1 = max(-width, min(2 * width, int((y1 - intercept) / slope)))
            x2 = max(-width, min(2 * width, int((y2 - intercept) / slope)))
            lane_lines.append([x1, y1, x2, y2])
        line_image = np.zeros_like(frame)
        line_color = (0, 255, 0)
        line_width = 2
        if lane_lines is not None:
            for line in lane_lines:
                print(lane_lines)
                [x1, y1, x2, y2]=line

                cv2.line(line_image, (x1, y1), (x2, y2), line_color, line_width)
        line_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)


        cv2.imshow("lane lines", line_image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
          break

    cv2.destroyAllWindows()


if __name__ == '__main__':
  main()
