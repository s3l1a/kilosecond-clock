from __future__ import annotations

import math
import sys
import time
from datetime import datetime

from PyQt6.QtCore import QPointF, QRectF, Qt, QTimer
from PyQt6.QtGui import QColor, QFont, QPainter, QPainterPath, QPen
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget


DAY_SECONDS = 86_400.0


class ClockFace(QWidget):
    """Anti-aliased, responsive clock face with continuous hand movement."""

    def __init__(self) -> None:
        super().__init__()
        self.setMinimumSize(520, 520)
        self.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent)
        self._now = time.time()
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(16)

    def _tick(self) -> None:
        self._now = time.time()
        self.update()

    @staticmethod
    def _point(center: QPointF, radius: float, angle: float) -> QPointF:
        radians = math.radians(angle - 90.0)
        return QPointF(center.x() + math.cos(radians) * radius,
                       center.y() + math.sin(radians) * radius)

    def paintEvent(self, _event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor("#0b1018"))

        side = min(self.width(), self.height())
        center = QPointF(self.width() / 2.0, self.height() / 2.0)
        radius = side * 0.43

        # Subtle halo gives the dial a calm, instrument-panel presence.
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(31, 224, 190, 18))
        painter.drawEllipse(QRectF(center.x() - radius - 12, center.y() - radius - 12,
                                   (radius + 12) * 2, (radius + 12) * 2))
        painter.setPen(QPen(QColor("#263543"), 1.5))
        painter.setBrush(QColor("#101923"))
        painter.drawEllipse(QRectF(center.x() - radius, center.y() - radius,
                                   radius * 2, radius * 2))
        painter.setPen(QPen(QColor("#1c2b38"), 1))
        painter.drawEllipse(QRectF(center.x() - radius + 15, center.y() - radius + 15,
                                   (radius - 15) * 2, (radius - 15) * 2))

        # Main marks: every 30 minutes is 1.8 Ks, and every hour is 3.6 Ks.
        for index in range(24):
            angle = index * 15.0
            major = index % 2 == 0
            outer = radius - 21
            inner = radius - (44 if major else 33)
            painter.setPen(QPen(QColor("#44d9be") if major else QColor("#4d6675"),
                                2.4 if major else 1.2))
            painter.drawLine(self._point(center, inner, angle), self._point(center, outer, angle))

        label_font = QFont("Segoe UI", max(9, int(side * 0.024)), QFont.Weight.DemiBold)
        painter.setFont(label_font)
        painter.setPen(QColor("#d8f6ef"))
        for hour in range(1, 13):
            angle = hour * 30.0
            point = self._point(center, radius - 65, angle)
            label = f"{hour * 3.6:.1f}" if hour != 12 else "0.0 / 43.2"
            bounds = QRectF(point.x() - 42, point.y() - 12, 84, 24)
            painter.drawText(bounds, Qt.AlignmentFlag.AlignCenter, label)

        small_font = QFont("Segoe UI", max(7, int(side * 0.014)))
        painter.setFont(small_font)
        painter.setPen(QColor("#76939c"))
        for half_hour in range(24):
            if half_hour % 2 == 0:
                continue
            angle = half_hour * 15.0
            point = self._point(center, radius - 55, angle)
            bounds = QRectF(point.x() - 30, point.y() - 9, 60, 18)
            painter.drawText(bounds, Qt.AlignmentFlag.AlignCenter, "+1.8")
        current = datetime.fromtimestamp(self._now)
        seconds = (current.hour * 3600 + current.minute * 60 + current.second
                   + self._now % 1)
        hour_angle = (seconds / 3600.0) * 30.0
        minute_angle = (seconds / 60.0) * 6.0
        second_angle = (seconds % 60.0) * 6.0
        self._draw_hand(painter, center, radius * 0.51, hour_angle, 7, QColor("#edf9f5"))
        self._draw_hand(painter, center, radius * 0.72, minute_angle, 4, QColor("#d2eae6"))
        self._draw_hand(painter, center, radius * 0.79, second_angle, 1.5, QColor("#ffbf69"))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#44d9be"))
        painter.drawEllipse(QRectF(center.x() - 7, center.y() - 7, 14, 14))
        painter.setBrush(QColor("#0b1018"))
        painter.drawEllipse(QRectF(center.x() - 3, center.y() - 3, 6, 6))

    def _draw_hand(self, painter: QPainter, center: QPointF, length: float,
                   angle: float, width: float, color: QColor) -> None:
        painter.setPen(QPen(color, int(width)))
        endpoint = self._point(center, length, angle)
        painter.drawLine(int(center.x()), int(center.y()), int(endpoint.x()), int(endpoint.y()))


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("KiloClock")
        self.resize(760, 850)
        self.setStyleSheet("QMainWindow { background: #0b1018; }")

        root = QWidget()
        layout = QVBoxLayout(root)
        layout.setContentsMargins(34, 26, 34, 30)
        layout.setSpacing(7)

        eyebrow = QLabel("KILOSECOND INSTRUMENT  /  LOCAL SYSTEM TIME")
        eyebrow.setStyleSheet("color: #44d9be; letter-spacing: 2px; font: 600 11px 'Segoe UI';")
        title = QLabel("KiloClock")
        title.setStyleSheet("color: #edf9f5; font: 700 32px 'Segoe UI';")
        subtitle = QLabel("Because seconds deserved a bigger unit.")
        subtitle.setStyleSheet("color: #78909b; font: 14px 'Segoe UI';")
        self.digital = QLabel()
        self.digital.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.digital.setStyleSheet("color: #ffbf69; font: 600 19px 'Consolas'; padding: 8px;")

        layout.addWidget(eyebrow)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(self.digital)
        layout.addWidget(ClockFace(), 1)

        footer = QLabel("24 half-hour markers  ·  3.6 Ks per hour  ·  86.4 Ks per day")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer.setStyleSheet("color: #516672; font: 12px 'Segoe UI';")
        layout.addWidget(footer)
        self.setCentralWidget(root)

        self._digital_timer = QTimer(self)
        self._digital_timer.timeout.connect(self._update_digital)
        self._digital_timer.start(50)
        self._update_digital()

    def _update_digital(self) -> None:
        now = datetime.now()
        seconds = now.hour * 3600 + now.minute * 60 + now.second + time.time() % 1
        ks = seconds / 1000.0
        self.digital.setText(f"{ks:06.3f} Ks   ·   {now:%H:%M:%S}")


def main() -> None:
    app = QApplication(sys.argv)
    app.setApplicationName("KiloClock")
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
