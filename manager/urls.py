from django.urls import path

from manager.views import index, TaskTypeListView, PositionListView, WorkerListView, WorkerDetailView, TaskListView, \
    TaskDetailView

urlpatterns = [
    path("", index, name="index"),
    path(
        "task_types/",
        TaskTypeListView.as_view(),
        name="task_type_list",
    ),
    path("positions/", PositionListView.as_view(), name="position_list"),
    path("workers/", WorkerListView.as_view(), name="worker_list"),
    path("workers/<int:pk>/", WorkerDetailView.as_view(), name="worker_detail"),
    path("tasks/", TaskListView.as_view(), name="task_list"),
    path(
        "tasks/<int:pk>/", TaskDetailView.as_view(), name="task_detail"
    ),
]

app_name = "manager"
