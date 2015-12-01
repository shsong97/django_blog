
function blog_like() {
    var item=$(this);
    var blog_id=item.find("#blog_like").attr('value');
    $.ajax({
        url:"/blog/"+blog_id+"/like",
        dataType:'json',
        success:function(result){
            item.find("#blog_like").text(result['result']);
        },
        error:function(e) {
            alert(e.responseText);
        }
    });
}

function blog_favorite() {
    var message="";
    $.ajax({
        url:"/blog/favorite",
        dataType:'json',
        success:function(result){
            for(var r in result) {
                var htmlmsg="<li><a href='/blog/"+r['blog_id']+">"+r['blog_title']+"</a></li>"
                message+=htmlmsg;
            }
            $("#favorite_article").html(message);
        },
        error:function(e){
            alert(e.responseText);
        }
    });
}
$(document).ready(function() {
    $(document).on("click","#blog_like_click",blog_like);
    $(document).on("click","#favorite_list",blog_favorite);
})