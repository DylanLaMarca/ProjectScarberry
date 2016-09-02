"""
Contains all of the code used to interpret, edit, analyze, and save images in ProjectScarberry.
    :author: Dylan Michael LaMarca
    :contact: dlamarca@u.washington.edu
    :Date: 27/7/2016 - 2/9/2016
    :function convert_to_cv: Converts a base64 string of an image to a numpy array image.
    :function save_image:  Saves an image and formats the file name like the following: "directory\\name_formatted_number.extention".
    :function format_number: Formats a number to a specific length by appending zeros to the front of the number.
    :function get_contours: Gleans the contour clusters from an image based on a basic binarization of an 8-Bit Monochrome bitmap.
    :function get_data: Stores information about the different contour clusters of an image into a dictionary for future access.
    :function draw_and_data: Analyzes an image, saving the information to a file, and drawing visual representations of the information on a copy of the image.
    :function save_data: Saves a dictionary containing information and other dictionaries of information about the contour clusters of an image to a file.
    :function format_data_dict: Formats and saves information from a dictionary to a file through recursion.
"""
import cv2
import numpy as np
import base64

def convert_to_cv(image_string):
    """
    Converts a base64 string of an image to a numpy array image.
        :argument image_string:
        :type image_string: base64 string
        :return: A numpy array of image_string
        :rtype: numpy.ndarray
    """
    decoded = base64.decodestring(image_string)
    numpy_image = np.fromstring(decoded,dtype=np.byte)
    cv_image = cv2.imdecode(numpy_image, cv2.IMREAD_REDUCED_GRAYSCALE_8)
    return cv_image

def save_image(image,formated_number,image_direcoty='images',name='image',extention='.TIFF'):
    """
    Saves an image and formats the file name like the following: "directory\\name_formatted_number.extention".
        :argument image: The image to be saved.
        :type image: numpy.ndarray
        :argument formated_number: The formated number that appears after the filename.
        :type formated_number: string
        :keyword image_direcoty: The directory where the image will be saved.
        :type image_directoory: string
        :keyword name: The main unchanging name of the image.
        :type name: string
        :keyword extention: The extention of the file the image will be saved to.
        :type extention: string
        """
    cv2.imwrite('{}\\{}_{}{}'.format(image_direcoty, name, formated_number, extention),image)

def format_number(number,padding):
    """
    Formats a number to a specific length by appending zeros to the front of the number.
        :argument number: The number to be formatted.
        :type number: int
        :argument padding: formatted number length.
        :type padding: int
        :return: String of the number with zeros in front of it.
        :rtype: string
    """
    formated_number = ''
    for count in range(int(padding) - len(str(number))):
        formated_number += '0'
    return formated_number + str(number)

def get_contours(image, blur_val, thresh_val):
    """
    Gleans the contour clusters from an image based on a basic binarization of an 8-Bit Monochrome bitmap.
        :argument image: Image to be analyzed.
        :type image: numpy.ndarray
        :argument blur_val: Size of the averaged pixel matrix used to blur the image before binarization.
        :type blur_val: int (must be positive and odd)
        :argument thresh_val: Minimum brightness a pixel must be to be binarized/stored as 1//White.
        :type thresh_val: int (between 0 and 255)
        :return: A list of the different clusters of contours.
        :rtype: numpy.ndarray[]
    """
    blur = cv2.GaussianBlur(image,(int(blur_val),int(blur_val)),0)
    ret, thresh = cv2.threshold(blur,int(thresh_val),255,cv2.THRESH_BINARY)
    im2, contours, hierarchy = cv2.findContours(thresh, 1, 2)
    return contours

