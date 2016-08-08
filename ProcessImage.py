import cv2
import numpy as np

class ProcessImage:
    @staticmethod
    def get_contours(image, blur_val, thresh_val):
        blur = cv2.GaussianBlur(image, (blur_val, blur_val), 0)
        grey_image = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(grey_image, thresh_val, 255, cv2.THRESH_BINARY)
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

    @staticmethod
    def save_images(images,name,file_type):
        count = 0
        for image in images:
            cv2.imwrite("{}{}.{}".format(name,count,file_type),image)
            count+=1

def main():
    #vectors = ProcessImage.get_vectors(cv2.imread('orbs.jpg'),11,150)
    ProcessImage.draw_vectors(cv2.imread('orbs.jpg'),'images\\vectors.png',11,150)

if __name__ == "__main__":
    main()