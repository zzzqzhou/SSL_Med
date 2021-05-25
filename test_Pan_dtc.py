import os
import argparse
import torch
from networks.vnet_sdf import VNet
from test_util_dtc import test_all_case

parser = argparse.ArgumentParser()
parser.add_argument('--root_path', type=str, default='./Datasets/Pancreas/npz_data/', help='Name of Experiment')
parser.add_argument('--model', type=str,  default='DTC_with_consis_weight_Pan_1', help='model_name')
parser.add_argument('--gpu', type=str,  default='0', help='GPU to use')
parser.add_argument('--save_result', action='store_true', help='Save Results')
FLAGS = parser.parse_args()


os.environ['CUDA_VISIBLE_DEVICES'] = FLAGS.gpu
snapshot_path = "./model/"+FLAGS.model+"/"
test_save_path = "./model/prediction/"+FLAGS.model+"_post/"
if not os.path.exists(test_save_path):
    os.makedirs(test_save_path)

save_result = False
if FLAGS.save_result:
    save_result = True

num_classes = 2

with open(FLAGS.root_path + '/../test.list', 'r') as f:
    image_list = f.readlines()
image_list = [FLAGS.root_path + item.replace('\n', '') for item in image_list]

def test_calculate_metric(epoch_num):
    net = VNet(n_channels=1, n_classes=num_classes-1, normalization='batchnorm', has_dropout=False).cuda()
    save_mode_path = os.path.join(snapshot_path, 'iter_' + str(epoch_num) + '.pth')
    net.load_state_dict(torch.load(save_mode_path))
    print("init weight from {}".format(save_mode_path))
    net.eval()

    avg_metric = test_all_case(net, image_list, num_classes=num_classes-1,
                               patch_size=(96, 96, 96), stride_xy=16, stride_z=16,
                               save_result=save_result, test_save_path=test_save_path)

    return avg_metric


if __name__ == '__main__':
    metric = test_calculate_metric(6000)
    print(metric)
