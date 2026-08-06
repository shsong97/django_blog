$(document).ready(function () {
  $(document).on('click', '.blog-like-btn', function () {
    var button = $(this);
    var blogId = button.data('blog-id');
    var post = button.closest('.ig-post');
    $.ajax({
      url: '/blog/' + blogId + '/like/',
      dataType: 'json',
      success: function (result) {
        button.addClass('is-liked');
        post.find('.blog-like-count').text(result.result);
      }
    });
  });
});
