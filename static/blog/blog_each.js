
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
 
$(document).ready(function() {
    $(document).on("click","#blog_like_click",blog_like);
})