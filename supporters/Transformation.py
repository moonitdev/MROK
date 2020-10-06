#-*- coding:utf-8 -*-
import cv2
import numpy as np
from matplotlib import pyplot as plt
import math

def point_to_three(point):
    """
    기능: 점 좌표를 변환 행렬 곱연산을 위한 배열로 변환
    입력:
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
        - point || 점 좌표 | list | None | [247, 102]

    출력:
        - 의미 | 데이터 타입 | 예시
        - 행렬 연산을 위한 배열 | list | [247, 102, 1]
    """
    return [point[0], point[1], 1] 

def three_to_point(three):
    """
    기능: 변환 행렬 곱연산 결과를 점 좌표로 변환
    입력:
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
        - three || 변환 행렬 곱연산 결과 배열 | list | None | [247, 102, 1]

    출력:
        - 의미 | 데이터 타입 | 예시
        - 점 좌표 | list | [247, 102]
    """
    return [round(three[0]/three[2]), round(three[1]/three[2])]

def screen_to_cartesian(point, screen_center=[960, 540]):
    """
    기능: 스크린 좌표계의 좌표를 직교(cartesian)좌표계 좌표로 변경
    입력:
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
        - point || 점 좌표(스크린 좌표계) | list | None | [247, 102]
        - screen_center || 화면 중앙 좌표(스크린 좌표계) | list | [960, 540] | 스크린 해상도가 1920*1080인 경우 : [960, 540]

    출력:
        - 의미 | 데이터 타입 | 예시
        - 점 좌표(직교 좌표계) | list | [247, 102]
    """
    # return [point[0]-screen_center[0], -point[1]+screen_center[1]]
    return [point[0], -point[1]+2*screen_center[1]]

def cartesian_to_screen(point, screen_center=[960, 540]):
    """
    기능: 스크린 좌표계의 좌표를 직교(cartesian)좌표계 좌표로 변경
    입력:
        - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
        - point || 점 좌표(직교 좌표계) | list | None | [247, 102]
        - screen_center || 화면 중앙 좌표(스크린 좌표계) | list | [960, 540] | 스크린 해상도가 1920*1080인 경우 : [960, 540]

    출력:
        - 의미 | 데이터 타입 | 예시
        - 점 좌표(스크린 좌표계) | list | [247, 102]
    """
    return [point[0], -point[1]+2*screen_center[1]]

