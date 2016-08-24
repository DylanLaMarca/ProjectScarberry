import cv2
import numpy as np

class ProcessImage:
    @staticmethod
    def get_contours(image, blur_val, thresh_val):
        blur = cv2.GaussianBlur(image, (blur_val, blur_val), 0)
        #ProcessImage.show_image(blur)
        grey_image = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
        #ProcessImage.show_image(grey_image)
        ret, thresh = cv2.threshold(grey_image, thresh_val, 255, cv2.THRESH_BINARY)
        #ProcessImage.show_image(thresh)
        im2, contours, hierarchy = cv2.findContours(thresh, 1, 2)
        return contours

    @staticmethod
    def get_rois(image, blur_val, thresh_val):
        contours = ProcessImage.get_contours(image, blur_val, thresh_val)
        rois = range(len(contours))
        count = 0
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            roi = image[y:y + h, x:x + w]
            rois[count] = roi
            count+=1
        return rois

    @staticmethod
    def get_vectors(image, blur_val, thresh_val):
        contours = ProcessImage.get_contours(image, blur_val, thresh_val)
        count = 0
        vectors = np.empty((len(contours),4))
        for cnt in contours:
            [vx, vy, x, y] = cv2.fitLine(cnt, cv2.DIST_L2, 0, 0.01, 0.01)
            vectors[count][0] = vx
            vectors[count][1] = vy
            vectors[count][2] = int(x)
            vectors[count][3] = int(y)
            count+=1
        return vectors

    @staticmethod
    def draw(image,out_image,blur_val,thresh_val,rois=False,centroid=False,vectors=False,colour=(0,0,255)):
        contours = ProcessImage.get_contours(image, blur_val, thresh_val)
        for contour in contours:
            if rois:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 1)
            if centroid:
                moments = cv2.moments(contour)
                centroid_x = int(moments['m10'] / moments['m00'])
                centroid_y = int(moments['m01'] / moments['m00'])
                cv2.circle(image, (centroid_x, centroid_y), 1, (0, 0, 255), -1)
            if vectors:
                rows, cols = image.shape[:2]
                [vx, vy, x, y] = cv2.fitLine(contour, cv2.DIST_L2, 0, 0.01, 0.01)
                lefty = int((-x * vy / vx) + y)
                righty = int(((cols - x) * vy / vx) + y)
                cv2.line(image, (cols - 1, righty), (0, lefty), (0, 0, 255), 1)
        ProcessImage.show_image(image)

    @staticmethod
    def show_image(img):
        cv2.imshow('image', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    @staticmethod
    def get_data(image,blur_val,thresh_val,):
        contours = ProcessImage.get_contours(image, blur_val, thresh_val)
        data = []
        for contour in contours:
                current_roi = {}
                moments = cv2.moments(contour)
                centroid_x = int(moments['m10'] / moments['m00'])
                centroid_y = int(moments['m01'] / moments['m00'])
                current_roi['Centroid'] = (centroid_x,centroid_y)
                [vx, vy, x, y] = cv2.fitLine(contour, cv2.DIST_L2, 0, 0.01, 0.01)
                current_roi['Vector'] = {'vx':vx[0],'vy':vy[0],'x':x[0],'y':y[0]}
                area = cv2.contourArea(contour)
                current_roi['Area'] = area
                perimeter = cv2.arcLength(contour, True)
                current_roi['ApproximatePerimeter'] = perimeter
                (x, y), (MA, ma), angle = cv2.fitEllipse(contour)
                current_roi['Axes'] = {'Major Axis':MA,'Minor Axis':ma}
                current_roi['Direction'] = angle
                data.append(current_roi)
        return data

    @staticmethod
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