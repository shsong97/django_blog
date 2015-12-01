
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
            for(var i in result) {
                var htmlmsg="<li><a href='/blog/"+result[i]['blog_id']+"'>"+result[i]['blog_title']+"</a></li>";
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
    blog_favorite();
    $(document).on("click","#blog_like_click",blog_like);
})