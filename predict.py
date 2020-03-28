import torch
from PIL import Image
from torchvision import transforms
from torch.autograd import Variable
import glob

transform = transforms.Compose([
            #transforms.Scale(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

idx_to_class = {0:'normal', 1:'pk'}

def predict(use_cuda, model, image_name):

    test_image = Image.open(image_name)

    test_image_tensor = transform(test_image)

    if use_cuda:
        test_image_tensor = test_image_tensor.cuda()
    else:
        test_image_tensor = test_image_tensor
    test_image_tensor = Variable(torch.unsqueeze(test_image_tensor, dim=0).float(), requires_grad=False)

    with torch.no_grad():
        model.eval()
        #print(model)
        out = model(test_image_tensor)
        ps = torch.exp(out)
        ps = ps / torch.sum(ps)
        topk, topclass = ps.topk(1, dim=1)
        return(idx_to_class[topclass.cpu().numpy()[0][0]], topk.cpu().numpy()[0][0])


if __name__ == '__main__':
    model_path = '/home/yinliang/works/pytorch_learn/PK/model/best_resnet.pkl'
    img_path = '/home/yinliang/works/pytorch_learn/PK/data/val/0'
    model = torch.load(model_path)
    use_cuda = True if torch.cuda.is_available else False
    if use_cuda:
        model.cuda()
    img_list = glob.glob(img_path + '/*.jpg')
    for img in img_list:
        label, score = predict(model, img)
        print(label, score)


