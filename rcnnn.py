from pascal_voc_parser import get_data
from keras.layers import Input
from keras.models import Model
from keras.optimizers import Adam, SGD, RMSprop
import cv2
import numpy as np
import random
import vgg as nn
import losses as losses

class config():

    def __init__(self):
        self.rpn_stride = 16
        self.anchor_box_scales = [128, 256, 512]
        self.anchor_box_ratios = [[1, 1], [1./np.sqrt(2), 2./np.sqrt(2)], [2./np.sqrt(2), 1./np.sqrt(2)]]

        self.rpn_min_overlap = 0.3
        self.rpn_max_overlap = 0.7

        self.img_channel_mean = [103.939, 116.779, 123.68]
        self.num_epochs = 1000

        self.base_net_weights = 'vgg16_weights_tf_dim_ordering_tf_kernels_notop.h5'

class dataLoad():

    def __init__(self):
        pass

    def union(self,a,b,area_intersection):
        area_a = (a[2]-a[0])*(a[3]-a[1])
        area_b = (b[2]-b[0])*(b[3]-b[1])
        return area_a + area_b - area_intersection

    def intersection(self,a,b):
        x = max(a[0],b[0])
        y = max(a[1],b[1])
        w = min(a[2],b[2]) - x
        h = min(a[3],b[3]) - y
        if w < 0 or h < 0:
            return 0.0
        return w*h

    def iou(self,a,b):
        if a[0] >= a[2] or a[1] >= a[3] or b[0] >= b[2] or b[1] >= b[3]:
            return 0.0
        area_i = self.intersection(a,b)
        area_u = self.union(a,b,area_i)
        return float(area_i)/float(area_u + 1e-6)

    def calc_rpn(self,config):
        downscale = float(config.rpn_stride)
        anchor_size = config.anchor_box_scales
        anchor_ratio = config.anchor_box_ratios
        num_anchors = len(anchor_ratio)*len(anchor_size)

        # divided by 16 is defined by the network you applied(VGG16?)
        self.output_width = self.resized_width//16
        self.output_height = self.resized_height//16

        # figure out rpn_box new truth after img_resize
        self.num_bboxes = len(self.img_bbox)
        self.gta = np.zeros((self.num_bboxes,4))
        for bbox_num,bbox in enumerate(self.img_bbox):
            self.gta[bbox_num,0] = bbox['x1']*((self.resized_width)/float(self.width))
            self.gta[bbox_num,1] = bbox['x2']*((self.resized_width)/float(self.width))
            self.gta[bbox_num,2] = bbox['y1']*((self.resized_height)/float(self.height))
            self.gta[bbox_num,3] = bbox['y2']*((self.resized_height)/float(self.height))

        # initial object for output
        y_rpn_overlap = np.zeros((self.output_height, self.output_width, num_anchors))
        y_is_box_valid = np.zeros((self.output_height, self.output_width, num_anchors))
        y_rpn_regr = np.zeros((self.output_height, self.output_width, num_anchors * 4))

        # update rpn data
        num_anchors_for_bbox = np.zeros(self.num_bboxes).astype(int)
        best_anchor_for_bbox = -1*np.ones((self.num_bboxes, 4)).astype(int)
        best_iou_for_bbox = np.zeros(self.num_bboxes).astype(np.float32)
        best_x_for_bbox = np.zeros((self.num_bboxes,4)).astype(int)
        best_dx_for_bbox = np.zeros((self.num_bboxes, 4)).astype(np.float32)
        for anchor_size_idx in range(len(anchor_size)):
            for anchor_ratio_idx in range(len(anchor_ratio)):
                anchor_x = anchor_size[anchor_size_idx]*anchor_ratio[anchor_ratio_idx][0]
                anchor_y = anchor_size[anchor_size_idx]*anchor_ratio[anchor_ratio_idx][1]
                anchor_number_idx = anchor_ratio_idx + len(anchor_ratio)*anchor_size_idx
                # real anchor in the img exclude the box which is outside of the img
                for ix in range(self.output_width):
                    x1_anc = downscale*(ix+0.5) - anchor_x/2
                    x2_anc = downscale*(ix+0.5) + anchor_x/2
                    if x1_anc < 0 or x2_anc > self.resized_width:
                        continue
                    for jy in range(self.output_height):
                        y1_anc = downscale*(jy+0.5) - anchor_y/2
                        y2_anc = downscale*(jy+0.5) + anchor_y/2
                        if y1_anc < 0 or y2_anc > self.resized_height:
                            continue
                        bbox_type = 'neg'
                        best_iou = 0.0
                        for bbox_num in range(self.num_bboxes):
                            cur_iou = self.iou([self.gta[bbox_num,0],self.gta[bbox_num,2],self.gta[bbox_num,1],self.gta[bbox_num,3]],
                                               [x1_anc,y1_anc,x2_anc,y2_anc])
                            if cur_iou > best_iou_for_bbox[bbox_num]:
                                # calculate regression targets
                                cx = (self.gta[bbox_num, 0] + self.gta[bbox_num, 1]) / 2.0
                                cy = (self.gta[bbox_num, 2] + self.gta[bbox_num, 3]) / 2.0
                                cxa = (x1_anc + x2_anc)/2.0
                                cya = (y1_anc + y2_anc)/2.0
                                tx = (cx - cxa) / (x2_anc - x1_anc)
                                ty = (cy - cya) / (y2_anc - y1_anc)
                                tw = np.log((self.gta[bbox_num, 1] - self.gta[bbox_num, 0]) / (x2_anc - x1_anc))
                                th = np.log((self.gta[bbox_num, 3] - self.gta[bbox_num, 2]) / (y2_anc - y1_anc))
                                # update
                                best_anchor_for_bbox[bbox_num] = [jy, ix, anchor_ratio_idx, anchor_size_idx]
                                best_iou_for_bbox[bbox_num] = cur_iou
                                best_x_for_bbox[bbox_num,:] = [x1_anc, x2_anc, y1_anc, y2_anc]
                                best_dx_for_bbox[bbox_num,:] = [tx, ty, tw, th]
                            if cur_iou > config.rpn_max_overlap:
                                bbox_type = 'pos'
                                num_anchors_for_bbox[bbox_num] += 1
                                if cur_iou > best_iou:
                                    best_iou = cur_iou
                                    best_regr = (tx, ty, tw, th)
                            if config.rpn_min_overlap < cur_iou < config.rpn_max_overlap:
                                bbox_type = 'neutral'
                        if bbox_type == 'neg':
                            y_is_box_valid[jy, ix, anchor_number_idx] = 1
                            y_rpn_overlap[jy, ix, anchor_number_idx] = 0
                        elif bbox_type == 'neutral':
                            y_is_box_valid[jy, ix, anchor_number_idx] = 0
                            y_rpn_overlap[jy, ix, anchor_number_idx] = 0
                        elif bbox_type == 'pos':
                            y_is_box_valid[jy, ix, anchor_number_idx] = 1
                            y_rpn_overlap[jy, ix, anchor_number_idx] = 1
                            start = 4 * (anchor_number_idx)
                            y_rpn_regr[jy, ix, start:start+4] = best_regr

        # check if some bbox don't get a good match
        for idx in range(self.num_bboxes):
            if num_anchors_for_bbox[idx] == 0:
                y_is_box_valid[
                    best_anchor_for_bbox[idx,0], best_anchor_for_bbox[idx,1], best_anchor_for_bbox[idx,2] + len(anchor_ratio)*
                    best_anchor_for_bbox[idx,3]] = 1
                y_rpn_overlap[
                    best_anchor_for_bbox[idx,0], best_anchor_for_bbox[idx,1], best_anchor_for_bbox[idx,2] + len(anchor_ratio) *
                    best_anchor_for_bbox[idx,3]] = 1
                start = 4 * (best_anchor_for_bbox[idx,2] + len(anchor_ratio) * best_anchor_for_bbox[idx,3])
                y_rpn_regr[
                    best_anchor_for_bbox[idx,0], best_anchor_for_bbox[idx,1], start:start+4] = best_dx_for_bbox[idx, :]

        y_rpn_overlap = np.transpose(y_rpn_overlap, (2, 0, 1))
        y_rpn_overlap = np.expand_dims(y_rpn_overlap, axis=0)
        y_is_box_valid = np.transpose(y_is_box_valid, (2, 0, 1))
        y_is_box_valid = np.expand_dims(y_is_box_valid, axis=0)
        y_rpn_regr = np.transpose(y_rpn_regr, (2, 0, 1))
        y_rpn_regr = np.expand_dims(y_rpn_regr, axis=0)
        pos_locate = np.where(np.logical_and(y_rpn_overlap[0, :, :, :] == 1, y_is_box_valid[0, :, :, :] == 1))
        neg_locate = np.where(np.logical_and(y_rpn_overlap[0, :, :, :] == 0, y_is_box_valid[0, :, :, :] == 1))

        # balance the number of pos and neg sample
        num_pos = len(pos_locate[0])
        num_regions = 256
        if len(pos_locate[0]) > num_regions/2:
            temp = random.sample(range(len(pos_locate[0])), len(pos_locate[0]) - num_regions//2)
            y_is_box_valid[0, pos_locate[0][temp], pos_locate[1][temp], pos_locate[2][temp]] = 0
            num_pos = num_regions/2

        if len(neg_locate[0]) + num_pos > num_regions:
            temp = random.sample(range(len(neg_locate[0])), len(neg_locate[0]) - num_pos)
            y_is_box_valid[0, neg_locate[0][temp], neg_locate[1][temp], neg_locate[2][temp]] = 0

        '''
        Here y_rpn_cls.shape = (1,anchor*2,height,width)
        y_rpn_regr.shape = (1,anchor*4*2,height,width)
        y_is_box_valid means whether the box is needed to be trained.
        If the box is negative or positive, it is 1. 
        If the box has the object, y_rpn_overlap = 1. 
        Notice: y_rpn_overlap = [0,1,0,---] after repeat is [0,0,0,0,1,1,1,1,0,---]
        '''
        self.y_rpn_cls = np.concatenate([y_is_box_valid, y_rpn_overlap], axis=1)
        self.y_rpn_regr = np.concatenate([np.repeat(y_rpn_overlap, 4, axis=1), y_rpn_regr], axis=1)


    def img_resize(self,min_side=600):
        if self.width <= self.height:
            f = float(min_side)/self.width
            self.resized_height = int(f*self.height)
            self.resized_width = min_side
        else:
            f = float(min_side)/self.height
            self.resized_height = min_side
            self.resized_width = int(f*self.width)
        self.x_img = cv2.resize(self.img,(self.resized_width,self.resized_height),interpolation=cv2.INTER_CUBIC)

    def get_anchor_info(self,config,all_img_data):
        while True:
            for img_data in all_img_data:
                self.img = cv2.imread(img_data['filepath'])
                self.width = img_data['width']
                self.height = img_data['height']
                self.img_bbox = img_data['bboxes']
                self.img_resize()
                self.calc_rpn(config)
                # BGR -- > RGB and normalize the img
                self.x_img = self.x_img[:,:, (2, 1, 0)]
                self.x_img = self.x_img.astype(np.float32)
                self.x_img[:, :, 0] -= config.img_channel_mean[0]
                self.x_img[:, :, 1] -= config.img_channel_mean[1]
                self.x_img[:, :, 2] -= config.img_channel_mean[2]

                self.x_img = np.expand_dims(self.x_img, axis=0)
                self.y_rpn_cls = np.transpose(self.y_rpn_cls, (0, 2, 3, 1))
                self.y_rpn_regr = np.transpose(self.y_rpn_regr, (0, 2, 3, 1))
                yield np.copy(self.x_img),[np.copy(self.y_rpn_cls),np.copy(self.y_rpn_regr)]

conf = config()
data = dataLoad()
