import cv2


def image2binary(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    canny = cv2.Canny(blur, 110, 200)
    return canny


def ground(frame):
    binary = image2binary(frame, 150)

    (_, contours, roi_hierarchy) = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    ground_list = []
    for i in range(len(contours)):
        x, y, w, h = cv2.boundingRect(contours[i])
        rect_area = w * h
        if roi_hierarchy[0][i][3] is not -1:
            if rect_area >= 250:
                ground_list.append([x, y, x+w, y+h])

    ground_list.sort()
    thr = 40
    for i in range(len(ground_list)):
        j = i+1
        while j < len(ground_list):
            merge = False
            if ground_list[i][2] + thr >= ground_list[j][0] >= ground_list[i][2]:
                ground_list[i][1] = min(ground_list[i][1], ground_list[j][1])
                ground_list[i][2] = ground_list[j][2]
                del ground_list[j]
                merge = True

            if merge is False:
                j += 1
            else:
                j = i + 1

    for i in range(len(ground_list)):
        x, y, w, h = ground_list[i]
        cv2.rectangle(frame, (x, y), (w, h), (255, 0, 0), 2)

    return
