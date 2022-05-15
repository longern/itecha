from django.db import models
from django.contrib.auth.models import User


class Contest(models.Model):
    name = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name


class Problem(models.Model):
    title = models.CharField(max_length=255, null=False)
    content = models.TextField()
    testcases = models.BinaryField()
    hidden_code = models.TextField(blank=True, null=True)
    tags = models.TextField(blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    contest = models.ForeignKey(
        Contest, on_delete=models.SET_NULL, blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @classmethod
    def import_markdown_package(cls, file):
        import os
        import zipfile

        all_problems = cls.objects.all()
        problem_map = {p.title: p for p in all_problems}

        with zipfile.ZipFile(file) as archive:
            namelist = archive.namelist()

            has_root_dir = namelist and all(
                name.startswith(namelist[0]) for name in namelist
            )
            if has_root_dir:
                root_dir = namelist.pop(0)

            for filename in namelist:
                basename = os.path.basename(filename)
                if not basename.endswith(".md") or basename == "README.md":
                    continue

                with archive.open(filename) as file:
                    content = file.read().decode("utf-8")

                title = filename.rsplit(".", 1)[0]
                if has_root_dir:
                    title = title[len(root_dir):]

                if title in problem_map:
                    problem = problem_map[title]
                    problem.content = content
                else:
                    problem = cls.objects.create(title=title, content=content)


class Submission(models.Model):
    code = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    creator_ip = models.CharField(max_length=31, blank=True, null=True)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.__class__.__name__}({self.id})"
