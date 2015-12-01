
function blog_like() {
    var item=$(this);
    var blog_id=item.find("#blog_like").val();
    $.ajax({
        url:"/blog/"+blog_id+"/like",
        dataType:'json',
        success:function(result){
            alert(result);
            item.find("#blog_like").val(result);
        },
        error:function(data) {
            alert("error"+data);
        }
    });
}

$(document).ready(function() {
    $("#blog_like_click").click(blog_like);
})