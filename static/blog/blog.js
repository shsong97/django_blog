$(document).ready(function() {
    $(function() {
        var message="";
        $.ajax({
            url:"/blog/favorite",
            dataType:'json',
            success:function(result){
                for(var i in result) {
                    var htmlmsg="<li><a href='/blog/"+result[i]['blog_id']+"'>"+result[i]['blog_title']+"</a></li>";
                    message+=htmlmsg;
                }
                $("#favorite_article").html(message);
            },
            error:function(e){
                alert("Error:favorite-"+e.responseText);
            }
        });
    });

    $(function() {
        var message="";
        $.ajax({
            url:"/blog/archive",
            dataType:'json',
            success:function(result){
                for(var i in result) {
                    var htmlmsg="<li><a href='/blog/list/"+result[i]['year']+"'>"+result[i]['year']+" ("+result[i]['count']+")</a></li>";
                    message+=htmlmsg;
                }
                $("#recent_article").html(message);
            },
            error:function(e){
                alert("Error:blog_archive-"+e.responseText);
            }
        });
    });

    $(document).on("click","#blog_like_click",
        function() {
            var item=$(this);
            var blog_id=item.find("#blog_like").attr('value');
            $.ajax({
                url:"/blog/"+blog_id+"/like",
                dataType:'json',
                success:function(result){
                    item.find("#blog_like").text(result['result']);
                },
                error:function(e) {
                    alert("Error:blog_like-"+e.responseText);
                }
            }); // ajax
        });
}) // ready