$(document).ready(function(){
    var font_id = 0;
    $("div.caption a.more_info").click(function(){
        var modal_box = $('div#font-preview');
        $.get($(this).attr("href"), function(data) {
            $("div.modal-header h1.font-name",modal_box).text(data[0]["fields"]["name"]);
            $("div.modal-header p span.font-sha",modal_box).text(data[0]["fields"]["sha"]);
            $("div.modal-header p span.font-path",modal_box).text(data[0]["fields"]["path"]);
            $("div.modal-footer p a.download-link",modal_box).attr("href","/get/"+data[0]["fields"]["sha"]);
            $("#live-preview").css("font-family","font_preview_pk_"+data[0]["pk"]);
            $("#glyph_chart div").css("font-family","font_preview_pk_"+data[0]["pk"]);
            $("#glyph_chart div p").css("font-family","arial");
            $("#myTabContent").animate({ scrollTop: 0 }, "slow");
            $("#myTab li,.tab-pane").removeClass("active");
            $("#myTab a:first").tab("show");
            $("#btn-cancel-add-tag").click();
            if (data[0]["fields"]["thumbnails"].length < 1){
                $("img.text-thumbnail",modal_box).attr("src","http://fakeimg.pl/800x600/?text=No preview...");
                $("img.big-thumbnail",modal_box).attr("src","http://fakeimg.pl/400x100/?text=Not yet calculated...");
                $("a.text-thumbnail-link",modal_box).attr("href","http://fakeimg.pl/800x600/?text=Preview not yet calculated...");
            }else{
                for(var i=0;i<data[0]["fields"]["thumbnails"].length;i++) {
                    if (data[0]["fields"]["thumbnails"][i] != ''){
                        $.get("/thumb/"+data[0]["fields"]["thumbnails"][i], function(data) {
                            if (data[0]["fields"]["name"] == "text"){
                                $("img.text-thumbnail",modal_box).attr("src","/thumbnail/"+data[0]["fields"]["path"]);
                                $("a.text-thumbnail-link",modal_box).attr("href","/thumbnail/"+data[0]["fields"]["path"]);
                            }
                            if (data[0]["fields"]["name"] == "big"){
                                $("img.big-thumbnail",modal_box).attr("src","/thumbnail/"+data[0]["fields"]["path"]);
                            }
                        });
                    }
                }
            }
        });
        $("div.modal-header p.tags span.label-info").remove();
        font_id = $(this).data("id");
        $.get("/tags/file/"+$(this).data("id"), function(data){
            $.each(data, function(key,value){
                $("div.modal-header p.tags").append("<span class='label label-info'>"+value.fields.name+"</span>")
            });
        });
        modal_box.modal();
        return false;
    });

    $('#tag-name').typeahead({
        source: function (query, typeahead) {
            return $.get('/tags/search', { query: query }, function (data) {
                return typeahead(data.options);
            });
        }
    });

    $("#btn-add-tag").click(function(){
        $("p.tags").addClass("hidden");
        $("form#form-add-tag").removeClass("hidden");
        $("#tag-name").val("");
        $("#tag-name").focus();
        return false;
    });

    $("#btn-cancel-add-tag").click(function(){
        $("p.tags").removeClass("hidden");
        $("form#form-add-tag").addClass("hidden");
        $("#tag-name").val("");
        $(".modal-header .alert").remove();
        return false;
    });

    $("#submit-add-tag").click(function(){
        $.get(
            "/tags/link/"+font_id+"/"+$("#tag-name").val(),
            function(data){
                $(".message_result").html(data);
                $("p.tags").after("<div class='alert alert-success'><button type='button' class='close' data-dismiss='alert'>&times;</button><span class='message_result'>"+data+"</span>");
                $("#btn-add-tag").click();
                $("div.modal-header p.tags span.label").remove();
                $.get("/tags/file/"+font_id, function(data){
                    $.each(data, function(key,value){
                        $("div.modal-header p.tags").append("<span class='label label-info'>"+value.fields.name+"</span>")
                    });
                });
                $("#tag-name").focus();
                return false;
            }
        );
    });
    $("#form-add-tag").on("submit",function(){
        $("#submit-add-tag").click();
        return false;
    });
});
