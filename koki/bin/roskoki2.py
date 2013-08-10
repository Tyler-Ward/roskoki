#!/usr/bin/env python
from pykoki import PyKoki, Point2Di, Point2Df, CameraParams
import cv, cv2
import sys

import roslib
roslib.load_manifest('koki')
import sys
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from koki.msg import KokiMsg

class roskoki:

  def __init__(self):
    self.tag_pub = rospy.Publisher("koki_tags",KokiMsg)

    cv.NamedWindow("Image window", 1)
    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("image_topic",Image,self.callback)

  def callback(self,data):
    try:
      cv_image = cv.GetImage(self.bridge.imgmsg_to_cv(data, "mono8")) 

      koki = PyKoki()

      params = CameraParams(Point2Df( cv_image.width/2, cv_image.height/2 ),
                          Point2Df(571, 571),
                          Point2Di( cv_image.width, cv_image.height ))

      markers = koki.find_markers( cv_image, 0.1, params )

      seencodes=[]
      #rospy.logwarn(markers)
      for m in markers:
          rospy.logwarn("Code: " + str(m.code))
          seencodes.append(m.code)

    except CvBridgeError, e:
      rospy.logwarn(str(e))
      """print 'did not get image'"""

#    cv.ShowImage("Image window", cv_image)
#    cv.WaitKey(3)

    tags = KokiMsg()
    tags.tags = seencodes

    try:
      self.tag_pub.publish(tags)
    except CvBridgeError, e:
      print e

def main(args):
  ic = roskoki()
  rospy.init_node('koki_marker_finder', anonymous=True)
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print "Shutting down"
  cv.DestroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)


