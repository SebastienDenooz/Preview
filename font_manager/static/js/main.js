$(document).ready(function(){
    $("div.caption a.more_info").click(function(){
        $.get($(this).attr("href"), function(data) {
            var modal_box = $('div#font-preview');
            $("div.modal-header h1.font-name",modal_box).text(data[0]["fields"]["name"]);
            $("div.modal-header p span.font-sha",modal_box).text(data[0]["fields"]["sha"]);
            $("div.modal-header p span.font-path",modal_box).text(data[0]["fields"]["path"]);
            $("div.modal-footer p a.download-link",modal_box).attr("href","/download/"+data[0]["fields"]["path"]);
            $("#live-preview").css("font-family","font_preview_pk_"+data[0]["pk"]);
            $("#glyph_chart div").css("font-family","font_preview_pk_"+data[0]["pk"]);
            $("#glyph_chart div p").css("font-family","arial");
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
            modal_box.modal();
        });
        return false;
    });
});
