class Animator:
    def __init__(self, **kwargs):
        self.looped = kwargs.get('looped', False)
        self.run = kwargs.get('run', False)
        self.duration = kwargs.get('duration', 1)
        self.updown = kwargs.get('updown', False)
        self.t = 0
        self.out = 0

    def loop(self, b):
        self.looped = b

    def updown(self, b):
        self.updown = b

    def start(self):
        self.reset()
        self.resume()

    def stop(self):
        self.run = False

    def resume(self):
        self.run = True

    def reset(self):
        self.t = 0
        self.out = self.transfert(self.t)

    def running(self):
        return self.run

    def update(self, dt):
        if self.run:
            self.t += dt
        p = self.t / self.duration
        if p > 1:
            if self.looped:
                self.t %= self.duration
                p = self.t / self.duration
            else:
                self.stop()
                p = 1
        if self.updown:
            p *= 2
            if p > 1:
                p = 2 - p
        self.out = self.transfert(p)

    def value(self):
        return self.out

class LinearAnimator(Animator):
    def __init__(self, knee=1, **kwargs):
        super().__init__(**kwargs)
        self.knee = knee

    def set_knee(self, knee):
        self.knee = knee

    def transfert(self, percent):
        if self.knee == 1: return percent
        elif percent > self.knee:
            return 1 + ((self.knee - percent) / (1 - self.knee))
        else:
            return percent / self.knee
