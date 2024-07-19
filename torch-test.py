import torch
x = torch.rand(5, 3)
print(x)

print(torch.cuda.get_device_name())