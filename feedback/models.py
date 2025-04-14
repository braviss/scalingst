from django.db import models

FEEDBACK_TYPE_CHOICES = [
    ("tech", "Техническая проблема"),
    ("complaint", "Жалоба"),
    ("suggestion", "Предложение"),
    ("question", "Вопрос"),
    ("service", "Сервис и обслуживание"),
    ("site", "Ошибка на сайте"),
    ("other", "Другое"),
]

class Feedback(models.Model):
    name = models.CharField("Имя", max_length=100, blank=True)
    email = models.EmailField("Email", blank=True)
    feedback_type = models.CharField("Тип обращения", max_length=20, choices=FEEDBACK_TYPE_CHOICES, default="other")
    message = models.TextField("Сообщение")
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    def __str__(self):
        return f"{self.get_feedback_type_display()} от {self.name or 'Аноним'}"
