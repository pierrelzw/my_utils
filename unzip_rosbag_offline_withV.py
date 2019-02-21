import rospy
import rosbag
import time
import math
import os

def main(bag_file, topic_list=[]):
    res = []
    rb = rosbag.bag.Bag(bag_file)
    str_list = str(rb).split("\n")
    #for k in str_list:
    #    print "*****" + k
    odometry_velocity = 0        
    for x in rb.read_messages(topics=topic_list):
        #print x
        topic_name = x.topic.split('/')[1]
        if topic_name == "odometry":
            odometry_timestamp = float(
                x.message.header.stamp.secs) + float(x.message.header.stamp.nsecs/1000000000.0)
            #print odometry_timestamp
            odometry_velocity = math.sqrt(x.message.twist.twist.linear.x**2 + x.message.twist.twist.linear.y**2
                                              + x.message.twist.twist.linear.z**2)
            #print odometry_velocity
        #     res.append({
        #         "topic": x.topic,
        #         "secs": x.message.header.stamp.secs,
        #         "nsecs": x.message.header.stamp.nsecs,
        #         "twist_x": x.message.twist.twist.linear.x,
        #         "twist_y": x.message.twist.twist.linear.y,
        #         "twist_z": x.message.twist.twist.linear.z
        #     }
        #     )
        else:
            #print topic_name
            sec_time = time.strftime("%Y-%m-%d-%H-%M-%S",time.localtime(x.message.header.stamp.secs))
            str_time= sec_time + "-%.3d" % (x.message.header.stamp.nsecs/1000000)
            #filename = "img/" + str(x.message.header.stamp.secs) + "-" + str(x.message.header.stamp.nsecs) + "_V%d" % (odometry_velocity) + ".jpg"
            filename = "img/" + str_time + "_V%02d" % (odometry_velocity) + ".jpg"
            print filename
            with open(filename,"w") as output_file:
                output_file.write(x.message.data)
        #     res.append({
        #         "topic": x.topic,
        #         "secs": x.message.header.stamp.secs,
        #         "nsecs": x.message.header.stamp.nsecs,
        #         "data": x.message.data
        #     }
        #     )
        #filename = str(x.message.header.stamp.secs) + "-" + str(x.message.header.stamp.nsecs)) + ".jpg"

	
	
    return res


if __name__ == "__main__":
    #read_bagfile("all_record.bag", ["/camera_6mm/image_compressed",
    #                         "/camera_12_5mm/image_compressed",
    #                         "/camera_25mm/image_compressed",
    #                         "/camera_50mm/image_compressed",
    #                         "/odometry" ,
    #                         ])
    rootdir = "/media/yshen/yshen_hdd_768GB/L39_2018-04-20/"
    dirnames = os.listdir(rootdir) # project 20171027_01
    for dirname in dirnames:
      subdir1 = os.path.join(rootdir, dirname)  
      print subdir1
      main(subdir1, [
          "/camera_6mm/image_compressed",
          "/odometry"
      ])
    pass
