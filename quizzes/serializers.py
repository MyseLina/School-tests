import students
from .models import Question, Test
from rest_framework import serializers
from django.db import transaction


class QuestionInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["text", "option1", "option2", "option3", "option4", "correct"]


class QuestionPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id", "text", "option1", "option2", "option3", "option4"]


class TestSerializer(serializers.ModelSerializer):
    questions = QuestionInputSerializer(many=True, write_only=True)
    is_open = serializers.SerializerMethodField()
    my_status = serializers.SerializerMethodField()
    my_score = serializers.SerializerMethodField()

    class Meta:
        model = Test
        fields = ["id", "title", "subject", "questions", "teacher", "created",
                  "is_open", "my_status", "my_score"]
        read_only_fields = ["teacher", "created"]


    def _attempt(self, obj):
        student = getattr(self.context["request"].user, "students", None)
        return obj.attempts.filter(student=student).first() if student else None

    def get_is_open(self, obj):
        return obj.is_open()

    def get_my_status(self, obj):
        attempt = self._attempt(obj)
        if attempt is None:
            return "new"
        return "finished" if attempt.finished else "started"

    def get_my_score(self, obj):
        attempt = self._attempt(obj)
        return attempt.score if attempt else 0

    def validate_subject(self, subjects):
        if not subjects:
            raise serializers.ValidationError("Kamida 1ta sinf tanlang!")
        teacher = getattr(self.context["request"].user, "teachers", None)
        if teacher and any(not s.teacher.filter(pk=teacher.pk).exists() for s in subjects):
            raise serializers.ValidationError("Siz bu sinflarga dars o'tmaysiz!")
        if len({(s.name, s.grade.number) for s in subjects}) > 1:
            raise serializers.ValidationError("Test faqat 1xil sinf darajasi uchun")
        return subjects

    def validate_questions(self, questions):
        if len(questions) != 10:
            raise serializers.ValidationError("Test 10ta savolli bo'lishi shart!")
        return questions

    @transaction.atomic
    def create(self, validated_data):
        questions = validated_data.pop("questions")
        subjects = validated_data.pop("subject")
        test = Test.objects.create(**validated_data)
        test.subject.set(subjects)
        Question.objects.bulk_create([Question(test=test, **q) for q in questions])
        return test