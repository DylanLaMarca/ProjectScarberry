import cv2
import numpy as np
import os
import base64

def convert_to_cv(image):
    decoded = base64.decodestring(image)
    numpy_image = np.fromstring(decoded,dtype=np.byte)
    return cv2.imdecode(numpy_image,cv2.IMREAD_REDUCED_GRAYSCALE_8)

def save_image(image,formated_number,image_direcoty='images',name='rawXimeaimage',extention='.TIFF'):
    cv2.imwrite('{}\\{}_{}{}'.format(image_direcoty, name, formated_number, extention),image)

def format_number(number,padding):
    formated_number = ''
    for count in range(int(padding) - len(str(number))):
        formated_number += '0'
    return formated_number + str(number)

def get_contours(image, blur_val, thresh_val):
    blur = cv2.GaussianBlur(image,(int(blur_val),int(blur_val)),0)
    #show_image(blur)
    #grey_image = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
    #show_image(grey_image)
    ret, thresh = cv2.threshold(blur,int(thresh_val),255,cv2.THRESH_BINARY)
    #show_image(thresh)
    im2, contours, hierarchy = cv2.findContours(thresh, 1, 2)
    return contours

def show_image(image):
    cv2.imshow('image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def get_data(image,blur_val,thresh_val):
    contours = get_contours(image, blur_val, thresh_val)
    data = []
    for contour in contours:
            current_roi = {}
            moments = cv2.moments(contour)
            centroid_x = 0
            centroid_y = 0
            try:
                centroid_x = int(moments['m10'] / moments['m00'])
                centroid_y = int(moments['m01'] / moments['m00'])
            except ZeroDivisionError:
                pass
            current_roi['Centroid'] = (centroid_x,centroid_y)
            [vx, vy, x, y] = cv2.fitLine(contour, cv2.DIST_L2, 0, 0.01, 0.01)
            current_roi['Vector'] = {'vx':vx[0],'vy':vy[0],'x':x[0],'y':y[0]}
            area = cv2.contourArea(contour)
            current_roi['Area'] = area
            perimeter = cv2.arcLength(contour, True)
            current_roi['ApproximatePerimeter'] = perimeter
            MA = 0
            ma = 0
            angle = 0
            try:
                (x, y), (MA, ma), angle = cv2.fitEllipse(contour)
            except cv2.error:
                pass
            current_roi['Axes'] = {'Major Axis':MA,'Minor Axis':ma}
            current_roi['Direction'] = angle
            data.append(current_roi)
    return data

def draw_and_data(image, new_image_filename, data_filename, blur_val, thresh_val, draw_rois=False, draw_centroid=False, draw_count=False, draw_vectors=False):
    out_image = cv2.cvtColor(image, cv2.COLOR_BAYER_GR2RGB)
    contours = get_contours(image, blur_val, thresh_val)
    data = []
    count = 0
    for contour in contours:
        current_roi = {}
        if draw_rois:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(out_image, (x, y), (x + w, y + h), (0, 0, 255), 1)
        centroid_x = 0
        centroid_y = 0
        moments = cv2.moments(contour)
        try:
            centroid_x = int(moments['m10'] / moments['m00'])
            centroid_y = int(moments['m01'] / moments['m00'])
            if draw_centroid:
                cv2.circle(out_image, (centroid_x, centroid_y), 1, (0, 0, 255), -1)
            if draw_count:
                cv2.putText(out_image,
                            str(count),
                            (centroid_x+2,
                             centroid_y+2),
                            cv2.FONT_HERSHEY_COMPLEX_SMALL,
                            .5,
                            (0,255,0))
        except ZeroDivisionError:
            pass
        current_roi['Centroid'] = (centroid_x, centroid_y)
        rows, cols = image.shape[:2]
        [vx, vy, x, y] = cv2.fitLine(contour, cv2.DIST_L2, 0, 0.01, 0.01)
        current_roi['Vector'] = {'vx': vx[0], 'vy': vy[0], 'x': x[0], 'y': y[0]}
        if draw_vectors:
            lefty = int((-x * vy / vx) + y)
            righty = int(((cols - x) * vy / vx) + y)
            cv2.line(out_image, (cols - 1, righty), (0, lefty), (0, 0, 255), 1)
        MA = 0
        ma = 0
        angle = 0
        try:
            if len(contour) >= 5:
                (x, y), (MA, ma), angle = cv2.fitEllipse(contour)
        except cv2.error:
            pass
        current_roi['Axes'] = {'Major Axis': MA, 'Minor Axis': ma}
        current_roi['Direction'] = angle
        area = cv2.contourArea(contour)
        current_roi['Area'] = area
        perimeter = cv2.arcLength(contour, True)
        current_roi['ApproximatePerimeter'] = perimeter
        data.append(current_roi)
        count+=1
    # show_image(image)
    save_data(data,data_filename)
    cv2.imwrite(new_image_filename, out_image)

def save_data(data,file_name):
    filename = file_name
    file = open(filename, 'w')
    file.truncate()
    count = 0
    for contour in data:
        file.write('Contour Cluster {}:\n'.format(count))
        file.write('    Centroid: {}\n'.format(contour.get('Centroid')))
        file.write('    Axes:\n')
        file.write('        Major Axis: {}\n'.format(contour.get('Axes').get('Major Axis')))
        file.write('        Minor Axis: {}\n'.format(contour.get('Axes').get('Minor Axis')))
        file.write('    Direction: {}\n'.format(contour.get('Direction')))
        file.write('    ApproximatePerimeter: {}\n'.format(contour.get('ApproximatePerimeter')))
        file.write('    Vector:\n')
        file.write('        x:  {}\n'.format(contour.get('Vector').get('x')))
        file.write('        y:  {}\n'.format(contour.get('Vector').get('y')))
        file.write('        vx: {}\n'.format(contour.get('Vector').get('vx')))
        file.write('        vy: {}\n'.format(contour.get('Vector').get('vy')))
        count+=1
    file.close()