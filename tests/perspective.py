#-*- coding:utf-8 -*-
import cv2
import numpy as np
from matplotlib import pyplot as plt

image = cv2.imread('C:\Dev\docMoon\projects\MROK\_setup\screenshots\perspective01.png')
# #image = cv2.imread('../images/test/perspective2_floor.png')
img = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
# [x,y] 좌표점을 4x2의 행렬로 작성
# 좌표점은 좌상->좌하->우상->우하
## perspective box(perspective -> floor plane 좌상->좌하->우상->우하)
points1 = [[247, 102], [49, 540], [1537, 102], [1696, 540]]
# points2 = [[49, 102], [49, 540], [1696, 102], [1696, 540]]
points2 = [[49, 102], [49, 540], [1696, 102], [1696, 540]]

pts1 = np.float32(points1)
pts2 = np.float32(points2)

M = cv2.getPerspectiveTransform(pts1, pts2)
M_inv = np.linalg.inv(M)

print(M)
# [[ 1.36469507e+00  6.50009648e-01 -3.51005210e+02]
#  [-8.37904170e-17  1.43358191e+00 -3.71988967e+01]
#  [-8.69685977e-21  6.75361233e-04  1.00000000e+00]]


# (c[0], c[1]), [x[0], x[1]] -> [m[0], m[1]] : (지도 중앙 좌표), [스크린 좌표] -> [지도 좌표]
# (300, 300), [222, 900] -> [172, 212] / [222, 160] -> [114, 435] / [1642, 900] -> [418, 212] / [1680, 314] -> [449, 366]
# 좌표값 : 스크린 중앙 기준, 지도 [0, 0] 기준 보정: [960, 540] / (300, 300)


# # ## horizontal line
# for i in range(1, 18):
#     if i == 9:
#         color = (255, 0, 0)
#     else:
#         color = (255, 255, 255)
#     cv2.line(img, (0, i*60), (1919, i*60), color, 2)

# ## vertical line
# for i in range(1, 32):
#     if i == 16:
#         color = (255, 0, 0)
#     else:
#         color = (255, 255, 255)
#     cv2.line(img, (i*60, 0), (i*60, 1079), color, 2)


## 한 점(1 point)
# p = [75, 148, 1]
# p = [960, 540, 1]  # 중앙점
# p = [0, 0, 1] # 좌상
# p = [0, 1080, 1] # 좌하
# p = [1920, 0, 1]  # 우상
# p = [1920, 1080, 1]  # 우하
points = {
    '중앙': [960, 540, 1],
    '좌상': [0, 0, 1],
    '좌하': [0, 1080, 1],
    '우상': [1920, 0, 1],
    '우하': [1920, 1080, 1]
}

for k, p in points.items():
    X = M.dot(np.array(p))
    print("{}: [{}, {}]".format(k, round(X[0]/X[2]), round(X[1]/X[2])))


### 여러 점
# original = np.array([((75, 148), (112, 100), (150, 75))], dtype=np.float32)
# converted = cv2.perspectiveTransform(original, M)
# print(converted)


# ## 이미지
# dst = cv2.warpPerspective(img, M, (1920,1080))
# cv2.imwrite('../_setiup/test/perspective02_.png', cv2.cvtColor(dst, cv2.COLOR_RGB2BGR))

# plt.subplot(121),plt.imshow(img),plt.title('Original(Perspective)')
# plt.subplot(122),plt.imshow(dst),plt.title('FloorPlan(Cartesian)')
# # plt.subplot(121),plt.imshow(img),plt.title('FloorPlan(Rectangular)')
# # plt.subplot(122),plt.imshow(dst),plt.title('Original(Perspective)')
# plt.show()



## 스크린 이미지 좌표 -> 게임 맵 좌표
# 스프린 좌표 -> perspective transformation -> 중앙 보정 이동 -> 확대 -> 중앙 보정 역이동?

# (c[0], c[1]), [x[0], x[1]] -> [m[0], m[1]] : (지도 중앙 좌표), [스크린 좌표] -> [지도 좌표]
# (300, 300), [222, 900] -> [172, 212] / [222, 160] -> [114, 435] / [1642, 900] -> [418, 212] / [1680, 314] -> [449, 366]
# 좌표값 : 스크린 중앙 기준, 지도 [0, 0] 기준 보정: [960, 540] / (300, 300)

_p = [0, 0]
p = [_p[0], _p[1], 1]
# M = [[ 1.36469507e+00  6.50009648e-01 -3.51005210e+02]
#  [-8.37904170e-17  1.43358191e+00 -3.71988967e+01]
#  [-8.69685977e-21  6.75361233e-04  1.00000000e+00]]
M = np.float32(
    [
        [1.36469507e+00,  6.50009648e-01, -3.51005210e+02],
        [-8.37904170e-17,  1.43358191e+00, -3.71988967e+01],
        [-8.69685977e-21,  6.75361233e-04,  1.00000000e+00]
    ]
)

X = M.dot(np.array(p))
p = [round(X[0]/X[2]), round(X[1]/X[2]), 1]


## x축으로 a, y축으로 b만큼 이동
# p = [0, 0, 1]
a = -920
b = -540
M = np.float32(
    [
        [1, 0, a],
        [0, 1, b]
    ]
)

p = M.dot(np.array(p).reshape((3, 1 )))

## 확대, 축소: a 배
a = 3
M = np.float32(
    [
        [a, 0],
        [0, a]
    ]
)


p = M.dot(np.array(p))

p = [p[0][0], p[1][0], 1]

a = 920
b = 540
M = np.float32(
    [
        [1, 0, a],
        [0, 1, b]
    ]
)

p = M.dot(np.array(p).reshape((3, 1 )))

print(p)

# ## 회전 이동
# # a = scale*cos@, b =scale*sin@
# # 회전 중심: (x0, y0)
# M = np.float32(
#     [
#         [a, b, (1-a)*x0 -b*y0],
#         [-b, a, b*x0 + (1-a)*y0]
#     ]
# )



