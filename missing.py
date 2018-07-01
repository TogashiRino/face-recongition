# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import re
import scipy.misc
import warnings
import face_recognition.api as face_recognition
import sys

def scan_known_people(known_people_folder):
    known_names = []
    known_face_encodings = []

    for file in image_files_in_folder(known_people_folder):
        basename = os.path.splitext(os.path.basename(file))[0]
        img = face_recognition.load_image_file(file)
        encodings = face_recognition.face_encodings(img)
        if len(encodings) == 1:
            known_names.append(basename)
            known_face_encodings.append(encodings[0])



    return known_names, known_face_encodings


def test_image(image_to_check, known_names, known_face_encodings):
    unknown_image = face_recognition.load_image_file(image_to_check)

    # Scale down image if it's giant so things run a little faster
    if unknown_image.shape[1] > 1600:
        scale_factor = 1600.0 / unknown_image.shape[1]
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            unknown_image = scipy.misc.imresize(unknown_image, scale_factor)

    unknown_encodings = face_recognition.face_encodings(unknown_image)

    for unknown_encoding in unknown_encodings:
        result = face_recognition.compare_faces(known_face_encodings, unknown_encoding)
      
        output=""


        if True in result:

          
            for is_match, name in zip(result, known_names):
                if is_match:
                    output += ("{} ".format(name))

           
        print(output)

   


def image_files_in_folder(folder):
    return [os.path.join(folder, f) for f in os.listdir(folder) if re.match(r'.*\.(jpg|jpeg|png)', f, flags=re.I)]


def main(known_people_folder, image_to_check):
    known_names, known_face_encodings = scan_known_people(known_people_folder)

    if os.path.isdir(image_to_check):
        [test_image(image_file, known_names, known_face_encodings) for image_file in image_files_in_folder(image_to_check)]
    else:
        test_image(image_to_check, known_names, known_face_encodings)


if __name__ == "__main__":

  main(sys.argv[1],sys.argv[2])

