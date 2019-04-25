

     $("#id_project").change(function() {
        var url = $("#GroupForm").attr("load-group-url");
        var projectId = $(this).val();
        $.ajax({
                url: url,
                data: {
                    'project_name': projectId
                },
                success: function (data) {
                    $("#id_group").html(data);
                }
            });

        });