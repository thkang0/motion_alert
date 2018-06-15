#!/usr/bin/env python

# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This application demonstrates how to perform basic operations with the
Google Cloud Vision API.
Example Usage:
python detect.py text ./resources/wakeupcat.jpg
python detect.py labels ./resources/landmark.jpg
python detect.py web ./resources/landmark.jpg
python detect.py web-uri http://wheresgus.com/dog.JPG
python detect.py web-geo ./resources/city.jpg
python detect.py faces-uri gs://your-bucket/file.jpg
For more information, the documentation at
https://cloud.google.com/vision/docs.
"""

import argparse
import io

from google.cloud import vision

from PIL import Image
import glob, os


def detect_faces(path):
    """Detects faces in an image."""
    client = vision.ImageAnnotatorClient()

    # [START migration_face_detection]
    # [START migration_image_file]
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)
    # [END migration_image_file]

    response = client.face_detection(image=image)
    faces = response.face_annotations

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')
    print('Faces:')
    print faces

    if not faces:
        print "Face is not detected"
        return

    for face in faces:
        print('anger: {}'.format(likelihood_name[face.anger_likelihood]))
        print('joy: {}'.format(likelihood_name[face.joy_likelihood]))
        print('surprise: {}'.format(likelihood_name[face.surprise_likelihood]))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in face.bounding_poly.vertices])

        print('face bounds: {}'.format(','.join(vertices)))

    i = 0
    x_offsets = {}
    y_offsets = {}
    for vertex in face.bounding_poly.vertices:
        x_offsets[i] = vertex.x
        y_offsets[i] = vertex.y
        i += 1

    x_offset = x_offsets[0]
    y_offset = y_offsets[0]
    x2_offset = x_offsets[2]
    y2_offset = y_offsets[2]
    #(181,390),(308,390),(308,537),(181,537)

    #width = x_offsets[1] - x_offsets[0]
    #height = y_offsets[3] - y_offsets[0]

    return x_offset, y_offset, x2_offset, y2_offset
    #return x_offset, y_offset, width, height


    # [END migration_face_detection]
# [END def_detect_faces]

def crop_image(path):
    for infile in glob.glob('{0}/*.jpg'.format(path)):
        output_image_path = "/root/temp/" 
        output_image = infile.split('/')
        output_image_path += output_image[3]
        print output_image_path
        x, y, x2, y2 = detect_faces(infile)
        im = Image.open(infile)
        box = (x, y, x2, y2)
        cropped_image = im.crop(box)
        cropped_image.save(output_image_path)
       
    #    file, ext = os.path.splitext(infile)
    #    im = Image.open(infile)
    #    im.thumbnail(size)
    #    im.save(file + ".thumbnail", "JPEG")

    #return crop.save(image_path, format)

def detect_faces_uri(uri):
    """Detects faces in the file located in Google Cloud Storage or the web."""
    client = vision.ImageAnnotatorClient()
    # [START migration_image_uri]
    image = vision.types.Image()
    image.source.image_uri = uri
    # [END migration_image_uri]

    response = client.face_detection(image=image)
    faces = response.face_annotations

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')
    print('Faces:')

    for face in faces:
        print('anger: {}'.format(likelihood_name[face.anger_likelihood]))
        print('joy: {}'.format(likelihood_name[face.joy_likelihood]))
        print('surprise: {}'.format(likelihood_name[face.surprise_likelihood]))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in face.bounding_poly.vertices])

        print('face bounds: {}'.format(','.join(vertices)))

# [END def_detect_faces_uri]

if __name__ == '__main__':
#    image_uri = "gs://thkang0/uploads/myfamily/min59.jpg"
#    detect_faces_uri(image_uri)
    #image_path = "/root/images/"
    #crop_image(image_path)
    image_path = "/var/lib/motion/01-20180615125159-01.jpg"
    detect_faces(image_path)



