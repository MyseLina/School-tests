from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from attempts.models import Attempt
from config.permissions import IsStudent, IsTeacherOrAdmin, is_admin
from .models import Test
from .serializers import TestSerializer, QuestionPublicSerializer


# Create your views here.
class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    http_method_names = ["get", "post", "delete", "head", "options"]

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [IsAuthenticated()]
        if self.action in ("create", "destroy"):
            return [IsTeacherOrAdmin()]
        return super().get_permissions()

    def get_queryset(self):
        qys = Test.objects.all().order_by("-created")
        user = self.request.user
        if is_admin(user):
            return qys
        if hasattr(user, "teachers"):
            return qys.filter(teacher=user.teachers)
        if hasattr(user, "students"):
            student = user.students
            if student.grade:
                return qys.filter(subject__grade=user.students.grade).distinct()
            return qys.none()

    def perform_create(self, serializer):
        serializer.save(teacher=getattr(self.request.user, "teachers", None))

    @action(detail=True, methods=["post"], permission_classes=[IsStudent])
    def start(self, request, pk=None):
        test = self.get_object()
        if not test.is_open():
            return Response({"detail": "Test muddati tugagan"}, status=400)
        if test.questions.count() != 10:
            return Response({"detail": "Test hali to'liq emas"}, status=400)
        attempt, _ = Attempt.objects.get_or_create(student=request.user.students, test=test)
        if attempt.finished:
            return Response({"Testni allaqachon topshirib bo'lgansiz!"}, status=400)
        questions = QuestionPublicSerializer(test.questions.all(), many=True).data
        return Response({"questions": questions, "answers": attempt.answers})

    @action(detail=True, methods=["post"], permission_classes=[IsStudent])
    def answer(self, request, pk=None):
        test = self.get_object()
        attempt = Attempt.objects.filter(student=request.user.students, test=test).first()
        if attempt is None or attempt.finished or not test.is_open():
            return Response({"detail": "Test faol emas"}, status=400)
        try:
            qu_id = int(request.data.get("question_id"))
            variant = int(request.data.get("variant"))
        except (TypeError, ValueError):
            return Response({"detail": "Noto'g'ri ma'lumot"}, status=400)
        question = test.questions.filter(pk=qu_id).first()
        if question is None or variant not in (1, 2, 3, 4):
            return Response({"detail": "Noto'g'ri savol yoki variant"}, status=400)
        if str(qu_id) in attempt.answers:
            return Response({"detail": "Bu savolga javob berilgan"}, status=400)
        attempt.answers[str(qu_id)] = variant
        attempt.save()
        return Response({"correct": variant == question.correct, "right": question.correct})

    @action(detail=True, methods=["post"], permission_classes=[IsStudent])
    def finish(self, request, pk=None):
        test = self.get_object()
        attempt = Attempt.objects.filter(student=request.user.students, test=test).first()
        if attempt is None or attempt.finished:
            return Response({"detail": "Test faol emas"}, status=400)
        if not test.is_open():
            return Response({"detail": "Test muddati tugagan"}, status=400)
        score = sum(1 for q in test.questions.all() if attempt.answers.get(str(q.id)) == q.correct)
        attempt.score = score
        attempt.finished = True
        attempt.save()
        return Response({"score": score, "total": test.questions.count()})
