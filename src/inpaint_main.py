# ---------------------------------------------------------
# TensorFlow Semantic Image Inpainting Implementation
# Licensed under The MIT License [see LICENSE for details]
# Written by Cheng-Bin Jin
# Email: sbkim0407@gmail.com
# ---------------------------------------------------------
import os
import tensorflow as tf
import cv2

from gen_mask import gen_mask
from inpaint_solver import Solver

FLAGS = tf.flags.FLAGS

tf.flags.DEFINE_string('gpu_index', '0', 'gpu index, default: 0')
tf.flags.DEFINE_string('dataset', 'celebA', 'dataset name for choice [celebA|svhn], default: celebA')

tf.flags.DEFINE_float('learning_rate', 0.01, 'learning rate to update latent vector z, default: 0.01')
tf.flags.DEFINE_float('momentum', 0.9, 'momentum term of Adam for latent vector, default: 0.9')
tf.flags.DEFINE_integer('z_dim', 100, 'dimension of z vector, default: 100')
tf.flags.DEFINE_integer('iters', 1500, 'number of iterations to optimize latent vector, default: 1500')
tf.flags.DEFINE_float('lambda', 0.003, 'hyper-parameter for prior loss, default: 0.003')
tf.flags.DEFINE_bool('is_blend', True, 'blend predicted image to original image, default: true')
tf.flags.DEFINE_string('mask_type', 'center', 'mask type choice in [center|random|half|pattern], default: center')
tf.flags.DEFINE_integer('img_size', 64, 'image height or width, default: 64')

tf.flags.DEFINE_integer('print_freq', 100, 'print frequency for loss, default: 100')
tf.flags.DEFINE_integer('sample_freq', 100, 'sample frequency for saving image, default: 100')
tf.flags.DEFINE_integer('sample_batch', 16, 'number of sampling images for check generator quality, default: 16')
tf.flags.DEFINE_string('load_model', None,
                       'folder of saved model that you wish to test, (e.g. 20180704-1736), default: None')


def main(_):
    os.environ['CUDA_VISIBLE_DEVICES'] = FLAGS.gpu_index

    masks = gen_mask(FLAGS)
    for idx in range(masks.shape[0]):
        print('idx: {}'.format(idx))
        img = masks[idx]
        cv2.imshow('Mask', img)
        cv2.waitKey(0)

    solver = Solver(FLAGS)
    solver.test()


if __name__ == '__main__':
    tf.app.run()