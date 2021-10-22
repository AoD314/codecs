from PIL import Image, ImageDraw, ImageFont
import random
from multiprocessing import Pool

settings = {'img_size': (3840, 2160), 'ratio': 0.012}


def get_color():
    colors = [(0, 0, 128, 255), (0, 0, 255, 255), (0, 128, 0, 255),
              (0, 128, 128, 255), (0, 128, 255, 255), (0, 255, 0, 255),
              (0, 255, 128, 255), (0, 255, 255, 255), (128, 0, 0, 255),
              (128, 0, 128, 255), (128, 0, 255, 255), (128, 128, 0, 255),
              (128, 128, 128, 255), (128, 128, 255, 255), (128, 255, 0, 255),
              (128, 255, 128, 255), (128, 255, 255, 255), (255, 0, 0, 255),
              (255, 0, 128, 255), (255, 0, 255, 255), (255, 128, 0, 255),
              (255, 128, 128, 255), (255, 128, 255, 255), (255, 255, 0, 255),
              (255, 255, 128, 255), (255, 255, 255, 255)]

    i = random.randint(0, len(colors) - 1)
    return colors[i]


class Ball:
    def __init__(self, x, y, r, color, border):
        self.x = float(x)
        self.y = float(y)
        self.r = r + random.randint(-5, 5)
        self.color = color
        self.border = border
        self.dir = [((1 << 15) - random.randint(0, 1 << 16)) / float(1 << 15),
                    ((1 << 15) - random.randint(0, 1 << 16)) / float(1 << 15)]

    def iter(self, speed=1):
        for _ in range(speed):
            self.x += self.dir[0]
            self.y += self.dir[1]

            self.dir[0] = -self.dir[0] if self.x - self.r <= 0 else self.dir[0]
            self.dir[1] = -self.dir[1] if self.y - self.r <= 0 else self.dir[1]

            self.dir[0] = -self.dir[0] if self.x + self.r >= self.border[
                0] else self.dir[0]
            self.dir[1] = -self.dir[1] if self.y + self.r >= self.border[
                1] else self.dir[1]


class Balls:
    def __init__(self, nb=10, speed=0.01):
        self.balls = []
        r = int(min(settings['img_size']) * settings['ratio'])
        for _ in range(nb):
            self.balls.append(
                Ball(
                    random.randint(settings['img_size'][0] / 2 - 4 * r,
                                   settings['img_size'][0] / 2 + 4 * r),
                    random.randint(settings['img_size'][1] / 2 - 4 * r,
                                   settings['img_size'][1] / 2 + 4 * r), r,
                    get_color(), settings['img_size']))

        self.speed = int(speed * settings['img_size'][1])
        self.frame_number = 0

    def iter(self):
        self.frame_number += 1
        for b in self.balls:
            b.iter(speed=self.speed)

        return 'image_{:05d}'.format(self.frame_number)

    def inc_speed(self, delta):
        self.speed += int(delta * settings['img_size'][1])

    def render(self, image):
        d = ImageDraw.Draw(image)
        fnt = ImageFont.truetype('LiberationMono-Regular.ttf', 24)
        for b in self.balls:
            d.ellipse([b.x - b.r, b.y - b.r, b.x + b.r, b.y + b.r],
                      fill=b.color)
        d.text((10, 10),
               "{:05d}".format(self.frame_number),
               font=fnt,
               fill=(255, 255, 255, 255))


def save_images(imgs):
    imgs['image'].save(imgs['name'], lossless=1, method=6)
    print('save: {}'.format(imgs['name']))


def main():

    balls = Balls(nb=1000, speed=0.003)
    N = 30 * 30
    p = Pool(30)

    images = []

    for i in range(N):
        image = Image.new(mode='RGB', size=settings['img_size'])
        balls.render(image)
        name = balls.iter()

        images.append({'image': image, 'name': 'render/' + name + '.webp'})

        if i % (30 * 1) == 0:
            balls.inc_speed(0.001)

        if i % (300) == 0:
            print('start to save')
            p.map(save_images, images)
            images = []

        print('iter: {}'.format(i))

    print('start to save')
    p.map(save_images, images)

    print('Done')


if __name__ == '__main__':
    main()
