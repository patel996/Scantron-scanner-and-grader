import sys
import numpy as np
import cv2
import imutils
from imutils import contours
from answerKey import *

def main():
    image = cv2.imread(sys.argv[1])

    grayed = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    thresh, thresh_image = cv2.threshold(grayed, 205, 255, cv2.THRESH_BINARY_INV)

    #find the contours (scantron bubbles)
    contour_image = cv2.findContours(thresh_image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(contour_image)

    #sort contours top to bottom
    big_cnt = sortContours(cnts)

    #get the mapped answer key
    ans_key = get_mapped_answers()

    #draw contours and mask to see one contour at a time (one scantron bubble at a time)
    non_zero_pixels = nonzeroPixelInCounters(image, thresh_image, big_cnt)

    #score
    scoreSheet(big_cnt, image, non_zero_pixels, ans_key)


def sortContours(cnts):
    (cnts, boundingBoxes) = contours.sort_contours(cnts, method='top-to-bottom')

    big_cnt = []
    moment = []
    x_coord = []

    #find x-axis moments to sort left to right
    for c in cnts:
        if cv2.contourArea(c) > 300:
            M = cv2.moments(c)
            moment.append(M)
            big_cnt.append(c)
            cx = int(M['m10']/M['m00'])
            x_coord.append(cx)

    #zip sort
    num = int(len(big_cnt) / 5)
    for i in range(num):
        x_coord[5*i : 5*i + 5 ], big_cnt[5*i : 5*i + 5 ] = zip(*sorted(zip(x_coord[5*i : 5*i + 5 ], big_cnt[5*i : 5*i + 5 ])))

    return big_cnt

def nonzeroPixelInCounters(image, thresh_image, big_cnt):
    non_zero_counts = []
    count = 0
    temp = []

    for c in big_cnt:
        fill_contour = cv2.drawContours(image.copy(), [c], -1, (255,0,0), -1)
        mask = cv2.inRange(fill_contour, np.array([255,0,0]),np.array([255,0,0]) )
        masked_one_at_a_time = cv2.bitwise_and(thresh_image, thresh_image, mask = mask)
        cv2.imshow("One scantron masked at a time", masked_one_at_a_time)
        cv2.waitKey(0)
        #record number of non-zero pixels
        temp.append(cv2.countNonZero(masked_one_at_a_time))
        count = count + 1
        if (count == 5):
            non_zero_counts.append(temp)
            temp = []
            count = 0

    return non_zero_counts

def scoreSheet(big_cnt, image, non_zero_counts, ans_key):
    #extract the marked answers for each qustion
    marked_ans = []
    for c in non_zero_counts:
        marked = c.index(max(c))
        marked_ans.append(marked + 1)

    #score
    score = 0
    fill = image.copy()
    for i in range(len(ans_key)):
        if ans_key[i] == marked_ans[i]:
            score = score + 20
            fill = cv2.drawContours(fill, [big_cnt[5*i + marked_ans[i] - 1]], -1, (0,255,0), 2)
        else:
            fill = cv2.drawContours(fill, [big_cnt[5*i + marked_ans[i] - 1]], -1, (0,0,255), 2)

    scored_sheet = cv2.putText(fill, str(score), (0,15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1, cv2.LINE_AA )
    cv2.imshow("Scored",scored_sheet)
    cv2.waitKey(0)

main()
