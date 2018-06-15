# Motion Detection with Google Cloud ML Engine
This is how to detect image and recognize who you are.

# alert_motion.py
1. Linux Motion Application detects image changes from my webcam.
2. Check face detection with Google Vision API service.
3. If the image has face, it will call Google ML Engine which is already trained by AUTOML Service.
4. Send notification via Telegram messenger with the image and who he/she is.

# detect.py
Google Vision API Sample code to recognize a face in image

# predict.py
Google ML Engine Sample code to predict who he/she is.

# How to use it
1. Install python packages needed. (requirements.txt)
2. Install motion application : sudo apt-get install motion (if you use debian)
3. Add this python code (alert_motion.py) to /etc/motion/motion.conf (on_event area)
4. python alert_motion.py -t <telegram_id> -i <image_number> 
   (Default images are located in /var/lib/motion )