def get_data(image,blur_val,thresh_val):
    """
    Stores information about the different contour clusters of an image into a dictionary for future access.
        :argument image: Image to be analyzed.
        :type image: numpy.ndarray
        :argument blur_val: Size of the averaged pixel matrix used to blur the image before binarization. Used to generate the contour clusters.
        :type blur_val: int (must be positive and odd)
        :argument thresh_val: Minimum brightness a pixel must be to be binarized/stored as 1/White. Used to generate the contour clusters.
        :type thresh_val: int (between 0 and 255)
        :return: Dictionary of data gathered from the contour clusters of image.
        :rtype: dict
    """
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
            if len(contour) > 5:
                try:
                    (x, y), (MA, ma), angle = cv2.fitEllipse(contour)
                except cv2.error:
                    pass
            current_roi['Axes'] = {'Major Axis':MA,'Minor Axis':ma}
            current_roi['Direction'] = angle
            data.append(current_roi)
    return data

def draw_and_data(image, new_image_filename, data_filename, blur_val, thresh_val, draw_rois=False, draw_centroid=False, draw_count=False, draw_colours=True):
    """
    Analyzes an image, saving the information to a file, and drawing visual representations of the information on a copy of the image.
        :argument image: The image to be analyzed, saved, and drawn on.
        :type image: numpy.ndarray
        :argument new_image_filename: The name of the new, drawn on image.
        :type new_image_filename: string
        :argument data_filename: The name of the file which will contain all of the information gleaned from the image's contour clusters.
        :type data_filename: string
        :argument blur_val: Size of the averaged pixel matrix used to blur the image before binarization. Used to generate the contour clusters.
        :type blur_val: int (must be positive and odd)
        :argument thresh_val: Minimum brightness a pixel must be to be binarized/stored as 1/White. Used to generate the contour clusters.
        :type thresh_val: int (between 0 and 255)
        :keyword draw_rois: Sets whether or not boxes will be drawn outlining the regions of interest about the contour clusters in image.
        :type draw_rois: boolean
        :keyword draw_centroid: Sets whether or not points will be draw pinpointing the centroid of the contour clusters in image.
        :type draw_centroid: boolean
        :keyword draw_count: Sets whether or not numbers will be drawn labelling the contour clusters in image.
        :type draw_count: boolean
        :keyword draw_colours: Sets whether or not the new image being drawn on will be coloured of 8bit Monochrome.
        :type draw_colours: boolean
    """
    out_image = image
    if draw_colours:
        out_image = cv2.cvtColor(image, cv2.COLOR_BAYER_GR2RGB)
    contours = get_contours(image, blur_val, thresh_val)
    data = []
    count = 0
    for contour in contours:
        print '~~~~~~~{}'.format(type(contour))
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
        [vx, vy, x, y] = cv2.fitLine(contour, cv2.DIST_L2, 0, 0.01, 0.01)
        current_roi['Vector'] = {'vx': vx[0], 'vy': vy[0], 'x': x[0], 'y': y[0]}
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
    save_data(data,data_filename)
    cv2.imwrite(new_image_filename, out_image)

def save_data(data,file_name):
    """
    Saves a dictionary containing information and other dictionaries of information about the contour clusters of an image to a file.
        :argument data: Dictionary of information about the contour clusters of an image
        :type data: dict
        :argument file_name: Name of the file which is being written to.
        :type file_name: string
    """
    filename = file_name
    file = open(filename, 'w')
    file.truncate()
    count = 0
    for contour in data:
        file.write('Contour Cluster {}:\n'.format(count))
        for key in contour.keys():
            current_value = contour.get(key)
            format_data_dict(file,current_value,key,1)
        count+=1
    file.close()

def format_data_dict(file,value,key,indent):
    """
    Formats and saves information from a dictionary to a file through recursion.
        :argument file: The open file which will be written to.
        :type file: file
        :argument value: The object which will be tested and printed.
        :type value: dict, int, float, string, tuple, list
        :argument key: The current key to value if it is a dict.
        :type key: string
        :argument indent: The number of indents in front of a data point's label.
        :type indent: int
    """
    dict = {}
    for count in range(indent):
        file.write('    ')
    if type(value) == type(dict):
        file.write('{}:\n'.format(key))
        for sub_key in value.keys():
            format_data_dict(file,value.get(sub_key), sub_key, indent+1)
    else:
        file.write('{}: {}\n'.format(key, value))