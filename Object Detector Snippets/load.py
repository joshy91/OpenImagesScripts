# plot a number of photographs and their mask
from os import listdir
from xml.etree import ElementTree
from numpy import zeros
from numpy import asarray
from mrcnn.utils import Dataset
from matplotlib import pyplot
import time

# class that defines and loads the kangaroo dataset
class OpenImageDataset(Dataset):
    # load the dataset definitions
    def load_dataset(self, dataset_dir, is_train=True):
        # define all classes
        num = 1
        for name in object_labels[1]:
            self.add_class("dataset", num, name)
            num += 1
        
        # define data locations
        images_dir = dataset_dir + '/images/'
        annotations_dir = dataset_dir + '/annots/'
        # find all images
        for filename in listdir(images_dir):
            # extract image id
            image_id = filename[:-4]
            img_path = images_dir + filename
            ann_path = annotations_dir + image_id + '.xml'
            # add to dataset
            self.add_image('dataset', image_id=image_id, path=img_path, annotation=ann_path)

    # extract bounding boxes from an annotation file
    def extract_boxes(self, filename):
        # load and parse the file
        tree = ElementTree.parse(filename)
        # get the root of the document
        root = tree.getroot()
        # extract image dimensions
        width = int(root.find('.//size/width').text)
        height = int(root.find('.//size/height').text)
        # extract each bounding box
        boxes = list()
        for box in root.findall('.//bndbox'):
            xmin = int((float(box.find('XMin').text))*width)
            ymin = int((float(box.find('YMin').text))*height)
            xmax = int((float(box.find('XMax').text))*width)
            ymax = int((float(box.find('YMax').text))*height)
            coors = [xmin, ymin, xmax, ymax]
            boxes.append(coors)
        names = list()
        for name in root.findall('.//object'):
            obj_name = name.find('Name').text
            names.append(obj_name)
        return boxes, names, width, height

    # load the masks for an image
    def load_mask(self, image_id):
        # get details of image
        info = self.image_info[image_id]
        # define box file location
        path = info['annotation']
        # load XML
        boxes, names, w, h = self.extract_boxes(path)
        # create one array for all masks, each on a different channel
        masks = zeros([h, w, len(boxes)], dtype='uint8')
        # create masks
        class_ids = list()
        for i in range(len(boxes)):
            box = boxes[i]
            name = names[i]
            row_s, row_e = box[1], box[3]
            col_s, col_e = box[0], box[2]
            masks[row_s:row_e, col_s:col_e, i] = 1
            class_ids.append(self.class_names.index(name))
        return masks, asarray(class_ids, dtype='int32')

    # load an image reference
    def image_reference(self, image_id):
        info = self.image_info[image_id]
        return info['path']

# train set
start = time.time()
train_set = OpenImageDataset()
end = time.time()
elapsed = end - start
print('1'+' finished in '+ str(elapsed))
start = time.time()
train_set.load_dataset('training')
end = time.time()
elapsed = end - start
print('2'+' finished in '+ str(elapsed))
start = time.time()
train_set.prepare()
end = time.time()
elapsed = end - start
print('3'+' finished in '+ str(elapsed))

# test set
start = time.time()
test_set = OpenImageDataset()
end = time.time()
elapsed = end - start
print('Test 1'+' finished in '+ str(elapsed))
start = time.time()
test_set.load_dataset('test')
end = time.time()
elapsed = end - start
print('Test 2'+' finished in '+ str(elapsed))
start = time.time()
test_set.prepare()
end = time.time()
elapsed = end - start
print('Test 3'+' finished in '+ str(elapsed))