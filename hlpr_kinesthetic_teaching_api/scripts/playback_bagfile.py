#!/usr/bin/env python

# Copyright (c) 2017, Elaine Short, SIM Lab
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# 
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# 
# * Neither the name of the SIM Lab nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import rospy
import os
import sys
from hlpr_kinesthetic_teaching_api.kinesthetic_teaching_api import KTInterface
from std_srvs.srv import Empty
from hlpr_manipulation_utils.srv import FreezeFrame, FreezeFrameRequest

if os.environ["ROBOT_NAME"]=="2d_arm":
    from hlpr_2d_arm_sim.sim_arm_moveit import Gripper2D, Planner2D
else:
    from hlpr_manipulation_utils.manipulator import Gripper
    from hlpr_manipulation_utils.arm_moveit2 import ArmMoveIt

if __name__=="__main__":
    rospy.init_node("kt_bagfile_playback")

    if os.environ["ROBOT_NAME"]=="2d_arm":
        k = KTInterface("~/test_bagfiles",Planner2D("/sim_arm/joint_state", "/sim_arm/move_arm"), Gripper2D("/sim_arm/gripper_state","/sim_arm/gripper_command"),False)
    else:
        k = KTInterface("~/test_bagfiles",ArmMoveIt(), Gripper(), is_joints=False)

    freezer = rospy.ServiceProxy('freeze_frames', FreezeFrame)
    
    k.load_bagfile(sys.argv[1], False)
    
    freezer(FreezeFrameRequest.UNFREEZE)
    rospy.sleep(2.0)

    k.move_to_keyframe(k.segment_pointer)
    freezer(FreezeFrameRequest.FREEZE)
    
    k.move_to_end()
    freezer(FreezeFrameRequest.UNFREEZE)
    k.stop_tf_threads()
