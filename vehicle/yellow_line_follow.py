import cv2
import numpy as np
import math
import time
import os


def analyze_yellow_line(image_path):
    """
    Определяет угол, на который нужно повернуть роботу, чтобы направиться к жёлтой линии.

    Args:
        image_path (str): Путь к изображению.

    Returns:
        float: Угол в градусах. Положительный — поворот вправо, отрицательный — влево.
    """
    image = cv2.imread(image_path)

    if image is None:
        raise FileNotFoundError(f"Image not found: {image_path}")

    # Переход в HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Диапазон цвета линии (#b27b1c — это примерно оранжево-жёлтый)
    lower_yellow = np.array([10, 50, 165])   # можно уточнить по образцу
    upper_yellow = np.array([25, 220, 215])

    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    
    # cv2.imshow("Mask", mask)
    # cv2.waitKey(0)


    height, width = mask.shape
    
    crop_left = int(width * 1 / 6)
    crop_right = int(width * 5 / 6)

    # Обрезанная маска
    cropped_mask = mask[:, crop_left:crop_right]

    # Теперь обновим переменные для дальнейшего использования
    mask = cropped_mask
    height, width = mask.shape

    # Возьмем одну горизонтальную линию (например, на 2/3 высоты)
    line_y = int(height * 1 / 2)
    scan_line = mask[line_y, :]

    # Найдем все пиксели с жёлтым цветом на линии
    yellow_indices = np.where(scan_line > 0)[0]

    if len(yellow_indices) == 0:
        print("Жёлтая линия не найдена")
        return None

    # Центр жёлтой области
    yellow_center = int(np.mean(yellow_indices))

    # Центр изображения
    image_center = width // 2

    # Визуальный угол: от центра изображения до найденной точки
    dx = yellow_center - image_center
    dy = height - line_y  # вертикальная проекция (расстояние от линии до низа кадра)

    angle_rad = math.atan2(dx, dy)
    angle_deg = -math.degrees(angle_rad)

    print(f"Yellow center: {yellow_center}, Image center: {image_center}, Angle: {angle_deg:.2f}°")


    mask_copy = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    cv2.line(mask_copy, (0, line_y), (width, line_y), (0, 255, 0), 2)

    if len(yellow_indices) > 0:
        cv2.circle(mask_copy, (yellow_center, line_y), 5, (255, 0, 0), -1)

    cv2.imwrite(f"D:/temp2/{str(int(time.time()))}_cropped.png", mask_copy)


    # os.remove(image_path)

    return angle_deg


if __name__ == "__main__":
    image_path = "D:\\vs\\autopilot\\vehicle\\test.webp"
    angle = analyze_yellow_line(image_path)

    if angle is not None:
        print(f"Повернуть на угол: {angle:.2f}°")
