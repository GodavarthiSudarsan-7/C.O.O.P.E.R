import math

from PySide6.QtCore import Qt, QTimer, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QRadialGradient
from PySide6.QtWidgets import QWidget

STATE_COLORS = {
    "idle": QColor("#00e5ff"),
    "listening": QColor("#39ff88"),
    "thinking": QColor("#ffb347"),
    "speaking": QColor("#00e5ff"),
}

STATE_SPEEDS = {
    "idle": 0.6,
    "listening": 2.2,
    "thinking": 1.6,
    "speaking": 1.9,
}

RING_SPECS = (
    (1.0, 3.0, 120, 1.0),
    (0.78, 2.0, 200, -1.4),
    (0.56, 2.0, 260, 1.8),
)


class ArcReactor(QWidget):
    def __init__(self, parent=None, size=200):
        super().__init__(parent)
        self.setFixedSize(size, size)
        self._angle = 0.0
        self._phase = 0.0
        self._state = "idle"

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(30)

    def set_state(self, state: str):
        self._state = state if state in STATE_COLORS else "idle"
        self.update()

    def _tick(self):
        speed = STATE_SPEEDS.get(self._state, 0.6)
        self._angle = (self._angle + speed * 4) % 360
        self._phase += 0.12
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        color = STATE_COLORS.get(self._state, QColor("#00e5ff"))
        w, h = self.width(), self.height()
        cx, cy = w / 2, h / 2
        base_radius = min(w, h) / 2 - 10

        pulse = 0.5 + 0.5 * math.sin(self._phase)

        glow_radius = base_radius * (1.05 + 0.08 * pulse)
        glow_color = QColor(color)
        glow_color.setAlpha(90)
        transparent = QColor(color)
        transparent.setAlpha(0)
        gradient = QRadialGradient(cx, cy, glow_radius)
        gradient.setColorAt(0.0, glow_color)
        gradient.setColorAt(1.0, transparent)
        painter.setPen(Qt.NoPen)
        painter.setBrush(gradient)
        painter.drawEllipse(QRectF(cx - glow_radius, cy - glow_radius, glow_radius * 2, glow_radius * 2))

        for radius_ratio, width_px, span, speed_mult in RING_SPECS:
            radius = base_radius * radius_ratio
            pen = QPen(color)
            pen.setWidthF(width_px)
            pen.setCapStyle(Qt.RoundCap)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)
            start_angle = int((self._angle * speed_mult) * 16)
            span_angle = int(span * 16)
            rect = QRectF(cx - radius, cy - radius, radius * 2, radius * 2)
            painter.drawArc(rect, start_angle, span_angle)

        core_radius = base_radius * 0.38 * (0.92 + 0.08 * pulse)
        bright = QColor(color).lighter(160)
        bright.setAlpha(230)
        dim = QColor(color)
        dim.setAlpha(40)
        core_gradient = QRadialGradient(cx, cy, core_radius)
        core_gradient.setColorAt(0.0, bright)
        core_gradient.setColorAt(1.0, dim)
        painter.setPen(Qt.NoPen)
        painter.setBrush(core_gradient)
        painter.drawEllipse(QRectF(cx - core_radius, cy - core_radius, core_radius * 2, core_radius * 2))
