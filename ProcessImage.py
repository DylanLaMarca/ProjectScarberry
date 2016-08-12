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
    def draw_vectors(in_image,out_image,blur_val,thresh_val):
        contours = ProcessImage.get_contours(in_image, blur_val, thresh_val)
        for cnt in contours:
            rows, cols = in_image.shape[:2]
            [vx, vy, x, y] = cv2.fitLine(cnt, cv2.DIST_L2, 0, 0.01, 0.01)
            lefty = int((-x * vy / vx) + y)
            righty = int(((cols - x) * vy / vx) + y)
            cv2.line(in_image, (cols - 1, righty), (0, lefty), (0, 0, 255), 1)
        cv2.imwrite(out_image,in_image)
        return in_image

    @staticmethod
    def draw_rois(in_image,out_image,blur_val,thresh_val):
        contours = ProcessImage.get_contours(in_image, blur_val, thresh_val)
        rois = range(len(contours))
        count = 0
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(in_image, (x, y), (x + w, y + h), (0, 0, 255), 1)
            count += 1
        cv2.imwrite(out_image, in_image)
        return in_image

    @staticmethod
    def maximize_rois(image, incrament, blur_val):
        incrament = 50.0
        value = incrament*-1
        roi_num = 0
        count = 0
        while (incrament > 1):
            current_roi_num = ProcessImage.get_contours(image,blur_val,value+incrament)
            ProcessImage.draw_rois(image,'images\\image119rois{}.png'.format(value+incrament),)
            if(current_roi_num >= roi_num):
                roi_num = current_roi_num
            elif(current_roi_num < roi_num):
                incrament *= .5
            value+=incrament
            count+=1

    @staticmethod
    def show_image(img):
        cv2.imshow('image', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    @staticmethod
    def save_images(images,name,file_type):
        count = 0
        for image in images:
            cv2.imwrite("{}{}.{}".format(name,count,file_type),image)
            count+=1

def main():
    file_path = 'images\\examples\\20-20-.5\\image119.jpg'
    filename = 'image119'
    for count in range(25):
        image = cv2.imread(file_path)
        ProcessImage.draw_rois(image,'images\\{}rois{}.png'.format(filename,(count*10)+10),11,(count*10)+10)

if __name__ == "__main__":
    main()