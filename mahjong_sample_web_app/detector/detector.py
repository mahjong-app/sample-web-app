from pathlib import Path
import numpy as np

# from scipy.misc import imresize
from PIL import Image as pil_image
from keras.preprocessing import image
from .postprocess import PostProcess
from .ssd.ssd import SingleShotMultiBoxDetector


model_file = Path(__file__).parent / "models" / "weights.25-0.05.hdf5"
param_file = (
    Path(__file__).parent / "models" / "ssd300_params_mahjong_vgg16_train_2.json"
)


def model_build(model_file, param_file):
    ssd = SingleShotMultiBoxDetector(
        overlap_threshold=0.5, nms_threshold=0.45, max_output_size=400
    )
    ssd.load_parameters(param_file)
    ssd.build(init_weight=model_file)
    return ssd


def _add_margin(img):
    img_shape = list(img.shape)
    if img_shape[0] == img_shape[1]:
        return img
    if img_shape[0] < img_shape[1]:
        min_arg = 0
        max_arg = 1
    else:
        min_arg = 1
        max_arg = 0
    margin_shape = img_shape
    margin_shape[min_arg] = int((img_shape[max_arg] - img_shape[min_arg]) / 2.0)
    margin = np.tile([0.0], margin_shape)
    new_img = np.concatenate([margin, img], axis=min_arg)
    new_img = np.concatenate([new_img, margin], axis=min_arg)
    return new_img


def pred(ssd, img):
    inputs = np.array([img.copy()])
    results = ssd.detect(inputs, batch_size=1, verbose=1, do_preprocess=True)
    return results


def load_image(img_obj, input_shape=(512, 512)):
    # img = image.load_img(img_path)
    img = pil_image.open(img_obj)
    if img.mode != "RGB":
        img = img.convert("RGB")

    img_array = image.img_to_array(img)
    new_img = _add_margin(img_array)
    new_img_float = np.array(
        pil_image.fromarray(new_img.astype("uint8")).resize(
            size=input_shape  # , resample=pil_image.BICUBIC
        )
    ).astype("float32")
    # new_img_float = imresize(new_img, input_shape).astype("float32")
    return new_img_float


def detect(img_obj):
    img = load_image(img_obj)
    ssd = model_build(model_file, param_file)
    pred_result = pred(ssd, img)

    pp = PostProcess(ssd.class_names, pred_threshold=0.9)
    pp.set_top_score(pred_result)
    list_label = pp.get_list_pi()
    # pp.save_image(img, pred_result, savepath)
    # print(list_label)
    return list_label
