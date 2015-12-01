
function blog_like() {
    var item=$(this);
    var blog_id=item.find("#blog_like").val();
    $.ajax({
        url:"/blog/"+blog_id+"/like",
        dataType:'json',
        success:function(result){
            item.find("#blog_like").val(result);
        }
    });
}

$(document).ready(function() {
    $("#bloglike_click").click(blog_like);
})