class Transformation:

    def __init__(self, M=None, zoom_rate=110.5/644, screen_center=[960, 540]):
        """
        기능: Transformation Class 초기화
        입력:
            - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
            - M || perspective 변환 행렬 | matrix | None | [[ 1.36469507e+00  6.50009648e-01 -3.51005210e+02] [-8.37904170e-17  1.43358191e+00 -3.71988967e+01] [-8.69685977e-21  6.75361233e-04  1.00000000e+00]]
            - screen_center || 변환시 중앙 좌표(스크린 좌표계) | list | [960, 540] | 스크린 해상도가 1920*1080인 경우 : [960, 540]
            - zoom_rate || 확대 배율(스크린 좌표계 -> 맵 좌표계) | float | 137/644 | 최소맵(full zoomout): 137/644
        Note:
            - ROK 좌표 매핑에 맞는 perspective 변환 행렬을 찾아야 함
        """
        self.screen_center = screen_center
        self.zoom_rate = zoom_rate
        if M == None:
            # perspective matrix(불변점: [960, 540] 기준)
            self.Matrix = np.float32(
                                            [
                                                [1.36469507e+00,  6.50009648e-01, -3.51005210e+02],
                                                [-8.37904170e-17,  1.43358191e+00, -3.71988967e+01],
                                                [-8.69685977e-21,  6.75361233e-04,  1.00000000e+00]
                                            ]
                                        )
        else:
            self.Matrix = self.perspective_matrix(self, M[0], M[1])

    def perspective_matrix(self, points1, points2):
        """
        기능: points1 좌표(변환전), points2 좌표(변환후)로부터 변환 행렬을 구함
        입력:
            - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
            - points1 || 변환전 좌표: 좌상->좌하->우상->우하 | list(of list) | None | [[247, 102], [49, 540], [1537, 102], [1696, 540]]
            - points2 || 변환후 좌표: 좌상->좌하->우상->우하 | list(of list) | None | [[49, 102], [49, 540], [1696, 102], [1696, 540]]
        출력:
            - 의미 | 데이터 타입 | 예시
            - perspective 변환 행렬 | matrix | [[ 1.36469507e+00  6.50009648e-01 -3.51005210e+02] [-8.37904170e-17  1.43358191e+00 -3.71988967e+01] [-8.69685977e-21  6.75361233e-04  1.00000000e+00]]
        Note:
            - ROK 좌표 매핑에 맞는 points1, points2 찾아야 함
        """
        return cv2.getPerspectiveTransform(np.float32(points1), np.float32(points2))
     
    def perspective(self, point, M):
        """
        기능: perspective 변환 이후의 point 좌표 구함
        입력:
            - 변수명 || 의미 | 데이터 ㅇ타입 | 디폴트값 | 예시
            - point || 변환전 좌표 | list | None | [247, 102]
        출력:
            - 의미 | 데이터 타입 | 예시
            - perspective 변환후 좌표 | list | []
        Note:
            - ROK 좌표 매핑에 맞는 points1, points2 찾아야 함
        """
        # print('M in perspective: {}'.format(M))
        return three_to_point(M.dot(np.array(point_to_three(point))))

    def translate(self, point, a, b):
        """
        기능: x축으로 a, y축으로 b만큼 평행 이동후 좌표
        입력:
            - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
            - point || 변환전 좌표 | list | None | [247, 102]
            - a || x축 방향 이동 거리 | int | None | 100
            - b || y축 방향 이동 거리 | int | None | 100
        출력:
            - 의미 | 데이터 타입 | 예시
            - 평행 이동후 좌표 | list | [347, 202]
        """
        _p = np.float32([[1, 0, a], [0, 1, b]]).dot(np.array(point_to_three(point)).reshape((3, 1)))
        return [round(y) for x in _p for y in x]

    def _zoom(self, point, z):
        """
        기능: z배 확대 후 좌표를 구함(확대 중심점: [0, 0])
        입력:
            - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
            - point || 변환전 좌표 | list | None | [100, 200]
            - z || 확대 배율 | float | None | 0.5
        출력:
            - 의미 | 데이터 타입 | 예시
            - 확대후 좌표 | list | [50, 100]
        """
        return list(np.float32([[z, 0], [0, z]]).dot(np.array(point)))

    def zoom(self, point, z, screen_center):
        """
        기능: z배 확대 후 좌표를 구함(확대 중심점: screen_center)
        입력:
            - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
            - point || 변환전 좌표 | list | None | [100, 200]
            - z || 확대 배율 | float | None | 2
            - screen_center || 확대 중심점 | list | None | [10, 30]
        출력:
            - 의미 | 데이터 타입 | 예시
            - 확대후 좌표 | list | [210, 430]
        """
        _point = self.translate(point, -screen_center[0], -screen_center[1])
        _point = self._zoom(_point, z)
        # print('zoom_rate: {}, screen_center: {}, last: {}'.format(z, screen_center, self.translate(_point, screen_center[0], screen_center[1])))
        return self.translate(_point, screen_center[0], screen_center[1])

    def _rotate(self, point, a):
        """
        기능: 각도 a(radian) 만큼 회전 후 좌표를 구함(회전 중심점: [0,0])
        입력:
            - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
            - point || 변환전 좌표 | list | None | [100, 0]
            - a || 회전 각도(radian) | float | None | math.pi/2 -> 90도
        출력:
            - 의미 | 데이터 타입 | 예시
            - 회전후 좌표 | list | [0, 100]
        """
        M = np.float32([[math.cos(a), -math.sin(a)], [math.sin(a), math.cos(a)]])
        return [round(y) for x in M.dot(np.array(point).reshape(2, 1)) for y in x]


    # @staticmethod
    def rotate(self, point, a, screen_center):
        """
        기능: 각도 a(radian) 만큼 회전 후 좌표를 구함(회전 중심점: screen_center)
        입력:
            - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
            - point || 변환전 좌표 | list | None | [100, 0]
            - a || 회전 각도(radian) | float | None | math.pi/2 -> 90도
            - screen_center || 확대 중심점 | list | None | [50, 80]
        출력:
            - 의미 | 데이터 타입 | 예시
            - 회전후 좌표 | list | [50, 180]
        """
        _point = self.translate(point, -screen_center[0], -screen_center[1])
        _point = self._rotate(_point, a)
        return self.translate(_point, screen_center[0], screen_center[1])

    def rok_screen_to_map(self, point, center, M=None, zoom_rate=None, screen_center=None):
        """
        기능: ROK 스크린 좌표, 맵 중앙 좌표에서 ROK 맵 좌표를 구함
        입력:
            - 변수명 || 의미 | 데이터 타입 | 디폴트값 | 예시
            - point || 변환전 좌표(스크린 좌표계) | list | None | [100, 0]
            - center || 맵 중앙 좌표(맵 좌표계) | list | None | math.pi/2 -> 90도
            - zoom_rate || 확대 배율(스크린 좌표계 -> 맵 좌표계) | float | None | 137/644
            - screen_center || 스크린 중앙 좌표(스크린 좌표계) | list | None | [960, 540]
            - M || perspective 변환 행렬 | matrix | None | self.Matrix 참조
        출력:
            - 의미 | 데이터 타입 | 예시
            - 변환후 ROK 맵 좌표 후 좌표 | list | ...
        """

        if type(M) is not np.ndarray:
            M = self.Matrix

        print('M: {}'.format(M))

        if zoom_rate == None:
            M = self.zoom_rate

        if screen_center == None:
            M = self.screen_center

        # print('point: {}, center: {}, screen_center: {}, zoom_rate :{}'.format(point, center, screen_center, zoom_rate))
        # print('rok_screen_to_map')
        _point = self.perspective(p, M) # perspective transform(screen 좌표)
        print('_point perspectived : {}'.format(_point))
        _point = self.zoom(_point, zoom_rate, screen_center) # zoom(screen 좌표)
        print('_point zoomed : {}'.format(_point))
        # 좌표계 변환: screen 좌표 -> 직교(cartesian) 좌표계
        _point = screen_to_cartesian(_point, screen_center)
        print('_point cartesian : {}'.format(_point))
        # return self.translate(_point, center[0], center[1]) # 평행이동(screen_center[960, 540] -> center[x, y])
        return self.translate(_point, center[0] - screen_center[0], center[1] - screen_center[1]) # 평행이동(screen_center[960, 540] -> center[x, y])


if __name__ == "__main__":

    p = [849, 818]
    # p = [410, 256]
    # p = [280, 538]
    # p = [960, 540]
    # p = [316, 540]
    zoom_rate = 129/644
    screen_center = [960, 540]
    center = [233, 263]

    t = Transformation()
    # original    
    points1 = [[169, 272], [48, 540], [1599, 272], [1696, 540]]
    points2 = [[51, 102], [48, 540], [1693, 102], [1696, 540]]
    print('point: {}, center: {}, zoom_rate: {}, points1: {}'.format(p, center, zoom_rate, points1))
    M = t.perspective_matrix(points1, points2)

    print(M)
    result = t.rok_screen_to_map(p, center, M, zoom_rate, screen_center)   
    print(result)

    """
    ROK 좌표계
    - 1200*1200(km)
    - perspective
    - 38단계 줌
    - view mode: city / map / world


    screen
    - 1920*1080

    """