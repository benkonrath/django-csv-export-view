from django.urls import path

from .views import (
    FieldTestAllView,
    FieldTestView,
    ManyToManyView,
    ManyToOneView,
    OneToOneView,
    OverrideGetCSVWriterFmtParamsView,
    OverrideGetFieldsView,
    OverrideGetFilenameView,
    OverrideGetQuerysetView,
    RelatedUsesModelStrView,
    SetFilenameView,
    VerboseNamesView,
)

urlpatterns = [
    path("fields/", FieldTestView.as_view(), name="fields"),
    path("fields-all/", FieldTestAllView.as_view(), name="fields-all"),
    path("verbose-names/", VerboseNamesView.as_view(), name="verbose-names"),
    path("many-to-many/", ManyToManyView.as_view(), name="many-to-many"),
    path("many-to-one/", ManyToOneView.as_view(), name="many-to-one"),
    path("one-to-one/", OneToOneView.as_view(), name="one-to-one"),
    path("override-get-queryset/", OverrideGetQuerysetView.as_view(), name="override-get-queryset"),
    path("override-get-fields/", OverrideGetFieldsView.as_view(), name="override-get-fields"),
    path("set-filename/", SetFilenameView.as_view(), name="set-filename"),
    path("override-get-filename/", OverrideGetFilenameView.as_view(), name="override-get-filename"),
    path(
        "override-get-csv-writer-fmtparams/",
        OverrideGetCSVWriterFmtParamsView.as_view(),
        name="override-get-csv-writer-fmtparams",
    ),
    path("related-uses-model-str/", RelatedUsesModelStrView.as_view(), name="related-uses-model-str"),
]
